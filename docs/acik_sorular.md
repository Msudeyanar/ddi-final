# Açık Sorular — Yol D (Kişi C)

> **Not:** Kurallara uymayan durumlarda varsayım yapılmamış olup, aşağıdaki maddeler toplantıda karara bağlanmak üzere listelenmiştir.

---

### 1. Dekstran Ürün Ayrımı (21 Ürün)
* **Durum:** Kayıt; dekstran 40 (`DDInter525`), dekstran 70 (`DDInter524`) ve `%5 dekstroz` ürünlerindeki `dekstran monohidrat` yazımlarını birbiriyle karıştırmaktadır.
* **Karar / Soru:** Ürün bazında ayrı ayrı mı ele alınmalıdır, yoksa kaynak veri düzeltilerek doğrudan dekstroz (`DDInter529`) olarak mı sayılmalıdır?

### 2. ATC Grup Adlarının Durumu (14 Bileşen)
* **Durum:** `combinations`, `other cold preparations`, `diuretics`, `enzyme inhibitor` vb. ifadeler gerçek birer etken madde değildir.
* **Karar / Soru:** Gerçek bileşen ürün adından veya ATC kodundan çıkarılmalı mıdır (örneğin `J01CR05` $\rightarrow$ *tazobaktam*, `C09DA08` $\rightarrow$ *HCTZ*), yoksa doğrudan eşleşmemiş mi bırakılmalıdır? *(Bu karar, bazı ürünlerin etkileşim sorgularında görünürlüğünü doğrudan belirlemektedir.)*

### 3. Tuz / Ester ve Form Ayrımı Kuralları
* **Durum:** Beklometazon (`DDInter168` *dipropiyonat*; nazal kayıt `169`), glikopironyum (`834` / topikal `835`), ksilometazolin (yalnızca nazal kayıt mevcut) ve insan normal immünoglobulini (IV kaydı `873` seçildi; SC/IM ürün ihtimali) gibi maddelerde form farklılıkları bulunmaktadır.
* **Karar / Soru:** Form bazlı kayıt seçimlerinde hangi standart kural uygulanacaktır?

### 4. Yazım Varyantlarının Birleştirilmesi
* **Durum:** *deksketoprofen / dexketoprofen*, *gliklazid / gliclazide*, *sultamisilin / sultamicillin*, *glukoz / glikoz / dekstroz* ve *tiamin / vitamin b1* ayrı bileşenler olarak sayılmaktadır.
* **Karar / Soru:** Bu normalizasyon işlemi Yol A aşamasında mı yoksa Yol B aşamasında mı düzeltilecektir?

### 5. `dimetil` Eşlemesi ve Kaynak Veri Düzeltmesi (22 Ürün)
* **Durum:** `tuz_at()` fonksiyonu `dimetil fumarat` ifadesini `dimetil`'e indirmiştir. Eşleme `DDInter564`'e yapılmıştır.
* **Karar / Soru:** Kaynak verinin orijinal hâline (`dimetil fumarat`) döndürülmesi gerekmektedir (Yol A sorumluluğu).

### 6. Aspartam ve Endikasyon Çelişkisi (SANPA, A10X, 16 Ürün)
* **Durum:** Ürün adı ve ATC grubu bir antidiyabetik düşündürürken, etken madde metni doğrudan `aspartam` olarak geçmektedir.
* **Karar / Soru:** Kaynak veride olası bir hata ihtimaline karşı bu kayıt doğrulanmalıdır.

### 7. Lipid Emülsiyonu ve Diyaliz / Amino Asit Bileşenleri
* **Durum:** Rafine soya yağı vb. lipid emülsiyon bileşenleri ile diyaliz/amino asit bileşenleri DDInter veritabanında yer almamaktadır.
* **Karar / Soru:** Bu ürün grubu ürün bazlı oranlarda doğrudan "eşleşmemiş" mi sayılacak, yoksa B05 raporunda ayrı bir kategoride mi raporlanacaktır?

### 8. Eşitlik Sınırı (Tie Sınırı) ve Kapsam Genişletme
* **Durum:** 15 ürünlük eşitlik grubunda 3 bileşen (*rafine soya yağı*, *rokuronyum*, *sulpiride*) ilk 100 incelemenin dışında kalmıştır. Özellikle *rokuronyum* `DDInter1612` ile eşleşebilir görünmektedir.
* **Karar / Soru:** Bu maddeler 100–300 ürün aralığına dahil edilerek incelenmeli midir?