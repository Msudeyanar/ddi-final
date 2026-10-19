# Açık Sorular ve Tartışma Konuları

## 1. DDInter Veri Dengesizliği ve Eksik ATC Grupları
* **Durum:** DDInter indirme dosyalarında yalnızca 8 ana grup (A, B, D, H, L, P, R, V) bulunmaktadır. Türkiye'de en çok reçete edilen C (Kardiyovasküler), N (Sinir Sistemi), M (Kas/İskelet) ve J (Antibiyotik) gibi grupların bağımsız indirme dosyaları bulunmamaktadır.
* **Soru:** İki ilacı da bu eksik gruplarda olan çiftlerin (örn. `C + C`, `M + J`) sistemde kapsanamaması kullanıcı senaryolarını ve proje kapsamını nasıl etkileyecek?
* **Detaylı Analiz:** [docs/ddinter_kayip_analizi.md](file:///Users/reyhanbuseyanar/Desktop/ddi-final/docs/ddinter_kayip_analizi.md) dosyasına eklendi.

## 2. PubChem ile Kurtarılan Bileşenlerin Yol Sınıflandırması ve İzlenebilirlik (`ad_en_ham`)
* **Durum:** En sık eşleşmeyen 100 kapsam içi bileşenden 14 tanesi (parasetamol, olmesartan, kolekalsiferol, glibenklamid, ipratropium vb.) PubChem API eş anlamlıları üzerinden DDInter kimliğine başarıyla bağlanmıştır.
* **Tasarım Kararı:** Plandaki `yol` kategorileri (A, B, C, D, SKRS, eslesmedi) sabit tutulmuş, yeni bir yol ('PubChem') icat edilmemiştir. Bunun yerine eşleşme kaynağını takip edebilmek adına `eslesme_kaynagi` sütunu ('tam_ad', 'pubchem') eklenmiştir.
* **İzlenebilirlik (Traceability):** PubChem eşleştirmesi `ad_en` üzerine yazdığı için, Yol A'dan gelen resmi ATC adı (örn. `paracetamol`) kaybolmaktadır. Bunu önlemek için `ad_en_ham` sütununda ilk çeviri dondurulmuş, `ad_en` sütununa ise DDInter ile eşleşen ad yazılmıştır.
* **Soru:** Ekip ve değerlendirme jürisi bu 14 bileşenin `yol` sütununda 'C' veya 'PubChem' olarak etiketlenmesini mi yoksa `eslesme_kaynagi` ayrımını mı tercih eder?

## 3. Yol A Parantezli ATC Adları ve DDInter'da Bulunmayan 725 Bileşen
* **Durum:** Yol A'da resmi ATC sözlüğünden İngilizce karşılığı bulunan 1.922 bileşenin 725'i DDInter'da doğrudan bulunamamaktadır (`ad_norm` birebir uyuşmamaktadır). Bunların bir kısmında parantezli açıklamalar (örn. `ascorbic acid (vit c)`, `calcium carbonate (calcium)`, `pyridoxine (vit b6)`, `thiamine (vit b1)`) yer almaktadır.
* **Kural:** Kişi A "parantez temizliği yapma, açık sorulara yaz" kuralını belirtmiştir. Parantez içindeki veya dışındaki kısmı ayrıştırarak ikincil eşleme denemek bir varsayımdır.
* **Soru:** Parantez temizliği yapılarak DDInter ile ek eşleme denensin mi, yoksa bu bileşenler Kişi C'nin Yol D taslağında `durum = 'ingilizce_var_ddinter_yok'` olarak manuel incelemeye mi bırakılsın?

## 4. Kural 6 ile SKRS'ten Tamamlanan Ruhsatlı Ürünler
* **Durum:** Ruhsatlı ürün listesinde ATC kodu boş olan 13 ürünün ATC bilgisi Kural 6 uyarınca SKRS tablosundan tamamlanmıştır. Ancak bu ürünlerin `kaynak` değeri `Ruhsatlı` olarak kaldığından, `kaynak == 'SKRS'` filtresi bu 13 ürünü ayırmamaktadır.
* **Soru:** Bu ürünlerin izlenebilirliği için `urun.csv` tablosuna `kural_6_skrs_tamamlandi = 1` şeklinde açık bir bayrak sütunu eklenmesi önerilir. Kişi A bu bayrağı eklemeli midir?

## 5. Kişi A Hücre 16 Assertion Kırılganlığı (Pipeline Risk Yönetimi)
* **Durum:** Kişi A'nın Hücre 16'sında yer alan `assert len(df_etken_madde) == 3111`, `assert (df_etken_madde['yol'] == 'A').sum() == 1922` gibi sabit sayısal kontroller, TİTCK veya SKRS'ten yeni bir veri indirildiğinde tüm pipeline'ın kırılmasına ve Kişi B hücrelerine ulaşılamamasına yol açacaktır.
* **Öneri:** Bu assertion'ların katı eşitlik (`== 3111`) yerine aralık kontrollerine (`assert len(...) >= 3000`) dönüştürülmesi önerilir.

## 6. İP2 Ayrıştırma Sorunları (Kişi A & B Geri Bildirimi)
* **Durum:** `urun_etken.csv` içinde `% 20'lik insan albumini` gibi yüzde/doz ibareli bileşenler ve `%25 insulin lispro / %75 insulin lispro protamin` gibi `/` ayırıcısı ile bölünmemiş kombine satırlar bulunmaktadır.
* **Etki:** Planda `/` ve `,` ayırıcıları tanımlanmıştır; bu satırların tek parça kalması hem tekil etken madde sayısını (3.111) hem de DDInter eşleşme oranlarını doğrudan etkilemektedir.
* **Öneri:** İP2 etken madde ayrıştırma fonksiyonunun regex kurallarına `/` bölücüsünün zorunlu kılınması ve yüzde ibarelerinin temizlenmesi önerilir.

## 7. Sözcük Düzeyinde Çeviri Kuralları (Tuz/Asit Eşlemeleri)
* **Durum:** `hidroklorotiyazid` (379 ürün), `kalsiyum klorur` (400 ürün), `magnezyum klorur` (293 ürün), `sodyum laktat` (315 ürün) ve `klavulanik asit` (105 ürün) gibi çok sık reçete edilen bileşenler `ceviri_yok` olarak kalmaktadır. Bunlar `kalsiyum → calcium`, `klorur → chloride`, `asit → acid` gibi sözcük düzeyinde çevirilerle çözülebilir.
* **Soru:** Plandaki 3 temel kural tipine (sonek, harf, doğrudan) sözcük düzeyinde kural eklemek mimari bir sapma mıdır? Bu bileşenler Yol D'de Kişi C'nin manuel eşlemesine mi bırakılmalı yoksa Yol C motoruna sözcük çevirisi eklenmeli midir?

## 8. Tuz ve Ester Budama Adımı (Salt/Ester Stripping)
* **Durum:** `olmesartan` (`olmesartan medoxomil`) ve `tiotropium` (`tiotropium bromide`) gibi bileşikler ATC sözlüğünde tuz/ester adıyla geçerken DDInter'da baz adıyla yer almaktadır. PubChem en sık 100 taraması ile bu iki bileşeni kurtarmıştır; ancak en sık 100 dışındaki tuzlu/esterli bileşikler eşleşmemektedir.
* **Soru:** İkinci bir tuz/ester temizleme kuralı (örn. `bromide`, `medoxomil`, `hydrochloride` kelimelerini budama) resmi pipeline kuralı olarak eklenmeli midir?

## 9. ATC Grup Adı ile Gelen İlaçlar (`dekstroz`, `glukoz` → `carbohydrates`)
* **Durum:** `dekstroz` (720 ürün) ve `glukoz` (177 ürün) için Yol A resmi ATC sözlüğünden `carbohydrates` adını getirmektedir. `carbohydrates` bir ATC grup adıdır, tekil ilaç adı değildir ve DDInter'da bulunmaz.
* **Öneri:** Kişi C'nin Yol D tablosunda bu iki bileşeni elle `dextrose` ve `glucose` olarak DDInter kimliklerine eşlemesi gerekmektedir.

## 10. Deksketoprofen (Arveles) DDInter Durumu
* **Durum:** Türkiye'de en çok reçete edilen NSAİİ'lerden deksketoprofen (131 ürün), DDInter ilaç kataloğunda tekil etken madde olarak yer almamaktadır (`dexketoprofen` yok, DDInter etkileşim tablosunda kombinasyon olarak geçmektedir). Bu nedenle uçtan uca testlerde Arveles için tekil DDInter kaydı bulunamaması beklenen bir durumdur.

## 11. SKRS'te Bölünmemiş Kombinasyonlar ve Karakter Hataları (ı/i)
* **Durum:** SKRS bileşenlerinde `other cold combınatıon preparatıons` gibi noktasız `ı` içeren Türkçe karakter hatası bulunan adlar ve `paracetamol, combinations excl. psycholeptics`, `calcium, combinations with vitamin d and/or other drugs` gibi bölünmemiş kombinasyon grupları yer almaktadır.
* **Açıklama:** SKRS eşleşme oranının %35.6'da kalmasının temel sebebi aşılar ve bu bölünmemiş kombinasyon gruplarıdır. Bunların tekilleştirilmesi için Kişi A'nın tokenization adımında revizyon gerekebilir.

## 12. SKRS'te İlaç Adı Olmayan ATC Sınıf Adları ve Kapsam Durumu
* **Durum:** `allergen extracts`, `tests for allergic diseases`, `peritoneal dialytics`, `antiseptics` gibi satırlar ATC sınıf adlarıdır (tekil molekül adı değildir). Bunların bir kısmı V06/V07 kuralı kapsamında elenirken; V01, V04, B05D gibi olanlar kapsam dışı kuralında tanımlanmadığı için kapsam içi sayılmaktadır.
* **Karar/Soru:** Bu satırların kapsam dışı filtresine dahil edilip edilmeyeceği bir tasarım kararıdır. Tahmin yürütülmeden açık soru olarak kaydedilmiştir; eğer kapsam dışına alınırsa kapsam içi payda küçülecek ve eşleşme oranı artacaktır.

## 13. TEKNAZOL (ketokonazol) Hatalı ATC Kodu ve DDInter Yanlış Birleşmesi
* **Durum:** Tekil DDInter ID denetiminde `DDInter1009` altında `['ketoprofen', 'ketokonazol', 'ketoprofen mikropelle']` eşleştiği görülmüştür. Antifungal olan `ketokonazol`, NSAİİ olan `ketoprofen` ile aynı DDInter ID'sine bağlanmıştır.
* **Kök Neden:** `urun.csv` dosyasında 19719-19721 indeksli TEKNAZOL 200 MG TABLET ürünlerinin ATC kodunun `M01AE03` (ketoprofen) girilmiş olmasıdır. Bu ürünler en sık frekansı oluşturduğu için Kişi A'nın Yol A adımında `ketokonazol` bileşenine `M01AE03` atanmış ve SKRS ATC sözlüğünden `ketoprofen` çekilmiştir.
* **Öneri:** Bu durum Kişi A'ya bildirilmelidir; `urun.csv` / TİTCK kaynak temizliğinde TEKNAZOL ürünlerinin ATC kodu `J02AB02` olarak düzeltilmelidir.

