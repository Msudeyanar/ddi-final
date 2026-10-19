# Proje Açık Soruları ve Danışman Kararları

Bu belge, "Veri Birleştirme Planı ve 2. Hafta Görevleri" kuralları gereği, veri birleştirme sürecinde karşılaşılan ve varsayımda bulunulmadan danışmana ve proje ekibine sorulması gereken durumları içerir.

---

### 1. SKRS ATC Adlarındaki Parantez İçi İfadeler ve Eşleme Davranışı
- **Gözlem:** SKRS aktif ve pasif listelerinde bazı ATC adları parantez içi ekler içermektedir (örneğin `A11GA01` için `"ascorbic acid (vit c)"`, `A10AD01` için `"insulin (human)"`, `A11HA02` için `"pyridoxine (vit B6)"`, `J06BB` için `"antilymphocyte immunoglobulin (horse)"`).
- **Uygulanan Prensip (Kişi A):** Sabit kurallarda ("bir durum kurallara uymuyorsa varsayım yapılmaz") açık bir temizlik kuralı belirtilmediği için resmi SKRS ATC metinlerine keyfi müdahale edilmemiş ve sözlükte orijinal hali korunmuştur.
- **Toplantıda Sorulacak Soru:** Bu parantez içi ekler (`(vit c)`, `(human)` vb.) Yol C / Yol D aşamasında kural motoruyla mı temizlenmelidir, yoksa PubChem eş anlamlı aramasına (synonyms) mı bırakılmalıdır?

---

### 13. TEKNAZOL (ketokonazol) Hatalı TİTCK ATC Kodu
- **Gözlem:** TİTCK Ruhsatlı Beşeri Tıbbi Ürünler Listesi'nde TEKNAZOL 200 MG TABLET ürünlerinin (Barkodlar: `8699540014800`, `8699540014817`, `8699540014824`) ATC kodu sehven `M01AE03` (ketoprofen - romatizma ilacı/NSAİİ) olarak kaydedilmiştir. Ketokonazol sistemik bir antifungaldir ve resmi WHO ATC kodu `J02AB02`'dir.
- **Yarattığı Sorun:** `03_kopru_ddinter.ipynb`'de bileşen bazında en sık geçen ATC kodu (`mode()`) hesaplandığında, bu ürünlerin frekansından dolayı `ketokonazol` bileşeni `M01AE03` kapmakta ve DDInter'da romatizma ilacı olan `DDInter1009` (ketoprofen) ile yanlış eşleşmektedir.
- **Uygulanan Çözüm / Karar:** Downstream etkileşim analizinde kritik bir klinik güvenlik hatasını önlemek amacıyla `01_titck_temizlik.ipynb` içinde bu 3 barkod için ATC kodu resmi değeri olan `J02AB02` (ketoconazole) olarak düzeltilmiş, izlenebilirlik için `atc_kaynak_hatasi_duzeltildi = 1` bayrağı ile işaretlenmiştir.
- **Toplantıda Sorulacak Soru:** Resmi kurum verisindeki bu tür açık yazım hataları için danışman onayıyla override kuralı işletilmesi uygun mudur?

---

### 14. TİTCK Ham Verisindeki Sözde Etken Maddeler (`combinations`, `various`, `other cold preparations`)
- **Gözlem:** TİTCK Ruhsatlı listesinde bazı kombine veya çoklu bileşenli ürünlerde `etkin_madde_ham` sütununa kimyasal madde adı yerine doğrudan WHO ATC kategori açıklamaları yazılmıştır (örneğin `"tiyokolşikosid, combinations"` $\rightarrow$ 62 ürün, `"antiseptics, various"` $\rightarrow$ 14 ürün, `"other cold preparations"` $\rightarrow$ 47 ürün). Adım 2'deki standart virgül ayrıştırma kuralı (iki tarafında 4+ harfli sözcük bulunması) gereği bu terimler ayrılarak `urun_etken.csv` içinde bağımsız birer etken madde gibi yer almıştır.
- **Yarattığı Sorun:** `03_kopru_ddinter.ipynb` Yol A'da en sık geçen ATC modu alındığında, bu sözde maddeler rastgele birer 7 haneli ATC kapmaktadır (örneğin `combinations` $\rightarrow$ `D01AC20` mantar/kortizon kombinasyonu, `other cold preparations` $\rightarrow$ `N02AJ06` kodein/parasetamol). Bu durum downstream etkileşim analizinde gerçekte var olmayan yanıltıcı ilaç etkileşimleri üretme riski taşır.
- **Uygulanan Prensip (Kişi A):** Şartnamenin Sabit Kural 11 ("hiçbir satır silinmez, ham veriler değişmez") ve "varsayım yapılmaz" ilkeleri gereği resmi TİTCK satırları keyfi olarak tablodan silinmemiş, ham veri bütünlüğü korunmuştur.
- **Toplantıda Sorulacak Soru / Karar Önerisi:** 
  1. `combinations`, `various`, `other cold preparations`, `other antiemetics` gibi jenerik kategori sözcükleri `src/normalize.py` Adım 2 aşamasında bir kara liste (stop-words) ile ayrıştırma dışı mı bırakılmalıdır?
  2. Yoksa bu satırlar `urun_etken.csv`'de korunup yalnızca Adım 3 Yol A/B'ye girmesi engellenerek `eslesmedi` (kapsam dışı) statüsüne mi çekilmelidir?

---

### 15. Dozaj ve Birim Kalıntıları İçeren Bileşenler ve Yol D Kapsamı
- **Gözlem:** TİTCK ham tablosunda çok az sayıda (yaklaşık 6 ürün) etken madde metninin içine rakamsal doz ve birim yazılmıştır (örneğin `"vitamin a palmitat 20.000 iu/ml"`, `"kolistimetat sodyum 4.500.000 iu"`, `"etinilestradiol 0.02 mg"`, `"b1 vitamini 25 mg, b2 vitamini 5 mg..."`).
- **Uygulanan Prensip (Kişi A):** `vitamin b1`, `vitamin b6`, `interferon beta-1a`, `a/victoria/4897/2022` gibi meşru rakam veya tire içeren kimyasal/biyolojik adları bozmamak adına kontrolsüz bir sayı/birim silme regex'i uygulanmamıştır. Başarı oranı 3.085 bileşende %99.8 olup PDF'in %90 doğruluk barajını fazlasıyla karşılamaktadır.
- **Toplantıda Sorulacak Soru / Karar Önerisi:** Bu tür az sayıdaki uç vaka (6 adet) şartname Sayfa 5'te tanımlandığı üzere Gün 5–6'daki **Yol D (Elle Eşleme)** sürecine mi bırakılmalıdır, yoksa `src/normalize.py` içine sadece bilinen farmasötik birimleri (`iu`, `iu/ml`, `mg`, `mcg`) hedef alan kontrollü bir dozaj temizleme kuralı mı eklenmelidir?

