# Proje Açık Soruları ve Danışman Kararları

> **Not:** Kurallara uymayan durumlarda varsayım yapılmamış olup, veri birleştirme ve eşleme süreçlerinde karşılaşılan tüm durumlar bu belgede toplanmıştır.

---

## BÖLÜM 1: Yol D — Kişi C Açık Soruları

### 1. Dekstran Ürün Ayrımı (21 Ürün)
- **Durum:** Kayıt; dekstran 40 (`DDInter525`), dekstran 70 (`DDInter524`) ve `%5 dekstroz` ürünlerindeki `dekstran monohidrat` yazımlarını birbiriyle karıştırmaktadır.
- **Karar / Soru:** Ürün bazında ayrı ayrı mı ele alınmalıdır, yoksa kaynak veri düzeltilerek doğrudan dekstroz (`DDInter529`) olarak mı sayılmalıdır?

### 2. ATC Grup Adlarının Durumu (14 Bileşen)
- **Durum:** `combinations`, `other cold preparations`, `diuretics`, `enzyme inhibitor` vb. ifadeler gerçek birer etken madde değildir.
- **Karar / Soru:** Gerçek bileşen ürün adından veya ATC kodundan çıkarılmalı mıdır (örneğin `J01CR05` $\rightarrow$ *tazobaktam*, `C09DA08` $\rightarrow$ *HCTZ*), yoksa doğrudan eşleşmemiş mi bırakılmalıdır? *(Bu karar, bazı ürünlerin etkileşim sorgularında görünürlüğünü doğrudan belirlemektedir.)*

### 3. Tuz / Ester ve Form Ayrımı Kuralları
- **Durum:** Beklometazon (`DDInter168` *dipropiyonat*; nazal kayıt `169`), glikopironyum (`834` / topikal `835`), ksilometazolin (yalnızca nazal kayıt mevcut) ve insan normal immünoglobulini (IV kaydı `873` seçildi; SC/IM ürün ihtimali) gibi maddelerde form farklılıkları bulunmaktadır.
- **Karar / Soru:** Form bazlı kayıt seçimlerinde hangi standart kural uygulanacaktır?

### 4. Yazım Varyantlarının Birleştirilmesi
- **Durum:** *deksketoprofen / dexketoprofen*, *gliklazid / gliclazide*, *sultamisilin / sultamicillin*, *glukoz / glikoz / dekstroz* ve *tiamin / vitamin b1* ayrı bileşenler olarak sayılmaktadır.
- **Karar / Soru:** Bu normalizasyon işlemi Yol A aşamasında mı yoksa Yol B aşamasında mı düzeltilecektir?

### 5. `dimetil` Eşlemesi ve Kaynak Veri Düzeltmesi (22 Ürün)
- **Durum:** `tuz_at()` fonksiyonu `dimetil fumarat` ifadesini `dimetil`'e indirmiştir. Eşleme `DDInter564`'e yapılmıştır.
- **Karar / Soru:** Kaynak verinin orijinal hâline (`dimetil fumarat`) döndürülmesi gerekmektedir (Yol A sorumluluğu).

### 6. Aspartam ve Endikasyon Çelişkisi (SANPA, A10X, 16 Ürün)
- **Durum:** Ürün adı ve ATC grubu bir antidiyabetik düşündürürken, etken madde metni doğrudan `aspartam` olarak geçmektedir.
- **Karar / Soru:** Kaynak veride olası bir hata ihtimaline karşı bu kayıt doğrulanmalıdır.

### 7. Lipid Emülsiyonu ve Diyaliz / Amino Asit Bileşenleri
- **Durum:** Rafine soya yağı vb. lipid emülsiyon bileşenleri ile diyaliz/amino asit bileşenleri DDInter veritabanında yer almamaktadır.
- **Karar / Soru:** Bu ürün grubu ürün bazlı oranlarda doğrudan "eşleşmemiş" mi sayılacak, yoksa B05 raporunda ayrı bir kategoride mi raporlanacaktır?

### 8. Eşitlik Sınırı (Tie Sınırı) ve Kapsam Genişletme
- **Durum:** 15 ürünlük eşitlik grubunda 3 bileşen (*rafine soya yağı*, *rokuronyum*, *sulpiride*) ilk 100 incelemenin dışında kalmıştır. Özellikle *rokuronyum* `DDInter1612` ile eşleşebilir görünmektedir.
- **Karar / Soru:** Bu maddeler 100–300 ürün aralığına dahil edilerek incelenmeli midir?

---

## BÖLÜM 2: Kişi A Tarafından Bildirilen Diğer Proje Soruları

### 9. SKRS ATC Adlarındaki Parantez İçi İfadeler ve Eşleme Davranışı
- **Gözlem:** SKRS aktif ve pasif listelerinde bazı ATC adları parantez içi ekler içermektedir (örneğin `A11GA01` için `"ascorbic acid (vit c)"`, `A10AD01` için `"insulin (human)"`, `A11HA02` için `"pyridoxine (vit B6)"`, `J06BB` için `"antilymphocyte immunoglobulin (horse)"`).
- **Uygulanan Prensip (Kişi A):** Sabit kurallarda açık bir temizlik kuralı belirtilmediği için resmi SKRS ATC metinlerine keyfi müdahale edilmemiş ve sözlükte orijinal hali korunmuştur.
- **Toplantıda Sorulacak Soru:** Bu parantez içi ekler Yol C / Yol D aşamasında kural motoruyla mı temizlenmelidir, yoksa PubChem eş anlamlı aramasına mı bırakılmalıdır?

### 10. TEKNAZOL (ketokonazol) Hatalı TİTCK ATC Kodu
- **Gözlem:** TİTCK Ruhsatlı Beşeri Tıbbi Ürünler Listesi'nde TEKNAZOL 200 MG TABLET ürünlerinin (Barkodlar: `8699540014800`, `8699540014817`, `8699540014824`) ATC kodu sehven `M01AE03` (ketoprofen) olarak kaydedilmiştir. Ketokonazol sistemik bir antifungaldir ve resmi WHO ATC kodu `J02AB02`'dir.
- **Uygulanan Çözüm / Karar:** `01_titck_temizlik.ipynb` içinde bu 3 barkod için ATC kodu resmi değeri olan `J02AB02` (ketoconazole) olarak düzeltilmiş, izlenebilirlik için `atc_kaynak_hatasi_duzeltildi = 1` bayrağı ile işaretlenmiştir.
- **Toplantıda Sorulacak Soru:** Resmi kurum verisindeki bu tür açık yazım hataları için danışman onayıyla override kuralı işletilmesi uygun mudur?

### 11. TİTCK Ham Verisindeki Sözde Etken Maddeler
- **Gözlem:** TİTCK Ruhsatlı listesinde bazı kombine ürünlerde `etkin_madde_ham` sütununa kimyasal madde adı yerine doğrudan WHO ATC kategori açıklamaları yazılmıştır (`combinations`, `various`, `other cold preparations`). 
- **Toplantıda Sorulacak Soru / Karar Önerisi:** 
  1. Bu jenerik kategori sözcükleri `src/normalize.py` aşamasında bir kara liste ile ayrıştırma dışı mı bırakılmalıdır?
  2. Yoksa bu satırlar `urun_etken.csv`'de korunup yalnızca Yol A/B'ye girmesi engellenerek `eslesmedi` statüsüne mi çekilmelidir?

### 12. Dozaj ve Birim Kalıntıları İçeren Bileşenler ve Yol D Kapsamı
- **Gözlem:** TİTCK ham tablosunda çok az sayıda (yaklaşık 6 ürün) etken madde metninin içine rakamsal doz ve birim yazılmıştır (`vitamin a palmitat 20.000 iu/ml`, `kolistimetat sodyum 4.500.000 iu` vb.).
- **Toplantıda Sorulacak Soru / Karar Önerisi:** Bu tür uç vakalar Yol D (Elle Eşleme) sürecine mi bırakılmalıdır, yoksa `src/normalize.py` içine kontrollü bir dozaj temizleme kuralı mı eklenmelidir?