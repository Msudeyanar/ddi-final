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
    """EAN-13 kontrol hanesi doğrulaması (PDF Kural 2: 13 haneli ve EAN-13 uyumlu)."""
    b = barkod_temizle(barkod)
    if not b or len(b) != 13:
        return False
    d = [int(c) for c in b[::-1]]
    toplam = sum(x * (3 if i % 2 == 0 else 1) for i, x in enumerate(d[1:]))
    return (10 - toplam % 10) % 10 == d[0]


# ══════════════════════════════════════════════════════════════════
# 3. tuz_at ve bilesenlere_ayir
# ══════════════════════════════════════════════════════════════════

_VARSAYILAN_TUZLAR = [
    # hidratlar
    "pentahidrat", "tetrahidrat", "trihidrat", "dihidrat", "hemihidrat",
    "monohidrat", "seskihidrat", "hekzahidrat", "heptahidrat", "oktahidrat",
    "hidrat", "anhidrat", "anhidrus", "anhidroz", "anhidrit", "anhidr", "susuz",
    # halojenürler ve kısaltmalar (hcl, hci: büyük I/OCR hatası, hbr)
    "dihidroklorür", "monohidroklorür", "hidroklorür", "hidrobromür",
    "bromhidrat", "bromür", "iyodür", "klorür", "hcl", "hci", "hbr",
    # katyonlar, bazlar ve aminler
    "trisodyum", "disodyum", "sodyum", "dipotasyum", "potasyum",
    "kalsiyum", "magnezyum", "trometamol", "trometamin", "erbumin",
    "tert-butilamin", "meglumin",
    # asit tuzları ve yaygın esterler / formlar
    "hemisülfat", "disülfat", "sülfat", "fosfat", "asetat", "sitrat",
    "fumarat", "hemifumarat", "maleat", "malat", "mezilat", "mesilat",
    "besilat", "tosilat", "tartrat", "tartarat", "bitartarat", "oksalat",
    "suksinat", "süksinat", "benzoat", "glukonat", "diglukonat", "laktat",
    "propiyonat", "dipropiyonat", "valerat", "nitrat", "stearat",
    "pamoat", "dekanoat", "enantat", "bikarbonat", "karbonat",
    "medoksomil", "sileksetil", "aksetil", "proksetil", "ksinafoat", "ksinofoat", "furoat",
    "trifenatat", "palmitat", "aseponat", "butirat", "etabonat",
    "salisilat", "nikotinat", "aspartat", "orotat", "kamsilat", "tertbutilamin",
    "hidroklorid", "mikropelle", "mikropellet", "pellet", "pelletleri", "pelletler",
]

_KATYONLAR = frozenset({"sodyum", "potasyum", "kalsiyum", "magnezyum", "disodyum", "trisodyum", "dipotasyum"})
_ON_EKLER = frozenset({"susuz", "anhidr"})

# Bağımsız ilaç/elektrolit olan inorganik bileşikler (hidratları atılır ama bileşik korunur)
_INORGANIK_BILESIKLER = frozenset({
    "sodyum klorur", "potasyum klorur", "kalsiyum klorur", "magnezyum klorur",
    "sodyum bikarbonat", "potasyum bikarbonat", "kalsiyum karbonat", "magnezyum karbonat",
    "magnezyum sulfat", "sodyum laktat", "sodyum asetat", "sodyum sitrat",
    "kalsiyum glukonat", "disodyum fosfat", "sodyum fosfat", "potasyum fosfat",
    "magnezyum oksit", "magnezyum hidroksit", "aluminyum hidroksit", "cinko oksit",
    "cinko sulfat", "sodyum florur", "baryum sulfat",
})

# Katyon önde / tuz formu farklı olanlar → baz (etkin) form
_ESDEGER = {
    "klavulanat": "klavulanik asit",
    "valproat": "valproik asit",
    "fusidat": "fusidik asit",
    "aljinat": "aljinik asit",
    "folinat": "folinik asit",
    "levofolinat": "levofolinik asit",
    "dobesilat": "dobesilik asit",
    "pikosulfat": "pikosulfurik asit",
    "sennosid": "sennozit",
}

_GECERSIZ_KALINTILAR = frozenset({
    "hidrojen", "disodyum", "trisodyum", "monobazik", "dibazik", "bi", "baz",
    "oksit", "hidroksit", "florur"
})
_PSEUDO_BILESENLER = frozenset({
    "plain", "combinations", "various", "concentrates", "hemofiltrates",
    "combinations excl. psycholeptics"
})
_PARANTEZ = re.compile(r"\([^)]*\)")
_ATC_SIFAT_REGEX = re.compile(
    r",\s*(?:plain|combinations(?:\s+excl\.[^,]*)?|various|concentrates)\b|\s+and\s+hemofiltrates\b",
    re.IGNORECASE
)



def _tuz_listesi_oku(dosya_yolu: Optional[str] = None) -> list[str]:
    """Dosya formatı: satır başına bir tuz adı, # ile başlayanlar yorum."""
    if dosya_yolu is None:
        proje_koku = Path(__file__).resolve().parent.parent
        varsayilan_yol = proje_koku / "config" / "tuz_listesi.txt"
        if not varsayilan_yol.exists():
            varsayilan_yol = Path("config/tuz_listesi.txt")
        yol = varsayilan_yol
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
        if p in _INORGANIK_BILESIKLER:
            return p
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


_RX_PERCENT = re.compile(r"^%\s*\d+(?:[\.,]\d+)?(?:\s*['’]?(?:l[ıiuü]k))?\s*")
_RX_PERCENT_TRAIL = re.compile(r"\s+%\s*\d+(?:[\.,]\d+)?(?:\s*['’]?(?:l[ıiuü]k))?\s*$")
_RX_HYDRATE = re.compile(r"[\.\s]*\b\d*h2o\b", re.IGNORECASE)


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
    temiz = _ATC_SIFAT_REGEX.sub("", temiz)
    rx = _tuz_regex(tuz_listesi_yolu)
    tuz_kume = _tuz_kume(tuz_listesi_yolu)

    # Sayısal olmayan virgülleri ayır (ondalık sayıları koru: 69,19 ayrılmaz)
    temiz = re.sub(r"(?<=\D)\s*,\s*(?=\D)", "|", temiz)
    temiz = re.sub(r"\s*(?:\+|;|\bve\b|\band\b)\s*", "|", temiz)
    temiz = re.sub(r"(?<=[a-zA-ZçğıöşüÇĞİÖŞÜ]{3})\s*/\s*(?=[%0-9\s]*[a-zA-ZçğıöşüÇĞİÖŞÜ]{3})", "|", temiz)

    sonuc: list[str] = []
    for parca in temiz.split("|"):
        parca = re.sub(r"\s+", " ", parca).strip()
        parca = _RX_PERCENT.sub("", parca).strip()
        parca = _RX_PERCENT_TRAIL.sub("", parca).strip()
        parca = _RX_HYDRATE.sub("", parca).strip(" \t\n\r,.-;/")
        if not parca:
            continue
        parca = _bilesen_temizle(parca, rx, tuz_kume)
        parca = _RX_PERCENT.sub("", parca)
        parca = _RX_PERCENT_TRAIL.sub("", parca)
        parca = _RX_HYDRATE.sub("", parca).strip(" \t\n\r,.-;/")
        if parca and parca not in _PSEUDO_BILESENLER and parca not in sonuc:  # tekrarları at, sırayı koru
            sonuc.append(parca)
    return ", ".join(sonuc) or None


def bilesenlere_ayir(
    etkin_madde_ham: Optional[str],
    tuz_listesi_yolu: Optional[str] = None,
    kaynak: Optional[str] = None,
) -> list[tuple[int, str, str]]:
    """Adım 2 kuralına göre etkin madde metnini bileşenlerine ayırır.

    Dönüş formatı: [(sira, bilesen_ham, bilesen_tr), ...]
    Örnek:
      'amlodipin besilat + valsartan'
      → [(1, 'amlodipin besilat', 'amlodipin'), (2, 'valsartan', 'valsartan')]
    """
    if _bos_mu(etkin_madde_ham):
        return []

    ham_str = str(etkin_madde_ham).strip()
    if not ham_str:
        return []

    # Sabit Kural 5: SKRS'te aktif olup ruhsatlıda olmayan ürünler:
    # Bu metin zaten İngilizce olduğu için Adım 2'deki Türkçe temizlikten geçmez:
    # bileşenleri ATC adından " and " ile bölünerek alınır
    if kaynak == "SKRS":
        parts = [p.strip() for p in re.split(r"\s+and\s+", ham_str, flags=re.IGNORECASE) if p.strip()]
        bilesenler: list[tuple[int, str, str]] = []
        for i, p in enumerate(parts, 1):
            norm = ad_normalize(p) or p.lower().strip()
            norm = norm.strip(" \t\n\r,.-;/")
            if norm and norm not in _PSEUDO_BILESENLER:
                bilesenler.append((i, p, norm))
        return bilesenler

    # Türkçe küçük harfe indirgeme
    t = tr_lower(ham_str)
    if not t:
        return []

    # Sennozit a+b gibi kısaltmaları açık yazıma çevir (sennozit / sennosid)
    t = re.sub(r"\b(senno[zs]i[td])\s+([a-d])\s*\+\s*([a-d])\b", r"\1 \2 + \1 \3", t)

    # Parantez içi stereoizomerleri temizle: (s)-laktat → laktat
    t = re.sub(r"\(\s*[sSrdRD]\s*\)\s*-\s*", "", t)
    # Parantez içi genel açıklamaları sil
    t = _PARANTEZ.sub(" ", t)

    # TİTCK/SKRS açıklama kalıntılarını (ATC sıfatlarını) virgülden bölmeden önce temizle
    t = _ATC_SIFAT_REGEX.sub("", t)

    # Sırayla ayırıcılar: +, ;, ve, and
    t = re.sub(r"\s*(?:\+|;|\bve\b|\band\b)\s*", "|", t)

    # Slash (/): İki tarafında en az 3 harfli sözcük varsa ayırır
    # (Virüs suşları A/Victoria/4897/2022 veya 27/3 gibi yapıları bozmaz; %25 insulin / %75 insulin gibi yüzdeli kombinasyonları ayırır)
    t = re.sub(r"(?<=[a-zA-ZçğıöşüÇĞİÖŞÜ]{3})\s*/\s*(?=[%0-9\s]*[a-zA-ZçğıöşüÇĞİÖŞÜ]{3})", "|", t)

    # Virgül kuralı: İki tarafında da harfle başlayan ve en az 4 harfli bir sözcük varsa ayırıcı sayılır
    # Sol parçada en az 4 harfli bir sözcük, sağ parçanın başında ise (l-, d- gibi önekler hariç) en az 4 harfli sözcük aranır
    tokens = t.split(",")
    parts = []
    current = []
    for i in range(len(tokens) - 1):
        left_chunk = tokens[i].strip()
        right_chunk = tokens[i + 1].strip()

        left_words = re.findall(r"[a-zA-ZçğıöşüÇĞİÖŞÜ]{4,}", left_chunk)
        clean_right = re.sub(r"^(%\s*\d+\s*|[ldLD]\-)", "", right_chunk)
        right_first_word = re.findall(r"^[a-zA-ZçğıöşüÇĞİÖŞÜ]+", clean_right)

        is_split = False
        if left_words and right_first_word and len(right_first_word[0]) >= 4:
            is_split = True

        current.append(tokens[i])
        if is_split:
            parts.append(",".join(current).strip())
            current = []
    current.append(tokens[-1])
    parts.append(",".join(current).strip())

    final_pieces = []
    for p in parts:
        for sub_p in p.split("|"):
            sub_p = re.sub(r"\s+", " ", sub_p).strip()
            if sub_p:
                final_pieces.append(sub_p)

    rx = _tuz_regex(tuz_listesi_yolu)
    tuz_kume = _tuz_kume(tuz_listesi_yolu)

    bilesenler: list[tuple[int, str, str]] = []
    gorulen_tr: set[str] = set()
    sira = 1

    for parca in final_pieces:
        parca_temiz = _RX_PERCENT.sub("", parca).strip()
        parca_temiz = _RX_PERCENT_TRAIL.sub("", parca_temiz).strip()
        parca_temiz = _RX_HYDRATE.sub("", parca_temiz).strip(" \t\n\r,.-;/")
        p_ascii = eslesme_anahtari(parca_temiz)
        if not p_ascii:
            continue
        b_tr = _bilesen_temizle(p_ascii, rx, tuz_kume)
        b_tr = _RX_PERCENT.sub("", b_tr)
        b_tr = _RX_PERCENT_TRAIL.sub("", b_tr)
        b_tr = _RX_HYDRATE.sub("", b_tr).strip(" \t\n\r,.-;/")
        if not re.search(r"[a-zA-ZçğıöşüÇĞİÖŞÜ]", b_tr) or len(b_tr) <= 1:
            continue
        if b_tr in _PSEUDO_BILESENLER:
            continue
        if b_tr and b_tr not in gorulen_tr:
            gorulen_tr.add(b_tr)
            bilesenler.append((sira, parca, b_tr))
            sira += 1

    return bilesenler


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
        ("MULTIVITAMINS, PLAIN", "multivitamins"),
        ("tiyokolşikosid, combinations", "tiyokolsikosid"),
        ("antiseptics, various", "antiseptics"),
        ("hemodialytics and hemofiltrates", "hemodialytics"),
        (None, None),
    ]
    for girdi, beklenen in testler:
        sonuc = tuz_at(girdi)
        durum = "✓" if sonuc == beklenen else "✗"
        print(f"  {durum} {repr(girdi):55s} → {repr(sonuc)}")
        if sonuc != beklenen:
            print(f"      BEKLENEN: {repr(beklenen)}")          