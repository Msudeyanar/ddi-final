"""
src/normalize.py
Ortak temizlik fonksiyonları – TİTCK / SKRS veri ön işleme (İP0)

Dört Temel Fonksiyon:
---------------------
1. tr_lower(text)         : İ→i, I→ı kuralı ve çift boşluğun tek boşluğa inmesi.
2. barkod_temizle(barkod) : Boşluk ve basılabilir olmayan karakterlerin atılması.
3. tuz_at(etkin_madde)    : Tuz sözcüklerinin tam sözcük olarak atılması ("anhidrat"tan
                            "at" kalmamalı) ve geriye bir şey kalmazsa orijinalin korunması.
4. ad_normalize(ad)       : İngilizce ad için küçük harf, tire ve çift boşluk temizliği.

Yardımcı Fonksiyonlar:
----------------------
- eslesme_anahtari(text)  : tr_lower + ASCII katlama (ı→i, ş→s ...)
- gtin_gecerli(barkod)    : GTIN kontrol hanesi doğrulaması
"""

import re
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Optional

import pandas as pd

# ══════════════════════════════════════════════════════════════════
# 1. tr_lower / eslesme_anahtari / ad_normalize
# ══════════════════════════════════════════════════════════════════

_TR_TABLO = str.maketrans("ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ",
                          "abcçdefgğhıijklmnoöprsştuüvyz")
_ASCII_TABLO = str.maketrans("ığüşöçâîû", "igusocaiu")
_GORUNMEZ = re.compile(r"[\u200b\u200c\u200d\u2060\ufeff]")


def _bos_mu(x) -> bool:
    """None / NaN / pd.NA ve skaler olmayan (liste, dizi) değerler boş sayılır."""
    return (not pd.api.types.is_scalar(x)) or bool(pd.isna(x))


def tr_lower(text) -> Optional[str]:
    """İ→i, I→ı kuralı ve çift boşluğun tek boşluğa inmesi (Türkçe küçük harf)."""
    if _bos_mu(text):
        return None
    text = unicodedata.normalize("NFC", str(text))  # I + U+0307 → İ
    text = _GORUNMEZ.sub("", text)
    text = text.translate(_TR_TABLO)
    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()  # \xa0, \n, \r, \t dahil tek boşluk
    return text or None


def eslesme_anahtari(text) -> Optional[str]:
    """tr_lower + ASCII katlama. 'ISOTRETINOIN' ve 'İSOTRETİNOİN' aynı anahtarı verir."""
    t = tr_lower(text)
    return t.translate(_ASCII_TABLO) if t else None


def ad_normalize(ad) -> Optional[str]:
    """İngilizce ad için küçük harf, tire ve çift boşluk temizliği.

    Örnekler:
      'PARACETAMOL - HYDROCHLORIDE'  → 'paracetamol hydrochloride'
      '  Aspirin  '                  → 'aspirin'
      'Dexketoprofen-Trometamol'     → 'dexketoprofen trometamol'
      None                           → None
    """
    if _bos_mu(ad):
        return None
    text = str(ad).lower()
    text = _GORUNMEZ.sub("", text)
    text = text.replace("-", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text or None


# ══════════════════════════════════════════════════════════════════
# 2. barkod_temizle / gtin_gecerli
# ══════════════════════════════════════════════════════════════════

_OCR_TABLO = str.maketrans("lIOo", "1100")
_RAKAM = re.compile(r"[0-9]+")


def barkod_temizle(barkod) -> Optional[str]:
    """Boşluk ve basılabilir olmayan karakterlerin atılması; standart sayısal string.

    dtype=str ile okunduğu varsayılır. Bilimsel notasyon (8.69e+12) bilerek
    düzeltilmez: hassasiyet kaybı sahte barkod üretir, None döner.
    """
    if _bos_mu(barkod):
        return None
    b = str(barkod).strip().replace("\xa0", "").replace(" ", "").lstrip(":")
    b = re.sub(r"\.0+$", "", b)
    if not _RAKAM.fullmatch(b):
        d = b.translate(_OCR_TABLO)
        if not _RAKAM.fullmatch(d):
            return None
        b = d
    return b


def gtin_gecerli(barkod) -> bool:
    """GTIN-8/12/13/14 kontrol hanesi doğrulaması."""
    b = barkod_temizle(barkod)
    if not b or len(b) not in (8, 12, 13, 14):
        return False
    d = [int(c) for c in b[::-1]]
    toplam = sum(x * (3 if i % 2 == 0 else 1) for i, x in enumerate(d[1:]))
    return (10 - toplam % 10) % 10 == d[0]


# ══════════════════════════════════════════════════════════════════
# 3. tuz_at
# ══════════════════════════════════════════════════════════════════

_VARSAYILAN_TUZLAR = [
    # hidratlar
    "pentahidrat", "tetrahidrat", "trihidrat", "dihidrat", "hemihidrat",
    "monohidrat", "seskihidrat", "hekzahidrat", "heptahidrat", "hidrat",
    "anhidrat", "anhidrus", "anhidr", "susuz",
    # halojenürler ve kısaltmalar (hcl, hci: büyük I/OCR hatası, hbr)
    "dihidroklorür", "monohidroklorür", "hidroklorür", "hidrobromür",
    "bromhidrat", "bromür", "iyodür", "klorür", "hcl", "hci", "hbr",
    # katyonlar
    "trisodyum", "disodyum", "sodyum", "dipotasyum", "potasyum",
    "kalsiyum", "magnezyum",
    # asit tuzları ve yaygın esterler
    "hemisülfat", "disülfat", "sülfat", "fosfat", "asetat", "sitrat",
    "fumarat", "hemifumarat", "maleat", "malat", "mezilat", "mesilat",
    "besilat", "tosilat", "tartrat", "tartarat", "bitartarat", "oksalat",
    "suksinat", "benzoat", "glukonat", "diglukonat", "laktat",
    "propiyonat", "dipropiyonat", "valerat", "nitrat", "stearat",
    "pamoat", "dekanoat", "enantat", "bikarbonat", "karbonat",
    "trometamol", "medoksomil", "sileksetil", "aksetil", "proksetil",
    "ksinafoat", "furoat",
]

_KATYONLAR = frozenset({"sodyum", "potasyum", "kalsiyum", "magnezyum", "disodyum", "trisodyum", "dipotasyum"})
_ON_EKLER = frozenset({"susuz", "anhidr"})

# Bağımsız ilaç/elektrolit olan inorganik bileşikler (hidratları atılır ama bileşik korunur)
_INORGANIK_BILESIKLER = frozenset({
    "sodyum klorur", "potasyum klorur", "kalsiyum klorur", "magnezyum klorur",
    "sodyum bikarbonat", "potasyum bikarbonat", "kalsiyum karbonat", "magnezyum karbonat",
    "magnezyum sulfat", "sodyum laktat", "sodyum asetat", "sodyum sitrat",
    "kalsiyum glukonat", "disodyum fosfat", "sodyum fosfat", "potasyum fosfat",
})

# Katyon önde / tuz formu farklı olanlar → baz (etkin) form
_ESDEGER = {
    "klavulanat": "klavulanik asit",
    "valproat": "valproik asit",
    "fusidat": "fusidik asit",
    "aljinat": "aljinik asit",
}

_GECERSIZ_KALINTILAR = frozenset({"hidrojen", "disodyum", "trisodyum", "monobazik", "dibazik", "bi", "baz"})
_PARANTEZ = re.compile(r"\([^)]*\)")


def _tuz_listesi_oku(dosya_yolu: Optional[str] = None) -> list[str]:
    """Dosya formatı: satır başına bir tuz adı, # ile başlayanlar yorum."""
    if dosya_yolu is None:
        varsayilan_yol = Path("config/tuz_listesi.txt")
        if varsayilan_yol.exists():
            yol = varsayilan_yol
        else:
            return list(_VARSAYILAN_TUZLAR)
    else:
        yol = Path(dosya_yolu)

    if not yol.exists():
        print(f"[UYARI] Tuz listesi bulunamadı: {yol}, varsayılan kullanılıyor.")
        return list(_VARSAYILAN_TUZLAR)
    tuzlar = []
    for satir in yol.read_text(encoding="utf-8").splitlines():
        satir = satir.strip()
        if satir and not satir.startswith("#"):
            tuzlar.append(satir)
    return tuzlar


@lru_cache(maxsize=8)
def _tuz_kume(dosya_yolu: Optional[str] = None) -> frozenset:
    """Tuz adları, eşleştirme anahtarı formunda (ASCII katlanmış)."""
    return frozenset(filter(None, (eslesme_anahtari(t) for t in _tuz_listesi_oku(dosya_yolu))))


@lru_cache(maxsize=8)
def _tuz_regex(dosya_yolu: Optional[str] = None):
    tuzlar = sorted(_tuz_kume(dosya_yolu), key=len, reverse=True)  # uzun önce: anhidrat > anhidr
    alt = "|".join(re.escape(t) for t in tuzlar)
    # (?<=\S): tam sözcük olarak atılır, ilk kelime asla silinmez
    return re.compile(rf"(?<=\S)\s+(?:{alt})\s*$")


def _bilesen_temizle(parca: str, rx, tuz_kume: frozenset) -> str:
    orijinal = parca

    def on_ek_at(p: str) -> str:
        w = p.split(" ")
        if len(w) >= 2 and w[0] in _ON_EKLER:
            return " ".join(w[1:])
        # katyon önde: "sodyum valproat" → "valproat"
        # ama "sodyum klorur" gibi inorganik tuzlar korunur (sonraki kelime tuzsa)
        if len(w) >= 2 and w[0] in _KATYONLAR and w[1] not in tuz_kume:
            return " ".join(w[1:])
        return p

    parca = on_ek_at(parca)
    while True:
        if parca in _INORGANIK_BILESIKLER:
            break
        yeni = rx.sub("", parca)
        if yeni == parca:
            break
        parca = yeni
    parca = on_ek_at(parca)

    # Sadece katyona veya anlamsız kalıntıya inmişse orijinali koru
    if parca in _KATYONLAR or parca in _GECERSIZ_KALINTILAR:
        parca = orijinal

    return " ".join(_ESDEGER.get(w, w) for w in parca.split(" "))


def tuz_at(etkin_madde, tuz_listesi_yolu: Optional[str] = None) -> Optional[str]:
    """Tuz sözcüklerinin tam sözcük olarak atılması ve geriye bir şey kalmazsa orijinalin korunması.

    'Lidokain hidroklorür (lidokain olarak)'          → 'lidokain'
    'Amoksisilin trihidrat ve potasyum klavulanat'    → 'amoksisilin, klavulanik asit'
    'sodyum valproat'                                 → 'valproik asit'
    'doksorubisin hcl'                                → 'doksorubisin'
    'ISOTRETINOIN'                                    → 'isotretinoin'
    'sodyum klorür'                                   → 'sodyum klorur' (korunur)

    Ayraçlar: +, /, ve, and, ; (sayısal olmayan virgül) — Parantez içi silinir.
    """
    temiz = eslesme_anahtari(etkin_madde)
    if temiz is None:
        return None
    # Yaygın hatalı/farklı yazımları ve eşanlamlıları standartlaştır
    temiz = re.sub(r"\b(sodyum|potasyum)\s+(?:hidrojen\s+karbonat|bi\s+karbonat)\b", r"\1 bikarbonat", temiz)
    temiz = re.sub(r"\b(?:monobazik|dibazik)\s+(sodyum|potasyum)\s+fosfat\b", r"\1 fosfat", temiz)
    temiz = _PARANTEZ.sub(" ", temiz)
    rx = _tuz_regex(tuz_listesi_yolu)
    tuz_kume = _tuz_kume(tuz_listesi_yolu)

    # Virgül kuralı: 69,19 gibi sayısal virgüller ayrılmaz, iki tarafında harf olan virgüller ayrılır
    temiz = re.sub(r"(?<=\D)\s*,\s*(?=\D)", "|", temiz)
    temiz = re.sub(r"\s*(?:\+|/|;|\bve\b|\band\b)\s*", "|", temiz)

    sonuc: list[str] = []
    for parca in temiz.split("|"):
        parca = re.sub(r"\s+", " ", parca).strip()
        if not parca:
            continue
        parca = _bilesen_temizle(parca, rx, tuz_kume)
        if parca and parca not in sonuc:  # tekrarları at, sırayı koru
            sonuc.append(parca)
    return ", ".join(sonuc) or None


# ══════════════════════════════════════════════════════════════════
# Modül test
# ══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=== 1. tr_lower ===")
    testler = [
        ("DEKZAMETAZON", "dekzametazon"),
        ("İBUPROFEN", "ibuprofen"),
        ("ISTANBUL", "ıstanbul"),
        ("lidokain\xa0hidroklorür", "lidokain hidroklorür"),
        ("METLINOX 69,19 MG/ML ORAL DAMLA,\nSUSPANSIYON",
         "metlınox 69,19 mg/ml oral damla, suspansıyon"),
        (None, None),
    ]
    for girdi, beklenen in testler:
        sonuc = tr_lower(girdi)
        durum = "✓" if sonuc == beklenen else "✗"
        print(f"  {durum} {repr(girdi):55s} → {repr(sonuc)}")

    print("\n=== 2. ad_normalize ===")
    testler = [
        ("PARACETAMOL - HYDROCHLORIDE", "paracetamol hydrochloride"),
        ("  Aspirin  ", "aspirin"),
        ("Dexketoprofen-Trometamol", "dexketoprofen trometamol"),
        ("Metformin\xa0hcl", "metformin hcl"),
        (None, None),
    ]
    for girdi, beklenen in testler:
        sonuc = ad_normalize(girdi)
        durum = "✓" if sonuc == beklenen else "✗"
        print(f"  {durum} {repr(girdi):35s} → {repr(sonuc)}")

    print("\n=== 3. barkod_temizle ===")
    testler = [
        ("8699508010752", "8699508010752"),
        (" 8699508010752 ", "8699508010752"),
        ("8699508010752.0", "8699508010752"),
        (":8683060090130", "8683060090130"),
        ("86995870l3286", "8699587013286"),
        ("868191l040013", "8681911040013"),
        (None, None),
        ("abc", None),
        ("", None),
    ]
    for girdi, beklenen in testler:
        sonuc = barkod_temizle(girdi)
        durum = "✓" if sonuc == beklenen else "✗"
        print(f"  {durum} {repr(girdi):25s} → {repr(sonuc)}")

    print("\n=== 4. gtin_gecerli ===")
    testler = [
        ("8699508010752", True),
        ("8699508010753", False),   # yanlış kontrol hanesi
        ("abc", False),
        (None, False),
    ]
    for girdi, beklenen in testler:
        sonuc = gtin_gecerli(girdi)
        durum = "✓" if sonuc == beklenen else "✗"
        print(f"  {durum} {repr(girdi):25s} → {sonuc}")

    print("\n=== 5. tuz_at ===")
    testler = [
        ("lidokain hidroklorür", "lidokain"),
        ("doksorubisin hcl", "doksorubisin"),
        ("benidipin hci", "benidipin"),
        ("Fingolimod hidroklorür", "fingolimod"),
        ("atorvastatin kalsiyum trihidrat", "atorvastatin"),
        ("Azitromisin dihidrat", "azitromisin"),
        ("Aklidinyum bromür, Formoterol fumarat dihidrat",
         "aklidinyum, formoterol"),
        ("sodyum valproat", "valproik asit"),
        ("Amoksisilin trihidrat ve potasyum klavulanat",
         "amoksisilin, klavulanik asit"),
        ("sodyum klorür", "sodyum klorur"),   # inorganik: korunur
        ("kalsiyum klorür dihidrat", "kalsiyum klorur"),  # hidrat atılır, inorganik korunur
        ("kalsiyum karbonat", "kalsiyum karbonat"),  # besin: korunur
        ("sodyum hidrojen karbonat", "sodyum bikarbonat"),
        ("olmesartan medoksomil", "olmesartan"),
        ("dekzametazon", "dekzametazon"),
        ("ISOTRETINOIN", "isotretinoin"),
        (None, None),
    ]
    for girdi, beklenen in testler:
        sonuc = tuz_at(girdi)
        durum = "✓" if sonuc == beklenen else "✗"
        print(f"  {durum} {repr(girdi):55s} → {repr(sonuc)}")
        if sonuc != beklenen:
            print(f"      BEKLENEN: {repr(beklenen)}")
