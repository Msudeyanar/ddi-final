"""
Production-Grade Notebook 03 Üretici ve Çıktı Oluşturucu

Tüm kıdemli veri mühendisi eleştirilerini çözer:
1. PubChem Cache Poisoning Koruması: Sadece HTTP 200 ve 404 cache'lenir; ağ hatalarında ASLA boş liste diske yazılmaz.
2. 3 denemeli Exponential Backoff Retry mekanizması.
3. Yol C Kural Motorunda Regex Sıralama Bağımlılığı Çözümü (suffix_specificity: uzundan kısaya / spesifikten genele).
4. Bellek (RAM) Optimizasyonu: 444 bin satırlık ara DataFrame listeleri kaldırıldı, akışkan tekil sözlük kullanıldı.
5. Savunmacı Merge (Defensive Join): urun_etken.csv ve etken_madde.csv birleştirilirken
   bilesen_tr anahtar sütunları zorla .astype(str).str.strip().str.lower() ile temizlenir;
   böylece boşluk ve büyük/küçük harf uyumsuzluğundan kaynaklı sessiz eşleşmeme (NaN) ve
   ürün eşleşme oranının (%Y) hatalı düşük çıkma riski sıfırlanır.
6. Çalıştırılmış hücre çıktıları doğrudan .ipynb dosyasına gömülü üretilir.
"""

import sys
import io
import re
import ast
import json
import uuid
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
NOTEBOOKS_DIR = BASE_DIR / "notebooks"


def gen_id():
    return uuid.uuid4().hex[:8]


def run_code_cell(code_str: str, global_env: dict, exec_count: int):
    outputs = []
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    captured_stdout = io.StringIO()
    sys.stdout = captured_stdout
    sys.stderr = captured_stdout

    last_val = None
    try:
        tree = ast.parse(code_str)
        if tree.body and isinstance(tree.body[-1], ast.Expr):
            last_expr = tree.body.pop()
            if tree.body:
                exec(compile(tree, filename="<cell>", mode="exec"), global_env)
            last_val = eval(compile(ast.Expression(last_expr.value), filename="<cell>", mode="eval"), global_env)
        else:
            exec(compile(tree, filename="<cell>", mode="exec"), global_env)
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

    stdout_text = captured_stdout.getvalue()
    if stdout_text:
        outputs.append({
            "name": "stdout",
            "output_type": "stream",
            "text": [line + "\n" for line in stdout_text.splitlines()]
        })

    if last_val is not None:
        data_dict = {}
        if hasattr(last_val, "to_html"):
            data_dict["text/html"] = [last_val.to_html()]
            data_dict["text/plain"] = [repr(last_val)]
        else:
            data_dict["text/plain"] = [repr(last_val)]
        outputs.append({
            "data": data_dict,
            "execution_count": exec_count,
            "metadata": {},
            "output_type": "execute_result"
        })

    return outputs


def generate():
    cells = []
    global_env = {"__file__": str(NOTEBOOKS_DIR / "03_kopru_ddinter.ipynb"), "__name__": "__main__"}
    exec_counter = 1

    def add_md(source_lines):
        cells.append({
            "cell_type": "markdown",
            "id": gen_id(),
            "metadata": {},
            "source": source_lines
        })

    def add_code(source_lines):
        nonlocal exec_counter
        code_str = "".join(source_lines)
        outs = run_code_cell(code_str, global_env, exec_counter)
        cells.append({
            "cell_type": "code",
            "execution_count": exec_counter,
            "id": gen_id(),
            "metadata": {},
            "outputs": outs,
            "source": source_lines
        })
        exec_counter += 1

    # 1. Başlık
    add_md([
        "# 03_kopru_ddinter: DDInter İlaç Eşleme Köprüsü (Kişi B)\n",
        "\n",
        "**İş Paketi:** İP3 (Gün 2–4, Bağımsız başlar; Gün 5–6'da A ve C kişileriyle birleşir)\n",
        "\n",
        "| Adım | Açıklama | Gün | Bağımlılık | Durum |\n",
        "|------|----------|-----|------------|-------|\n",
        "| A1 – `ddinter_ilac.csv` | 8 DDInter dosyasından tekil ilaç listesi (1.939 satır) | 2–3 | Bağımsız | Tamamlandı |\n",
        "| A2 – Kural dosyası | `config/tr_en_kurallar.csv` (isin$→icin, in$→ine, f→ph) | 2–3 | Bağımsız | Tamamlandı |\n",
        "| A3 – PubChem eş anlamlı fonksiyonu | Rate Limiter (5 req/s) + Cache (Poisoning korumalı) + Exponential Backoff | 2–4 | Bağımsız | Tamamlandı |\n",
        "| A4 – Yol C'yi kalanlara uygula | A kişisinin çıktısına Yol C + PubChem uygulama | 5–6 | A kişisi (`etken_madde.csv`) | Hazır (Bekliyor) |\n",
        "| A5 – `ruhsatli_esleme_taslagi.csv` | C kişisine Yol D için taslak teslim | 5–6 | A kişisi | Hazır (Bekliyor) |\n",
        "| A6 – `docs/esleme_raporu.md` | Nihai eşleme raporu (4 zorunlu tablo) | 6 | A + C kişileri | Hazır (Bekliyor) |"
    ])

    # 2. Kurulum ve Ortam
    add_code([
        "# ─── Kurulum ve import'lar ────────────────────────────────────────\n",
        "import os\n",
        "import re\n",
        "import json\n",
        "import time\n",
        "import hashlib\n",
        "import urllib.parse\n",
        "from pathlib import Path\n",
        "import pandas as pd\n",
        "import numpy as np\n",
        "import requests\n",
        "\n",
        "# Proje kök dizini (hem proje kökünden hem notebooks/ içinden çalışmaya uyumlu)\n",
        "cwd = Path().resolve()\n",
        "ROOT = cwd.parent if cwd.name == 'notebooks' else cwd\n",
        "RAW     = ROOT / 'data' / 'raw'\n",
        "INTERIM = ROOT / 'data' / 'interim'\n",
        "CACHE   = ROOT / 'data' / 'cache' / 'pubchem'\n",
        "CONFIG  = ROOT / 'config'\n",
        "DOCS    = ROOT / 'docs'\n",
        "\n",
        "# Dizinleri oluştur\n",
        "for d in [INTERIM, CACHE, CONFIG, DOCS]:\n",
        "    d.mkdir(parents=True, exist_ok=True)\n",
        "\n",
        "print(f'Kök dizin : {ROOT}')\n",
        "print(f'Ham veri  : {RAW}')\n",
        "print(f'Ara çıktı : {INTERIM}')\n",
        "print(f'Cache     : {CACHE}')"
    ])

    # 3. Yardımcı Fonksiyonlar Markdown
    add_md([
        "---\n",
        "## Yardımcı Fonksiyonlar\n",
        "\n",
        "Tüm adımlarda kullanılacak ortak fonksiyonlar:\n",
        "1. **`ddinter_num`**: Sayısal ID sıralaması (`DDInter1263` -> 1263).\n",
        "2. **`normalize_drug_name`** (`ad_normalize`): Küçük harf, boşluk ve tire temizliği."
    ])

    # 4. Yardımcı Fonksiyonlar Kod
    add_code([
        "def ddinter_num(ddinter_id: str) -> int:\n",
        "    \"\"\"\n",
        "    DDInterID'nin sayısal kısmını döndürür.\n",
        "    'DDInter1263' → 1263\n",
        "    Metin sıralaması 'DDInter10' < 'DDInter2' hatasını önlemek için int kullanılır.\n",
        "    \"\"\"\n",
        "    if not isinstance(ddinter_id, str):\n",
        "        return 0\n",
        "    m = re.search(r'(\\d+)$', ddinter_id.strip())\n",
        "    return int(m.group(1)) if m else 0\n",
        "\n",
        "\n",
        "def normalize_drug_name(name: str) -> str:\n",
        "    \"\"\"\n",
        "    İlaç adı normalizasyonu (PDF Adım 4'teki kurala uygun):\n",
        "    - Küçük harf\n",
        "    - Baştaki/sondaki boşlukları sil\n",
        "    - Farklı tire/alt tire karakterlerini tek boşluğa çevir\n",
        "    - Birden fazla boşluğu teke indir\n",
        "    \"\"\"\n",
        "    if not isinstance(name, str):\n",
        "        return ''\n",
        "    name = name.replace('İ', 'i').replace('I', 'ı').strip().lower().replace('\\u0307', '')\n",
        "    name = re.sub(r'[\\-_—–\\u2010\\u2011\\u2012\\u2013\\u2014]+', ' ', name)\n",
        "    name = re.sub(r'\\s+', ' ', name).strip()\n",
        "    return name\n",
        "\n",
        "ad_normalize = normalize_drug_name\n",
        "\n",
        "# Hızlı testler\n",
        "assert ddinter_num('DDInter1263') == 1263\n",
        "assert ddinter_num('DDInter58') == 58\n",
        "assert ddinter_num('DDInter1') < ddinter_num('DDInter582') < ddinter_num('DDInter1263')\n",
        "assert normalize_drug_name('  Aluminum  Hydroxide ') == 'aluminum hydroxide'\n",
        "assert normalize_drug_name('Dexketoprofen') == 'dexketoprofen'\n",
        "assert normalize_drug_name(' İBUPROFEN ') == 'ibuprofen'\n",
        "print('✅ Yardımcı fonksiyon testleri başarıyla geçti.')"
    ])

    # 5. Adım A1 Markdown
    add_md([
        "---\n",
        "# Adım A1 — `ddinter_ilac.csv` Çıkar (Bellek Dostu ve Savunmacı Okuma)\n",
        "\n",
        "8 DDInter CSV dosyasındaki tüm ilaç adlarını toplayıp tekilleştirir.\n",
        "- **Bellek Optimizasyonu (RAM-Friendly):** Yüzbinlerce kopyayı bellekte tutan devasa listeler yerine `safe_read_csv` ile akışkan ve tekil sözlük yaklaşımı kullanılır.\n",
        "- Hedef: Tam **1.939 benzersiz ilaç**."
    ])

    # 6. Adım A1 Kod
    add_code([
        "# ─── 8 CSV dosyasını bul ve oku ──────────────────────────────────\n",
        "def safe_read_csv(fpath: Path, required_cols: list[str]) -> pd.DataFrame:\n",
        "    \"\"\"Savunmacı okuyucu: Farklı encoding'leri dener ve zorunlu sütunları denetler.\"\"\"\n",
        "    for enc in ['utf-8', 'utf-8-sig', 'latin1']:\n",
        "        try:\n",
        "            df = pd.read_csv(fpath, encoding=enc)\n",
        "            if set(required_cols).issubset(df.columns):\n",
        "                return df\n",
        "        except Exception:\n",
        "            continue\n",
        "    raise ValueError(f'Bozuk veya eksik sütunlu dosya: {fpath.name}')\n",
        "\n",
        "csv_files = sorted(RAW.glob('ddinter_downloads_code_*.csv'))\n",
        "print(f'{len(csv_files)} DDInter dosyası bulundu:\\n')\n",
        "\n",
        "# Bellek dostu tekilleştirme: RAM'i 444 bin satırla şişirmeden tekil sözlükte topla\n",
        "unique_drugs = {}  # ddinter_id -> drug_name\n",
        "required_cols = ['DDInterID_A', 'Drug_A', 'DDInterID_B', 'Drug_B']\n",
        "\n",
        "toplam_ham_satir = 0\n",
        "for fpath in csv_files:\n",
        "    df_tmp = safe_read_csv(fpath, required_cols)\n",
        "    satir = len(df_tmp)\n",
        "    toplam_ham_satir += satir\n",
        "    clean_a = df_tmp[['DDInterID_A', 'Drug_A']].dropna()\n",
        "    clean_b = df_tmp[['DDInterID_B', 'Drug_B']].dropna()\n",
        "    unique_drugs.update(dict(zip(clean_a['DDInterID_A'], clean_a['Drug_A'])))\n",
        "    unique_drugs.update(dict(zip(clean_b['DDInterID_B'], clean_b['Drug_B'])))\n",
        "    print(f'  {fpath.name:30s}: {satir:>6,} satır')\n",
        "\n",
        "print(f'\\nToplam okunan satır: {toplam_ham_satir:,}')\n",
        "print(f'Bellekte çıkarılan tekil ilaç sayısı: {len(unique_drugs):,}')"
    ])

    # 7. Adım A1 Dedup Kod
    add_code([
        "# ─── İlaç tablosu oluştur ve normalize et ────────────────────────\n",
        "df_ilac = pd.DataFrame([\n",
        "    {'ddinter_id': k, 'drug_name': v}\n",
        "    for k, v in unique_drugs.items()\n",
        "])\n",
        "\n",
        "# Ad normalizasyonu (hem ad_norm hem drug_norm)\n",
        "norm_col = df_ilac['drug_name'].apply(normalize_drug_name)\n",
        "df_ilac['ad_norm'] = norm_col\n",
        "df_ilac['drug_norm'] = norm_col\n",
        "\n",
        "# Sayısal sıralama (DDInter1 < DDInter582 < DDInter1263)\n",
        "df_ilac['_id_num'] = df_ilac['ddinter_id'].apply(ddinter_num)\n",
        "df_ilac = df_ilac.sort_values('_id_num').reset_index(drop=True)\n",
        "df_ilac = df_ilac.drop(columns=['_id_num'])\n",
        "\n",
        "print(f'Benzersiz ilaç sayısı: {len(df_ilac):,}')\n",
        "print(f'\\nİlk 5 ilaç:')\n",
        "df_ilac.head(5)"
    ])

    # 8. Adım A1 Kaydet Kod
    add_code([
        "# ─── Kaydet ──────────────────────────────────────────────────────\n",
        "out_ilac = INTERIM / 'ddinter_ilac.csv'\n",
        "df_ilac.to_csv(out_ilac, index=False, encoding='utf-8')\n",
        "\n",
        "print(f'✅ Kaydedildi: {out_ilac}')\n",
        "print(f'   Satır sayısı : {len(df_ilac):,}')\n",
        "print(f'   Sütunlar     : {df_ilac.columns.tolist()}')"
    ])

    # 9. Adım A1 Doğrulama Kod
    add_code([
        "# ─── Doğrulama kontrolleri ───────────────────────────────────────\n",
        "assert df_ilac['ddinter_id'].isna().sum() == 0, 'Boş ddinter_id var!'\n",
        "assert df_ilac['drug_name'].isna().sum() == 0, 'Boş drug_name var!'\n",
        "assert df_ilac['ddinter_id'].is_unique, 'Tekrarlı ddinter_id var!'\n",
        "nums = df_ilac['ddinter_id'].apply(ddinter_num).tolist()\n",
        "assert nums == sorted(nums), 'Sayısal sıralama bozuk!'\n",
        "assert (df_ilac['drug_norm'] == '').sum() == 0, 'Boş drug_norm var!'\n",
        "assert len(df_ilac) == 1939, f'Beklenen 1.939, bulunan: {len(df_ilac)}'\n",
        "\n",
        "print('✅ Tüm doğrulama kontrolleri geçti.')\n",
        "print(f'   1.939 beklenen → Gerçek: {len(df_ilac):,} benzersiz ilaç')"
    ])

    # 10. Adım A2 Markdown
    add_md([
        "---\n",
        "# Adım A2 — `config/tr_en_kurallar.csv` Oluştur ve Yol C Kural Motoru\n",
        "\n",
        "Türkçe bileşen adlarını İngilizce ilaç adlarına dönüştürmek için kural tablosu oluşturulur.\n",
        "- **Regex Sıralama Bağımlılığı Çözümü (`suffix_specificity`):** Sonek kuralları, regex sözdizimi yerine eşleşen gerçek sonek harf uzunluğuna (`isin$` -> 4 harf, `in$` -> 2 harf) göre **uzundan kısaya (spesifikten genele)** sıralanır. Böylece genel kuralların spesifik kuralları ezmesi kesin olarak önlenir."
    ])

    # 11. Adım A2 Kural Dosyası Kod
    add_code([
        "# ─── Kural dosyasını oluştur ─────────────────────────────────────\n",
        "kurallar = [\n",
        "    {'kural_tipi': 'suffix_replace', 'eski': 'isin$',  'yeni': 'icin',  'ornek': 'gentamisin → gentamicin'},\n",
        "    {'kural_tipi': 'suffix_replace', 'eski': '(?<!c)in$',    'yeni': 'ine',   'ornek': 'amlodipin → amlodipine'},\n",
        "    {'kural_tipi': 'char_replace',   'eski': 'f',      'yeni': 'ph',    'ornek': 'morfin → morphine'},\n",
        "]\n",
        "\n",
        "df_kurallar = pd.DataFrame(kurallar)\n",
        "kural_path = CONFIG / 'tr_en_kurallar.csv'\n",
        "df_kurallar.to_csv(kural_path, index=False, encoding='utf-8')\n",
        "\n",
        "print(f'✅ Kaydedildi: {kural_path}')\n",
        "df_kurallar"
    ])

    # 12. Adım A2 Kural Motoru Kod
    add_code([
        "# ─── Yol C kural motoru (Öncelik ve Sıralama Garantili) ──────────\n",
        "def suffix_specificity(eski: str) -> int:\n",
        "    \"\"\"Regex içindeki gerçek harf sonek uzunluğunu çıkarır (isin$ -> 4, in$ -> 2).\"\"\"\n",
        "    m = re.search(r'([a-zA-ZçğıöşüÇĞİÖŞÜ]+)[$]', str(eski))\n",
        "    return len(m.group(1)) if m else len(str(eski))\n",
        "\n",
        "\n",
        "def kural_uygula(bilesen_tr: str, kurallar_df: pd.DataFrame) -> str:\n",
        "    \"\"\"\n",
        "    Türkçe bileşen adına kuralları deterministik sırayla uygular.\n",
        "    1. Sonek kuralları spesifiklik derecesine göre azalan (uzundan kısaya) sıralanır.\n",
        "       'isin$' her zaman 'in$' gibi genel kurallardan önce çalışır.\n",
        "    2. Bir sonek kuralı eşleştiğinde ek sonek uygulanmaz.\n",
        "    3. Karakter kuralları güvenle uygulanır.\n",
        "    \"\"\"\n",
        "    if not isinstance(bilesen_tr, str) or not bilesen_tr.strip():\n",
        "        return \"\"\n",
        "    aday = bilesen_tr.lower().strip()\n",
        "    \n",
        "    df_rules = kurallar_df.dropna(subset=[\"kural_tipi\", \"eski\", \"yeni\"]).copy()\n",
        "    suffix_rules = df_rules[df_rules[\"kural_tipi\"] == \"suffix_replace\"].copy()\n",
        "    suffix_rules[\"_spec\"] = suffix_rules[\"eski\"].apply(suffix_specificity)\n",
        "    suffix_rules = suffix_rules.sort_values(\"_spec\", ascending=False)\n",
        "    \n",
        "    char_rules = df_rules[df_rules[\"kural_tipi\"] == \"char_replace\"]\n",
        "    \n",
        "    suffix_applied = False\n",
        "    for _, kural in suffix_rules.iterrows():\n",
        "        eski = str(kural[\"eski\"])\n",
        "        yeni = str(kural[\"yeni\"])\n",
        "        if not suffix_applied and re.search(eski, aday):\n",
        "            aday = re.sub(eski, yeni, aday)\n",
        "            suffix_applied = True\n",
        "            break\n",
        "            \n",
        "    for _, kural in char_rules.iterrows():\n",
        "        eski = str(kural[\"eski\"])\n",
        "        yeni = str(kural[\"yeni\"])\n",
        "        aday = aday.replace(eski, yeni)\n",
        "        \n",
        "    return aday\n",
        "\n",
        "\n",
        "def yol_c_esle(bilesen_tr: str, ddinter_norm_set: set, kurallar_df: pd.DataFrame) -> str | None:\n",
        "    \"\"\"\n",
        "    Yol C Mantığı (PDF Adım 3):\n",
        "    Türkçe ada kuralları uygula, DDInter listesinde ara.\n",
        "    Bulunursa normalize edilmiş adı döndürür, bulunmazsa None (→ Yol D'ye düşer).\n",
        "    \"\"\"\n",
        "    aday = kural_uygula(bilesen_tr, kurallar_df)\n",
        "    norm = normalize_drug_name(aday)\n",
        "    if norm in ddinter_norm_set:\n",
        "        return norm\n",
        "    return None\n",
        "\n",
        "# Savunmacı ilac yükleme (bağımsız çalışma desteği)\n",
        "if 'df_ilac' not in globals():\n",
        "    df_ilac = pd.read_csv(INTERIM / 'ddinter_ilac.csv')\n",
        "if 'df_kurallar' not in globals():\n",
        "    df_kurallar = pd.read_csv(CONFIG / 'tr_en_kurallar.csv')\n",
        "\n",
        "col = 'drug_norm' if 'drug_norm' in df_ilac.columns else 'ad_norm'\n",
        "ddinter_norm_set = set(df_ilac[col].dropna().tolist())\n",
        "\n",
        "test_cases = [\n",
        "    (\"amlodipin\",       \"amlodipine\",       \"Yol C ile DDInter'da bulunur\"),\n",
        "    (\"gentamisin\",      \"gentamicin\",       \"Yol C ile DDInter'da bulunur\"),\n",
        "    (\"morfin\",          \"morphine\",         \"Yol C ile DDInter'da bulunur\"),\n",
        "    (\"deksketoprofen\",  \"deksketoprophen\",  \"DDInter'da yok → Yol D'ye düşer\"),\n",
        "    (\"parasetamol\",     \"parasetamol\",      \"DDInter'da yok → Yol D / PubChem'e düşer\"),\n",
        "]\n",
        "\n",
        "print(\"Yol C kural testleri:\")\n",
        "print(\"─\" * 75)\n",
        "for tr_ad, beklenen, aciklama in test_cases:\n",
        "    sonuc = kural_uygula(tr_ad, df_kurallar)\n",
        "    eslesti = yol_c_esle(tr_ad, ddinter_norm_set, df_kurallar)\n",
        "    durum = f\"✅ DDInter: {eslesti}\" if eslesti else \"❌ DDInter'da yok → Yol D'ye Düşer\"\n",
        "    print(f\"  {tr_ad:16s} → {sonuc:18s} │ {durum:32s}\")"
    ])

    # 13. Adım A3 Markdown
    add_md([
        "---\n",
        "# Adım A3 — PubChem Eş Anlamlı Fonksiyonu (Production-Grade & Güvenli Mimari)\n",
        "\n",
        "**API:** `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{AD}/synonyms/JSON`\n",
        "\n",
        "### Güvenlik ve Dayanıklılık Standartları:\n",
        "1. **Cache Poisoning Koruması:** Geçici sunucu/ağ hatalarında (5xx, timeout, kopma) ASLA boş liste diske yazılmaz. Sadece kesin 200 veya 404 durumları cache'lenir.\n",
        "2. **Exponential Backoff Retry:** PubChem 429 veya 5xx döndüğünde 3 denemeye kadar artan aralıklarla yeniden dener.\n",
        "3. **Rate Limiting:** PubChem sınırlarına uyarak saniyede en fazla 5 istek (en az 0.20 sn aralık) gönderilir.\n",
        "4. **Bozuk Cache Dosyası Kurtarma:** Boş (0 bayt) veya hatalı JSON cache dosyaları otomatik ayıklanır."
    ])

    # 14. Adım A3 Kod
    add_code([
        "LAST_PUBCHEM_REQUEST_TIME = 0.0\n",
        "\n",
        "def pubchem_synonyms(drug_name: str, cache_dir: Path = CACHE, max_retries: int = 3) -> list[str]:\n",
        "    \"\"\"\n",
        "    PubChem'den ilacın eş anlamlı adlarını güvenle çeker.\n",
        "    - Rate limiter: Saniyede maks 5 istek (>= 0.20s).\n",
        "    - Retry & Backoff: 429 veya 5xx yanıtlarında 3 denemeye kadar bekler.\n",
        "    - Cache Poisoning Koruması: Sadece 200 (bulundu) veya 404 (kesin yok) cache'lenir. Ağ hatasında boş liste diske YAZILMAZ.\n",
        "    \"\"\"\n",
        "    global LAST_PUBCHEM_REQUEST_TIME\n",
        "    if not drug_name or not str(drug_name).strip():\n",
        "        return []\n",
        "        \n",
        "    ad = drug_name.strip().lower()\n",
        "    cache_key  = hashlib.md5(ad.encode(\"utf-8\")).hexdigest()\n",
        "    cache_file = cache_dir / f\"{cache_key}.json\"\n",
        "    \n",
        "    # 1. Cache kontrolü (Bozuk veya sıfır baytlık dosya korumalı)\n",
        "    if cache_file.exists():\n",
        "        try:\n",
        "            if cache_file.stat().st_size > 0:\n",
        "                return json.loads(cache_file.read_text(encoding=\"utf-8\"))\n",
        "        except Exception:\n",
        "            try:\n",
        "                cache_file.unlink()\n",
        "            except Exception:\n",
        "                pass\n",
        "    \n",
        "    # 2. Güvenli URL encode\n",
        "    encoded_name = urllib.parse.quote(ad)\n",
        "    url = f\"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{encoded_name}/synonyms/JSON\"\n",
        "    \n",
        "    synonyms = []\n",
        "    should_cache = False\n",
        "    \n",
        "    for attempt in range(1, max_retries + 1):\n",
        "        elapsed = time.time() - LAST_PUBCHEM_REQUEST_TIME\n",
        "        if elapsed < 0.20:\n",
        "            time.sleep(0.20 - elapsed)\n",
        "        LAST_PUBCHEM_REQUEST_TIME = time.time()\n",
        "        \n",
        "        try:\n",
        "            resp = requests.get(url, timeout=12)\n",
        "            if resp.status_code == 200:\n",
        "                data = resp.json()\n",
        "                info_list = data.get(\"InformationList\", {}).get(\"Information\", [])\n",
        "                if info_list:\n",
        "                    synonyms = info_list[0].get(\"Synonym\", [])\n",
        "                should_cache = True\n",
        "                break\n",
        "            elif resp.status_code == 404:\n",
        "                synonyms = []\n",
        "                should_cache = True\n",
        "                break\n",
        "            elif resp.status_code in (429, 500, 502, 503, 504):\n",
        "                if attempt < max_retries:\n",
        "                    time.sleep(attempt * 1.0)\n",
        "                    continue\n",
        "                else:\n",
        "                    print(f\"  ⚠️ PubChem sunucu hatası (HTTP {resp.status_code}) [{drug_name}], denemeler tükendi.\")\n",
        "                    return []\n",
        "            else:\n",
        "                return []\n",
        "        except Exception as e:\n",
        "            if attempt < max_retries:\n",
        "                time.sleep(attempt * 1.0)\n",
        "                continue\n",
        "            else:\n",
        "                print(f\"  ⚠️ PubChem ağ/bağlantı hatası ({drug_name}): {e}\")\n",
        "                return []\n",
        "    \n",
        "    # 3. Yalnızca geçerli sonuçları cache'e yaz\n",
        "    if should_cache:\n",
        "        try:\n",
        "            cache_file.write_text(json.dumps(synonyms, ensure_ascii=False), encoding=\"utf-8\")\n",
        "        except Exception as e:\n",
        "            print(f\"  ⚠️ Cache yazma hatası ({drug_name}): {e}\")\n",
        "            \n",
        "    return synonyms\n",
        "\n",
        "\n",
        "def pubchem_ddinter_esle(drug_name: str, ddinter_norm_set: set) -> str | None:\n",
        "    \"\"\"\n",
        "    PubChem eş anlamlılarını DDInter ilaç listesinde arar.\n",
        "    Bulunursa eşleşen normalize adı döndürür, bulunmazsa None.\n",
        "    \"\"\"\n",
        "    synonyms = pubchem_synonyms(drug_name)\n",
        "    for syn in synonyms:\n",
        "        norm = normalize_drug_name(syn)\n",
        "        if norm in ddinter_norm_set:\n",
        "            return norm\n",
        "    return None\n",
        "\n",
        "print(\"✅ PubChem fonksiyonları (Rate Limiter, Retry & Cache Poisoning Koruması) tanımlandı.\")\n",
        "print(f\"   Cache dizini: {CACHE}\")\n",
        "print(f\"   Mevcut cache dosyası: {len(list(CACHE.glob('*.json')))} adet\")"
    ])

    # 15. Adım A3 Test Kod
    add_code([
        "# ─── PubChem fonksiyon testi (3 örnek ilaç) ─────────────────────\n",
        "if 'df_ilac' not in globals():\n",
        "    df_ilac = pd.read_csv(INTERIM / 'ddinter_ilac.csv')\n",
        "if 'ddinter_norm_set' not in globals():\n",
        "    col = 'drug_norm' if 'drug_norm' in df_ilac.columns else 'ad_norm'\n",
        "    ddinter_norm_set = set(df_ilac[col].dropna().tolist())\n",
        "\n",
        "test_drugs = ['paracetamol', 'dexketoprofen', 'warfarin']\n",
        "\n",
        "print('PubChem eş anlamlı testleri:')\n",
        "print('=' * 70)\n",
        "for drug in test_drugs:\n",
        "    syns = pubchem_synonyms(drug)\n",
        "    eslesen = pubchem_ddinter_esle(drug, ddinter_norm_set)\n",
        "    print(f'\\n{drug}:')\n",
        "    print(f'  Eş anlamlı sayısı: {len(syns)}')\n",
        "    if syns:\n",
        "        print(f'  İlk 5 eş anlamlı: {syns[:5]}')\n",
        "    if eslesen:\n",
        "        ddinter_match = df_ilac[df_ilac['drug_norm'] == eslesen]\n",
        "        if len(ddinter_match) > 0:\n",
        "            ddid = ddinter_match.iloc[0]['ddinter_id']\n",
        "            print(f'  ✅ DDInter eşleşmesi: {eslesen} ({ddid})')\n",
        "    else:\n",
        "        print(f'  ❌ DDInter\\'da bulunamadı')"
    ])

    # 16. Adım A4 Markdown
    add_md([
        "---\n",
        "# Adım A4 — Yol C'yi Kalanlara Uygula\n",
        "\n",
        "⚠️ **Bu hücre A kişisinin çıktısına (`data/interim/etken_madde.csv`) bağımlıdır.**\n",
        "Dosya mevcut değilse kontrollü olarak bekler, mevcut olduğunda Yol C ve PubChem eşlemesini gerçekleştirir."
    ])

    # 17. Adım A4 Kontrol Kod
    add_code([
        "# ─── A kişisinin çıktısını kontrol et ────────────────────────────\n",
        "etken_madde_path = INTERIM / 'etken_madde.csv'\n",
        "\n",
        "if not etken_madde_path.exists():\n",
        "    print('⏳ etken_madde.csv henüz hazır değil.')\n",
        "    print('   A kişisinin Yol A/B çıktısı bekleniyor.')\n",
        "    print('   Bu hücreyi A kişisi teslim ettikten sonra yeniden çalıştırın.')\n",
        "else:\n",
        "    df_etken = pd.read_csv(etken_madde_path)\n",
        "    print(f'✅ etken_madde.csv yüklendi: {len(df_etken):,} etken madde')\n",
        "    print(f'   Sütunlar: {df_etken.columns.tolist()}')\n",
        "    if 'yol' in df_etken.columns:\n",
        "        print('\\nYol dağılımı:')\n",
        "        print(df_etken['yol'].value_counts().to_string())\n",
        "        eslesmemis = df_etken[df_etken['yol'].isna() | (df_etken['yol'] == '')]\n",
        "        print(f'\\nEşleşmemiş (Yol C/D adayı): {len(eslesmemis):,} bileşen')\n",
        "    else:\n",
        "        print('⚠️ \"yol\" sütunu yok — A kişisinden kontrol edin.')"
    ])

    # 18. Adım A4 Çalıştır Kod
    add_code([
        "# ─── Yol C uygulama (etken_madde.csv hazır olunca) ──────────────\n",
        "if etken_madde_path.exists():\n",
        "    df_etken = pd.read_csv(etken_madde_path)\n",
        "    bilesen_col = 'bilesen_tr' if 'bilesen_tr' in df_etken.columns else 'etken_madde'\n",
        "    yol_col = 'yol'\n",
        "    \n",
        "    if bilesen_col not in df_etken.columns:\n",
        "        print(f'⚠️ \"{bilesen_col}\" sütunu bulunamadı. Sütunlar: {df_etken.columns.tolist()}')\n",
        "    else:\n",
        "        if 'df_ilac' not in globals():\n",
        "            df_ilac = pd.read_csv(INTERIM / 'ddinter_ilac.csv')\n",
        "        if 'df_kurallar' not in globals():\n",
        "            df_kurallar = pd.read_csv(CONFIG / 'tr_en_kurallar.csv')\n",
        "            \n",
        "        col = 'drug_norm' if 'drug_norm' in df_ilac.columns else 'ad_norm'\n",
        "        ddinter_norm_set = set(df_ilac[col].dropna().tolist())\n",
        "        ddinter_norm_to_id = dict(zip(df_ilac[col], df_ilac['ddinter_id']))\n",
        "        \n",
        "        # Yol C adayları: yol sütunu boş olanlar\n",
        "        mask_c = df_etken[yol_col].isna() | (df_etken[yol_col] == '')\n",
        "        adaylar = df_etken[mask_c].copy()\n",
        "        print(f'Yol C adayı: {len(adaylar):,} bileşen')\n",
        "        \n",
        "        # 1) Kural motoru ile dene\n",
        "        c_eslesti = 0\n",
        "        for idx, row in adaylar.iterrows():\n",
        "            tr_ad = str(row[bilesen_col])\n",
        "            sonuc = yol_c_esle(tr_ad, ddinter_norm_set, df_kurallar)\n",
        "            if sonuc:\n",
        "                df_etken.at[idx, yol_col] = 'C'\n",
        "                df_etken.at[idx, 'ad_en'] = sonuc\n",
        "                df_etken.at[idx, 'ddinter_id'] = ddinter_norm_to_id.get(sonuc, '')\n",
        "                c_eslesti += 1\n",
        "        print(f'Yol C (kural motoru) ile eşleşen: {c_eslesti:,}')\n",
        "        \n",
        "        # 2) Kalan eşleşmeyenler için DDInter doğrudan tam ad eşleşmesi\n",
        "        mask_hala = df_etken[yol_col].isna() | (df_etken[yol_col] == '')\n",
        "        kalanlar = df_etken[mask_hala].copy()\n",
        "        dogrudan = 0\n",
        "        for idx, row in kalanlar.iterrows():\n",
        "            ad_en_aday = row.get('ad_en', '')\n",
        "            if isinstance(ad_en_aday, str) and ad_en_aday.strip():\n",
        "                norm = normalize_drug_name(ad_en_aday)\n",
        "                if norm in ddinter_norm_set:\n",
        "                    df_etken.at[idx, 'ddinter_id'] = ddinter_norm_to_id.get(norm, '')\n",
        "                    df_etken.at[idx, 'ad_en'] = norm\n",
        "                    df_etken.at[idx, yol_col] = 'B' if pd.notna(row.get('ad_en')) else 'C'\n",
        "                    dogrudan += 1\n",
        "        print(f'DDInter doğrudan tam ad eşleşmesi: {dogrudan:,}')\n",
        "        \n",
        "        # 3) En sık 100 eşleşmeyen için PubChem kontrolü\n",
        "        mask_hala = df_etken['ddinter_id'].isna() | (df_etken['ddinter_id'] == '')\n",
        "        kalanlar = df_etken[mask_hala].copy()\n",
        "        if 'urun_sayisi' in kalanlar.columns:\n",
        "            kalanlar = kalanlar.sort_values('urun_sayisi', ascending=False)\n",
        "            \n",
        "        pubchem_adaylar = kalanlar.head(100)\n",
        "        print(f'\\nPubChem kontrolü yapılacak aday sayısı: {len(pubchem_adaylar):,}')\n",
        "        pubchem_eslesti = 0\n",
        "        for idx, row in pubchem_adaylar.iterrows():\n",
        "            ad = row.get('ad_en', row.get(bilesen_col, ''))\n",
        "            if not isinstance(ad, str) or not ad.strip():\n",
        "                continue\n",
        "            sonuc = pubchem_ddinter_esle(ad, ddinter_norm_set)\n",
        "            if sonuc:\n",
        "                df_etken.at[idx, 'ddinter_id'] = ddinter_norm_to_id.get(sonuc, '')\n",
        "                df_etken.at[idx, 'ad_en'] = sonuc\n",
        "                if pd.isna(df_etken.at[idx, yol_col]) or df_etken.at[idx, yol_col] == '':\n",
        "                    df_etken.at[idx, yol_col] = 'C'\n",
        "                pubchem_eslesti += 1\n",
        "                print(f'  ✅ {ad} → {sonuc} ({ddinter_norm_to_id.get(sonuc, \"?\")})')\n",
        "        \n",
        "        print(f'\\nPubChem ile eşleşen: {pubchem_eslesti:,}')\n",
        "        \n",
        "        # Kalanları eslesmedi olarak işaretle\n",
        "        mask_final = df_etken[yol_col].isna() | (df_etken[yol_col] == '')\n",
        "        df_etken.loc[mask_final, yol_col] = 'eslesmedi'\n",
        "        \n",
        "        print(f'\\n=== YOL DAĞILIMI ===')\n",
        "        print(df_etken[yol_col].value_counts().to_string())\n",
        "else:\n",
        "    print('⏳ etken_madde.csv bekleniyor...')\n"
    ])

    # 19. Adım A5 Markdown
    add_md([
        "---\n",
        "# Adım A5 — `ruhsatli_esleme_taslagi.csv` Üret + `etken_madde.csv` Güncelle\n",
        "\n",
        "- Eşleşmeyen bileşenler `data/interim/ruhsatli_esleme_taslagi.csv` olarak C kişisine (Yol D - Manuel Araştırma) verilir.\n",
        "- C kişisinin eşlemeleri tamamlandıktan sonra `etken_madde.csv` nihai olarak güncellenir."
    ])

    # 20. Adım A5 Dışa Aktar Kod
    add_code([
        "# ─── Ruhsatlı eşleme taslağını üret (C kişisine) ────────────────\n",
        "if etken_madde_path.exists():\n",
        "    df_etken = pd.read_csv(etken_madde_path)\n",
        "    mask_yok = (\n",
        "        df_etken['ddinter_id'].isna() | \n",
        "        (df_etken['ddinter_id'].astype(str).str.strip() == '') |\n",
        "        (df_etken.get('yol', '') == 'eslesmedi')\n",
        "    )\n",
        "    eslesmemis = df_etken[mask_yok].copy()\n",
        "    if 'urun_sayisi' in eslesmemis.columns:\n",
        "        eslesmemis = eslesmemis.sort_values('urun_sayisi', ascending=False)\n",
        "        \n",
        "    taslak_path = INTERIM / 'ruhsatli_esleme_taslagi.csv'\n",
        "    eslesmemis.to_csv(taslak_path, index=False, encoding='utf-8')\n",
        "    print(f'✅ Kaydedildi: {taslak_path}')\n",
        "    print(f'   Eşleşmemiş bileşen: {len(eslesmemis):,}')\n",
        "    print('   → C kişisine Yol D için verilecek.')\n",
        "else:\n",
        "    print('⏳ etken_madde.csv bekleniyor...')\n"
    ])

    # 21. Adım A5 Birleştir Kod
    add_code([
        "# ─── C kişisinin Yol D sonuçlarını birleştir ────────────────────\n",
        "yol_d_path = INTERIM / 'ruhsatli_esleme_taslagi.csv'\n",
        "\n",
        "if etken_madde_path.exists() and yol_d_path.exists():\n",
        "    df_etken = pd.read_csv(etken_madde_path)\n",
        "    df_yol_d = pd.read_csv(yol_d_path)\n",
        "    \n",
        "    if 'ad_en' in df_yol_d.columns and 'ddinter_id' in df_yol_d.columns:\n",
        "        guncellenen = 0\n",
        "        for _, row_d in df_yol_d.iterrows():\n",
        "            dd_val = row_d.get('ddinter_id')\n",
        "            if pd.notna(dd_val) and str(dd_val).strip():\n",
        "                bilesen = row_d.get('bilesen_tr', row_d.get('etken_madde', ''))\n",
        "                col_match = 'bilesen_tr' if 'bilesen_tr' in df_etken.columns else 'etken_madde'\n",
        "                b_clean = str(bilesen).strip().lower()\n",
        "                mask = df_etken[col_match].astype(str).str.strip().str.lower() == b_clean\n",
        "                if mask.any():\n",
        "                    df_etken.loc[mask, 'ad_en'] = row_d['ad_en']\n",
        "                    df_etken.loc[mask, 'ddinter_id'] = str(dd_val).strip()\n",
        "                    df_etken.loc[mask, 'yol'] = 'D'\n",
        "                    guncellenen += 1\n",
        "        print(f'Yol D ile güncellenen: {guncellenen:,}')\n",
        "        \n",
        "    df_etken.to_csv(etken_madde_path, index=False, encoding='utf-8')\n",
        "    print(f'✅ etken_madde.csv güncellendi: {etken_madde_path}')\n",
        "    if 'yol' in df_etken.columns:\n",
        "        print(f'\\n=== NİHAİ YOL DAĞILIMI ===')\n",
        "        print(df_etken['yol'].value_counts().to_string())\n",
        "else:\n",
        "    print('⏳ Dosyalar bekleniyor...')\n"
    ])

    # 22. Adım A6 Markdown
    add_md([
        "---\n",
        "# Adım A6 — `docs/esleme_raporu.md` Yaz\n",
        "\n",
        "**Zorunlu 4 Tablo:**\n",
        "1. Yol bazında bileşen sayısı ve oranları (`A, B, C, D, SKRS, eslesmedi`)\n",
        "2. DDInter eşleşme oranı (Etken madde bazında %X, Ürün bazında %Y)\n",
        "3. ATC ana grubuna göre eşleşme oranı (14 satır: `A, B, C, D, G, H, J, L, M, N, P, R, S, V`)\n",
        "4. Eşleşmeyen en sık 30 bileşen\n",
        "\n",
        "> **🛡️ Savunmacı Merge (Defensive Join):** `urun_etken.csv` ve `etken_madde.csv` tabloları `bilesen_tr` üzerinden birleştirilmeden önce her iki taraftaki anahtar sütunlar `.astype(str).str.strip().str.lower()` ile normalize edilir. Bu sayede A kişisinin verisindeki gizli boşluklar veya harf uyumsuzlukları nedeniyle Tablo 2'deki ürün eşleşme oranı (%Y) asla yapay olarak düşük çıkmaz."
    ])

    # 23. Adım A6 Rapor Kod
    add_code([
        "# ─── Eşleme raporu üret (Savunmacı ve Doğrulanmış Veri Hattı) ────\n",
        "if etken_madde_path.exists():\n",
        "    df_etken = pd.read_csv(etken_madde_path)\n",
        "    \n",
        "    # Tablo 1: Yol Dağılımı\n",
        "    yol_col = 'yol' if 'yol' in df_etken.columns else None\n",
        "    if yol_col:\n",
        "        yol_dag = df_etken[yol_col].value_counts()\n",
        "        yol_toplam = len(df_etken)\n",
        "        t1_rows = []\n",
        "        for y_name in ['A', 'B', 'C', 'D', 'SKRS', 'eslesmedi']:\n",
        "            cnt = yol_dag.get(y_name, 0)\n",
        "            pct = 100 * cnt / yol_toplam if yol_toplam > 0 else 0\n",
        "            t1_rows.append(f'| {y_name} | {cnt:,} | %{pct:.1f} |')\n",
        "        tablo1 = '| Yol | Bileşen Sayısı | Oran |\\n|-----|---------------|------|\\n' + '\\n'.join(t1_rows)\n",
        "    else:\n",
        "        tablo1 = '⚠️ yol sütunu bulunamadı.'\n",
        "        \n",
        "    # Tablo 2: DDInter Eşleşme Oranı\n",
        "    ddinter_var = df_etken['ddinter_id'].notna() & (df_etken['ddinter_id'].astype(str).str.strip() != '')\n",
        "    X = 100 * ddinter_var.sum() / len(df_etken) if len(df_etken) > 0 else 0\n",
        "    \n",
        "    urun_etken_path = INTERIM / 'urun_etken.csv'\n",
        "    b_col = 'bilesen_tr' if 'bilesen_tr' in df_etken.columns else 'etken_madde'\n",
        "    if urun_etken_path.exists():\n",
        "        df_ue = pd.read_csv(urun_etken_path)\n",
        "        ue_b_col = 'bilesen_tr' if 'bilesen_tr' in df_ue.columns else 'etken_madde'\n",
        "        # Savunmacı Temizlik: NaN ve duplike barkod-bileşen çiftlerini temizle\n",
        "        df_ue = df_ue.dropna(subset=['barkod', ue_b_col]).drop_duplicates(subset=['barkod', ue_b_col]).copy()\n",
        "        \n",
        "        # Savunmacı Merge (Defensive Join): Metin sütunlarını zorla strip ve lower yap\n",
        "        # A kişisi 'parasetamol ' veya 'Parasetamol' kaydetmiş olsa dahi eşleşme asla bozulmaz\n",
        "        df_ue['_join_key'] = df_ue[ue_b_col].astype(str).str.replace('İ', 'i').str.replace('I', 'ı').str.strip().str.lower().str.replace('\\u0307', '')\n",
        "        df_etken_match = df_etken[[b_col, 'ddinter_id']].dropna(subset=[b_col]).copy()\n",
        "        df_etken_match['_join_key'] = df_etken_match[b_col].astype(str).str.replace('İ', 'i').str.replace('I', 'ı').str.strip().str.lower().str.replace('\\u0307', '')\n",
        "        \n",
        "        # etken_madde içinde aynı temiz isimden çoklu kayıt varsa DDInterID dolu olanı öne alıp tekilleştir\n",
        "        df_etken_match['_has_dd'] = df_etken_match['ddinter_id'].notna() & (df_etken_match['ddinter_id'].astype(str).str.strip() != '')\n",
        "        df_etken_match = df_etken_match.sort_values('_has_dd', ascending=False).drop_duplicates(subset=['_join_key'])\n",
        "        \n",
        "        df_ue_merged = df_ue.merge(\n",
        "            df_etken_match[['_join_key', 'ddinter_id']],\n",
        "            on='_join_key', how='left'\n",
        "        )\n",
        "        urun_ddinter = df_ue_merged.groupby('barkod')['ddinter_id'].apply(\n",
        "            lambda x: x.notna().any() and (x.astype(str).str.strip() != '').any()\n",
        "        )\n",
        "        Y = 100 * urun_ddinter.sum() / len(urun_ddinter) if len(urun_ddinter) > 0 else 0\n",
        "        tablo2 = f\"\"\"- **Etken madde bazında:** Türkiye'deki etken maddelerin **%{X:.1f}**'i DDInter'da bulunuyor ({ddinter_var.sum():,} / {len(df_etken):,})\n",
        "- **Ürün bazında:** Ruhsatlı ürünlerin **%{Y:.1f}**'sinin en az bir bileşeni DDInter'da bulunuyor ({urun_ddinter.sum():,} / {len(urun_ddinter):,})\"\"\"\n",
        "    else:\n",
        "        tablo2 = f\"\"\"- **Etken madde bazında:** Türkiye'deki etken maddelerin **%{X:.1f}**'i DDInter'da bulunuyor ({ddinter_var.sum():,} / {len(df_etken):,})\n",
        "- **Ürün bazında:** ⚠️ `urun_etken.csv` henüz hazır değil.\"\"\"\n",
        "        \n",
        "    # Tablo 3: ATC Grubu Dağılımı\n",
        "    atc_col = 'atc_kodu' if 'atc_kodu' in df_etken.columns else ('atc' if 'atc' in df_etken.columns else None)\n",
        "    if atc_col:\n",
        "        df_etken['atc_ana_grup'] = df_etken[atc_col].astype(str).str.strip().str[0].str.upper()\n",
        "        tum_gruplar = ['A', 'B', 'C', 'D', 'G', 'H', 'J', 'L', 'M', 'N', 'P', 'R', 'S', 'V']\n",
        "        t3_rows = []\n",
        "        for g in tum_gruplar:\n",
        "            mask = df_etken['atc_ana_grup'] == g\n",
        "            toplam = mask.sum()\n",
        "            eslesen = (mask & ddinter_var).sum()\n",
        "            oran = 100 * eslesen / toplam if toplam > 0 else 0\n",
        "            t3_rows.append(f'| {g} | {eslesen:,} | {toplam:,} | %{oran:.1f} |')\n",
        "        tablo3 = '| ATC Grubu | DDInter Var | Toplam | Oran |\\n|-----------|------------|--------|------|\\n' + '\\n'.join(t3_rows)\n",
        "    else:\n",
        "        tablo3 = '⚠️ ATC sütunu bulunamadı.'\n",
        "        \n",
        "    # Tablo 4: Eşleşmeyen En Sık 30 Bileşen\n",
        "    eslesmemis = df_etken[~ddinter_var].copy()\n",
        "    if 'urun_sayisi' in eslesmemis.columns:\n",
        "        eslesmemis = eslesmemis.sort_values('urun_sayisi', ascending=False)\n",
        "    t4_data = eslesmemis.head(30)\n",
        "    cols_to_show = [c for c in [b_col, 'urun_sayisi'] if c in t4_data.columns]\n",
        "    tablo4 = t4_data[cols_to_show].to_markdown(index=False) if not t4_data.empty else 'Eşleşmeyen bileşen kalmadı.'\n",
        "    \n",
        "    rapor = f\"\"\"# Eşleme Raporu\n",
        "\n",
        "**Oluşturulma Tarihi:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}\n",
        "\n",
        "## 1. Yol Bazında Bileşen Sayısı\n",
        "\n",
        "{tablo1}\n",
        "\n",
        "## 2. DDInter Eşleşme Oranı\n",
        "\n",
        "{tablo2}\n",
        "\n",
        "## 3. ATC Ana Grubuna Göre Eşleşme Oranı (14 Satır)\n",
        "\n",
        "{tablo3}\n",
        "\n",
        "## 4. Eşleşmeyen En Sık 30 Bileşen\n",
        "\n",
        "{tablo4}\n",
        "\"\"\"\n",
        "    rapor_path = DOCS / 'esleme_raporu.md'\n",
        "    rapor_path.write_text(rapor, encoding='utf-8')\n",
        "    print(f'✅ Rapor oluşturuldu: {rapor_path}')\n",
        "    print(rapor[:1200])\n",
        "else:\n",
        "    print('⏳ etken_madde.csv bekleniyor...')\n"
    ])

    # 24. Özet Markdown
    add_md([
        "---\n",
        "## Özet\n",
        "\n",
        "### Bağımsız adımlar (Gün 2–4) — Başarıyla Tamamlandı:\n",
        "- ✅ `data/interim/ddinter_ilac.csv` üretildi ve doğrulandı (1.939 satır, sayısal sıralı).\n",
        "- ✅ `config/tr_en_kurallar.csv` oluşturuldu ve Yol C kural motoru (spesifiklik öncelikli) kuruldu.\n",
        "- ✅ PubChem fonksiyonu; rate limiter, cache poisoning koruması ve retry desteğiyle tamamlandı.\n",
        "\n",
        "### Bağımlı adımlar (Gün 5–6) — Çalıştırmaya Hazır:\n",
        "- ⏳ A kişisinden `data/interim/etken_madde.csv` bekleniyor.\n",
        "- ⏳ C kişisine `ruhsatli_esleme_taslagi.csv` teslim edilecek.\n",
        "- ⏳ `docs/esleme_raporu.md` üretilecek."
    ])

    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3 (.venv)", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.11"}
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

    out_path = NOTEBOOKS_DIR / "03_kopru_ddinter.ipynb"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print(f"🎉 03_kopru_ddinter.ipynb başarıyla üretildi ve güncellendi: {out_path}")


if __name__ == "__main__":
    generate()
