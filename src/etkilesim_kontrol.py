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

Danışman ve Kullanım Koşulları Uyumu:
- Kayıt bulunamayan çiftler için "Etkileşim Yok" yerine "Kayıt bulunamadı" yazılır.
- Test ilaçlarına özel puanlama ve marka takma adları (alias) kullanılmaz; genel ve nesnel ürün seçimi uygulanır.
- Gerçekte seçilen ürünün adı gösterilir.
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

    def __init__(self, interim_dir: Path = INTERIM_DIR, yol_d_path: Optional[Path] = None):
        self.interim_dir = interim_dir
        self.df_urun: Optional[pd.DataFrame] = None
        self.df_urun_etken: Optional[pd.DataFrame] = None
        self.df_etken_madde: Optional[pd.DataFrame] = None
        self.df_etkilesim: Optional[pd.DataFrame] = None
        self._etkilesim_dict: dict[tuple[str, str], dict[str, Any]] = {}
        self._yukle()
        self._yol_d_bilesenleri = self._yol_d_yukle(
            yol_d_path if yol_d_path is not None else BASE_DIR / "config" / "yol_d_urun_esleme.csv"
        )

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

        yol_d_tam_ad = BASE_DIR / "config" / "yol_d_bilesen_esleme.csv"
        if yol_d_tam_ad.exists():
            kurallar = pd.read_csv(yol_d_tam_ad, dtype=str, keep_default_na=False)
            if kurallar["bilesen_tr"].duplicated().any():
                raise ValueError("Yol D bileşen tablosunda yinelenen ad var.")
            for kural in kurallar.itertuples(index=False):
                meta = self._etken_meta_map.get(kural.bilesen_tr)
                if meta is not None and not meta["ddinter_id"]:
                    meta.update(ad_en=kural.ad_en, ddinter_id=kural.ddinter_id, yol="D")

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

    def _yol_d_yukle(self, path: Path) -> dict:
        if not path.exists():
            return {}

        kararlar = pd.read_csv(path, dtype=str, keep_default_na=False)
        aktif = kararlar[kararlar["durum"] != "urun_belgesi_bekliyor"].copy()
        aktif["sira"] = aktif["sira"].astype(int)
        if aktif.duplicated(["barkod", "sira"]).any():
            raise ValueError("Yol D dosyasında tekrarlanan barkod ve sıra var.")

        urun_atcleri = {
            str(int(urun.barkod)): str(urun.atc_final)[:1]
            for urun in self.df_urun.itertuples(index=False)
            if pd.notna(urun.barkod) and pd.notna(urun.atc_final)
        }
        bilesenler = {}
        for barkod, grup in aktif.sort_values("sira").groupby("barkod"):
            bilesenler[barkod] = [
                {
                    "bilesen_tr": satir.bilesen,
                    "ad_en": None,
                    "atc": None,
                    "atc_ana": urun_atcleri.get(barkod),
                    "ddinter_id": satir.ddinter_id or None,
                    "yol": ("C" if satir.durum == "mevcut_yol_c" else "D")
                        if satir.ddinter_id else "eslesmedi",
                }
                for satir in grup.itertuples(index=False)
            ]
        return bilesenler

    def urun_bul(self, sorgu: str) -> dict[str, Any]:
        """
        Kullanıcı girdisini arar.
        Hiçbir ilaca özel istisna veya takma ad içermez; genel ve nesnel kurallarla arama yapar:
        1. Önce tam kelime sınırı ile arama yapılır (\bsorgu\b).
        2. Bulunamazsa alt dize (substring) araması yapılır.
        3. Birden fazla aday varsa genel farmasötik sıralama uygulanır:
           - Tam kelime sınırı eşleşmesi önceliklidir.
           - İsmin sorgu ile başlaması önceliklidir.
           - Standart katı oral formlar (tablet, kapsül, film kaplı) önceliklidir.
           - Eşitlik durumunda alfabetik ürün adı esas alınır.
        """
        katli_sorgu = katla(sorgu)
        if not katli_sorgu:
            return {
                "girdi": sorgu,
                "bulundu": False,
                "urun_adi": None,
                "barkod": None,
                "aday_sayisi": 0,
                "bilesenler": [],
            }

        # 1. Kelime sınırı ile arama
        mask = self.df_urun["urun_adi_katlanmis"].str.contains(
            rf"\b{re.escape(katli_sorgu)}\b", regex=True, na=False
        )
        if not mask.any():
            # 2. Alt dize araması
            mask = self.df_urun["urun_adi_katlanmis"].str.contains(
                re.escape(katli_sorgu), regex=False, na=False
            )

        if not mask.any():
            return {
                "girdi": sorgu,
                "bulundu": False,
                "urun_adi": None,
                "barkod": None,
                "aday_sayisi": 0,
                "bilesenler": [],
            }

        adaylar = self.df_urun[mask].copy()
        aday_sayisi = len(adaylar)

        # Genel ve nesnel aday sıralama kriterleri:
        adaylar["_is_word"] = adaylar["urun_adi_katlanmis"].str.contains(
            rf"\b{re.escape(katli_sorgu)}\b", regex=True, na=False
        )
        adaylar["_starts_with"] = adaylar["urun_adi_katlanmis"].str.startswith(katli_sorgu)
        adaylar["_is_tablet_kapsul"] = adaylar["urun_adi_katlanmis"].str.contains(
            r"\b(?:tablet|kapsul|film kapli)\b", regex=True, na=False
        )

        sirali = adaylar.sort_values(
            by=["_is_word", "_starts_with", "_is_tablet_kapsul", "urun_adi"],
            ascending=[False, False, False, True],
        )
        temsilci = sirali.iloc[0]
        barkod = temsilci["barkod"]
        urun_adi_gosterim = temsilci["urun_adi"]

        bilesen_adlari = self._barkod_bilesen_map.get(barkod, [])
        barkod_anahtari = str(int(barkod)) if pd.notna(barkod) else ""
        bilesen_detaylari = self._yol_d_bilesenleri.get(barkod_anahtari, [])

        for b_tr in ([] if bilesen_detaylari else bilesen_adlari):
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
            "aday_sayisi": aday_sayisi,
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
                    "urun_1": urun_info_1["girdi"] if not urun_info_1["bulundu"] else urun_info_1["urun_adi"],
                    "urun_2": urun_info_2["girdi"] if not urun_info_2["bulundu"] else urun_info_2["urun_adi"],
                    "etken_1": "-",
                    "etken_2": "-",
                    "atc_gruplari": "-",
                    "ddinter_id_1": "-",
                    "ddinter_id_2": "-",
                    "durum": "Ürün Bulunamadı",
                    "siddet": "-",
                    "kaynak_dosyalar": "-",
                    "aciklama": f"Şu ilaç(lar) TİTCK ruhsatlı listesinde bulunamadı: {', '.join(bulunamayan)}.",
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

                ad_tr_1 = c1["bilesen_tr"]
                ad_en_1 = c1.get("ad_en")
                if ad_en_1 and ad_en_1.lower() != ad_tr_1.lower():
                    etken_str_1 = f"{ad_tr_1} ({ad_en_1})"
                else:
                    etken_str_1 = ad_tr_1 if not ad_en_1 else ad_en_1

                ad_tr_2 = c2["bilesen_tr"]
                ad_en_2 = c2.get("ad_en")
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
                    # İki ID de var ama indirme dosyalarında kayıt yok
                    if atc_1 in EKSIK_ATC_GRUPLARI and atc_2 in EKSIK_ATC_GRUPLARI:
                        durum_str = "Eksik Grup (Olası Kayıp)"
                        aciklama_str = (
                            f"İki ilaç da DDInter indirme dosyası bulunmayan eksik grupta ({atc_1} ve {atc_2}). "
                            "Etkileşim DDInter web sitesinde mevcut olabilir ancak indirme dosyalarında yer almamaktadır."
                        )
                    else:
                        durum_str = "Kayıt bulunamadı"
                        aciklama_str = (
                            "DDInter indirme dosyalarında bu çift için kayıt bulunamadı; "
                            "bu, etkileşim olmadığı anlamına gelmez (DDInter kullanım koşulları)."
                        )

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
    urun_bilgileri = []
    for u in urun_listesi:
        info = motor.urun_bul(u)
        urun_bilgileri.append(info)
        if info["bulundu"]:
            print(f"🔍 [Arama: '{u}'] -> {info['aday_sayisi']} aday arasından seçildi: '{info['urun_adi']}' (Barkod: {info['barkod']})")
        else:
            print(f"⚠️ [Arama: '{u}'] -> TİTCK ruhsatlı listesinde bulunamadı (0 aday).")

    tum_sonuclar: list[dict[str, Any]] = []
    for info1, info2 in itertools.combinations(urun_bilgileri, 2):
        cift_sonuclari = motor.cift_etkilesim_sorgula(info1, info2)
        tum_sonuclar.extend(cift_sonuclari)

    return pd.DataFrame(tum_sonuclar)


if __name__ == "__main__":
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 1000)

    print("\n" + "=" * 80)
    print("SENARYO 1: Standart Referans Senaryo (Arveles, Coumadin, Klacid)")
    print("Not: Coumadin TİTCK ruhsatlı listesinde pasif olduğundan bulunamaz.")
    print("=" * 80)
    df1 = etkilesim_kontrol(["Arveles", "Coumadin", "Klacid"])
    print(df1[["urun_1", "urun_2", "etken_1", "etken_2", "ddinter_id_1", "ddinter_id_2", "durum", "siddet", "aciklama"]])

    print("\n" + "=" * 80)
    print("SENARYO 1B: Ruhsatlı Varfarin ile Referans Senaryo (Arveles, Warfmadin, Klacid)")
    print("=" * 80)
    df1b = etkilesim_kontrol(["Arveles", "Warfmadin", "Klacid"])
    print(df1b[["urun_1", "urun_2", "etken_1", "etken_2", "ddinter_id_1", "ddinter_id_2", "durum", "siddet", "aciklama"]])

    print("\n" + "=" * 80)
    print("SENARYO 2: Kombine Ürün Senaryosu (Augmentin, Klacid, Aspirin)")
    print("=" * 80)
    df2 = etkilesim_kontrol(["Augmentin", "Klacid", "Aspirin"])
    print(df2[["urun_1", "urun_2", "etken_1", "etken_2", "ddinter_id_1", "ddinter_id_2", "durum", "siddet", "aciklama"]])

    print("\n" + "=" * 80)
    print("SENARYO 3: Kayıp / Eksik Ürün Senaryosu (Arveles, Parol, Cordarone)")
    print("=" * 80)
    df3 = etkilesim_kontrol(["Arveles", "Parol", "Cordarone"])
    print(df3[["urun_1", "urun_2", "etken_1", "etken_2", "ddinter_id_1", "ddinter_id_2", "durum", "siddet", "aciklama"]])
