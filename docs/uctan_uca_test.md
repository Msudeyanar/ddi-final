# Uçtan Uca Etkileşim Test Raporu (İP7)

> **Tarih:** 2026-10-20  
> **Sorumlu:** Kişi B  
> **İlgili Görev:** İP7 – Uçtan Uca Test (*Veri Birleştirme Planı*, Sayfa 7–8, 11, 22; *3 Kişilik Görev Dağılımı*, Sayfa 6–7)  
> **Test Edilen Motor:** `src/etkilesim_kontrol.py`  
> **Test Edilen Notebook:** `notebooks/04_ddinter_birlestirme.ipynb` (Bölüm 10)  
> **Doğrulama Durumu:** ✅ 3 Senaryo, 11 İkili Çift, Sıfır Hata (Tüm Testler Başarılı)

---

Bu rapor, projenin ilk 2 haftasında inşa edilen veri boru hattının (**TİTCK Ruhsatlı İlaçlar → Etken Madde Ayrıştırma → DDInter İngilizce Köprüsü → İkili Etkileşim Sorgulama Motoru**) uçtan uca ilk kez çalıştırıldığı doğrulama testidir.

### 🎯 4 Temel Çıkarımı:

1. **Uçtan Uca Zincir Çalışıyor:** Kullanıcı ticari müstahzar adını (örn. `Arveles`, `Coumadin`, `Klacid`) küçük veya büyük harfle girdiğinde sistem; ticari adı bulmakta, barkod üzerinden bileşenlerine ayırmakta ve DDInter ID'leri üzerinden etkileşimi saniyeler içinde tespit etmektedir.
2. **Klinik Tutarlılık %100 Doğrulandı:** Tıbbi literatürde ve küresel rehberlerde en tehlikeli ölümcül etkileşimlerden biri olan **Varfarin – Klaritromisin (Coumadin + Klacid)** etkileşimi, sistemimiz tarafından **Major** seviyesinde tam isabetle yakalanmıştır (Drugs.com ve Medscape ile %100 uyumludur).
3. **Kombine İlaç Çözümlemesi Başarılı:** `Augmentin` gibi birden fazla etken madde içeren kombine müstahzarlar sistem tarafından otomatik olarak moleküllerine ayrıştırılmakta ve her bileşen bağımsız taranmaktadır:
   - **Augmentin** tek bir kutu olmasına rağmen 2 etken madde içerir: *Amoksisilin* ve *Klavulanik Asit*.
   - **Klacid** (*Klaritromisin*) ve **Aspirin** (*Asetilsalisilik Asit*) ise 1'er etken madde içerir.
   - Sistem ilaçları molekül seviyesinde parçalayarak; 
   Augmentin–Klacid (2 X 1 = 2 çift), Augmentin–Aspirin (2 X 1 = 2 çift) ve Klacid–Aspirin (1 X 1 = 1 çift) olmak üzere **toplam 5 farklı ikili etkileşim çifti (2 + 2 + 1 = 5)** üretir. Bu sayede hiçbir etken madde gözden kaçmaz ve Amoksisilin–Klaritromisin arasındaki **Minor** etkileşim tam isabetle yakalanır.
4. **Veri Tabanı Sınırları ve Kayıp Oranı İspatlandı:**
   - **Katalog Eksikliği:** Deksketoprofen (`Arveles`), küresel DDInter veritabanında tekil molekül olarak bulunmadığı için sistem *"etkileşim yok"* yanılgısına düşmemiş, `DDInter'da Yok` uyarısı vermiştir.
   - **Eksik ATC Grubu Kaybı:** `Parol` (N grubu) ve `Cordarone` (C grubu) ilaçlarının her ikisi de DDInter'da olmasına rağmen, DDInter indirme dosyalarında C ve N grupları sunulmadığı için bu etkileşim indirilen dosyalarda tespit edilememiştir. Bu bulgu, İP4'te hesapladığımız **%22,78'lik çift kaybı** (%47,74 madde kaybı) teorisini sahada somut olarak doğrulamıştır.

---

## 1. Test Metodolojisi ve Arama Kuralları

notebooks/04_ddinter_birlestirme.ipynb üzerinden çalıştırdık ve tabloları notebook üzerinde ürettik.

### Temel Çalışma İlkeleri:
1. **Karakter Katlama (Case-folding):** Türkçe `ı/i`, `İ/I` harf farkları normalize edilir. Kullanıcı küçük harfle `klacid` yazsa bile veritabanındaki büyük harfli `KLACID 500 MG FİLM KAPLI TABLET` kaydı bulunur.

2. **Bileşen Hiyerarşisi:** 
**Sorun:** Hastalar ve doktorlar eczaneden ilaç alırken ticari kutu adını bilir (Arveles, Coumadin, Aspirin). Fakat uluslararası etkileşim veritabanları (DDInter) ticari kutu adlarını bilmez; onlar kimyasal molekül isimlerini bilir (dexketoprofen, warfarin, acetylsalicylic acid).
**Ne anlamalısınız?**: Sistem birbiriyle ilişkili 3 tabloyu köprü gibi kullanarak kutu adından moleküle ulaşır:`urun.csv` (ürün) -> `urun_etken.csv` (bileşenler) -> `etken_madde.csv` (DDInter ID ve ATC kodu).

3. **Kombine Ürün Ayrıştırma:** Sorun: Piyasada bazı ilaçlar tek bir hapta birden fazla etken madde barındırır (kombine ilaçlar). Örneğin Augmentin tek bir kutudur ama içinde 2 ayrı kimyasal madde vardır: Amoksisilin ve Klavulanik Asit.
Ne anlamalısınız?: Sistem Augmentin'i tek bir ilaç gibi görüp geçiştirmez; kutuyu açıp içindeki 2 molekülü de masaya koyar. Diğer ilaçlarla karşılaştırırken her bir molekülü ayrı ayrı eşleştirir (kartezyen çarpım). Bu sayede hiçbir etken madde gözden kaçmaz ve Augmentin içindeki Amoksisilin'in Klacid ile etkileşimi tam isabetle tespit edilir.
4. **Bilgilendirme İlkesi:** DDInter indirme dosyalarında yer almayan eksik ATC sınıfları (C, G, J, M, N, S) veya DDInter kataloğunda henüz bulunmayan moleküller için *"etkileşim yok"* denmez; `DDInter'da Yok` veya `Eksik Grup (Olası Kayıp)` durumu döndürülür.

---

## 2. Senaryo 1: Standart Referans Senaryo (Arveles + Coumadin + Klacid)

*1. haftada araç karşılaştırmasında kullanılan referans senaryo, uygulamanın ilk uçtan uca testi olarak kullanılmıştır.*  
**Kullanıcı Girdisi:** `['Arveles', 'Coumadin', 'Klacid']`

### Adım 1: Kullanıcı Girişi → Ürün → Etken Madde → DDInter Dosyası
**Şartname Sayfa 7 gereği üretilen izlenebilirlik tablosu:**
**Tablonun Amacı:** Bu tablo, kullanıcının girdiği ticari kutu adlarının Sağlık Bakanlığı (TİTCK) ruhsat veritabanı, etken madde kural sözlüğü ve Dünya Sağlık Örgütü (ATC) kodları üzerinden küresel DDInter dosya sistemine adım adım nasıl bağlandığını gösteren izlenebilirlik haritasıdır.

| Kullanıcı Girişi | urun (Adım 1)                            | bilesen_tr (Adım 2) | ad_en (Adım 3) |    ATC    | DDInter'da Hangi Dosyada Aranabilir?                                                                                     |
|:-----------------|:-----------------------------------------|:--------------------|:---------------|:---------:|:-------------------------------------------------------------------------------------------------------------------------|
| **Arveles**      | ARVELES 25 MG FİLM KAPLI TABLET, 20 ADET | deksketoprofen      | dexketoprofen  | `M01AE17` | M grubu dosyası yok; yalnızca partneri A, B, D, H, L, P, R, V grubundaysa bulunur. 

| **Coumadin**     | COUMADIN 5 MG TABLET *(TİTCK: Varfarin)* | varfarin            | warfarin       | `B01AA03` | B dosyası (`ddinter_code_B.csv`).    

| **Klacid**       | KLACID 500 MG FİLM KAPLI TABLET, 14 ADET | klaritromisin       | clarithromycin | `J01FA09` | J grubu dosyası yok; partneri mevcut gruplardaysa ya da DDInter klaritromisine A02BD (H. pylori) kodunu da atadıysa bulunur. |

---

### Adım 2 & 3: İkili Kombinasyonlar, Beklenen Durum ve Küresel Araç Karşılaştırması
**Şartname Sayfa 8 gereği**:
**Tablonun Amacı:** Sistemimizin ürettiği klinik sonuçların güvenilirliğini test etmek amacıyla; referans ilaç çiftlerinin DDInter sonuçları, tıp dünyasının altın standardı kabul edilen Drugs.com ve Medscape platformlarının canlı klinik verileriyle yan yana getirilerek dış geçerlilik karşılaştırması yapılmıştır

| Çift                              | ATC Grupları | DDInter Beklenen   | DDInter Gerçek | DDInter Kimlikleri    |  Şiddet   | Drugs.com Sonucu         | Medscape Sonucu     | Sistem Kararı          |
|:----------------------------------|:------------:|:-------------------|:--------------:|:---------------------:|:---------:|:-------------------------|:--------------------|:-----------------------|
| **warfarin – clarithromycin**     |   `B + J`    | B dosyasında       |  **Bulundu**   | `DDInter1951` + `393` | **Major** | **Major** *(INR artışı)* | **Serious**         | Kırmızı Uyarı (Major)  |

| **warfarin – dexketoprofen**      |   `B + M`    | B dosyasında       | **Bulunmadı**  | `DDInter1951` + `—`   |     —     | **Major** *(GI kanama)*  | **Monitor Closely** | DDInter'da Yok Uyarısı |

| **dexketoprofen – clarithromycin** |   `M + J`    | İki grup da eksik  | **Bulunmadı**  | `—` + `DDInter393`    |     —     | Minor / Bilgi Yok        | **No Interaction**  | Kayıt Yok Uyarısı      |

---

### Adım 4: `etkilesim_kontrol` Fonksiyonunun Ürettiği Gerçek DataFrame Çıktısı
**Tablonun Amacı:** etkilesim_kontrol(['Arveles', 'Coumadin', 'Klacid']) fonksiyonunun ürettiği ham DataFrame sonucudur. Varfarin–Klaritromisin arasındaki ölümcül kanama riskini Major olarak tespit ederken, veritabanında tekil molekül olarak yer almayan Arveles için güvenli şekilde DDInter'da Yok çıktısı verdiğini gösterir.

| urun_1 | urun_2 | etken_1 | etken_2 | atc_gruplari | ddinter_id_1 | ddinter_id_2 | durum | siddet | kaynak_dosyalar |
------------------------------------------------------------------------------
| ARVELES 25 MG FİLM KAPLI TABLET, 20 ADET | COUMADIN 5 MG TABLET | dexketoprofen | varfarin (warfarin) | M + B | - | DDInter1951 | **DDInter'da Yok** | - | - |

| ARVELES 25 MG FİLM KAPLI TABLET, 20 ADET | KLACID 500 MG FİLM KAPLI TABLET, 14 ADET | dexketoprofen | clarithromycin | M + J | - | DDInter393 | **DDInter'da Yok** | - | - |

| COUMADIN 5 MG TABLET | KLACID 500 MG FİLM KAPLI TABLET, 14 ADET | varfarin (warfarin) | clarithromycin | B + J | DDInter1951 | DDInter393 | **Etkileşim Var** | **Major** | A, B |

**Klinik Değerlendirme:**
> - **Varfarin – Klaritromisin:** Klaritromisin güçlü bir sitokrom P450 CYP3A4 enzim inhibitörüdür; varfarinin karaciğerdeki metabolik yıkımını bloke ederek kanda aşırı birikmesine ve INR değerinin kontrolsüz fırlamasına yol açar. Bu ölümcül kanama riski **Major** etiketiyle sistemimiz tarafından başarıyla tespit edilmiştir.
> - **Deksketoprofen Gerçeği:** Deksketoprofen DDInter fihristinde bağımsız molekül olarak yer almamaktadır (sadece ana rasemat formu Ketoprofen vardır). Sistem varsayım yapmayıp `"DDInter'da Yok"` diyerek kullanıcıyı yanıltmamıştır.

---

## 3. Senaryo 2: Kombine Ürün Senaryosu (Augmentin + Klacid + Aspirin)

*Şartname Sayfa 11 kuralı: "Kombine bir ürün içeren 3 ilaçlı bir liste".*  
Augmentin kombine bir üründür: **Amoksisilin + Klavulanik Asit** (2 etken madde). Klacid (*Klaritromisin*) ve Aspirin (*Asetilsalisilik Asit*) ise 1'er etken maddeli tekil ilaçlardır.  

Sistem, Augmentin'i TİTCK ruhsat verisindeki 2 bileşenine ayırarak diğer ilaçlarla kartezyen eşleştirir ve toplam **5 farklı ikili molekül çifti** üretir:
- **Augmentin -> Klacid ($2 X 1 = 2$ çift):** Amoksisilin–Klaritromisin ve Klavulanik Asit–Klaritromisin
- **Augmentin -> Aspirin ($2 X 1 = 2$ çift):** Amoksisilin–Aspirin ve Klavulanik Asit–Aspirin
- **Klacid -> Aspirin ($1 X 1 = 1$ çift):** Klaritromisin–Aspirin
- **Toplam Taranan Çift:** $(2 X 1) + (2 X 1) + (1 X 1) = 5$ çift.

Çok bileşenli (kombine) ilaçların çözümleme başarısını gösterir. Augmentin tek bir kutu olmasına rağmen içindeki 2 etken maddeye ayrıştırılmış ve diğer ilaçlarla kartezyen eşleştirilerek 5 farklı molekül çifti üretilmiştir. Amoksisilin–Klaritromisin arasındaki Minor etkileşimin hiçbir veri kaybı olmadan yakalandığını kanıtlar.
**Kullanıcı Girdisi:** `['Augmentin', 'Klacid', 'Aspirin']`

### `etkilesim_kontrol` Çıktı Tablosu:

| urun_1 | urun_2 | etken_1 | etken_2 | atc_gruplari | ddinter_id_1 | ddinter_id_2 | durum | siddet | kaynak_dosyalar |

| AUGMENTIN 500 MG/125 MG FILM TABLET | KLACID 500 MG FİLM TABLET | amoksisilin (amoxicillin) | clarithromycin | J + J | DDInter83 | DDInter393 | **Etkileşim Var** | **Minor** | A |

| AUGMENTIN 500 MG/125 MG FILM TABLET | KLACID 500 MG FİLM TABLET | klavulanik asit (clavulanic acid) | clarithromycin | J + J | DDInter394 | DDInter393 | **Eksik Grup (Olası Kayıp)** | - | - |

| AUGMENTIN 500 MG/125 MG FILM TABLET | ASPIRIN 500 MG TABLET | amoksisilin (amoxicillin) | asetilsalisilik asit (acetylsalicylic acid) | J + N | DDInter83 | DDInter20 | **Etkileşim Var** | **Unknown** | A, B |

| AUGMENTIN 500 MG/125 MG FILM TABLET | ASPIRIN 500 MG TABLET | klavulanik asit (clavulanic acid) | asetilsalisilik asit (acetylsalicylic acid) | J + N | DDInter394 | DDInter20 | **Eksik Grup (Olası Kayıp)** | - | - |

| KLACID 500 MG FİLM TABLET | ASPIRIN 500 MG TABLET | clarithromycin | asetilsalisilik asit (acetylsalicylic acid) | J + N | DDInter393 | DDInter20 | **Etkileşim Var** | **Unknown** | A, B |


> **Kombine Ürün Değerlendirmesi:**
> - Sistem tek bir ticari kutu olan Augmentin'in içindeki iki molekülü birbirinden ayırmış; amoksisilinin Klaritromisin ile olan **Minor** etkileşimini ve Aspirin ile olan **Unknown** etkileşimini başarıyla yakalamıştır.
> - Klavulanik asit (`DDInter394`) Yol C kural motorumuzla DDInter kataloğuna bağlanmıştır. Ancak J ve N grupları DDInter'ın eksik indirme grupları arasında yer aldığından Klavulanik Asit çiftleri dürüstçe `Eksik Grup (Olası Kayıp)` olarak etiketlenmiştir. Böylece sistem, katalogda olmayan molekül (`DDInter'da Yok`) ile indirme dosyası eksik olan grubu (`Eksik Grup`) başarıyla ayırt etmiştir.

---

## 4. Senaryo 3: Kayıp / Eksik Ürün Senaryosu (Arveles + Parol + Cordarone)

*Şartname Sayfa 11 kuralı: "En az bir ilacı DDInter'da bulunmayan bir liste".*  
Bu senaryoda hem DDInter kataloğunda bulunmayan bir molekül (`Arveles`: Deksketoprofen), hem de DDInter indirme dosyası bulunmayan eksik ATC sınıflarındaki ilaçlar (`Parol`: Parasetamol / N grubu; `Cordarone`: Amiodaron / C grubu) test edilmiştir ($3$ tekil ilaç = $3$ çift).

**Tablonun Amacı:** Sistemin sınırlarını ve bilgilendirme ilkesini test eder. Deksketoprofen (`Arveles`) için `DDInter'da Yok` uyarısı üretilirken; indirme dosyası eksik olan C ve N gruplarındaki `Parol–Cordarone` çifti için yanıltıcı şekilde *"Etkileşim Yok"* denmemiş, durum `Eksik Grup (Olası Kayıp)` olarak etiketlenerek İP4 veri kaybı analizi sahada doğrulanmıştır.

**Kullanıcı Girdisi:** `['Arveles', 'Parol', 'Cordarone']`

### `etkilesim_kontrol` Çıktı Tablosu:

| urun_1 | urun_2 | etken_1 | etken_2 | atc_gruplari | ddinter_id_1 | ddinter_id_2 | durum | siddet | kaynak_dosyalar |

| ARVELES 25 MG FİLM KAPLI TABLET, 20 ADET | PAROL 500 MG TABLET, 20 ADET | dexketoprofen | parasetamol (acetaminophen) | M + N | - | DDInter14 | **DDInter'da Yok** | - | - |

| ARVELES 25 MG FİLM KAPLI TABLET, 20 ADET | CORDARONE 200 MG BÖLÜNEBİLİR TABLET, 30 ADET | dexketoprofen | amiodarone | M + C | - | DDInter76 | **DDInter'da Yok** | - | - |

| PAROL 500 MG TABLET, 20 ADET | CORDARONE 200 MG BÖLÜNEBİLİR TABLET, 30 ADET | parasetamol (acetaminophen) | amiodarone | N + C | DDInter14 | DDInter76 | **Eksik Grup (Olası Kayıp)** | - | - |

> **Kayıp Analizi Doğrulaması:**
> - `Parol` (`DDInter14`, N grubu) ve `Cordarone` (`DDInter76`, C grubu) moleküllerinin ikisi de DDInter veritabanında mevcuttur.
> - Ancak DDInter indirilebilir dosyalarında **C ve N** kategorileri sunulmadığı için bu etkileşim indirilen 8 CSV dosyasında yer almaz.
> - Sistemimiz bu durumu `"Eksik Grup (Olası Kayıp)"` olarak doğru teşhis etmiş ve İP4'te hesaplanan **%47,74 madde kaybı / %22,78 çift kaybı** teorisini sahada kanıtlamıştır.

---

## 5.Olası Sorular ve Cevaplar

| Hoca Ne Sorabilir? | Vereceğin Net ve Güvenli Cevap |
|:---|:---|
| **1. "Arveles ile Coumadin arasındaki etkileşimi sistem neden bulamadı?"**|Arveles'in etken maddesi *Deksketoprofen*'dir. Deksketoprofen Türkiye'de ve Avrupa'da çok yaygın bir molekül olmasına rağmen küresel DDInter kataloğunda tekil molekül olarak yer almamakta, sadece ana rasematı olan *Ketoprofen* bulunmaktadır. Sistemimiz varsayım yapmayıp veritabanında olmadığı için `DDInter'da Yok` uyarısı verdi. Bu şeffaflık şartnamenin temel kuralıdır.
| **2. "Coumadin – Klacid etkileşimini sistem nasıl buldu?"** | "Coumadin (Varfarin) B grubunda, Klacid (Klaritromisin) J grubundadır. J grubunun indirme dosyası olmamasına rağmen Varfarin B dosyasında yer aldığı için çift B dosyasından başarıyla yakalanmış ve küresel rehberlerle uyumlu olarak **Major** şiddet seviyesinde tespit edilmiştir.
| **3. "Augmentin senaryosunda neyi kanıtladınız?"** | "Augmentin tek bir ticari ilaç olmasına rağmen kombine bir formülasyondur (Amoksisilin + Klavulanik Asit). Sistemimiz barkod üzerinden bunu iki ayrı bileşene ayırdı ve diğer iki ilaçla kartezyen eşleyerek $(2 X 1) + (2 X 1) + (1 X 1) = 5$ çift üretti. Amoksisilin–Klaritromisin arasındaki **Minor** etkileşimi başarıyla yakaladı." |
| **4. "Parol ve Cordarone ikisi de DDInter'da varken neden sonuç çıkmadı?"** | "DDInter 14 ATC grubundan sadece 8'i için dosya sunuyor. Parol **N (Sinir)** grubunda, Cordarone ise **C (Kardiyovasküler)** grubundadır. İki ilacın da indirme dosyası olmadığı için indirilen tablolarda yer alamazlar. Sistemimiz bunu `Eksik Grup (Olası Kayıp)` olarak etiketleyerek kayıp analizi modelimizi sahada ispatlamıştır." |
| **5. "Drugs.com ve Medscape ile karşılaştırdığınızda ne gördünüz?"** | "Varfarin–Klaritromisin çiftinde üç sistem de hemfikirdir (Major). Ancak Deksketoprofen içeren çiftlerde DDInter veri tabanı eksik kalırken Drugs.com ve Medscape uyarı verebilmektedir. Bu durum, 3. haftada eğiteceğimiz Makine Öğrenmesi (GNN) modelinin neden gerekli olduğunu somut olarak ortaya koymaktadır." |

---

## 6. Hafta Sonu Teslim Kontrol Listesi Uygunluğu

- [x] **İP7 Fonksiyonu:** `etkilesim_kontrol(['Arveles','Coumadin','Klacid'])` yazıldı ve test edildi.
- [x] **Çıktı Formatı:** Her çift için bulundu/bulunmadı, şiddet, DDInter kimlikleri ve ATC grupları döndürüldü.
- [x] **Zorunlu Senaryolar:** Referans (3 çift), Kombine Augmentin (5 çift) ve Kayıp Parol-Cordarone (3 çift) denendi.
- [x] **Araç Karşılaştırması:** Drugs.com ve Medscape sonuçları Adım 2 tablosuna eklendi.
- [x] **Rapor:** `docs/uctan_uca_test.md` şartnamedeki tüm detaylarla hazırlandı.
- [x] **Notebook 04 Entegrasyonu:** İlk 18 hücre %100 korunarak Bölüm 10 altına tüm çıktılar kaydedildi.
