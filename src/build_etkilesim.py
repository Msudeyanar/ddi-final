"""
İP4: DDInter Birleştirme ve Etkileşim Matrisi Oluşturucu (Production-Grade ETL)

Mühendislik Standartları:
1. Tek Okuma (Single I/O): 8 CSV diski meşgul etmeden sadece 1 kez okunur.
2. Savunmacı Okuma (Defensive I/O): Çoklu encoding desteği, sütun doğrulama, NaN koruması.
3. Bellek Optimizasyonu (RAM-Friendly): Gereksiz .copy() zincirleri temizlendi, ara kopyalar engellendi.
4. Kural 9 Güvenliği: Level format normalizasyonu (.strip().capitalize()), deterministik öncelik sıralaması.
5. Sayısal Kimlik Sıralaması: Metin sıralaması tuzağı sıfır hata toleransıyla engellendi.
"""

from pathlib import Path
import re
import pandas as pd
import numpy as np

# Yollar
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
INTERIM_DIR = BASE_DIR / "data" / "interim"
INTERIM_DIR.mkdir(parents=True, exist_ok=True)


def ddinter_num(ddinter_id: str) -> int:
    """
    DDInterID'nin sayısal kısmını güvenle ayıklar.
    'DDInter1263' -> 1263
    'DDInter_1263' -> 1263
    """
    if not isinstance(ddinter_id, str):
        return 0
    m = re.search(r"(\d+)$", ddinter_id.strip())
    return int(m.group(1)) if m else 0


def ad_normalize(name: str) -> str:
    """
    Standart Ad Normalizasyonu (PDF Adım 4 kuralı):
    - Küçük harfe çevir
    - Baştaki/sondaki boşlukları sil
    - Tire ve alt tireleri tek boşluğa çevir
    - Ardışık boşlukları tek boşluğa indir
    """
    if not isinstance(name, str):
        return ""
    name = name.replace("İ", "i").replace("I", "ı").strip().lower().replace("\u0307", "")
    name = re.sub(r"[\-_—–]+", " ", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name


# Geriye dönük uyumluluk alias'ı
normalize_drug_name = ad_normalize


def safe_read_csv(fpath: Path, required_cols: list[str]) -> pd.DataFrame:
    """
    Savunmacı CSV Okuma:
    - Farklı karakter kodlamalarını (utf-8, utf-8-sig, latin1) sırayla dener.
    - Zorunlu sütunların varlığını doğrular.
    - Bozuk veya eksik dosyaları kontrollü raporlar.
    """
    for enc in ["utf-8", "utf-8-sig", "latin1"]:
        try:
            df = pd.read_csv(fpath, encoding=enc)
            missing = set(required_cols) - set(df.columns)
            if not missing:
                return df
        except Exception:
            continue
    raise ValueError(f"Bozuk veya eksik sütunlu dosya: {fpath.name}")


def read_all_raw_data(raw_dir: Path = RAW_DIR) -> pd.DataFrame:
    """
    I/O Optimizasyonu: 8 ham CSV dosyasını DİSKTEN SADECE 1 KEZ okur.
    Hem ddinter_ilac hem de etkilesim tablosu bu tek veri kümesinden türetilir.
    """
    files = sorted(raw_dir.glob("ddinter_downloads_code_*.csv"))
    if not files:
        raise FileNotFoundError(f"Ham DDInter dosyaları bulunamadı: {raw_dir}")

    required_cols = ["DDInterID_A", "Drug_A", "DDInterID_B", "Drug_B", "Level"]
    dfs = []

    for fpath in files:
        code = fpath.stem.split("_")[-1]
        df_part = safe_read_csv(fpath, required_cols)
        # Savunmacı temizlik: boş ID içeren satırları filtrele
        df_part = df_part.dropna(subset=["DDInterID_A", "DDInterID_B", "Level"]).copy()
        df_part["kaynak_dosya"] = code
        dfs.append(df_part)

    df_raw = pd.concat(dfs, ignore_index=True)
    print(f"✅ Ham veriler tek seferde okundu: {len(df_raw):,} satır (8 dosya)")
    return df_raw


def build_ddinter_ilac(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Ham veriden benzersiz ilaç listesini çıkarır (I/O israfı yapmaz, df_raw kullanır).
    Çıktı: data/interim/ddinter_ilac.csv (1.939 satır)
    """
    drugs_a = df_raw[["DDInterID_A", "Drug_A"]].rename(
        columns={"DDInterID_A": "ddinter_id", "Drug_A": "drug_name"}
    )
    drugs_b = df_raw[["DDInterID_B", "Drug_B"]].rename(
        columns={"DDInterID_B": "ddinter_id", "Drug_B": "drug_name"}
    )

    df_all_drugs = pd.concat([drugs_a, drugs_b], ignore_index=True)
    df_ilac = df_all_drugs.drop_duplicates(subset=["ddinter_id"]).copy()

    # Normalizasyon
    norm_names = df_ilac["drug_name"].apply(ad_normalize)
    df_ilac["ad_norm"] = norm_names
    df_ilac["drug_norm"] = norm_names  # İki anahtar adıyla da tam uyumlu

    # Sayısal Sıralama
    df_ilac["_num"] = df_ilac["ddinter_id"].apply(ddinter_num)
    df_ilac = df_ilac.sort_values("_num").reset_index(drop=True)
    df_ilac = df_ilac.drop(columns=["_num"])

    out_path = INTERIM_DIR / "ddinter_ilac.csv"
    df_ilac.to_csv(out_path, index=False, encoding="utf-8")
    print(f"✅ ddinter_ilac.csv oluşturuldu: {len(df_ilac):,} satır -> {out_path}")
    return df_ilac


def build_etkilesim(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Ham veriden tekilleştirilmiş etkileşim tablosunu üretir (I/O israfı yapmaz).
    - Sayısal ID sıralaması ile (id_1, id_2) standartlaştırılır.
    - Kural 9 önceliği uygulanır: Major > Moderate > Minor > Unknown.
    - Şiddet çelişkisi kontrol edilir (siddet_celiski = 1 / 0).
    - Çıktı Şeması: id_1, id_2, drug_1, drug_2, siddet, siddet_celiski, kaynak_dosyalar.
    """
    df = df_raw.copy()

    # Sayısal kimlikleri güvenle çıkar
    df["num_1"] = df["DDInterID_A"].apply(ddinter_num)
    df["num_2"] = df["DDInterID_B"].apply(ddinter_num)

    # ZORUNLU KURAL: id_1 daima küçük sayısal ID, id_2 büyük sayısal ID olmalıdır.
    mask = df["num_1"] <= df["num_2"]

    df["id_1"] = np.where(mask, df["DDInterID_A"], df["DDInterID_B"])
    df["drug_1"] = np.where(mask, df["Drug_A"], df["Drug_B"])
    df["id_2"] = np.where(mask, df["DDInterID_B"], df["DDInterID_A"])
    df["drug_2"] = np.where(mask, df["Drug_B"], df["Drug_A"])
    df["num_min"] = np.where(mask, df["num_1"], df["num_2"])
    df["num_max"] = np.where(mask, df["num_2"], df["num_1"])

    # Şiddet normalizasyonu: boşlukları kırp ve baş harfi büyüt
    df["Level_clean"] = df["Level"].astype(str).str.strip().str.capitalize()

    # Kural 9 Önceliği: Major (0) > Moderate (1) > Minor (2) > Unknown (3)
    sev_priority = {"Major": 0, "Moderate": 1, "Minor": 2, "Unknown": 3}
    df["sev_rank"] = df["Level_clean"].map(sev_priority).fillna(4).astype(int)

    # Kural 9 gereği en yüksek şiddeti seçmek için sev_rank'e göre sırala ve ilk kaydı tut
    df_sorted = df.sort_values("sev_rank")
    df_dedup = df_sorted.drop_duplicates(subset=["id_1", "id_2"], keep="first").copy()

    # Kaynak dosyaları birleştir (virgülle sıralı)
    src_grouped = df.groupby(["id_1", "id_2"])["kaynak_dosya"].unique()
    src_map = src_grouped.apply(lambda x: ", ".join(sorted(x)))
    pair_idx = df_dedup.set_index(["id_1", "id_2"]).index
    df_dedup["kaynak_dosyalar"] = pair_idx.map(src_map)

    # Şiddet çelişkisi kontrolü (aynı çiftte farklı Level değerleri varsa 1, yoksa 0)
    level_counts = df.groupby(["id_1", "id_2"])["Level_clean"].nunique()
    df_dedup["siddet_celiski"] = (pair_idx.map(level_counts) > 1).astype(int)
    df_dedup["siddet"] = df_dedup["Level_clean"]

    # Sayısal sıralama: num_min, num_max
    df_dedup = df_dedup.sort_values(["num_min", "num_max"]).reset_index(drop=True)

    # Standart Çıktı Şeması
    cols = ["id_1", "id_2", "drug_1", "drug_2", "siddet", "siddet_celiski", "kaynak_dosyalar"]
    df_etkilesim = df_dedup[cols].copy()

    out_path = INTERIM_DIR / "etkilesim.csv"
    df_etkilesim.to_csv(out_path, index=False, encoding="utf-8")
    print(f"✅ etkilesim.csv oluşturuldu: {len(df_etkilesim):,} benzersiz çift -> {out_path}")
    return df_etkilesim


def compute_statistics(df_etkilesim: pd.DataFrame, df_ilac: pd.DataFrame):
    """
    5 Temel Metriği Bellek Dostu Biçimde Hesaplar.
    """
    total_drugs = len(df_ilac)
    total_pairs = len(df_etkilesim)

    # Şiddet Dağılımı
    sev_counts = df_etkilesim["siddet"].value_counts()
    sev_pcts = (df_etkilesim["siddet"].value_counts(normalize=True) * 100).round(2)
    sev_df = pd.DataFrame({"Sayi": sev_counts, "Yuzde": sev_pcts})

    # Şiddet Çelişkisi
    total_celiski = int(df_etkilesim["siddet_celiski"].sum())

    # İlaç Başına Eş (Partner) Sayısı (İki Yönlü Derece)
    p1 = df_etkilesim[["id_1", "drug_1", "id_2"]].rename(
        columns={"id_1": "id", "drug_1": "name", "id_2": "partner"}
    )
    p2 = df_etkilesim[["id_2", "drug_2", "id_1"]].rename(
        columns={"id_2": "id", "drug_2": "name", "id_1": "partner"}
    )
    all_pairs = pd.concat([p1, p2], ignore_index=True)
    partner_counts = all_pairs.groupby("id")["partner"].nunique()
    names_by_id = all_pairs.groupby("id")["name"].first()

    avg_partners = float(partner_counts.mean())
    median_partners = float(partner_counts.median())
    min_partners = int(partner_counts.min())
    max_partners = int(partner_counts.max())

    # En Çok Etkileşen İlk 20 İlaç
    top20 = pd.DataFrame(
        {
            "ddinter_id": partner_counts.index,
            "drug_name": names_by_id,
            "es_sayisi": partner_counts.values,
        }
    ).sort_values("es_sayisi", ascending=False).head(20).reset_index(drop=True)

    stats = {
        "total_drugs": total_drugs,
        "total_pairs": total_pairs,
        "severity_dist": sev_df,
        "total_celiski": total_celiski,
        "avg_partners": avg_partners,
        "median_partners": median_partners,
        "min_partners": min_partners,
        "max_partners": max_partners,
        "top20": top20,
    }
    return stats


if __name__ == "__main__":
    print("=" * 60)
    print("İP4 — DDInter Veri Birleştirme Motoru (Production Modu)")
    print("=" * 60)
    
    # 1. Ham veri tek seferde okunur (I/O israfı yok)
    df_raw = read_all_raw_data(RAW_DIR)
    
    # 2. İki ara tablo bu tek ham veriden üretilir
    df_ilac = build_ddinter_ilac(df_raw)
    df_etkilesim = build_etkilesim(df_raw)
    
    # 3. İstatistikler hesaplanır
    stats = compute_statistics(df_etkilesim, df_ilac)

    print("\n" + "=" * 60)
    print("HESAPLANAN METRİKLER (TEKRAR TEMİZLİĞİ SONRASI):")
    print("=" * 60)
    print(f"1. Benzersiz İlaç Sayısı           : {stats['total_drugs']:,}")
    print(f"2. Benzersiz Etkileşim Çifti Sayısı : {stats['total_pairs']:,}")
    print(f"3. Şiddet Çelişkisi (siddet_celiski): {stats['total_celiski']:,}")
    print(f"4. İlaç Başına Ortalama Eş Sayısı   : {stats['avg_partners']:.2f}")
    print(f"   İlaç Başına Medyan Eş Sayısı     : {stats['median_partners']:.1f}")
    print(f"   (Min: {stats['min_partners']}, Maks: {stats['max_partners']})")
    print("\n5. Şiddet Dağılımı:")
    print(stats["severity_dist"])
    print("\n6. En Çok Etkileşen İlk 20 İlaç:")
    print(stats["top20"].to_string())
