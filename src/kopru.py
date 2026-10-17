"""
src/kopru.py
İngilizce ad köprüsü ve DDInter eşleme fonksiyonları (İP3 - Kişi A).

Bu modül, Veri Birleştirme Planı ve 2. Hafta Görevleri belgesindeki
Adım 3 (Yol A, Yol B, SKRS) ve Adım 4'ün ilk maddesini (ddinter_ilac tablosu) uygular:

1. SKRS ATC Sözlüğü:
   - SKRS'in tüm satırlarından (aktif + pasif) "ATC kodu → ATC adı" sözlüğü çıkarılır.
   - ATC adı ürünün kendi satırından değil sözlükten alınır, böylece SKRS'te satırı
     olmayan ruhsatlı ürünler de Yol A'yı kullanabilir.

2. ddinter_ilac.csv Tablosu:
   - 8 DDInter dosyasından (A, B, D, H, L, P, R, V) benzersiz ilaç tablosu çıkarılır:
     DDInterID_A, Drug_A ve DDInterID_B, Drug_B alt alta eklenir, tekrarlar atılır (1.939 satır).
   - Ad normalizasyonu ad_normalize() ile yapılır.

3. Yol A (Tek bileşenli ürünler):
   - Tek bileşenli, 7 haneli ATC'li, atc_celiski=0 olan ürünlerde ATC adı doğrudan
     İngilizce addır (deksketoprofen → dexketoprofen).
   - "combinations", "excl." veya "various" içeren ATC adları elenir.
   - Birden fazla tek bileşenli üründe geçen bileşenler için en sık geçen ATC/ad çifti (mode) seçilir.

4. Yol B (Kombine ürünler):
   - Kombine ürünlerde ATC adı "and" ve "," ile parçalara bölünür.
   - Parça sayısı bileşen sayısına eşitse rapidfuzz ile eşleştirme yapılır (benzerlik >= 80).
   - "combinations", "excl." veya "various" içeren adlar bölünmez, Yol C ve D'ye bırakılır.

5. SKRS Kural 5:
   - SKRS kaynaklı ürünlerin ATC adından gelen bileşenleri doğrudan İngilizce kabul edilir (yol='SKRS').

6. etken_madde.csv Taslağı (Kişi A → Kişi B Teslimi):
   - Tüm benzersiz Türkçe bileşenler için Yol A, Yol B ve SKRS uygulanır.
   - urun_sayisi (ürün sayısı) hesaplanır ve büyükten küçüğe sıralanır.
   - Kalanlar (Yol C ve Yol D için) Kişi B'ye devredilir.
"""

from collections import Counter
from pathlib import Path
import re
from typing import Optional, Union

import pandas as pd
from rapidfuzz import fuzz

from src.normalize import ad_normalize, eslesme_anahtari


# ══════════════════════════════════════════════════════════════════
# 1. SKRS ATC SÖZLÜĞÜ
# ══════════════════════════════════════════════════════════════════

def _temizle_atc_adi(atc_adi: Optional[str]) -> Optional[str]:
    """ATC adından görünmez karakterleri ve parantez içi ekleri temizler."""
    if pd.isna(atc_adi):
        return None
    s = str(atc_adi).strip()
    if not s or s.lower() == "nan":
        return None
    # Parantez içi açıklamaları temizle: (vit c), (human), (horse) vb.
    s = re.sub(r"\s*\([^)]*\)\s*", " ", s).strip()
    s = re.sub(r"\s+", " ", s)
    return s or None


def skrs_atc_sozlugu_olustur(skrs_yolu: Union[str, Path]) -> dict[str, str]:
    """SKRS'in aktif ve pasif sekmelerinden 'ATC kodu → ATC adı' sözlüğü çıkarır.

    Birden fazla ad geçen kodlar için en sık geçen (mode) ad alınır.
    """
    skrs_p = Path(skrs_yolu)
    if not skrs_p.exists():
        raise FileNotFoundError(f"SKRS dosyası bulunamadı: {skrs_p}")

    df_aktif = pd.read_excel(skrs_p, sheet_name="AKTİF ÜRÜNLER LİSTESİ", header=2, dtype=str)
    df_pasif = pd.read_excel(skrs_p, sheet_name="PASİF ÜRÜNLER LİSTESİ", header=2, dtype=str)
    df_skrs = pd.concat([df_aktif, df_pasif], ignore_index=True)

    df_skrs["ATC Kodu"] = df_skrs["ATC Kodu"].astype(str).str.strip().str.upper()
    df_skrs["ATC Adı Temiz"] = df_skrs["ATC Adı"].apply(_temizle_atc_adi)

    gecerli = df_skrs[
        df_skrs["ATC Kodu"].notna()
        & (df_skrs["ATC Kodu"] != "")
        & (df_skrs["ATC Kodu"] != "NAN")
        & df_skrs["ATC Adı Temiz"].notna()
        & (df_skrs["ATC Adı Temiz"] != "")
    ]

    # En sık geçen adı sözlük değeri olarak belirle
    sozluk = (
        gecerli.groupby("ATC Kodu")["ATC Adı Temiz"]
        .agg(lambda x: x.mode().iloc[0] if not x.empty else "")
        .to_dict()
    )
    return sozluk


# ══════════════════════════════════════════════════════════════════
# 2. DDINTER İLAÇ TABLOSU (Adım 4'ün ilk maddesi)
# ══════════════════════════════════════════════════════════════════

def ddinter_ilac_tablosu_olustur(ddinter_dosyalari: list[Union[str, Path]]) -> pd.DataFrame:
    """8 DDInter CSV dosyasından benzersiz ilaç tablosunu çıkarır.

    DDInterID_A, Drug_A ve DDInterID_B, Drug_B alt alta eklenir, tekrarlar atılır.
    Ad normalizasyonu ad_normalize() ile yapılır.
    Beklenen satır sayısı: ~1.939 satır.
    """
    records = []
    for f in ddinter_dosyalari:
        p = Path(f)
        if not p.exists():
            continue
        df = pd.read_csv(p)
        part_a = df[["DDInterID_A", "Drug_A"]].rename(
            columns={"DDInterID_A": "ddinter_id", "Drug_A": "drug_name"}
        )
        part_b = df[["DDInterID_B", "Drug_B"]].rename(
            columns={"DDInterID_B": "ddinter_id", "Drug_B": "drug_name"}
        )
        records.append(part_a)
        records.append(part_b)

    if not records:
        raise ValueError("Hiçbir DDInter dosyası okunamadı.")

    df_all = pd.concat(records, ignore_index=True).drop_duplicates()
    df_all["ad_norm"] = df_all["drug_name"].apply(ad_normalize)
    df_all = df_all.sort_values("ddinter_id").reset_index(drop=True)
    return df_all[["ddinter_id", "drug_name", "ad_norm"]]


# ══════════════════════════════════════════════════════════════════
# 3. YOL A: TEK BİLEŞENLİ ÜRÜNLER
# ══════════════════════════════════════════════════════════════════

_KOMBINASYON_REGEX = re.compile(r"\b(?:combinations|excl\.|various)\b", re.IGNORECASE)


def atc_kombinasyon_mu(atc_adi: Optional[str]) -> bool:
    """ATC adının 'combinations', 'excl.' veya 'various' içerip içermediğini kontrol eder."""
    if not atc_adi:
        return False
    return bool(_KOMBINASYON_REGEX.search(str(atc_adi)))


def yol_a_esle(
    df_urun: pd.DataFrame,
    df_urun_etken: pd.DataFrame,
    atc_sozlugu: dict[str, str],
) -> pd.DataFrame:
    """Yol A eşleştirmesi: Tek bileşenli, 7 haneli ATC'li, atc_celiski=0 olan ürünler.

    ATC adı SKRS sözlüğünden alınır ve doğrudan İngilizce karşılık olarak kullanılır.
    """
    # Barkod bazında bileşen sayıları
    bilesen_sayisi = df_urun_etken.groupby("barkod")["bilesen_tr"].count().to_dict()

    # Filtreler: Tek bileşenli, 7 haneli ATC, atc_celiski=0, kaynak=Ruhsatlı
    mask = (
        df_urun["barkod"].map(bilesen_sayisi).eq(1)
        & df_urun["atc_final"].astype(str).str.len().eq(7)
        & df_urun["atc_celiski"].astype(str).isin(["0", "0.0", 0])
        & df_urun["kaynak"].eq("Ruhsatlı")
    )
    yol_a_urunler = df_urun[mask].copy()

    # Sözlükten ATC adı çek
    yol_a_urunler["atc_adi"] = yol_a_urunler["atc_final"].map(atc_sozlugu)
    yol_a_urunler = yol_a_urunler[
        yol_a_urunler["atc_adi"].notna() & (yol_a_urunler["atc_adi"] != "")
    ]

    # Kombinasyon ifadelerini filtrele (tek bileşenli ilaç 'combinations' adı alamaz)
    yol_a_urunler = yol_a_urunler[~yol_a_urunler["atc_adi"].apply(atc_kombinasyon_mu)].copy()

    # urun_etken ile birleştir
    m = df_urun_etken.merge(
        yol_a_urunler[["barkod", "atc_final", "atc_adi"]], on="barkod", how="inner"
    )
    m["ad_en"] = m["atc_adi"].apply(ad_normalize)

    # Her benzersiz bilesen_tr için en sık geçen (ad_en, atc) çiftini belirle
    sonuclar = []
    for b_tr, grp in m.groupby("bilesen_tr"):
        best_cand = None
        best_votes = -1
        best_score = -1
        for (ad_en, atc), count in Counter(zip(grp["ad_en"], grp["atc_final"])).items():
            score = fuzz.token_sort_ratio(eslesme_anahtari(b_tr), ad_en)
            if (count > best_votes) or (count == best_votes and score > best_score):
                best_cand = (ad_en, atc)
                best_votes = count
                best_score = score

        if best_cand:
            sonuclar.append({
                "bilesen_tr": b_tr,
                "ad_en": best_cand[0],
                "atc": best_cand[1],
                "yol": "A",
                "eslesme_skoru": best_score,
            })

    return pd.DataFrame(sonuclar)


# ══════════════════════════════════════════════════════════════════
# 4. YOL B: KOMBİNE ÜRÜNLER
# ══════════════════════════════════════════════════════════════════

def atc_adi_parcala(atc_adi: str) -> list[str]:
    """ATC adını 'and' ve ',' ile parçalara ayırır."""
    if not atc_adi:
        return []
    parts = [p.strip() for p in re.split(r"\s+and\s+|,", str(atc_adi), flags=re.IGNORECASE) if p.strip()]
    return parts


def yol_b_esle(
    df_urun: pd.DataFrame,
    df_urun_etken: pd.DataFrame,
    atc_sozlugu: dict[str, str],
    onceki_eslesmeler: Optional[set[str]] = None,
) -> pd.DataFrame:
    """Yol B eşleştirmesi: Kombine ürünlerde ATC adını parçalayarak rapidfuzz ile eşleme.

    Kural:
    - Kombine ürün (bilesen_sayisi > 1), 7 haneli ATC, atc_celiski=0, kaynak=Ruhsatlı.
    - ATC adı 'combinations', 'excl.' veya 'various' içeriyorsa bölünmez (Yol C/D'ye kalır).
    - Parça sayısı bileşen sayısına eşit olmalıdır.
    - Parçalar rapidfuzz benzerlik skoru >= 80 ile eşlenir.
    - Yol A'da eşleşenler hariç tutulur.
    """
    onceki = set(onceki_eslesmeler) if onceki_eslesmeler else set()

    # Barkod başına sıralı bileşen listesi
    ue_grouped = (
        df_urun_etken.sort_values(["barkod", "sira"])
        .groupby("barkod")["bilesen_tr"]
        .apply(list)
        .to_dict()
    )

    mask = (
        df_urun["barkod"].map(lambda b: len(ue_grouped.get(b, []))).gt(1)
        & df_urun["atc_final"].astype(str).str.len().eq(7)
        & df_urun["atc_celiski"].astype(str).isin(["0", "0.0", 0])
        & df_urun["kaynak"].eq("Ruhsatlı")
    )
    kombine_urunler = df_urun[mask].copy()

    kombine_urunler["atc_adi"] = kombine_urunler["atc_final"].map(atc_sozlugu)
    kombine_urunler = kombine_urunler[
        kombine_urunler["atc_adi"].notna() & (kombine_urunler["atc_adi"] != "")
    ]
    # Kombinasyon sözcüklerini içerenler bölünmez
    kombine_urunler = kombine_urunler[~kombine_urunler["atc_adi"].apply(atc_kombinasyon_mu)].copy()

    adaylar = []
    for _, row in kombine_urunler.iterrows():
        barkod = row["barkod"]
        atc = row["atc_final"]
        atc_adi = row["atc_adi"]
        tr_bilesenler = ue_grouped.get(barkod, [])

        parts = atc_adi_parcala(atc_adi)
        if len(parts) != len(tr_bilesenler):
            continue

        # Eşleştirme matrisi
        used_parts = set()
        prod_matches = []
        for tr in tr_bilesenler:
            best_p = None
            best_score = -1
            best_idx = -1
            for idx, p in enumerate(parts):
                if idx in used_parts:
                    continue
                score = fuzz.ratio(eslesme_anahtari(tr), ad_normalize(p))
                if score > best_score:
                    best_score = score
                    best_p = p
                    best_idx = idx

            if best_score >= 80 and best_p is not None:
                used_parts.add(best_idx)
                prod_matches.append((tr, ad_normalize(best_p), atc, best_score))

        if len(prod_matches) == len(tr_bilesenler):
            adaylar.extend(prod_matches)

    # Yol A'da eşleşmeyenler için en yüksek skorlu eşleşmeyi seç
    yol_b_dict = {}
    for tr, ad_en, atc, score in adaylar:
        if tr in onceki:
            continue
        if tr not in yol_b_dict or score > yol_b_dict[tr]["eslesme_skoru"]:
            yol_b_dict[tr] = {
                "bilesen_tr": tr,
                "ad_en": ad_en,
                "atc": atc,
                "yol": "B",
                "eslesme_skoru": score,
            }

    return pd.DataFrame(list(yol_b_dict.values()))


# ══════════════════════════════════════════════════════════════════
# 5. SKRS KURAL 5 EŞLEMESİ
# ══════════════════════════════════════════════════════════════════

def skrs_esle(
    df_urun: pd.DataFrame,
    df_urun_etken: pd.DataFrame,
    onceki_eslesmeler: Optional[set[str]] = None,
) -> pd.DataFrame:
    """SKRS kaynaklı ürünlerin Kural 5 gereği doğrudan yol='SKRS' olarak eşlenmesi."""
    onceki = set(onceki_eslesmeler) if onceki_eslesmeler else set()

    skrs_barkodlar = set(df_urun[df_urun["kaynak"] == "SKRS"]["barkod"])
    skrs_ue = df_urun_etken[df_urun_etken["barkod"].isin(skrs_barkodlar)]

    skrs_dict = {}
    for b_tr in skrs_ue["bilesen_tr"].unique():
        if b_tr in onceki:
            continue
        # Ürünün ATC kodunu bul
        iliskili_barkodlar = set(skrs_ue[skrs_ue["bilesen_tr"] == b_tr]["barkod"])
        skrs_urun = df_urun[df_urun["barkod"].isin(iliskili_barkodlar) & (df_urun["kaynak"] == "SKRS")].iloc[0]
        skrs_dict[b_tr] = {
            "bilesen_tr": b_tr,
            "ad_en": b_tr,
            "atc": skrs_urun.get("atc_final"),
            "yol": "SKRS",
            "eslesme_skoru": 100.0,
        }

    return pd.DataFrame(list(skrs_dict.values()))


# ══════════════════════════════════════════════════════════════════
# 6. ETKEN MADDE TABLOSU (Kişi A → Kişi B Teslimi)
# ══════════════════════════════════════════════════════════════════

def etken_madde_olustur(
    df_urun: pd.DataFrame,
    df_urun_etken: pd.DataFrame,
    atc_sozlugu: dict[str, str],
) -> pd.DataFrame:
    """Yol A, Yol B ve SKRS eşlemelerini birleştirerek etken_madde.csv taslağını üretir.

    Çıktı sütunları:
    - bilesen_tr : Benzersiz Türkçe bileşen adı (3.111 adet)
    - ad_en      : Eşleşen İngilizce ad (A, B, SKRS'ten gelir; eşleşmeyenler NaN)
    - atc        : İlgili ATC kodu
    - yol        : 'A', 'B', 'SKRS' veya 'eslesmedi'
    - urun_sayisi: Bu bileşeni içeren ürün sayısı (azalan sırada)
    """
    # 1. urun_sayisi hesabı
    urun_sayisi_seri = df_urun_etken.groupby("bilesen_tr")["barkod"].nunique()
    tum_bilesenler = pd.DataFrame({
        "bilesen_tr": urun_sayisi_seri.index,
        "urun_sayisi": urun_sayisi_seri.values,
    })

    # 2. Yol A
    df_yol_a = yol_a_esle(df_urun, df_urun_etken, atc_sozlugu)
    eslesenler_a = set(df_yol_a["bilesen_tr"])

    # 3. Yol B (Yol A haricindekiler)
    df_yol_b = yol_b_esle(df_urun, df_urun_etken, atc_sozlugu, onceki_eslesmeler=eslesenler_a)
    eslesenler_ab = eslesenler_a | set(df_yol_b["bilesen_tr"])

    # 4. SKRS (A ve B haricindekiler)
    df_skrs = skrs_esle(df_urun, df_urun_etken, onceki_eslesmeler=eslesenler_ab)

    # 5. Eşleşenleri birleştir
    birlestirilen = pd.concat([df_yol_a, df_yol_b, df_skrs], ignore_index=True)

    # 6. Tüm bileşenlerle sol birleştirme (left join)
    sonuc = tum_bilesenler.merge(
        birlestirilen[["bilesen_tr", "ad_en", "atc", "yol"]],
        on="bilesen_tr",
        how="left",
    )

    # Eşleşmeyenleri işaretle
    sonuc["yol"] = sonuc["yol"].fillna("eslesmedi")

    # Sütun sırası: bilesen_tr, ad_en, atc, yol, urun_sayisi
    sonuc = sonuc[["bilesen_tr", "ad_en", "atc", "yol", "urun_sayisi"]]
    sonuc = sonuc.sort_values(by=["urun_sayisi", "bilesen_tr"], ascending=[False, True]).reset_index(drop=True)

    return sonuc
