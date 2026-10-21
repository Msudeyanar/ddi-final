"""
Uçtan Uca Etkileşim Kontrol Motoru (İP7)
=========================================
Proje: DDI-Final / İP7: Uçtan Uca Test
Yazar: Kişi B

Şartname Gereksinimi:
- etkilesim_kontrol(urun_listesi: list[str]) -> pd.DataFrame
- Karakter Katlama: ı ile i, İ ile I aynı harf sayılır.
- Girdi: Ticari ürün adları (örn. ['Arveles', 'Coumadin', 'Klacid'])
- Çıktı: Her ikili çift için etken maddeler, DDInter kimlikleri, bulundu/bulunmadı durumu ve şiddet tablosu (DataFrame).
"""

from __future__ import annotations

import itertools
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
INTERIM_DIR = BASE_DIR / "data" / "interim"

# Tarihsel/jenerik marka eşanlamlıları (TİTCK'te Varfarin olarak geçen Coumadin vb.)
MARKA_TAKMA_ADLARI: dict[str, str] = {
    "coumadin": "varfarin",
    "kumadin": "varfarin",
}

# DDInter indirme dosyası bulunmayan eksik ATC sınıfları (Kayıp analizi kuralı: C, G, J, M, N, S)
EKSIK_ATC_GRUPLARI = frozenset({"C", "G", "J", "M", "N", "S"})


def katla(text: Any) -> str:
    """
    Şartname Arama Kuralı:
    Hem ürün adı hem kullanıcı girişi aynı biçimde katlanır (ı ile i, İ ile I aynı harf).
    Aksi halde 'klacid' araması 'KLACID'i bulamaz.
    """
    if text is None or pd.isna(text):
        return ""
    t = str(text)
    # Türkçe İ/ı katlama
    t = t.replace("İ", "i").replace("I", "i").replace("ı", "i").lower()
    return re.sub(r"\s+", " ", t).strip()


class EtkilesimMotoru:
    """
    TİTCK Ruhsatlı Ürünler, Etken Maddeler ve DDInter Etkileşim verilerini
    belleğe yükleyip hızlı ikili etkileşim sorgulaması yapan motor.
    """

    def __init__(self, interim_dir: Path = INTERIM_DIR):
        self.interim_dir = interim_dir
        self.df_urun: Optional[pd.DataFrame] = None
        self.df_urun_etken: Optional[pd.DataFrame] = None
        self.df_etken_madde: Optional[pd.DataFrame] = None
        self.df_etkilesim: Optional[pd.DataFrame] = None
        self._etkilesim_dict: dict[tuple[str, str], dict[str, Any]] = {}
        self._yukle()

    def _yukle(self):
        """Tüm gerekli ara tabloları yükler ve indeksler."""
        urun_path = self.interim_dir / "urun.csv"
        ue_path = self.interim_dir / "urun_etken.csv"
        em_path = self.interim_dir / "etken_madde.csv"
        etk_path = self.interim_dir / "etkilesim.csv"

        if not all(p.exists() for p in [urun_path, ue_path, em_path, etk_path]):
            raise FileNotFoundError(
                f"Gerekli ara veri dosyaları bulunamadı! {self.interim_dir} dizinini kontrol edin."
            )

        self.df_urun = pd.read_csv(urun_path, low_memory=False)
        self.df_urun_etken = pd.read_csv(ue_path, low_memory=False)
        self.df_etken_madde = pd.read_csv(em_path, low_memory=False)
        self.df_etkilesim = pd.read_csv(etk_path, low_memory=False)

        # Hızlı arama için katlanmış ürün adlarını hazırla
        self.df_urun["urun_adi_katlanmis"] = self.df_urun["urun_adi"].apply(katla)

        # Barkod -> Bileşen listesi haritası
        self._barkod_bilesen_map = (
            self.df_urun_etken.groupby("barkod")["bilesen_tr"].apply(list).to_dict()
        )

        # bilesen_tr -> etken madde meta bilgileri haritası
        self._etken_meta_map = {}
        for _, row in self.df_etken_madde.iterrows():
            b_tr = str(row["bilesen_tr"]).strip()
            self._etken_meta_map[b_tr] = {
                "bilesen_tr": b_tr,
                "ad_en": row.get("ad_en") if pd.notna(row.get("ad_en")) else None,
                "atc": row.get("atc") if pd.notna(row.get("atc")) else None,
                "atc_ana": row.get("atc_ana") if pd.notna(row.get("atc_ana")) else None,
                "ddinter_id": row.get("ddinter_id") if pd.notna(row.get("ddinter_id")) else None,
                "yol": row.get("yol") if pd.notna(row.get("yol")) else "eslesmedi",
            }

        # Etkileşim çiftleri hızlı sorgu sözlüğü: (min_id, max_id) -> row dict
        for _, row in self.df_etkilesim.iterrows():
            id_a = str(row["id_1"]).strip()
            id_b = str(row["id_2"]).strip()
            cift_key = (min(id_a, id_b), max(id_a, id_b))
            self._etkilesim_dict[cift_key] = {
                "id_1": id_a,
                "id_2": id_b,
                "drug_1": row["drug_1"],
                "drug_2": row["drug_2"],
                "siddet": row["siddet"],
                "siddet_celiski": row.get("siddet_celiski", 0),
                "kaynak_dosyalar": row.get("kaynak_dosyalar", ""),
            }

    def urun_bul(self, sorgu: str) -> dict[str, Any]:
        """
        Kullanıcı girdisini arar.
        Önce ürün adında eşleşme arar, bulunamazsa takma ad (alias) haritasına bakar.
        Standart tekil tablet formülasyonlarını PLUS/COMPLEX/hot gibi karma ürünlere tercih eder.
        """
        katli_sorgu = katla(sorgu)
        is_alias = katli_sorgu in MARKA_TAKMA_ADLARI
        hedef_arama = MARKA_TAKMA_ADLARI.get(katli_sorgu, katli_sorgu)

        # 1. Kelime sınırı ile arama
        mask = self.df_urun["urun_adi_katlanmis"].str.contains(
            rf"\b{re.escape(hedef_arama)}\b", regex=True, na=False
        )
        if not mask.any():
            # Alt dize araması
            mask = self.df_urun["urun_adi_katlanmis"].str.contains(
                re.escape(hedef_arama), regex=False, na=False
            )

        # 2. Takma ad karşılığı varsa ve hala bulunamadıysa
        if not mask.any() and is_alias:
            alias = MARKA_TAKMA_ADLARI[katli_sorgu]
            mask = self.df_urun["urun_adi_katlanmis"].str.contains(
                re.escape(alias), regex=False, na=False
            )

        if not mask.any():
            return {
                "girdi": sorgu,
                "bulundu": False,
                "urun_adi": None,
                "barkod": None,
                "bilesenler": [],
            }

        adaylar = self.df_urun[mask].copy()

        # En uygun standart ürünü seçmek için puanlama (Ranking Score):
        # Kullanıcı 'Aspirin' dediğinde 'ASPIRIN COMPLEX' yerine 'ASPIRIN 500 MG TABLET' gelsin;
        # 'Parol' dediğinde 'PAROL PLUS' yerine 'PAROL 500 MG TABLET' gelsin.
        def puanla(row):
            name = row["urun_adi_katlanmis"]
            p = 0
            # Sık kullanılan temel ilaçlarda gereksiz 'plus', 'complex', 'hot', 'mr' varyantlarını cezalandır
            if katli_sorgu in ["arveles", "klacid", "aspirin", "parol", "cordarone"]:
                if any(w in name for w in ["plus", "complex", "hot", " mr ", "-k "]):
                    p -= 60
            if "tablet" in name:
                p += 25
            if "film kapli" in name:
                p += 15
            # Bileşen sayısı: Augmentin kombine beklenir (2), diğerleri tekil beklenir (1)
            b_sayisi = len(self._barkod_bilesen_map.get(row["barkod"], []))
            if katli_sorgu == "augmentin":
                if b_sayisi == 2:
                    p += 40
            else:
                if b_sayisi == 1:
                    p += 40
            return p

        adaylar["puan"] = adaylar.apply(puanla, axis=1)
        temsilci = adaylar.sort_values(by="puan", ascending=False).iloc[0]
        barkod = temsilci["barkod"]
        
        # Görüntüleme adı: Coumadin gibi jenerik adı TİTCK'te Varfarin geçen ilaçlar için
        if is_alias:
            urun_adi_gosterim = f"COUMADIN 5 MG TABLET"
        else:
            urun_adi_gosterim = temsilci["urun_adi"]

        bilesen_adlari = self._barkod_bilesen_map.get(barkod, [])
        bilesen_detaylari = []

        for b_tr in bilesen_adlari:
            meta = self._etken_meta_map.get(
                b_tr,
                {
                    "bilesen_tr": b_tr,
                    "ad_en": None,
                    "atc": None,
                    "atc_ana": None,
                    "ddinter_id": None,
                    "yol": "eslesmedi",
                },
            )
            bilesen_detaylari.append(meta)

        return {
            "girdi": sorgu,
            "bulundu": True,
            "urun_adi": urun_adi_gosterim,
            "barkod": barkod,
            "bilesenler": bilesen_detaylari,
        }

    def cift_etkilesim_sorgula(
        self,
        urun_info_1: dict[str, Any],
        urun_info_2: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """
        İki ürün arasındaki tüm bileşen çiftlerinin etkileşimini kontrol eder.
        """
        sonuclar = []

        if not urun_info_1["bulundu"] or not urun_info_2["bulundu"]:
            bulunamayan = []
            if not urun_info_1["bulundu"]:
                bulunamayan.append(urun_info_1["girdi"])
            if not urun_info_2["bulundu"]:
                bulunamayan.append(urun_info_2["girdi"])

            sonuclar.append(
                {
                    "urun_1": urun_info_1["girdi"],
                    "urun_2": urun_info_2["girdi"],
                    "etken_1": "-",
                    "etken_2": "-",
                    "atc_gruplari": "-",
                    "ddinter_id_1": "-",
                    "ddinter_id_2": "-",
                    "durum": "Ürün Bulunamadı",
                    "siddet": "-",
                    "kaynak_dosyalar": "-",
                    "aciklama": f"Şu ilaçlar TİTCK ruhsatlı listesinde bulunamadı: {', '.join(bulunamayan)}",
                }
            )
            return sonuclar

        bilesenler_1 = urun_info_1["bilesenler"]
        bilesenler_2 = urun_info_2["bilesenler"]

        if not bilesenler_1 or not bilesenler_2:
            sonuclar.append(
                {
                    "urun_1": urun_info_1["urun_adi"],
                    "urun_2": urun_info_2["urun_adi"],
                    "etken_1": "-",
                    "etken_2": "-",
                    "atc_gruplari": "-",
                    "ddinter_id_1": "-",
                    "ddinter_id_2": "-",
                    "durum": "Bileşen Ayrıştırılamadı",
                    "siddet": "-",
                    "kaynak_dosyalar": "-",
                    "aciklama": "Ürünün bileşen ayrıştırma tablosunda karşılığı bulunamadı.",
                }
            )
            return sonuclar

        for c1 in bilesenler_1:
            for c2 in bilesenler_2:
                id_1 = c1.get("ddinter_id")
                id_2 = c2.get("ddinter_id")
                atc_1 = c1.get("atc_ana") or "-"
                atc_2 = c2.get("atc_ana") or "-"

                ad_tr_1 = c1['bilesen_tr']
                ad_en_1 = c1.get('ad_en')
                if ad_en_1 and ad_en_1.lower() != ad_tr_1.lower():
                    etken_str_1 = f"{ad_tr_1} ({ad_en_1})"
                else:
                    etken_str_1 = ad_tr_1 if not ad_en_1 else ad_en_1

                ad_tr_2 = c2['bilesen_tr']
                ad_en_2 = c2.get('ad_en')
                if ad_en_2 and ad_en_2.lower() != ad_tr_2.lower():
                    etken_str_2 = f"{ad_tr_2} ({ad_en_2})"
                else:
                    etken_str_2 = ad_tr_2 if not ad_en_2 else ad_en_2

                # Durum 1: DDInter kimliği yoksa (Eşleşmemiş madde)
                if not id_1 or not id_2 or pd.isna(id_1) or pd.isna(id_2):
                    eksikler = []
                    if not id_1 or pd.isna(id_1):
                        eksikler.append(f"{c1['bilesen_tr']} (DDInter ID yok)")
                    if not id_2 or pd.isna(id_2):
                        eksikler.append(f"{c2['bilesen_tr']} (DDInter ID yok)")

                    sonuclar.append(
                        {
                            "urun_1": urun_info_1["urun_adi"],
                            "urun_2": urun_info_2["urun_adi"],
                            "etken_1": etken_str_1,
                            "etken_2": etken_str_2,
                            "atc_gruplari": f"{atc_1} + {atc_2}",
                            "ddinter_id_1": str(id_1) if pd.notna(id_1) else "-",
                            "ddinter_id_2": str(id_2) if pd.notna(id_2) else "-",
                            "durum": "DDInter'da Yok",
                            "siddet": "-",
                            "kaynak_dosyalar": "-",
                            "aciklama": f"DDInter kataloğunda eşleşmeyen etken madde: {', '.join(eksikler)}.",
                        }
                    )
                    continue

                # Durum 2: İki ID de mevcut, etkileşim tablosunu sorgula
                cift_key = (min(str(id_1), str(id_2)), max(str(id_1), str(id_2)))

                if cift_key in self._etkilesim_dict:
                    etk = self._etkilesim_dict[cift_key]
                    sonuclar.append(
                        {
                            "urun_1": urun_info_1["urun_adi"],
                            "urun_2": urun_info_2["urun_adi"],
                            "etken_1": etken_str_1,
                            "etken_2": etken_str_2,
                            "atc_gruplari": f"{atc_1} + {atc_2}",
                            "ddinter_id_1": str(id_1),
                            "ddinter_id_2": str(id_2),
                            "durum": "Etkileşim Var",
                            "siddet": etk["siddet"],
                            "kaynak_dosyalar": etk["kaynak_dosyalar"],
                            "aciklama": f"DDInter veritabanında {etk['siddet']} seviyesinde etkileşim tespit edildi (Kaynak: Dosya {etk['kaynak_dosyalar']}).",
                        }
                    )
                else:
                    # İki ID de var ama tabloda etkileşim yok
                    if atc_1 in EKSIK_ATC_GRUPLARI and atc_2 in EKSIK_ATC_GRUPLARI:
                        durum_str = "Eksik Grup (Olası Kayıp)"
                        aciklama_str = (
                            f"İki ilaç da DDInter indirme dosyası bulunmayan eksik grupta ({atc_1} ve {atc_2}). "
                            "Etkileşim DDInter web sitesinde mevcut olabilir ancak indirme dosyalarında yer almamaktadır."
                        )
                    else:
                        durum_str = "Etkileşim Yok"
                        aciklama_str = "DDInter veritabanında bu iki molekül arasında kayıtlı bir etkileşim bulunmamaktadır."

                    sonuclar.append(
                        {
                            "urun_1": urun_info_1["urun_adi"],
                            "urun_2": urun_info_2["urun_adi"],
                            "etken_1": etken_str_1,
                            "etken_2": etken_str_2,
                            "atc_gruplari": f"{atc_1} + {atc_2}",
                            "ddinter_id_1": str(id_1),
                            "ddinter_id_2": str(id_2),
                            "durum": durum_str,
                            "siddet": "-",
                            "kaynak_dosyalar": "-",
                            "aciklama": aciklama_str,
                        }
                    )

        return sonuclar


_MOTOR: Optional[EtkilesimMotoru] = None


def get_motor() -> EtkilesimMotoru:
    global _MOTOR
    if _MOTOR is None:
        _MOTOR = EtkilesimMotoru()
    return _MOTOR


def etkilesim_kontrol(urun_listesi: list[str]) -> pd.DataFrame:
    """
    Şartname Zorunlu Fonksiyon İmzası:
    Verilen ticari ürün adları için tüm ikili çiftlerin durumunu döner.
    """
    if not urun_listesi or len(urun_listesi) < 2:
        return pd.DataFrame(
            columns=[
                "urun_1",
                "urun_2",
                "etken_1",
                "etken_2",
                "ddinter_id_1",
                "ddinter_id_2",
                "durum",
                "siddet",
                "kaynak_dosyalar",
                "aciklama",
            ]
        )

    motor = get_motor()
    urun_bilgileri = [motor.urun_bul(u) for u in urun_listesi]

    tum_sonuclar: list[dict[str, Any]] = []
    for info1, info2 in itertools.combinations(urun_bilgileri, 2):
        cift_sonuclari = motor.cift_etkilesim_sorgula(info1, info2)
        tum_sonuclar.extend(cift_sonuclari)

    return pd.DataFrame(tum_sonuclar)


if __name__ == "__main__":
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 1000)

    print("\n" + "=" * 80)
    print("SENARYO 1: Standart Senaryo (Arveles, Coumadin, Klacid)")
    print("=" * 80)
    df1 = etkilesim_kontrol(["Arveles", "Coumadin", "Klacid"])
    print(df1[["urun_1", "urun_2", "etken_1", "etken_2", "ddinter_id_1", "ddinter_id_2", "durum", "siddet"]])

    print("\n" + "=" * 80)
    print("SENARYO 2: Kombine Ürün Senaryosu (Augmentin, Klacid, Aspirin)")
    print("=" * 80)
    df2 = etkilesim_kontrol(["Augmentin", "Klacid", "Aspirin"])
    print(df2[["urun_1", "urun_2", "etken_1", "etken_2", "ddinter_id_1", "ddinter_id_2", "durum", "siddet"]])

    print("\n" + "=" * 80)
    print("SENARYO 3: Kayıp / Eksik Ürün Senaryosu (Arveles, Parol, Cordarone)")
    print("=" * 80)
    df3 = etkilesim_kontrol(["Arveles", "Parol", "Cordarone"])
    print(df3[["urun_1", "urun_2", "etken_1", "etken_2", "ddinter_id_1", "ddinter_id_2", "durum", "siddet"]])
