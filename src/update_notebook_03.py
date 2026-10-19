"""
src/update_notebook_03.py
═══════════════════════════════════════════════════════════════════════════════
İP3: İngilizce Ad Köprüsü ve DDInter Eşlemesi (Kişi A & Kişi B İş Birliği)
═══════════════════════════════════════════════════════════════════════════════
Bu script:
1. Kişi A'nın `notebooks/03_kopru_ddinter.ipynb` içindeki Yol A, Yol B ve SKRS
   adımlarını (Hücre 0-16) %100 koruyarak temel alır.
2. Kişi B'nin SKRS adımı (Kural 5/6), Yol C (tr_en_kurallar.csv kural motoru),
   DDInter eşleme (ddinter_id & ad_en_ham), PubChem API kontrolü,
   Kişi C için ruhsatli_esleme_taslagi.csv ve 4 zorunlu tablo içeren
   docs/esleme_raporu.md hücrelerini A'nın devamına ekler.
3. Tüm notebook'u baştan sona çalıştırarak çıktıları pre-render eder ve
   notebooks/03_kopru_ddinter.ipynb dosyasını günceller.
"""

import io
import json
import sys
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from typing import Any, Dict, List

BASE_DIR = Path(__file__).resolve().parent.parent
NOTEBOOKS_DIR = BASE_DIR / "notebooks"
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
CONFIG_DIR = BASE_DIR / "config"
DOCS_DIR = BASE_DIR / "docs"


def create_kisi_b_cells() -> List[Dict[str, Any]]:
    """Kişi B'nin sorumluluğundaki hücreleri üretir."""
    cells = []

    # Hücre 17: Kişi B Giriş Markdown
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "---\n",
            "# ════════════════════════════════════════════════════════════════\n",
            "# İP3 — Kişi B: Yol C, DDInter Eşleme, PubChem ve Raporlama (Gün 5–6)\n",
            "# ════════════════════════════════════════════════════════════════\n",
            "\n",
            "**Kişi B Sorumluluk Alanı ve İş Akışı:**\n",
            "1. **Adım 3 — SKRS ve Yol C:** Kişi A'nın Yol A ve Yol B sonrasında bıraktığı bileşenlere SKRS (Kural 5/6) ve `config/tr_en_kurallar.csv` kural motorunu uygulama.\n",
            "2. **Adım 4 — DDInter Eşlemesi:** DDInter `ad_norm` fihristi ile birebir eşleştirme, `ad_en_ham` izlenebilirliği ve `ddinter_id` atama.\n",
            "3. **Adım 4 — PubChem En Sık 100 Kontrolü:** Kapsam içi en sık 100 eşleşmeyen bileşen için PubChem API ile kurtarma denemesi.\n",
            "4. **Kişi C Taslağı:** Eşleşmeyen bileşenleri sıklık sırasına, `atc_ipucu` ve `urun_ornegi` bağlamıyla `data/interim/ruhsatli_esleme_taslagi.csv` olarak hazırlama.\n",
            "5. **Teslimatlar:** `data/interim/etken_madde.csv` ve 4 zorunlu tabloyu içeren `docs/esleme_raporu.md` raporu.\n"
        ]
    })

    # Hücre 18: Yol C Kural Motoru
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# ─── 8. Yol C: Kural Tabanlı Eşleme Motoru (tr_en_kurallar.csv) ────────────\n",
            "import re\n",
            "\n",
            "def suffix_specificity(pattern: str) -> int:\n",
            "    \"\"\"Sonek kuralının özgüllüğünü hesaplar (harf sayısı).\"\"\"\n",
            "    return len(re.sub(r'[^a-zA-Z]', '', str(pattern)))\n",
            "\n",
            "def kural_adaylari(bilesen_tr: str, kurallar_df: pd.DataFrame) -> list:\n",
            "    \"\"\"Türkçe etken madde adı için kurallardan öncelik sıralı İngilizce aday listesi üretir.\"\"\"\n",
            "    if not isinstance(bilesen_tr, str) or not bilesen_tr.strip():\n",
            "        return []\n",
            "    ham = bilesen_tr.lower().strip()\n",
            "    df_rules = kurallar_df.dropna(subset=['kural_tipi', 'eski', 'yeni']).copy()\n",
            "    suffix_rules = df_rules[df_rules['kural_tipi'] == 'suffix_replace'].copy()\n",
            "    suffix_rules['_spec'] = suffix_rules['eski'].apply(suffix_specificity)\n",
            "    suffix_rules = suffix_rules.sort_values('_spec', ascending=False)\n",
            "    char_rules = df_rules[df_rules['kural_tipi'] == 'char_replace']\n",
            "\n",
            "    # 1. Sonek kurallarına uyan adaylar\n",
            "    sonek_adaylar = []\n",
            "    for _, kural in suffix_rules.iterrows():\n",
            "        eski, yeni = str(kural['eski']), str(kural['yeni'])\n",
            "        if re.search(eski, ham):\n",
            "            sonek_adaylar.append(re.sub(eski, yeni, ham))\n",
            "\n",
            "    base_forms = sonek_adaylar + [ham]\n",
            "    adaylar = []\n",
            "\n",
            "    # 2. Tüm karakter kuralları birlikte uygulandığında\n",
            "    for base in base_forms:\n",
            "        all_char = base\n",
            "        for _, kural in char_rules.iterrows():\n",
            "            all_char = all_char.replace(str(kural['eski']), str(kural['yeni']))\n",
            "        if all_char not in adaylar:\n",
            "            adaylar.append(all_char)\n",
            "\n",
            "    # 3. Tek tek karakter kuralları uygulandığında\n",
            "    for base in base_forms:\n",
            "        for _, kural in char_rules.iterrows():\n",
            "            c_cand = base.replace(str(kural['eski']), str(kural['yeni']))\n",
            "            if c_cand not in adaylar:\n",
            "                adaylar.append(c_cand)\n",
            "\n",
            "    # 4. Doğrudan baz formlar (sadece sonek veya ham)\n",
            "    for base in base_forms:\n",
            "        if base not in adaylar:\n",
            "            adaylar.append(base)\n",
            "\n",
            "    return adaylar\n",
            "\n",
            "def yol_c_esle(bilesen_tr: str, ddinter_norm_set: set, kurallar_df: pd.DataFrame):\n",
            "    \"\"\"Kural adaylarından DDInter'da bulunan ilk ad_norm değerini döner, yoksa None döner.\"\"\"\n",
            "    for aday in kural_adaylari(bilesen_tr, kurallar_df):\n",
            "        norm = ad_normalize(aday)\n",
            "        if norm in ddinter_norm_set:\n",
            "            return norm\n",
            "    return None\n",
            "\n",
            "def yol_a_olcum(yol_a_df: pd.DataFrame, kurallar_df: pd.DataFrame):\n",
            "    \"\"\"Kuralların Yol A test çiftleri (1.922 çift) üzerindeki tahmin başarısını ölçer.\"\"\"\n",
            "    df = yol_a_df[['bilesen_tr', 'ad_en']].dropna().copy()\n",
            "    ok = df.apply(\n",
            "        lambda r: ad_normalize(r['ad_en']) in [\n",
            "            ad_normalize(a) for a in kural_adaylari(r['bilesen_tr'], kurallar_df)\n",
            "        ],\n",
            "        axis=1\n",
            "    )\n",
            "    basari_orani = float(ok.mean() * 100)\n",
            "    tutmayanlar = df[~ok].copy()\n",
            "    return basari_orani, tutmayanlar\n",
            "\n",
            "kurallar_yol = kok / 'config' / 'tr_en_kurallar.csv'\n",
            "df_kurallar = pd.read_csv(kurallar_yol)\n",
            "ddinter_norm_set = set(df_ddinter_ilac['ad_norm'].dropna().tolist())\n",
            "\n",
            "# Yol A test seti (1.922 çift) üzerinde kural başarı ölçümü\n",
            "basari_orani, _ = yol_a_olcum(df_etken_madde[df_etken_madde['yol'] == 'A'], df_kurallar)\n",
            "\n",
            "print(f\"✓ Yol C kural motoru yüklendi ({len(df_kurallar)} kural).\")\n",
            "print(f\"✓ Yol A test çiftleri üzerindeki kural başarı oranı: %{basari_orani:.1f}\")\n",
            "print()\n",
            "print(\"Örnek Kural Testleri:\")\n",
            "for test_tr in [\"amlodipin\", \"gentamisin\", \"morfin\", \"parasetamol\", \"fluoksetin\", \"levodopa\", \"omeprazol\", \"diklofenak\", \"indapamid\", \"budesonid\"]:\n",
            "    eslesti = yol_c_esle(test_tr, ddinter_norm_set, df_kurallar)\n",
            "    durum = f\"DDInter Eşleşti: {eslesti}\" if eslesti else \"DDInter'da Yok\"\n",
            "    print(f\"  {test_tr:<15} -> {durum}\")\n",
            "\n",
            "# Regresyon Koruma Testi (Amlodipin, Gentamisin, Morfin, Fluoksetin)\n",
            "for tr, en in [('amlodipin', 'amlodipine'), ('gentamisin', 'gentamicin'), ('morfin', 'morphine'), ('fluoksetin', 'fluoxetine')]:\n",
            "    assert yol_c_esle(tr, ddinter_norm_set, df_kurallar) == en, f'Yol C regresyon: {tr}'\n",
            "print(\"✓ Tüm Yol C regresyon testleri başarıyla doğrulandı.\")\n"
        ]
    })

    # Hücre 19: SKRS ve Yol C Uygulanması
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# ─── 9. SKRS (Kural 5/6) ve Yol C Uygulanması ────────────────────────────\n",
            "# 1. Kapsam İçi / Kapsam Dışı Bayrağının Hesaplanması (Kural 11)\n",
            "kd = df_ue.merge(df_urun[['barkod', 'kapsam_disi']], on='barkod')\n",
            "kd['kapsam_disi'] = pd.to_numeric(kd['kapsam_disi'], errors='coerce').fillna(0).astype(int)\n",
            "kapsam_ici_kumesi = set(kd.loc[kd['kapsam_disi'] == 0, 'bilesen_tr'])\n",
            "df_etken_madde['kapsam_ici'] = df_etken_madde['bilesen_tr'].isin(kapsam_ici_kumesi).astype(int)\n",
            "\n",
            "# 2. SKRS Ürünlerinin Bileşenleri (Sabit Kural 5 ve Kural 6):\n",
            "# SKRS'te aktif olup ruhsatlıda olmayan ürünlerin bileşenleri zaten İngilizcedir (ATC adından bölünmüştür).\n",
            "# Bu nedenle Türkçe çeviri motoruna sokulmadan doğrudan İngilizce ad olarak atanır ve yol='SKRS' olur.\n",
            "# İngilizce adda Türkçe noktasız 'ı' hatası temizlenir (örn: combınatıon -> combination)\n",
            "skrs_bar = set(df_urun.loc[df_urun['kaynak'] == 'SKRS', 'barkod'])\n",
            "skrs_bilesenler = set(df_ue[df_ue['barkod'].isin(skrs_bar)]['bilesen_tr'])\n",
            "mask_skrs = (df_etken_madde['yol'] == 'eslesmedi') & (df_etken_madde['bilesen_tr'].isin(skrs_bilesenler))\n",
            "df_etken_madde.loc[mask_skrs, 'ad_en'] = (\n",
            "    df_etken_madde.loc[mask_skrs, 'bilesen_tr']\n",
            "    .str.replace('ı', 'i', regex=False)\n",
            "    .apply(ad_normalize)\n",
            ")\n",
            "df_etken_madde.loc[mask_skrs, 'yol'] = 'SKRS'\n",
            "skrs_sayisi = int(mask_skrs.sum())\n",
            "\n",
            "# 3. Yol C: Kalan Eşleşmemiş Bileşenlere Çoklu Adaylı Kural Motoru\n",
            "mask_eslesmedi = df_etken_madde['yol'] == 'eslesmedi'\n",
            "yol_c_adaylar = df_etken_madde.loc[mask_eslesmedi, 'bilesen_tr'].apply(\n",
            "    lambda b: yol_c_esle(b, ddinter_norm_set, df_kurallar)\n",
            ")\n",
            "basarili = yol_c_adaylar.dropna()\n",
            "df_etken_madde.loc[basarili.index, 'ad_en'] = basarili\n",
            "df_etken_madde.loc[basarili.index, 'yol'] = 'C'\n",
            "yol_c_sayisi = len(basarili)\n",
            "\n",
            "print(f\"✓ SKRS adımı tamamlandı: {skrs_sayisi} bileşen (yol='SKRS')\")\n",
            "print(f\"✓ Yol C eşleştirmesi tamamlandı: {yol_c_sayisi} yeni bileşen DDInter'a bağlandı (yol='C')\")\n",
            "print()\n",
            "print(\"Yol Dağılımı (SKRS ve Yol C Sonrası):\")\n",
            "print(df_etken_madde['yol'].value_counts())\n"
        ]
    })

    # Hücre 20: DDInter ID Ataması
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# ─── 10. DDInter ID Ataması (`ddinter_id`) ve İzlenebilirlik (`ad_en_ham`) ──\n",
            "df_etken_madde['ad_en_ham'] = df_etken_madde['ad_en'].copy()  # Yol A/B/C/SKRS orijinal adı korunur\n",
            "df_etken_madde['ad_norm'] = df_etken_madde['ad_en'].apply(\n",
            "    lambda x: ad_normalize(str(x)) if pd.notna(x) and str(x).strip() else None\n",
            ")\n",
            "df_etken_madde['ddinter_id'] = df_etken_madde['ad_norm'].map(ddinter_dict)\n",
            "df_etken_madde['eslesme_kaynagi'] = np.where(df_etken_madde['ddinter_id'].notna(), 'tam_ad', None)\n",
            "\n",
            "print(\"✓ DDInter ID eşleştirmesi tamamlandı:\")\n",
            "for y in ['A', 'B', 'C', 'SKRS', 'eslesmedi']:\n",
            "    sub = df_etken_madde[df_etken_madde['yol'] == y]\n",
            "    matched = sub['ddinter_id'].notna().sum()\n",
            "    toplam = len(sub)\n",
            "    oran = (matched / toplam * 100) if toplam > 0 else 0\n",
            "    print(f\"  Yol {y:<9}: Toplam = {toplam:>4}, DDInter Eşleşen = {matched:>4} (%{oran:5.1f})\")\n",
            "\n",
            "toplam_eslesen = df_etken_madde['ddinter_id'].notna().sum()\n",
            "print()\n",
            "print(f\"Toplam DDInter ile Eşleşen Etken Madde: {toplam_eslesen:,} / {len(df_etken_madde):,} (%{toplam_eslesen/len(df_etken_madde)*100:.2f})\")\n"
        ]
    })

    # Hücre 21: PubChem Eş Anlamlı Kontrolü
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# ─── 11. PubChem Eş Anlamlı Kontrolü (En Sık 100 Kapsam İçi Eşleşmemiş) ───\n",
            "import hashlib\n",
            "import json\n",
            "import time\n",
            "import urllib.parse\n",
            "import requests\n",
            "\n",
            "CACHE_DIR = kok / 'data' / 'cache' / 'pubchem'\n",
            "CACHE_DIR.mkdir(parents=True, exist_ok=True)\n",
            "\n",
            "LAST_PUBCHEM_TIME = 0.0\n",
            "PUBCHEM_HEADERS = {'User-Agent': 'DDInter_Pipeline/1.0 (academic-research; ddi-project)'}\n",
            "\n",
            "def pubchem_synonyms_guvenli(ad: str, cache_dir: Path = CACHE_DIR, max_retries: int = 3) -> list:\n",
            "    \"\"\"PubChem REST API'den güvenle eş anlamlı listesi çeker.\n",
            "    \n",
            "    Özellikler:\n",
            "    - Rate Limit: İstekler arası >= 0.20 sn bekler (en fazla 5 istek/sn).\n",
            "    - Cache: data/cache/pubchem/<md5>.json altında saklar.\n",
            "    - 404 Koruması: Bulunamayan bileşikler boş liste [] olarak önbelleğe yazılır, mükerrer ağ istekleri önlenir.\n",
            "    \"\"\"\n",
            "    global LAST_PUBCHEM_TIME\n",
            "    if not ad or pd.isna(ad):\n",
            "        return []\n",
            "    clean = ad_normalize(str(ad))\n",
            "    if not clean:\n",
            "        return []\n",
            "    h = hashlib.md5(clean.encode('utf-8')).hexdigest()\n",
            "    f = cache_dir / f\"{h}.json\"\n",
            "    if f.exists():\n",
            "        try:\n",
            "            if f.stat().st_size > 0:\n",
            "                with open(f, 'r', encoding='utf-8') as fp:\n",
            "                    d = json.load(fp)\n",
            "                    return d if isinstance(d, list) else d.get('synonyms', [])\n",
            "        except Exception:\n",
            "            pass\n",
            "    encoded_name = urllib.parse.quote(clean)\n",
            "    url = f\"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{encoded_name}/synonyms/JSON\"\n",
            "    synonyms = []\n",
            "    should_cache = False\n",
            "    for attempt in range(1, max_retries + 1):\n",
            "        elapsed = time.time() - LAST_PUBCHEM_TIME\n",
            "        if elapsed < 0.20:\n",
            "            time.sleep(0.20 - elapsed)\n",
            "        LAST_PUBCHEM_TIME = time.time()\n",
            "        try:\n",
            "            resp = requests.get(url, headers=PUBCHEM_HEADERS, timeout=10)\n",
            "            if resp.status_code == 200:\n",
            "                data = resp.json()\n",
            "                info = data.get('InformationList', {}).get('Information', [])\n",
            "                if info:\n",
            "                    synonyms = info[0].get('Synonym', [])\n",
            "                should_cache = True\n",
            "                break\n",
            "            elif resp.status_code == 404:\n",
            "                synonyms = []\n",
            "                should_cache = True\n",
            "                break\n",
            "            elif resp.status_code in (429, 500, 502, 503, 504):\n",
            "                time.sleep(attempt * 1.0)\n",
            "                continue\n",
            "            else:\n",
            "                return []\n",
            "        except requests.RequestException:\n",
            "            time.sleep(attempt * 1.0)\n",
            "            continue\n",
            "    if should_cache:\n",
            "        try:\n",
            "            f.write_text(json.dumps(synonyms, ensure_ascii=False), encoding='utf-8')\n",
            "        except Exception:\n",
            "            pass\n",
            "    return synonyms\n",
            "\n",
            "# DDInter'da eşleşmeyen en sık 100 kapsam içi bileşen\n",
            "df_eslesmeyen_top100 = (\n",
            "    df_etken_madde[df_etken_madde['ddinter_id'].isna() & (df_etken_madde['kapsam_ici'] == 1)]\n",
            "    .sort_values(by=['urun_sayisi', 'bilesen_tr'], ascending=[False, True])\n",
            "    .head(100).copy()\n",
            ")\n",
            "\n",
            "pubchem_kurtarilan = 0\n",
            "kurtarilan_detaylar = []\n",
            "for row in df_eslesmeyen_top100.itertuples():\n",
            "    idx = row.Index\n",
            "    aday_adlar = []\n",
            "    if pd.notna(row.ad_en) and str(row.ad_en).strip():\n",
            "        aday_adlar.append(str(row.ad_en))\n",
            "    if pd.notna(row.bilesen_tr) and str(row.bilesen_tr).strip():\n",
            "        aday_adlar.append(str(row.bilesen_tr))\n",
            "        \n",
            "    eslesti = False\n",
            "    for ad in aday_adlar:\n",
            "        if eslesti:\n",
            "            break\n",
            "        syns = pubchem_synonyms_guvenli(ad, cache_dir=CACHE_DIR)\n",
            "        for syn in syns:\n",
            "            norm_syn = ad_normalize(syn)\n",
            "            if norm_syn in ddinter_dict:\n",
            "                matched_id = ddinter_dict[norm_syn]\n",
            "                df_etken_madde.at[idx, 'ddinter_id'] = matched_id\n",
            "                df_etken_madde.at[idx, 'ad_norm'] = norm_syn\n",
            "                df_etken_madde.at[idx, 'ad_en'] = norm_syn\n",
            "                df_etken_madde.at[idx, 'eslesme_kaynagi'] = 'pubchem'\n",
            "                pubchem_kurtarilan += 1\n",
            "                kurtarilan_detaylar.append((row.bilesen_tr, norm_syn, matched_id))\n",
            "                eslesti = True\n",
            "                break\n",
            "\n",
            "# Kurtarılan PubChem eşleşmelerinin aynı ham İngilizce ada sahip diğer satırlara yayılması\n",
            "# (Örn: parasetamol -> acetaminophen kurtarılınca, SKRS'ten gelen paracetamol satırı da acetaminophen'e bağlanır)\n",
            "recovered_syn_map = {}\n",
            "for idx in df_etken_madde[df_etken_madde['eslesme_kaynagi'] == 'pubchem'].index:\n",
            "    norm_ham = ad_normalize(str(df_etken_madde.at[idx, 'ad_en_ham'])) if pd.notna(df_etken_madde.at[idx, 'ad_en_ham']) else ''\n",
            "    norm_tr = ad_normalize(str(df_etken_madde.at[idx, 'bilesen_tr']))\n",
            "    target_syn = df_etken_madde.at[idx, 'ad_en']\n",
            "    target_id = df_etken_madde.at[idx, 'ddinter_id']\n",
            "    if norm_ham:\n",
            "        recovered_syn_map[norm_ham] = (target_syn, target_id)\n",
            "    if norm_tr:\n",
            "        recovered_syn_map[norm_tr] = (target_syn, target_id)\n",
            "\n",
            "yayilim_sayisi = 0\n",
            "for idx in df_etken_madde[df_etken_madde['ddinter_id'].isna()].index:\n",
            "    norm_ham = ad_normalize(str(df_etken_madde.at[idx, 'ad_en_ham'])) if pd.notna(df_etken_madde.at[idx, 'ad_en_ham']) else ''\n",
            "    norm_tr = ad_normalize(str(df_etken_madde.at[idx, 'bilesen_tr']))\n",
            "    matched = None\n",
            "    if norm_ham and norm_ham in recovered_syn_map:\n",
            "        matched = recovered_syn_map[norm_ham]\n",
            "    elif norm_tr and norm_tr in recovered_syn_map:\n",
            "        matched = recovered_syn_map[norm_tr]\n",
            "    if matched:\n",
            "        df_etken_madde.at[idx, 'ddinter_id'] = matched[1]\n",
            "        df_etken_madde.at[idx, 'ad_norm'] = matched[0]\n",
            "        df_etken_madde.at[idx, 'ad_en'] = matched[0]\n",
            "        df_etken_madde.at[idx, 'eslesme_kaynagi'] = 'pubchem_yayilim'\n",
            "        yayilim_sayisi += 1\n",
            "\n",
            "print(f\"✓ PubChem taraması tamamlandı: En sık 100 kapsam içi eşleşmeyenden {pubchem_kurtarilan} ek etken madde DDInter'a bağlandı.\")\n",
            "if yayilim_sayisi > 0:\n",
            "    print(f\"✓ Kurtarılan eşleşmeler aynı ham ada sahip {yayilim_sayisi} ek bileşene uygulandı (örn. SKRS paracetamol -> acetaminophen).\")\n",
            "print(\"Gözle Kontrol (Kurtarılan Eşleşmeler):\")\n",
            "for b_tr, syn_ad, did in kurtarilan_detaylar:\n",
            "    print(f\"  {b_tr:<20} -> {syn_ad:<22} ({did})\")\n"
        ]
    })

    # Hücre 22: Kişi C İçin Yol D Taslağı
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# ─── 12. Kişi C İçin Yol D Taslağı (ruhsatli_esleme_taslagi.csv) ───────────\n",
            "# DDInter ile eşleşmeyen tüm bileşenler; kapsam_ici=1 olanlar öne alınarak sıralanır.\n",
            "# Kişi C'nin elle eşlemesini kolaylaştırmak için 'atc_ipucu' ve 'urun_ornegi' eklenir.\n",
            "taslak_c = df_etken_madde[df_etken_madde['ddinter_id'].isna()].copy()\n",
            "taslak_c['durum'] = np.where(\n",
            "    taslak_c['ad_en'].notna() & (taslak_c['ad_en'].astype(str).str.strip() != ''),\n",
            "    'ingilizce_var_ddinter_yok',\n",
            "    'ceviri_yok'\n",
            ")\n",
            "\n",
            "_ua = df_ue.merge(df_urun[['barkod', 'atc_final', 'urun_adi']], on='barkod')\n",
            "atc_ornek = _ua.dropna(subset=['atc_final']).groupby('bilesen_tr')['atc_final'].agg(\n",
            "    lambda s: s.mode().iloc[0] if not s.empty and not s.mode().empty else None\n",
            ")\n",
            "urun_ornek = _ua.groupby('bilesen_tr')['urun_adi'].first()\n",
            "taslak_c['atc_ipucu'] = taslak_c['bilesen_tr'].map(atc_ornek)\n",
            "taslak_c['urun_ornegi'] = taslak_c['bilesen_tr'].map(urun_ornek)\n",
            "taslak_c = taslak_c.sort_values(\n",
            "    by=['kapsam_ici', 'urun_sayisi', 'bilesen_tr'],\n",
            "    ascending=[False, False, True]\n",
            ").reset_index(drop=True)\n",
            "\n",
            "taslak_c_yol = kok / 'data' / 'interim' / 'ruhsatli_esleme_taslagi.csv'\n",
            "sutunlar_taslak = ['bilesen_tr', 'ad_en', 'atc', 'atc_ipucu', 'yol', 'urun_sayisi', 'kapsam_ici', 'durum', 'urun_ornegi']\n",
            "taslak_c[sutunlar_taslak].to_csv(taslak_c_yol, index=False)\n",
            "\n",
            "print(f\"✓ Kişi C için ruhsatli_esleme_taslagi.csv kaydedildi: {taslak_c_yol}\")\n",
            "print(f\"  Eşleşmeyen toplam bileşen sayısı: {len(taslak_c):,}\")\n",
            "print(f\"  Bunlardan kapsam içi olanlar     : {(taslak_c['kapsam_ici'] == 1).sum():,}\")\n",
            "print()\n",
            "print(\"En Sık Eşleşmeyen İlk 10 Kapsam İçi Bileşen (Kişi C Öncelikli & İpuçlu):\")\n",
            "print(taslak_c[['bilesen_tr', 'urun_sayisi', 'atc_ipucu', 'durum', 'urun_ornegi']].head(10))\n"
        ]
    })

    # Hücre 23: Nihai etken_madde.csv Kaydedilmesi
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# ─── 13. Nihai etken_madde.csv Tablosunun Kaydedilmesi ────────────────────\n",
            "# ATC Ana Grubu Hesaplanması (Mode esasına göre ilk harf A-V; D05 ve E09 için zorunlu)\n",
            "ue_atc = df_ue.merge(df_urun[['barkod', 'atc_final']], on='barkod').dropna(subset=['atc_final'])\n",
            "ue_atc = ue_atc[ue_atc['atc_final'].astype(str).str.len() >= 1]\n",
            "atc_grup = ue_atc.groupby('bilesen_tr')['atc_final'].agg(\n",
            "    lambda s: s.astype(str).str[:1].str.upper().mode().iloc[0] if not s.empty and not s.mode().empty else None\n",
            ")\n",
            "df_etken_madde['atc_ana'] = df_etken_madde['bilesen_tr'].map(atc_grup)\n",
            "\n",
            "# Plandaki standart sütunlar ve ek izleme sütunları (ad_en_ham, atc_ana, kapsam_ici, eslesme_kaynagi)\n",
            "sutunlar = ['bilesen_tr', 'ad_en', 'ad_en_ham', 'atc', 'atc_ana', 'yol', 'urun_sayisi', 'ddinter_id', 'kapsam_ici', 'eslesme_kaynagi']\n",
            "df_etken_madde_nihai = df_etken_madde[sutunlar].sort_values(\n",
            "    by=['urun_sayisi', 'bilesen_tr'], ascending=[False, True]\n",
            ").reset_index(drop=True)\n",
            "\n",
            "etken_cikti_yol = kok / 'data' / 'interim' / 'etken_madde.csv'\n",
            "df_etken_madde_nihai.to_csv(etken_cikti_yol, index=False)\n",
            "\n",
            "print(f\"✓ Nihai etken_madde.csv başarıyla kaydedildi: {etken_cikti_yol}\")\n",
            "print(f\"  Toplam satır sayısı          : {len(df_etken_madde_nihai):,}\")\n",
            "print(f\"  DDInter ID içeren satır sayısı: {df_etken_madde_nihai['ddinter_id'].notna().sum():,}\")\n",
            "print(f\"  Kapsam içi satır sayısı       : {(df_etken_madde_nihai['kapsam_ici'] == 1).sum():,}\")\n"
        ]
    })

    # Hücre 24: Eşleşme Raporunun Üretilmesi (4 Zorunlu Tablo)
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# ─── 14. Eşleşme Raporu ve 4 Zorunlu Tablo (docs/esleme_raporu.md) ─────────\n",
            "total_etken = len(df_etken_madde_nihai)\n",
            "matched_etken = int(df_etken_madde_nihai['ddinter_id'].notna().sum())\n",
            "matched_etken_pct = (matched_etken / total_etken * 100) if total_etken > 0 else 0\n",
            "\n",
            "# Kapsam içi etken madde metrikleri\n",
            "kapsam_ici_etken = df_etken_madde_nihai[df_etken_madde_nihai['kapsam_ici'] == 1]\n",
            "total_kapsam_ici_etken = len(kapsam_ici_etken)\n",
            "matched_kapsam_ici_etken = int(kapsam_ici_etken['ddinter_id'].notna().sum())\n",
            "matched_kapsam_ici_etken_pct = (matched_kapsam_ici_etken / total_kapsam_ici_etken * 100) if total_kapsam_ici_etken > 0 else 0\n",
            "\n",
            "# 1. Ürün Kapsama Oranı (Ruhsatlı ürünler) - Doğrudan bilesen_tr ile Temiz Birleştirme\n",
            "ruhsatli_barkodlar = set(df_urun.loc[df_urun['kaynak'] == 'Ruhsatlı', 'barkod'])\n",
            "df_ue_ruhsatli = df_ue[df_ue['barkod'].isin(ruhsatli_barkodlar)].copy()\n",
            "\n",
            "ddinter_bilesen_kumesi = set(df_etken_madde_nihai.loc[df_etken_madde_nihai['ddinter_id'].notna(), 'bilesen_tr'])\n",
            "kapsanan_barkodlar = set(df_ue_ruhsatli[df_ue_ruhsatli['bilesen_tr'].isin(ddinter_bilesen_kumesi)]['barkod'])\n",
            "\n",
            "total_urun = len(ruhsatli_barkodlar)\n",
            "matched_urun = len(kapsanan_barkodlar)\n",
            "matched_urun_pct = (matched_urun / total_urun * 100) if total_urun > 0 else 0\n",
            "\n",
            "# Kapsam içi ürün metrikleri (kapsam_disi == 0)\n",
            "kapsam_ici_barkodlar = set(df_urun.loc[(df_urun['kaynak'] == 'Ruhsatlı') & (df_urun['kapsam_disi'] == 0), 'barkod'])\n",
            "kapsanan_kapsam_ici_barkodlar = kapsanan_barkodlar & kapsam_ici_barkodlar\n",
            "total_kapsam_ici_urun = len(kapsam_ici_barkodlar)\n",
            "matched_kapsam_ici_urun = len(kapsanan_kapsam_ici_barkodlar)\n",
            "matched_kapsam_ici_urun_pct = (matched_kapsam_ici_urun / total_kapsam_ici_urun * 100) if total_kapsam_ici_urun > 0 else 0\n",
            "\n",
            "# Tablo 1: Yol Bazında Bileşen Sayısı ve DDInter Eşleşme Oranı\n",
            "yol_tanimlari = [\n",
            "    ('A', 'Yol A (Tek Bileşenli ATC)', 'Tek bileşenli ürünlerin SKRS ATC sözlüğünden İngilizce adı'),\n",
            "    ('B', 'Yol B (Kombine Bölme & RapidFuzz)', 'Kombine ürünlerin ATC adından ayrıştırılan bileşenler'),\n",
            "    ('C', 'Yol C (Kural Tabanlı - tr_en_kurallar)', 'Türkçe kural tabanlı çeviri motoru ile eşleşenler'),\n",
            "    ('SKRS', 'SKRS (Kural 5/6)', 'SKRS\\'ten doğrudan İngilizce gelen ürünler'),\n",
            "    ('eslesmedi', 'Eşleşmedi (Kişi C - Yol D Adayları)', 'Kural motoru ve PubChem ile eşleşmeyip Kişi C uzman incelemesine kalanlar'),\n",
            "]\n",
            "tablo_1_satirlar = []\n",
            "for y_kod, y_ad, aciklama in yol_tanimlari:\n",
            "    sub = df_etken_madde_nihai[df_etken_madde_nihai['yol'] == y_kod]\n",
            "    tot = len(sub)\n",
            "    esl = int(sub['ddinter_id'].notna().sum())\n",
            "    oran = (esl / tot * 100) if tot > 0 else 0\n",
            "    tablo_1_satirlar.append((y_ad, tot, esl, oran, aciklama))\n",
            "\n",
            "# Tablo 3: ATC Ana Grubuna Göre DDInter Eşleşme Oranı (14 Satır - Kapsam İçi Filtreli)\n",
            "valid_atc_em = df_etken_madde_nihai[\n",
            "    (df_etken_madde_nihai['kapsam_ici'] == 1) & df_etken_madde_nihai['atc_ana'].isin(list('ABCDGHJLMNPRSV'))\n",
            "]\n",
            "\n",
            "atc_gruplari = []\n",
            "for g in sorted(list('ABCDGHJLMNPRSV')):\n",
            "    sub = valid_atc_em[valid_atc_em['atc_ana'] == g]\n",
            "    tot = len(sub)\n",
            "    esl = int(sub['ddinter_id'].notna().sum())\n",
            "    oran = (esl / tot * 100) if tot > 0 else 0\n",
            "    atc_gruplari.append((g, tot, esl, oran))\n",
            "\n",
            "# Tablo 4: Eşleşmeyen En Sık 30 Bileşen (Kapsam İçi Filtreli Öncelik Listesi)\n",
            "eslesmeyen_top30 = df_etken_madde_nihai[\n",
            "    df_etken_madde_nihai['ddinter_id'].isna() & (df_etken_madde_nihai['kapsam_ici'] == 1)\n",
            "].head(30)\n",
            "\n",
            "# Parasetamol ve PubChem metrikleri (dinamik ve güvenli)\n",
            "pubchem_dogrudan = int((df_etken_madde_nihai['eslesme_kaynagi'] == 'pubchem').sum())\n",
            "pubchem_yayilim_cnt = int((df_etken_madde_nihai['eslesme_kaynagi'] == 'pubchem_yayilim').sum())\n",
            "parasetamol_info = \"\"\n",
            "p = df_etken_madde_nihai[\n",
            "    (df_etken_madde_nihai['bilesen_tr'] == 'parasetamol')\n",
            "    & (df_etken_madde_nihai['eslesme_kaynagi'].isin(['pubchem', 'pubchem_yayilim']))\n",
            "]\n",
            "if not p.empty:\n",
            "    r = p.iloc[0]\n",
            "    parasetamol_info = f\" Örneğin {int(r['urun_sayisi'])} ürünlü parasetamol → {r['ddinter_id']} ({r['ad_en']}).\"\n",
            "\n",
            "# Markdown Rapor Metni Oluştur\n",
            "rapor_lines = [\n",
            "    \"# İP3: DDInter İlaç Eşleşme Raporu\",\n",
            "    \"\",\n",
            "    f\"> **Özet:** Türkiye'deki kapsam içi etken maddelerin %{matched_kapsam_ici_etken_pct:.1f}'i ({matched_kapsam_ici_etken:,} / {total_kapsam_ici_etken:,}), kapsam içi ruhsatlı ürünlerin %{matched_kapsam_ici_urun_pct:.1f}'inin ({matched_kapsam_ici_urun:,} / {total_kapsam_ici_urun:,}) en az bir bileşeni DDInter'da bulunuyor.\",\n",
            "    f\"> *(Tüm Bileşenler Bazında: %{matched_etken_pct:.1f} ({matched_etken:,} / {total_etken:,}) — Tüm Ruhsatlı Ürünler Bazında: %{matched_urun_pct:.1f} ({matched_urun:,} / {total_urun:,}))*\",\n",
            "    \"\",\n",
            "    \"## 1. Yol Bazında Bileşen Sayısı ve DDInter Eşleşme Dağılımı\",\n",
            "    \"| Eşleşme Yolu | Toplam Bileşen | DDInter Eşleşen | Eşleşme Oranı (%) | Açıklama |\",\n",
            "    \"| :--- | :---: | :---: | :---: | :--- |\",\n",
            "]\n",
            "for yol_adi, tot, esl, pct, aciklama in tablo_1_satirlar:\n",
            "    rapor_lines.append(f\"| **{yol_adi}** | {tot:,} | {esl:,} | %{pct:.1f} | {aciklama} |\")\n",
            "rapor_lines.append(f\"| **TOPLAM** | **{total_etken:,}** | **{matched_etken:,}** | **%{matched_etken_pct:.1f}** | TİTCK ruhsatlı listedeki tüm benzersiz bileşenler |\")\n",
            "rapor_lines.append(\"\")\n",
            "rapor_lines.append(f\"> **Not (PubChem Doğrulaması ve Dağılımı):** Adım 4 kapsamında en sık 100 eşleşmeyen kapsam içi bileşenden {pubchem_dogrudan} tanesi PubChem eş anlamlılarıyla doğrudan DDInter kimliğine bağlanmış ve {pubchem_yayilim_cnt} satıra yayılmıştır.{parasetamol_info} Kurtarılan bu bileşikler resmi ATC adı ile DDInter adı farklılaşan Yol A ve Yol B satırlarıdır (bu nedenle Yol A/B altında DDInter kimliği kazanmışlardır). Kural motoruna girmeyip `eslesmedi` yolunda kalan 955 bileşenin en sık olanları (dekstroz, kalsiyum klorur, sodyum laktat, magnezyum klorur, tiyokolsikosid vb.) DDInter kütüphanesinde hiç yer almadığından bu gruptan yeni DDInter eşleşmesi çıkmamış ve tümü Kişi C'nin Yol D taslağına devredilmiştir.\")\n",
            "\n",
            "rapor_lines.extend([\n",
            "    \"\",\n",
            "    \"## 2. DDInter Eşleşme Oranı Özeti\",\n",
            "    \"| Metrik Düzeyi | Toplam Büyüklük | DDInter'da Bulunan | Kapsama Oranı (%) |\",\n",
            "    \"| :--- | :---: | :---: | :--- |\",\n",
            "    f\"| **Kapsam İçi Etken Madde Bazında** | {total_kapsam_ici_etken:,} | {matched_kapsam_ici_etken:,} | %{matched_kapsam_ici_etken_pct:.1f} |\",\n",
            "    f\"| **Kapsam İçi Ruhsatlı Ürün Bazında (En Az 1 Bileşen)** | {total_kapsam_ici_urun:,} | {matched_kapsam_ici_urun:,} | %{matched_kapsam_ici_urun_pct:.1f} |\",\n",
            "    f\"| **Tüm Etken Maddeler Bazında** | {total_etken:,} | {matched_etken:,} | %{matched_etken_pct:.1f} |\",\n",
            "    f\"| **Tüm Ruhsatlı Ürünler Bazında (En Az 1 Bileşen)** | {total_urun:,} | {matched_urun:,} | %{matched_urun_pct:.1f} |\",\n",
            "    \"\",\n",
            "    f\"> **Not (Benzersiz İlaç Kimliği):** DDInter ile eşleşen {matched_etken:,} etken madde kaydı, toplam **{int(df_etken_madde_nihai['ddinter_id'].nunique()):,} benzersiz DDInter kimliğine** (`ddinter_id`) karşılık gelmektedir (örn. `vitamin d3` ve `kolekalsiferol` her ikisi de `DDInter367` kimliğine bağlanmıştır).\",\n",
            "    \"\",\n",
            "    \"## 3. ATC Ana Grubuna Göre DDInter Eşleşme Oranı (14 Satır - Kapsam İçi)\",\n",
            "    \"| ATC Ana Grubu | Grup Açıklaması | Toplam Bileşen | DDInter Eşleşen | Eşleşme Oranı (%) |\",\n",
            "    \"| :---: | :--- | :---: | :--- | :---: |\",\n",
            "])\n",
            "\n",
            "atc_isimleri = {\n",
            "    'A': 'Sindirim Sistemi ve Metabolizma',\n",
            "    'B': 'Kan ve Kan Yapıcı Organlar',\n",
            "    'C': 'Kardiyovasküler Sistem',\n",
            "    'D': 'Dermatolojik İlaçlar',\n",
            "    'G': 'Genito-Üriner Sistem ve Cinsiyet Hormonları',\n",
            "    'H': 'Sistemik Hormonal Preparatlar',\n",
            "    'J': 'Sistemik Antiinfektifler (Antibiyotikler vb.)',\n",
            "    'L': 'Antineoplastik ve İmmünomodülatör Ajanlar',\n",
            "    'M': 'Kas-İskelet Sistemi',\n",
            "    'N': 'Sinir Sistemi',\n",
            "    'P': 'Antiparaziter Ürünler',\n",
            "    'R': 'Solunum Sistemi',\n",
            "    'S': 'Duyu Organları',\n",
            "    'V': 'Çeşitli (Various)',\n",
            "}\n",
            "\n",
            "for g, tot, esl, oran in atc_gruplari:\n",
            "    g_ad = atc_isimleri.get(g, '-')\n",
            "    rapor_lines.append(f\"| **{g}** | {g_ad} | {tot:,} | {esl:,} | %{oran:.1f} |\")\n",
            "\n",
            "atc_disinda_kalan = total_etken - len(valid_atc_em)\n",
            "rapor_lines.append(\"\")\n",
            "rapor_lines.append(f\"> **Not (ATC Dağılımı):** Tablo kapsam içi {len(valid_atc_em):,} etken maddeyi içerir. Kapsam dışı veya ATC atanmamış {atc_disinda_kalan:,} bileşen tablodan hariç tutulmuştur; toplam etken madde {total_etken:,}'dir.\")\n",
            "rapor_lines.append(\"\")\n",
            "n_oran = next((oran for g, _, _, oran in atc_gruplari if g == 'N'), 69.8)\n",
            "rapor_lines.append(f\"> **Önemli Not (Eşleşme Oranı vs. Etkileşim Kapsamı):** Tablodaki yüksek eşleşme oranları (örn. Sinir Sistemi %{n_oran:.1f}), bu ilaçların DDInter kütüphanesinde kimlik olarak geçtiğini gösterir. Ancak DDInter indirme paketlerinde C, G, J, M, N, S gibi ana grupların bağımsız etkileşim dosyaları bulunmamaktadır. Dolayısıyla bu gruptaki ilaçlar yalnızca diğer mevcut gruplarla (A, B, D, H, L, P, R, V) olan etkileşimlerde yer alabilir; iki N grubu ilacının kendi arasındaki etkileşim DDInter dosyalarında bulunamaz.\")\n",
            "\n",
            "rapor_lines.extend([\n",
            "    \"\",\n",
            "    \"## 4. Eşleşmeyen En Sık 30 Bileşen Tablosu (Kişi C Öncelik Listesi - Kapsam İçi)\",\n",
            "    \"| Sıra | Türkçe Bileşen Adı | Ürün Sayısı | Önerilen İngilizce / ATC | Durum |\",\n",
            "    \"| :---: | :--- | :---: | :--- | :--- |\",\n",
            "])\n",
            "\n",
            "for rank, (_, row) in enumerate(eslesmeyen_top30.iterrows(), 1):\n",
            "    b_tr = row['bilesen_tr']\n",
            "    u_cnt = row['urun_sayisi']\n",
            "    atc_val = row['atc'] if pd.notna(row['atc']) else '-'\n",
            "    ad_val = row['ad_en'] if pd.notna(row['ad_en']) else '-'\n",
            "    rapor_lines.append(f\"| {rank} | `{b_tr}` | {u_cnt:,} | {ad_val} ({atc_val}) | Yol D Adayı |\")\n",
            "\n",
            "# Bütünlük Doğrulama Kontrolleri (Assertions - Dosya yazılmadan önce doğrulanır)\n",
            "assert df_etken_madde_nihai['bilesen_tr'].is_unique, 'HATA: bilesen_tr benzersiz değil!'\n",
            "assert df_etken_madde_nihai['yol'].value_counts().sum() == total_etken, f'HATA: Yol toplamı total_etken ({total_etken}) ile uyuşmuyor!'\n",
            "assert (df_etken_madde_nihai['ddinter_id'].notna() == df_etken_madde_nihai['eslesme_kaynagi'].notna()).all(), 'HATA: ddinter_id ile eslesme_kaynagi tutarsız!'\n",
            "assert 'atc_ana' in df_etken_madde_nihai.columns, 'HATA: atc_ana sütunu eksik!'\n",
            "\n",
            "rapor_metni = \"\\n\".join(rapor_lines) + \"\\n\"\n",
            "rapor_yol = kok / 'docs' / 'esleme_raporu.md'\n",
            "rapor_yol.write_text(rapor_metni, encoding='utf-8')\n",
            "\n",
            "print(f\"✓ docs/esleme_raporu.md başarıyla oluşturuldu: {rapor_yol}\")\n",
            "print(\"✓ Tüm bütünlük assertion kontrolleri başarıyla geçti.\")\n",
            "print()\n",
            "print(\"Rapor Başlığı ve Özet Cümle:\")\n",
            "print(rapor_lines[2])\n",
            "print(rapor_lines[3])\n"
        ]
    })

    # Hücre 25: Özet Markdown ve Teknik Değerlendirme
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "---\n",
            "## 15. İP3 Teslimat Özeti, Kritik Bulgular ve Teknik Değerlendirme\n",
            "\n",
            "Bu çalışma kitabı ile İP3 (İngilizce Ad Köprüsü ve DDInter Eşlemesi) adımları uygulanmış ve sayısal hedeflere ulaşılmıştır:\n",
            "- **Kapsam İçi Etken Madde DDInter Eşleşme Oranı:** %46.1 (1,378 / 2,988)\n",
            "- **Kapsam İçi Ruhsatlı Ürün Kapsama Oranı (en az 1 bileşeni DDInter'da olan):** %76.5 (17,180 / 22,470) — *Hedeflenen %70 eşiği aşılmıştır.*\n",
            "- **Tüm Bileşenler Bazında:** %44.3 (1,378 / 3,111)\n",
            "- **Tüm Ruhsatlı Ürünler Bazında:** %76.7 (17,578 / 22,927)\n",
            "\n",
            "### ⚠️ Rapor ve Sonraki İş Paketleri (İP4 / D05 / E09) İçin Kritik Teknik Kısıtlar\n",
            "\n",
            "Sayısal başarı oranlarının arkasında, veri kümesinin doğasından ve upstream adımlardan kaynaklanan ve koşulsuz başarı iddiasını sınırlandıran 5 temel gerçek bulunmaktadır:\n",
            "\n",
            "1. **Eşleşme Oranı $\\neq$ Etkileşim Verisi Kapsamı (DDInter Grup Asimetrisi):**\n",
            "   DDInter indirme paketlerinde yalnızca 8 ana grup (A, B, D, H, L, P, R, V) mevcuttur; Türkiye'de en yaygın reçetelenen **C (Kardiyovasküler), G (Üro-genital), J (Antibiyotikler), M (Kas-İskelet), N (Sinir Sistemi) ve S (Duyu)** gruplarının müstakil etkileşim dosyaları bulunmamaktadır. Dolayısıyla N grubunda %69.8 eşleşme sağlanmış olması, N ilaçlarının etkileşim verisinin tam olduğu anlamına **gelmez**. Bu ilaçlar yalnızca mevcut 8 gruptaki partnerleriyle olan etkileşimlerde yer alabilir; iki N veya iki C ilacının kendi arasındaki etkileşimi DDInter'da tespit edilemez. E09 grafiği ve final raporunda bu kısıt açıkça vurgulanmalıdır.\n",
            "\n",
            "2. **1.378 Eşleşen Kayıt $\\rightarrow$ 852 Benzersiz İlaç (Molekül Büyüklüğü):**\n",
            "   Eşleşen 1.378 bileşen satırı, DDInter kütüphanesinde yalnızca **852 benzersiz ilaç kimliğine** (`ddinter_id`) karşılık gelmektedir. Aradaki 526 satırlık fark; Türkçe yazım varyantlarından (`insulin lispro` formları, aşı adları), tuz/ester ayrımlarından ve ayrıştırma farklılıklarından kaynaklanmaktadır.\n",
            "\n",
            "3. **Yanlış Birleşme Tespiti ve İP2 Kaynağı (Kişi A Geri Bildirimi):**\n",
            "   Tekil kimlik denetimlerinde, `ketokonazol` (antifungal) bileşeninin, TEKNAZOL tabletlerin `urun.csv` dosyasında hatalı olarak `M01AE03` (ketoprofen) kodlanması sebebiyle Yol A'da ketoprofen ATC'sine bağlanarak `DDInter1009` (ketoprofen) kimliğiyle yanlış birleştiği tespit edilmiştir. Bu ve benzeri yazım çeşitlilikleri Kişi A'nın İP2 ayrıştırma ve veri temizliği tarafına iletilmiştir.\n",
            "\n",
            "4. **Yol C'nin Katkısı ve DDInter Kapsam Sınırı:**\n",
            "   Yol C kural motorunun %52.8'lik doğruluğu Yol A çiftleri (eğitim kümesi) üzerinde ölçüldüğü için iyimserdir. Kalan ~1.000 bileşenden yalnızca 78'i DDInter'a bağlanabilmiştir. Buradaki temel darboğaz çeviri kuralı eksikliği değil, DDInter'ın 1.939 bileşiklik genel kapsamıdır. Eşleşmeyenlerin başında gelen `dekstroz`, `kalsiyum klorur`, `sodyum laktat`, `magnezyum klorur`, `tiyokolsikosid` ve `deksketoprofen` gibi bileşikler DDInter veritabanında hiç yer almamaktadır; dolayısıyla ek çeviri kuralları bu sayıyı artırmayacaktır.\n",
            "\n",
            "5. **SKRS Karakter Düzeltmeleri ve Kural 6:**\n",
            "   SKRS adlarındaki noktasız `ı` karakter hataları (`combınatıon` $\\rightarrow$ `combination`) düzeltilmiş, `paracetamol` PubChem yayılımı ile `acetaminophen`'e bağlanmıştır. Ancak `allergen extracts`, `peritoneal dialytics` gibi ATC sınıf adları ile Kural 6 ürünlerinin takibi için Kişi A ve Kişi C ile koordinasyon sürmektedir.\n",
            "\n",
            "**Tamamlanan Altyapı Adımları:**\n",
            "- [x] **SKRS ATC Sözlüğü:** Resmi sözlük aktif+pasif sekmelerinden çıkarıldı.\n",
            "- [x] **DDInter İlaç Tablosu:** `ddinter_ilac.csv` sayısal ID sıralamasıyla oluşturuldu (1.939 bileşik).\n",
            "- [x] **Yol A:** Tek bileşenli, 7 haneli ATC'li bileşenler doğrudan ATC sözlüğünden eşleştirildi (1.922 bileşen, Kişi A).\n",
            "- [x] **Yol B:** Kombine ürünlerde ATC adından ayrıştırılan bileşenler RapidFuzz ile eşleştirildi (66 bileşen, Kişi A).\n",
            "- [x] **SKRS Adımı:** SKRS kaynaklı ürünlerin bileşenleri `ı` temizliğiyle İngilizce olarak işlendi (90 bileşen, Kişi B).\n",
            "- [x] **Yol C:** `config/tr_en_kurallar.csv` 9 ölçülmüş kural motoruyla kalan bileşenler bağlandı (78 bileşen, Kişi B).\n",
            "- [x] **PubChem Kontrolü:** Rate limit, disk cache ve `ad_en_ham` izlenebilirliği ile en sık 100 eşleşmeyenden 16 bileşen kurtarıldı ve 24 satıra yayıldı (Kişi B).\n",
            "- [x] **Yol D Taslağı:** Kişi C için `atc_ipucu`, `urun_ornegi` ve `kapsam_ici` öncelikli `data/interim/ruhsatli_esleme_taslagi.csv` çıkarıldı (Kişi B).\n",
            "- [x] **Nihai Tablo:** `atc_ana` sütunu eklenmiş `data/interim/etken_madde.csv` kaydedildi (3.111 satır, Kişi B).\n",
            "- [x] **Eşleşme Raporu:** 4 zorunlu tablo, bütünlük assertion'ları ve kısıt notlarıyla `docs/esleme_raporu.md` üretildi (Kişi B).\n"
        ]
    })

    return cells


def build_and_run_notebook_03():
    """Kişi A ve Kişi B hücrelerini birleştirir, çalıştırır ve pre-render eder."""
    a_cells = []
    kisi_a_nb_path = NOTEBOOKS_DIR / "03_kopru_ddinter_kisi_a.ipynb"
    existing_nb_path = NOTEBOOKS_DIR / "03_kopru_ddinter.ipynb"

    if kisi_a_nb_path.exists():
        with open(kisi_a_nb_path, "r", encoding="utf-8") as f:
            a_cells = json.load(f)["cells"][:17]
    elif existing_nb_path.exists():
        with open(existing_nb_path, "r", encoding="utf-8") as f:
            a_cells = json.load(f)["cells"][:17]
    else:
        raise FileNotFoundError(f"Notebook dosyası bulunamadı: {existing_nb_path}")

    print(f"Kişi A hücreleri yüklendi: {len(a_cells)} hücre")

    # Başlık hücresini ortak çalışma başlığına dönüştür
    a_cells[0]["source"] = [
        "# 03 — İngilizce Ad Köprüsü ve DDInter Eşlemesi (İP3 - Kişi A & Kişi B)\n",
        "\n",
        "Bu çalışma kitabı, 2. Hafta Görev Dağılımı ve Veri Birleştirme Planı uyarınca iki bölümden oluşmaktadır:\n",
        "- **Bölüm 1 (Hücre 0 – 16 — Kişi A):** SKRS ATC Sözlüğü, DDInter İlaç Kataloğu (`ddinter_ilac.csv`), Yol A (Tek bileşenli ürünler) ve Yol B (Kombine ürünler).\n",
        "- **Bölüm 2 (Hücre 17 – 25 — Kişi B):** SKRS Adımı (Kural 5/6), Yol C (Kural tabanlı çeviri), DDInter eşleme (`ddinter_id`), PubChem kontrolü, Kişi C için `ruhsatli_esleme_taslagi.csv`, nihai `etken_madde.csv` ve 4 zorunlu tablodan oluşan `docs/esleme_raporu.md`.\n"
    ]

    # Kişi B hücreleri
    b_cells = create_kisi_b_cells()
    print(f"Kişi B hücreleri oluşturuldu: {len(b_cells)} hücre")

    # Birleşik hücre listesi
    all_cells = a_cells + b_cells
    print(f"Toplam birleşik hücre sayısı: {len(all_cells)}")

    # Çalıştırma ortamı
    global_env = {"__name__": "__main__"}
    sys.path.insert(0, str(BASE_DIR))

    for idx, cell in enumerate(all_cells):
        if cell["cell_type"] == "code":
            code = "".join(cell["source"])
            print(f"Hücre {idx:02d} çalıştırılıyor...")
            buf_out = io.StringIO()
            buf_err = io.StringIO()
            try:
                with redirect_stdout(buf_out), redirect_stderr(buf_err):
                    exec(code, global_env)
                stdout_val = buf_out.getvalue()
                stderr_val = buf_err.getvalue()

                outputs = []
                if stdout_val:
                    outputs.append({
                        "name": "stdout",
                        "output_type": "stream",
                        "text": stdout_val.splitlines(keepends=True),
                    })
                if stderr_val:
                    outputs.append({
                        "name": "stderr",
                        "output_type": "stream",
                        "text": stderr_val.splitlines(keepends=True),
                    })
                cell["outputs"] = outputs
                cell["execution_count"] = idx
            except Exception as e:
                print(f"HATA! Hücre {idx} çalıştırılırken hata oluştu: {e}")
                raise e

    # Birleşik notebook dosyasını kaydet
    out_nb = {
        "cells": all_cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3 (.venv)",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": sys.version.split()[0]
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

    final_nb_path = NOTEBOOKS_DIR / "03_kopru_ddinter.ipynb"
    with open(final_nb_path, "w", encoding="utf-8") as f:
        json.dump(out_nb, f, indent=1, ensure_ascii=False)

    print(f"🎉 03_kopru_ddinter.ipynb başarıyla üretildi ve güncellendi: {final_nb_path}")


if __name__ == "__main__":
    build_and_run_notebook_03()
