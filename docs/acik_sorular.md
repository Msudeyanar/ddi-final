# Açık Sorular, Çözülen Konular ve Mimari Tasarım Kararları

Bu doküman, proje geliştirme sürecinde (İP1–İP7) karşılaşılan veri kalitesi sorunlarını, çözüme kavuşturulan mimari kararları ve sonraki iş paketlerinde (İP5, İP6, web arayüzü ve makine öğrenmesi) yanıtlanması gereken açık soruları detaylandırmaktadır.

---

## 1. DDInter Veri Dengesizliği ve Eksik ATC Grupları (İP4 / İP6)
* **Durum:** DDInter indirme paketlerinde yalnızca 8 ana grup (A, B, D, H, L, P, R, V) bağımsız CSV olarak sunulmaktadır. Türkiye'de en çok reçetelenen Kardiyovasküler (C), Sinir Sistemi (N), Kas/İskelet (M) ve Antibiyotik (J) gibi 6 kritik grubun bağımsız indirme dosyası bulunmamaktadır.
* **Sayısal ve Analitik Boyut (D05 & D06):**
  - [Notebook 04, `926ce095` hücresi](../notebooks/04_ddinter_birlestirme.ipynb#cell-id=926ce095) kayıtlı çıktısında 1.418 DDInter eşleşmeli etken madde satırının 677’si (%47,74) bağımsız indirme dosyası olmayan ATC gruplarında. Bu 677 satırdan oluşturulabilen 228.826 çift, 1.004.653 olası çiftin %22,78’ine karşılık gelir. Hesap, olası çiftleri ATC grubuna göre sınıflandırır. İndirilen dosyalardaki gerçek etkileşim kapsamı çift bazında ayrıca kontrol edilir.
  - D05 ısı haritasında görüldüğü üzere, Kalp (C) ve Sinir (N) ilaçları diğer mevcut dosyalarla (C-L: 3.079 çift, L-N: 4.862 çift, A-C: 2.303 çift) güçlü çapraz köprüler kurmuştur.
  - Geriye kalan 775.827 olası çiftte en az bir bileşen indirme dosyası bulunan bir ATC grubunda.
* **Açık Soru ve Arayüz Tasarımı:** Kullanıcı reçetesinde iki ilaç da eksik grupta çıktığında, sistem kullanıcıyı yanıltarak *"Etkileşim Yok"* mu demelidir, yoksa *"Bu ilaç kombinasyonu DDInter indirme paketlerinde yer almayan C/N gruplarında olduğundan etkileşim verisi bulunamamaktadır (Veri Kısıtı)"* şeklinde şeffaf bir uyarı mı vermelidir?
* **Öneri:** Klinik güvenilirlik açısından şeffaf uyarı bayrağı (`veri_yetersiz_uyarisi = True`) dönülmesi zorunlu olmalıdır.

---

## 2. PubChem ile Kurtarılan Bileşenlerin Yol Sınıflandırması ve İzlenebilirlik (`ad_en_ham`) (İP3)
* **Durum:** Notebook 03’ün kayıtlı PubChem taramasında kapsam içi ilk 100 eşleşmeyen bileşenden 17’sine doğrudan DDInter kimliği atanmış ve aynı ham ada sahip 24 ek bileşen satırına eşleşme aktarılmıştır. [Notebook 03, PubChem hücresi](https://github.com/Msudeyanar/ddi-final/blob/main/notebooks/03_kopru_ddinter.ipynb#cell-id=3c300ca4)
* **Tasarım Çelişkisi:** PubChem eşleştirmesi doğrudan `ad_en` üzerine yazıldığında, Yol A'dan gelen resmi WHO ATC adı (örn. `paracetamol`) ezilmekte ve veri izlenebilirliği (traceability) kaybolmaktadır.
* **Çözüm / Güncel Durum (✅ Çözüldü):** 
  - Plandaki standart `yol` kategorileri (A, B, C, D, SKRS, eslesmedi) korunmuş; yeni bir 'PubChem' yolu icat edilmemiştir.
  - `etken_madde.csv` tablosuna `ad_en_ham` sütunu eklenerek ilk ATC adı dondurulmuş; `ad_en` sütununa DDInter karşılığı yazılmıştır.
  - Eşleşme kaynağı ise `eslesme_kaynagi` ('tam_ad', 'pubchem') sütununa kaydedilerek %100 veri izlenebilirliği sağlanmıştır.

---

## 3. Yol (A) Parantezli ATC Adları ve DDInter'da Bulunmayan 668 Bileşen (İP3 / İP6)
* **Durum:** Yol A'da resmi ATC sözlüğünden İngilizce karşılığı bulunan 1.887 bileşenin 668'i DDInter'da doğrudan bulunamamaktadır. Bunların önemli bir bölümü parantezli açıklama içeren moleküllerdir:
  - `ascorbic acid (vit c)` ➔ DDInter'da `ascorbic acid`
  - `calcium carbonate (calcium)` ➔ DDInter'da `calcium carbonate`
  - `pyridoxine (vit b6)` ➔ DDInter'da `pyridoxine`
  - `thiamine (vit b1)` ➔ DDInter'da `thiamine`
* **Kural:** Şartname gereğince kontrolsüz parantez budama regex'i işletilmemiş, bu durum açık soru olarak bırakılmıştır.
* **Açık Soru:** Parantez içindeki açıklamalar için `\s*\(.*?\)` regex'i Adım 2/3 normalizasyonuna resmi bir kural olarak eklenip yaklaşık 40–50 kritik vitamin ve mineral doğrudan kurtarılmalı mıdır, yoksa bu maddeler Kişi C'nin Yol D manuel eşleme sürecine mi bırakılmalıdır?
* **Öneri:** Parantez içini budayan kontrollü bir regex kuralı eklenmeli; orijinal ad `ad_en_ham` içinde saklanmalıdır.

---

## 4. Kural 6 ile SKRS'ten Tamamlanan Ruhsatlı Ürünler (İP1 / İP3)
* **Durum:** Ruhsatlı ürün listesinde ATC kodu boş olan 14 ürünün ATC bilgisi Kural 6 uyarınca SKRS tablosundan tamamlanmıştır. Bu ürünlerin `kaynak` değeri `Ruhsatlı` olarak kaldığından, `kaynak == 'SKRS'` filtresi bu 14 ürünü ayırmamakta ve izlenebilirlik kaybı riski doğurmaktaydı.
* **Çözüm / Güncel Durum (✅ Çözüldü):** 
  - `urun.csv` tablosuna `kural_6_skrs_tamamlandi` bayrak sütunu eklenmiştir.
  - İlgili 14 üründe bu bayrak `1`, diğer tüm ürünlerde `0` olarak işaretlenmiş; ruhsatlı ürün kaynağı bozulmadan SKRS tamamlaması izlenebilir kılınmıştır.

---

## 5. Kişi A Hücre 16 Assertion Kırılganlığı ve Pipeline Dayanıklılığı (İP1–İP3)
* **Durum:** Kişi A'nın Hücre 16'sında yer alan `assert len(df_etken_madde) == 3111`, `assert (df_etken_madde['yol'] == 'A').sum() == 1922` gibi sabit sayısal kontroller, TİTCK veya SKRS'ten yeni bir veri eklendiğinde pipeline'ın kırılmasına ve Kişi B hücrelerine ulaşılamamasına yol açmaktaydı.
* **Çözüm / Güncel Durum (✅ Çözüldü):** 
  - PR #20 kapsamında Adım 2 normalizasyonu konsolide edilmiş; veri boyutları 3.065 etken madde ve 32.076 satır olarak güncellenmiştir.
  - Assert kontrolleri güncel veri boyutlarıyla uyumlu hale getirilerek pipeline kırılganlığı giderilmiştir.

---

## 6. İP2 Ayrıştırma Sorunları (Dozaj ve Yüzde İbareleri) (İP2 / İP3)
* **Durum:** İlk taslakta `urun_etken.csv` içinde `% 20'lik insan albumini` gibi yüzde ibareli bileşenler ve `%25 insulin lispro / %75 insulin lispro protamin` gibi `/` ayırıcısı ile bölünmemiş kombine satırlar yer almaktaydı.
* **Yarattığı Sorun:** Bölünmeyen kombinasyonlar bağımsız birer etken madde sanılmakta ve DDInter ile eşleşememekteydi.
* **Çözüm / Güncel Durum (✅ Çözüldü):** 
  - Kişi A tarafından PR #20 kapsamında ayrıştırma regex'ine `/` bölücüsü entegre edilmiş ve yüzde ibareleri temizlenmiştir.
  - `urun_etken.csv` tablosunda `%` karakteri içeren satır sayısı **0'a indirilmiştir**.
  - `insulin lispro` başarıyla ayrılarak Yol A üzerinden `DDInter940` kimliğine bağlanmıştır.

---

## 7. Sözcük Düzeyinde Çeviri Kuralları (Tuz/Asit Eşlemeleri) (İP3)
* **Durum:** `hidroklorotiyazid` (379 ürün), `kalsiyum klorur` (409 ürün), `magnezyum klorur` (300 ürün), `sodyum laktat` (315 ürün) ve `klavulanik asit` (105 ürün) gibi Türkiye'de çok sık reçetelenen bileşenler İngilizce çevirisi olmadığı için `ceviri_yok` olarak kalmaktaydı.
* **Çözüm / Güncel Durum (✅ Çözüldü):** 
  - Kişi B tarafından `config/tr_en_kurallar.csv` kural motoruna tekil ilaç adı yazılmadan **38 jenerik morfolojik, fonetik ve kimyasal kural** (`kalsiyum → calcium`, `klorur → chloride`, `asit → acid` vb.) eklenmiştir.
  - Bu kurallarla kalsiyum klorur (`DDInter272`), hidroklorotiyazid (`DDInter883`), magnezyum klorur (`DDInter1114`) ve klavulanik asit (`DDInter394`) başarıyla Yol C kapsamında DDInter kimliklerine bağlanmıştır.

---

## 8. Tuz ve Ester Budama Adımı (Salt/Ester Stripping) (İP3)
* **Durum:** `olmesartan medoxomil` (`DDInter1330`) ve `tiotropium bromide` (`DDInter1815`) gibi bileşikler ATC sözlüğünde tuz/ester adıyla geçerken DDInter'da baz adıyla (`olmesartan`, `tiotropium`) yer almaktadır. Tepe moleküller PubChem ve Yol D ile kurtarılmıştır; ancak en sık 100 dışındaki tuzlu/esterli bileşikler (örn. `maleate`, `tartrate`, `hydrochloride`, `succinate`) DDInter baz adıyla eşleşememektedir.
* **Açık Soru:** İkinci bir genel tuz/ester budama kuralı (örn. `bromide`, `medoxomil`, `hydrochloride`, `sodium` kelimelerinin adın sonundan budanması) resmi kural motoruna eklenmeli midir?
* **Öneri:** Farmakolojik etkileşimler molekülün baz yapısı üzerinden yürüdüğünden, tuz/ester budama kuralının eklenmesi eşleşme oranını güvenli şekilde %2–3 artıracaktır.

---

## 9. ATC Grup Adı ile Gelen İlaçlar (`dekstroz`, `glukoz` → `carbohydrates`) (İP3 / İP4)
* **Durum:** Türkiye'de serum ve infüzyonlarda en çok kullanılan `dekstroz` (720 ürün) ve `glukoz` (180 ürün) için Yol A resmi ATC sözlüğünden `carbohydrates` adını getirmekteydi. `carbohydrates` bir ATC sınıf adıdır, tekil ilaç adı değildir ve DDInter'da bulunmaz. Bu durum 900 ürünlük devasa bir hasta hacminin etkileşim kontrolü dışı kalmasına yol açmaktaydı.
* **Çözüm / Güncel Durum (✅ Çözüldü - Kişi C Yol D Entegrasyonu):** 
  - Kişi C tarafından Yol D ilk 100 incelemesinde bu iki bileşen kaynakta düzeltilmiş; `dekstroz` ➔ `dextrose` ve `glukoz` ➔ `glucose` olarak `DDInter529` kimliğine bağlanmıştır.
  - Kapsama oranı ile ilgili proje hedefi için görev dağılımı ve kapsam kararına bakılır. İkinci hafta görev planında %70 kapsama eşiği belirtilmediği için bu değer şartname hedefi olarak kullanılmaz. [Kapsam kararı](kapsam_karari.md)

---

## 10. Deksketoprofen (Arveles) DDInter Durumu ve Kiral Türetme (İP4 / İP7)
* **Durum:** Türkiye'de en çok reçete edilen NSAİİ'lerden deksketoprofen (131 ürün), DDInter ilaç kataloğunda tekil etken madde olarak yer almamaktadır (`dexketoprofen` yok; DDInter'da sadece rasemat formu olan `ketoprofen` mevcuttur). Bu nedenle uçtan uca testlerde Arveles için tekil DDInter kaydı bulunamaması beklenen bir durumdur.
* **Açık Soru / Tasarım Kararı:** Deksketoprofen gibi yaygın kiral moleküller (enantiyomerler) için rasemat formu olan ketoprofen (`DDInter1009`) üzerinden klinik bir türetme kuralı uygulanarak etkileşimler miras alınmalı mıdır, yoksa tekil karşılığı olmadığı için 'DDInter'da Yok' statüsünde mi bırakılmalıdır?
* **Öneri:** Klinik pratikte deksketoprofen ile ketoprofenin ilaç etkileşim profili neredeyse özdeştir. Karar destek motorunda *"Deksketoprofen için ketoprofen etkileşim profili baz alınmıştır"* açıklamasıyla türetme kuralı uygulanabilir.

---

## 11. SKRS'te Bölünmemiş Kombinasyonlar ve Karakter Hataları (ı/i) (İP3)
* **Durum:** SKRS bileşenlerinde `other cold combınatıon preparatıons` gibi noktasız `ı` içeren Türkçe karakter hatası bulunan adlar ve `paracetamol, combinations excl. psycholeptics`, `calcium, combinations with vitamin d and/or other drugs` gibi bölünmemiş kombinasyon grupları yer almaktadır.
* **Açıklama:** SKRS eşleşme oranının %35,6'da kalmasının temel sebebi bu bölünmemiş kombinasyon gruplarıdır.
* **Açık Soru:** SKRS kaynaklı bu noktasız 'ı' karakter hataları ve bölünmemiş kombinasyonlar için Adım 2 normalizasyonuna otomatik bir karakter düzeltme ve kombinasyon ayıklama kuralı eklenmeli midir?

---

## 12. SKRS'te İlaç Adı Olmayan ATC Sınıf Adları ve Kapsam Kriterleri (İP3)
* **Durum:** `allergen extracts`, `tests for allergic diseases`, `peritoneal dialytics`, `antiseptics` gibi satırlar ATC sınıf adlarıdır (tekil molekül değildir). Bunların bir kısmı V06/V07 kuralı kapsamında elenirken; V01, V04, B05D gibi olanlar şartnamedeki kapsam dışı filtresinde tanımlanmadığı için kapsam içi sayılmaktadır.
* **Açık Soru:** Bu sınıf adları kapsam dışı (`kapsam_ici = 0`) filtresine dahil edilmeli midir? Eğer kapsam dışına alınırsa kapsam içi payda (2.945) küçülecek ve DDInter eşleşme oranı (%48,1'den yaklaşık %49,5'e) yükselecektir.
* **Öneri:** Bu satırlar tekil ilaç olmadığı ve etkileşim taramasına giremeyeceği için kapsam dışına alınmalıdır.

---

## 13. TEKNAZOL (ketokonazol) Hatalı ATC Kodu ve Ayrıştırma (İP1 / İP3)
* **Durum:** İlk taramalarda `DDInter1009` altında `['ketoprofen', 'ketokonazol']` şeklinde iki tamamen alakasız molekülün birleştiği görülmüştür. Antifungal olan `ketokonazol`, NSAİİ olan `ketoprofen` ile aynı DDInter ID'sini kapmıştır.
* **Kök Neden:** `urun.csv` dosyasında TEKNAZOL 200 MG TABLET ürünlerinin ATC kodunun sehven `M01AE03` (ketoprofen) girilmiş olmasıdır.
* **Çözüm / Güncel Durum (✅ Çözüldü):** 
  - `urun.csv` dosyasında TEKNAZOL ürünlerinin ATC kodu doğru karşılığı olan `J02AB02` (ketokonazol) olarak düzeltilmiştir.
  - `etken_madde.csv` tablosunda `ketokonazol` bağımsız olarak `DDInter1008` kimliğine bağlanmış; `ketoprofen` ise `DDInter1009`'da kalarak hatalı birleşme tamamen çözülmüştür.

---

## 14. TİTCK Ham Verisindeki Sözde Etken Maddeler (`combinations`, `various`) (İP1 / İP2)
* **Durum:** TİTCK Ruhsatlı listesinde bazı kombine ürünlerde `etkin_madde_ham` sütununa kimyasal madde adı yerine doğrudan WHO ATC kategori açıklamaları yazılmıştır (`"tiyokolşikosid, combinations"` ➔ 62 ürün, `"antiseptics, various"` ➔ 14 ürün, `"other cold preparations"` ➔ 47 ürün). Bu terimler virgülle ayrılarak `urun_etken.csv` içinde bağımsız birer etken madde gibi yer almaktaydı.
* **Çözüm / Güncel Durum (✅ Çözüldü):** 
  - Kişi A tarafından PR #20 kapsamında Adım 2 normalizasyonuna sıfat/kategori kara listesi (`plain`, `combinations`, `hemofiltrates` vb.) eklenmiştir.
  - Bu sözde maddeler elenerek `urun_etken.csv` 32.076 satıra ve etken madde sayısı 3.065'e konsolide edilmiştir.

---

## 15. Dozaj ve Birim Kalıntıları İçeren Bileşenler ve Yol D Kapsamı (İP2 / İP3)
* **Gözlem:** TİTCK ham tablosunda çok az sayıda (tam olarak 6 adet) etken madde metninin içine rakamsal doz ve birim yazılmıştır:
  - `vitamin a palmitat 20.000 iu/ml` (Barkodlu infüzyon ürünü)
  - `kolistimetat sodyum 4.500.000 iu` (Barkodlu flakon)
  - `etinilestradiol 0.02 mg`
  - `gestoden 0.075 mg`
  - `dekstran-70 1.0 mg hidroksipropil metil seluloz`
  - `b1 vitamini 25 mg, b2 vitamini 5 mg, b6 vitamini...`
* **Uygulanan Prensip:** `vitamin b1`, `interferon beta-1a` gibi meşru rakam veya tire içeren kimyasal/biyolojik adları bozmamak adına kontrolsüz bir sayı/birim silme regex'i uygulanmamıştır.
* **Açık Soru:** Bu 6 uç vaka Yol D manuel eşleme sürecine mi bırakılmalıdır, yoksa `src/normalize.py` içine sadece bilinen farmasötik birimleri (`iu`, `iu/ml`, `mg`, `mcg`) hedef alan kontrollü bir dozaj temizleme kuralı mı eklenmelidir?

---

## 16. Dexamethasone Tepe Hub Molekülü ve Klinik Alarm Yorgunluğu (İP4 / İP6)
* **Durum:** Ağ derecesi (degree) analizinde sistemik kortikosteroid olan Dexamethasone (`DDInter513`), **910 tekil partnerle** veri tabanının en merkez hub'ı çıkmıştır. Karaciğerde sitokrom P450 (CYP3A4) enzimlerinin güçlü indükleyicisi olması nedeniyle neredeyse tüm ilaç sınıflarıyla etkileşmektedir.
* **Açık Soru:** Bir hekim veya hasta reçetesinde Dexamethasone bulunduğunda, arayüzün 910 farklı etkileşim alarmı üreterek hekimde "alarm yorgunluğuna" (alert fatigue) yol açması nasıl engellenmelidir?
* **Öneri:** Arayüzde kademeli şiddet filtresi uygulanmalı; yalnızca Major (106 çift) alarmlar kırmızı zorunlu bildirim olarak açılmalı, Moderate (470 çift) alarmlar sarı bilgi kartı olarak sunulmalı, Minor (47 çift) alarmlar varsayılan olarak gizlenmelidir.

---

## 17. İki İlacı da Eksik Grupta Olan Çiftlerin Kapsamı (İP6 - D05 & D06)
* **Durum:** C, bağımsız indirme dosyası bulunmayan ATC gruplarından biridir. Olası çiftlerin %22,78’i için iki bileşen de bu gruplardadır. [Notebook 04, `926ce095` hücresi](../notebooks/04_ddinter_birlestirme.ipynb#cell-id=926ce095)
* **Açık Soru:** İki ilacı da eksik grupta olan bu kritik kardiyovasküler çiftlerin taranabilmesi için 3. haftada Kişi C'nin TDC DrugBank ve harici kaynak entegrasyonu mu devreye alınmalıdır?
* **Öneri:** Eksik ATC gruplarındaki öncelikli çiftlerin ek veri kaynaklarıyla eşlenebilirliğini ve kaynakların kapsama farkını ayrı değerlendirin.

---

## 18. Moderate ve Unknown Şiddet Düzeylerinin Kullanıcı Arayüzünde Gösterimi (İP4 / İP7)
* **Durum:** DDInter veri tabanındaki 160.235 tekil çiftin **%60,33'ü (96.675) Moderate**, **%18,61'i (29.813) Unknown** seviyesindedir. Minor düzeyi ise yalnızca %4,26'dır.
* **Açık Soru:** DDInter kaynaklarında şiddet seviyesi belirtilmemiş (Unknown) olan 29.813 çift arayüzde kullanıcıya nasıl yansıtılmalıdır?
* **Öneri:** Hekime yanlış güven vermemek veya panik yaratmamak adına "Etkileşim Var — Klinik Kanıt Düzeyi Belirsiz" şeklinde özel sarı/gri bir uyarı etiketiyle sunulmalı; hekime hastayı klinik olarak gözlemlemesi tavsiye edilmelidir.

---

## 16a. Tek Kaynaklı Ürünlerde Eski WHO ATC Kodu (Kişi A - Kural 8 Kapsamı Dışı)
* **Gözlem (Kişi A):** Güncellenmiş Kural 8 ile WHO kümülatif değişiklik listesinde yer alan çelişkili 167 ürün yeni koda çekilmiştir. Ancak SKRS'te karşılığı bulunmayan (`bos` sınıfı) 154 üründe `atc_final` hâlâ eski WHO kodunu taşımaktadır. Bu ürünlerin 89'u pregabalin (N03AX16), 16'sı gabapentin (N03AX12), geri kalanı fingolimod, barisitinib, sirolimus vb. etken maddelerdir.
* **Neden Dokunulmadı:** Güncellenmiş Kural 8 yalnızca iki kaynak arasında çelişki bulunan ürünleri kapsamaktadır. Bu 154 üründe bir çelişki (karşı tarafta kod) olmadığından kural devreye girmemektedir. Ayrıca Sabit Kural 1 ("Ürün adı, etkin madde ve ATC için Ruhsatlı Liste esas alınır") gereği ruhsatlı koddaki değişiklik için danışman onayı gerekmektedir.
* **Olası Etki:** Aynı etken madde (ör. pregabalin) veri setinde iki farklı ATC koduyla (N03AX16 ve N02BF02) görünmektedir. Bu durum ATC bazlı analizlerde (ör. ATC ana grubu dağılımı, Yol A eşleştirmesi) bölünmeye yol açabilir.
* **Karar / Soru:** WHO eşlemesi bu 154 tek kaynaklı ürüne de uygulanmalı mıdır, yoksa yalnızca çelişki kuralı kapsamında mı kalmalıdır?

---

## 17a. TİTCK ATC Kodlarındaki Karakter Hataları (CONTUBEL `DO3AX` ve Benzerleri) (Kişi A)
* **Gözlem (Kişi A):** TİTCK Ruhsatlı İlaçlar Listesinde az sayıda üründe ATC kodu karakter düzeyinde hatalı girilmiştir. Tespit edilen örnekler:
  - **CONTUBEL** (barkod `8699540019614`): ATC kodu `DO3AX` olarak girilmiş; sıfır (`0`) yerine İngilizce büyük harf `O` yazılmıştır. Doğru kod `D03AX` (other cicatrizants) olmalıdır.
  - Benzer potansiyel hatalar: `M02A A15` (fazla boşluk), `S03CA0L` (sıfır/L karışıklığı), `N06AX2I` (rakam/harf karışıklığı).
* **Mevcut Durum:** CONTUBEL şu anda `atc_final = DO3AX` ve `atc_celiski = 1` olarak işaretlidir. Güncellenmiş Kural 8 (WHO kümülatif değişiklik listesi) bu tür karakter hatalarını kapsamamaktadır çünkü `DO3AX` → `D03AX` bir WHO kod değişikliği değildir.
* **Olası Etki:** `DO3AX` geçerli bir ATC kodu olmadığı için bu ürün Yol A (ATC köprüsü) eşleştirmesine giremez ve ATC ana grubu dağılımında `D` grubu yerine sınıflandırma dışı kalır.
* **Karar / Soru:** Bu tür karakter hataları `src/normalize.py` veya Notebook 01'deki ATC temizleme adımına bir düzeltme regex'i eklenerek otomatik mi düzeltilmelidir (ör. `DO3AX` → `D03AX`), yoksa mevcut `atc_kaynak_hatasi_duzeltildi` mekanizması (TEKNAZOL örneğinde olduğu gibi) kullanılarak elle mi müdahale edilmelidir?
