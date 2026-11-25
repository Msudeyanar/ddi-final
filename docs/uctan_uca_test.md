# Uçtan Uca Etkileşim Test Raporu (İP7)

> **Tarih:** 2026-10-20 (Güncelleme: 2026-11-19)  
> **Sorumlu:** Kişi B  
> **İlgili Görev:** İP7 – Uçtan Uca Test (*Veri Birleştirme Planı*, Sayfa 7–8, 11, 22; *3 Kişilik Görev Dağılımı*, Sayfa 6–7)  
> **Test Edilen Motor:** `src/etkilesim_kontrol.py`  
> **Test Edilen Notebook:** `notebooks/04_ddinter_birlestirme.ipynb` (Bölüm 10, NB04 Hücre [10]–[15])  
> **Doğrulama Durumu:** ✅ Zorunlu Senaryolar, 14 İkili Çift, Sıfır Hata (Tüm Testler Başarılı - [NB04 In [13]](../notebooks/04_ddinter_birlestirme.ipynb#cell-id=f7e3f999))

---

Bu rapor, projenin ilk 2 haftasında inşa edilen veri boru hattının (**TİTCK Ruhsatlı İlaçlar → Etken Madde Ayrıştırma → DDInter İngilizce Köprüsü → İkili Etkileşim Sorgulama Motoru**) uçtan uca ilk kez çalıştırıldığı doğrulama testidir.

### 🎯 4 Temel Çıkarım:

1. **Uçtan Uca Zincir Çalışıyor:** Kullanıcı ticari müstahzar adını (örn. `Arveles`, `Klacid`, `Warfmadin`, `Augmentin`) küçük veya büyük harfle girdiğinde sistem; ticari adı bulmakta, barkod üzerinden bileşenlerine ayırmakta ve DDInter ID'leri üzerinden etkileşimi saniyeler içinde tespit etmektedir (NB04 Hücre [10]–[15]).
2. **Klinik Araçlar Şiddet Konusunda Anlaşmıyor (Önemli Bulgu):** Tıbbi literatürde ölümcül kabul edilen **Varfarin – Klaritromisin** etkileşimi, taranan küresel araçlarda farklı şiddet seviyelerinde etiketlenmiştir (NB04 Hücre [12]):
   - **DDInter:** Major (Dosya A, B - NB04 Hücre [5] ve [12])
   - **Drugs.com:** Major (INR artışı ve kanama riski — [Şekil 7](../images/sekil07.png))
   - **Medscape:** Önemli – Yakından Takip Edin (*Serious – Monitor Closely* — [Şekil 14](../images/sekil14.png))
   - **WebMD:** Yakından takip edin (*Monitor Closely* — [Şekil 20](../images/sekil20.png))  
   Bu bulgu, çevrimiçi araçlar arasında şiddet tanımlamalarında tam bir klinik mutabakat olmadığını, her platformun risk eşiğinin farklı olduğunu somut olarak ortaya koymaktadır.
3. **Kombine İlaç Çözümlemesi Başarılı:** `Augmentin` gibi birden fazla etken madde içeren kombine müstahzarlar sistem tarafından otomatik olarak moleküllerine ayrıştırılmakta ve her bileşen bağımsız taranmaktadır (NB04 Hücre [13]):
   - **Augmentin** tek bir kutu olmasına rağmen 2 etken madde içerir: *Amoksisilin* ve *Klavulanik Asit* (NB04 Hücre [13]).
   - **Klacid** (*Klaritromisin*) ve **Aspirin** (*Asetilsalisilik Asit*) ise 1'er etken madde içerir (NB04 Hücre [13]).
   - Sistem ilaçları molekül seviyesinde kartezyen eşleştirerek; Augmentin–Klacid ($2 \times 1 = 2$ çift), Augmentin–Aspirin ($2 \times 1 = 2$ çift) ve Klacid–Aspirin ($1 \times 1 = 1$ çift) olmak üzere **toplam 5 farklı ikili etkileşim çifti ($2 + 2 + 1 = 5$)** üretir (NB04 Hücre [13]). Amoksisilin–Klaritromisin arasındaki **Minor** etkileşim tam isabetle yakalanır (NB04 Hücre [13]).
4. **Veri Tabanı Sınırları ve Kayıp Oranı İspatlandı:**
   - **Ruhsat Gerçeği (Coumadin):** Coumadin markası güncel TİTCK ruhsatlı listesinde yer almamaktadır; Sağlık Bakanlığı SKRS Pasif Ürünler Listesi'nde kayıtlıdır (5 mg: 2022-10-11, 10 mg: 2023-07-11 pasife alınmıştır). Sistem yapay takma ad kullanmayıp dürüstçe `Ürün Bulunamadı` dönmüştür. Bu durum resmi verilerle kanıtlanmıştır (NB04 Hücre [11]). Ruhsatlı aktif Varfarin müstahzarı olan `Warfmadin` ile klinik test başarıyla tekrarlanmıştır (NB04 Hücre [12]).
   - **Katalog Eksikliği (Deksketoprofen):** Deksketoprofen (`Arveles`), küresel DDInter veritabanında tekil molekül olarak bulunmadığı için sistem *"etkileşim yok"* yanılgısına düşmemiş, `DDInter'da Yok` uyarısı vermiştir (NB04 Hücre [10] ve [12]). Drugs.com ([Şekil 9](../images/sekil09.png)), Medscape ([Şekil 15](../images/sekil15.png)) ve WebMD ([Şekil 21](../images/sekil21.png)) araçlarında da ABD pazarı odaklı olmaları nedeniyle Deksketoprofen tanınamamış ve etkileşim doğrulanamamıştır.
   - **Eksik ATC Grubu Kaybı:** `Parol` (N grubu) ve `Cordarone` (C grubu) ilaçlarının her ikisi de DDInter'da olmasına rağmen, DDInter indirme dosyalarında C ve N grupları sunulmadığı için bu etkileşim indirilen dosyalarda tespit edilememiştir (NB04 Hücre [14]). Bu bulgu, İP4'te hesapladığımız **%22,71'lik çift kaybı** (%47,68 madde kaybı - NB04 Hücre [9]) teorisini sahada somut olarak doğrulamıştır.

---

## 1. Test Metodolojisi ve Arama Kuralları

Testler `notebooks/04_ddinter_birlestirme.ipynb` Bölüm 10 üzerinden çalıştırılmış ve çıktılar kaydedilmiştir (NB04 Hücre [10]–[15]).

### Temel Çalışma İlkeleri:
1. **Karakter Katlama (Case-folding):** Türkçe `ı/i`, `İ/I` harf farkları normalize edilir. Kullanıcı küçük harfle `klacid` yazsa bile veritabanındaki büyük harfli `KLACID 500 MG FİLM KAPLI TABLET, 14 ADET` kaydı bulunur.
2. **Bileşen Hiyerarşisi:** Sistem kutu adından moleküle 3 aşamalı köprüyle ulaşır: `urun.csv` (ürün) ➔ `urun_etken.csv` (bileşenler) ➔ `etken_madde.csv` (DDInter ID ve ATC kodu).
3. **Kombine Ürün Ayrıştırma:** Augmentin gibi çok bileşenli ilaçlar tekil kabul edilmez; kutu açılıp içindeki tüm moleküller diğer ilaçlarla kartezyen eşleştirilir (NB04 Hücre [13]).
4. **Bilgilendirme İlkesi ve Kullanım Koşulları:** DDInter kullanım koşulları uyarınca, bir etkileşimin bulunmaması kesin olarak etkileşim olmadığı anlamına gelmez. Bu nedenle:
   - DDInter indirme dosyalarında yer almayan eksik ATC sınıfları (C, G, J, M, N, S) için `Eksik Grup (Olası Kayıp)`,
   - İndirme dosyalarında kayıt bulunmayan çiftler için ise `"Etkileşim Yok"` yerine **`"Kayıt bulunamadı"`** durumu döndürülür.

---

## 2. Senaryo 1 ve 1B: Standart Referans Senaryolar

### Adım 1: Kullanıcı Girişi → Ürün → Etken Madde → DDInter Dosyası
**Şartname Sayfa 7 gereği üretilen izlenebilirlik tablosu (NB04 Hücre [10]):**

| Kullanıcı Girişi | urun (Adım 1) | bilesen_tr (Adım 2) | ad_en (Adım 3) | ATC | DDInter'da Hangi Dosyada Aranabilir? | Doğrulama Hücresi |
|:---|:---|:---|:---|:---:|:---|:---:|
| **Arveles** | ARVELES 25 MG FİLM KAPLI TABLET, 20 ADET | deksketoprofen | dexketoprofen | `M01AE17` | M grubu dosyası yok; yalnızca partneri A, B, D, H, L, P, R, V grubundaysa bulunur. | (NB04 Hücre [10]) |
| **Coumadin** | *(TİTCK Ruhsatlı Listede Yok - SKRS Pasif)* | — | — | — | Ruhsatlı listede bulunamadığı için ürün arama aşamasında bildirilir. | (NB04 Hücre [11]) |
| **Warfmadin** | WARFMADIN 10 MG TABLET (28 TABLET) | varfarin | warfarin | `B01AA03` | B dosyası (`ddinter_code_B.csv`). | (NB04 Hücre [10]) |
| **Klacid** | KLACID 500 MG FİLM KAPLI TABLET, 14 ADET | klaritromisin | clarithromycin | `J01FA09` | J grubu dosyası yok; partneri mevcut gruplardaysa bulunur. | (NB04 Hücre [10]) |

---

### Adım 2 & 3: İkili Kombinasyonlar, Gerçek Durum ve Çevrimiçi Araç Karşılaştırması
**Şartname Sayfa 8 gereği canlı araç testleri ve ekran görüntüsü atıfları:**

| Çift | ATC Grupları | DDInter Gerçek | DDInter Kimlikleri | DDInter Şiddet | Drugs.com Sonucu | Medscape Sonucu | WebMD Sonucu | Sistem Kararı | Doğrulama Hücresi |
|:---|:---:|:---:|:---:|:---:|:---|:---|:---|:---|:---:|
| **warfarin – clarithromycin** | `B + J` | **Bulundu** | `DDInter1951` + `DDInter393` | **Major** | **Major** ([Şekil 7](../images/sekil07.png)) | **Önemli – Yakından Takip Edin** ([Şekil 14](../images/sekil14.png)) | **Yakından takip edin** ([Şekil 20](../images/sekil20.png)) | Kırmızı Uyarı (Major) | (NB04 Hücre [12]) |
| **warfarin – dexketoprofen** | `B + M` | **Bulunmadı** | `DDInter1951` + `—` | — | **Doğrulanamadı** ([Şekil 9](../images/sekil09.png)) | **Doğrulanamadı** ([Şekil 15](../images/sekil15.png)) | **Doğrulanamadı** ([Şekil 21](../images/sekil21.png)) | DDInter'da Yok Uyarısı | (NB04 Hücre [12]) |
| **dexketoprofen – clarithromycin** | `M + J` | **Bulunmadı** | `—` + `DDInter393` | — | **Doğrulanamadı** ([Şekil 10](../images/sekil10.png)) | Test edilmedi | Test edilmedi | DDInter'da Yok Uyarısı | (NB04 Hücre [10] ve [12]) |

> **Önemli Bulgular:**  
> 1. **Şiddet Uyuşmazlığı:** Araçlar Varfarin–Klaritromisin etkileşiminin şiddetinde anlaşmamaktadır. Drugs.com **Major** seviyesinde değerlendirirken (Şekil 7), Medscape (Şekil 14) ve WebMD (Şekil 20) **"yakından takip edin"** (*Monitor Closely*) kategorisinde klinik izlem önermektedir.  
> 2. **Dexketoprofen Arama Sonuçları (İP8 Doğrulaması):** Kişi C'nin İP8 raporundaki ([IP8 Raporu](../IP8_Ilac_Etkilesim_Karsilastirma_Raporu.md)) canlı test bulgularına göre; hem Türkçe "deksketoprofen" hem de İngilizce "dexketoprofen" aramalarında ABD odaklı küresel araçlar (Drugs.com, Medscape, WebMD) molekülü tanıyamamış ve etkileşim doğrulanamamıştır ([Şekil 9](../images/sekil09.png), [Şekil 12](../images/sekil12.png), [Şekil 15](../images/sekil15.png), [Şekil 21](../images/sekil21.png)). Canlı araçlarda doğrulanamayan bu sonuç kesinlikle **"etkileşim yok" anlamına gelmez**; yalnızca bu platformların Amerikan pazarı dışındaki molekülleri listelememesinden kaynaklanan bir veri tabanı kısıtıdır.

---

### Adım 4: `etkilesim_kontrol` Gerçek Çıktı Tabloları

#### A. Senaryo 1: `etkilesim_kontrol(['Arveles', 'Coumadin', 'Klacid'])` (NB04 Hücre [10])

| urun_1 | urun_2 | etken_1 | etken_2 | atc_gruplari | ddinter_id_1 | ddinter_id_2 | durum | siddet | kaynak_dosyalar | Doğrulama Hücresi |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| ARVELES 25 MG FİLM KAPLI TABLET, 20 ADET | Coumadin | - | - | - | - | - | **Ürün Bulunamadı** | - | - | (NB04 Hücre [10]) |
| ARVELES 25 MG FİLM KAPLI TABLET, 20 ADET | KLACID 500 MG FİLM KAPLI TABLET, 14 ADET | dexketoprofen | clarithromycin | M + J | - | DDInter393 | **DDInter'da Yok** | - | - | (NB04 Hücre [10]) |
| Coumadin | KLACID 500 MG FİLM KAPLI TABLET, 14 ADET | - | - | - | - | - | **Ürün Bulunamadı** | - | - | (NB04 Hücre [10]) |

#### B. Senaryo 1B: `etkilesim_kontrol(['Arveles', 'Warfmadin', 'Klacid'])` (NB04 Hücre [12])

| urun_1 | urun_2 | etken_1 | etken_2 | atc_gruplari | ddinter_id_1 | ddinter_id_2 | durum | siddet | kaynak_dosyalar | Doğrulama Hücresi |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| ARVELES 25 MG FİLM KAPLI TABLET, 20 ADET | WARFMADIN 10 MG TABLET (28 TABLET) | dexketoprofen | warfarin | M + B | - | DDInter1951 | **DDInter'da Yok** | - | - | (NB04 Hücre [12]) |
| ARVELES 25 MG FİLM KAPLI TABLET, 20 ADET | KLACID 500 MG FİLM KAPLI TABLET, 14 ADET | dexketoprofen | clarithromycin | M + J | - | DDInter393 | **DDInter'da Yok** | - | - | (NB04 Hücre [12]) |
| WARFMADIN 10 MG TABLET (28 TABLET) | KLACID 500 MG FİLM KAPLI TABLET, 14 ADET | warfarin | clarithromycin | B + J | DDInter1951 | DDInter393 | **Etkileşim Var** | **Major** | A, B | (NB04 Hücre [12]) |

---

## 3. Senaryo 2: Kombine Ürün Senaryosu (Augmentin + Klacid + Aspirin) (NB04 Hücre [13])

*Şartname Sayfa 11 kuralı: "Kombine bir ürün içeren 3 ilaçlı bir liste".* (NB04 Hücre [13])

Augmentin tek bir kutu olmasına rağmen 2 etken madde içerir: **Amoksisilin + Klavulanik Asit**. Klacid (*Klaritromisin*) ve Aspirin (*Asetilsalisilik Asit*) ise 1'er etken maddeli tekil ilaçlardır. Sistem kartezyen eşleştirme ile **toplam 5 farklı ikili molekül çifti** üretir (NB04 Hücre [13]):

| urun_1 | urun_2 | etken_1 | etken_2 | atc_gruplari | ddinter_id_1 | ddinter_id_2 | durum | siddet | kaynak_dosyalar | Doğrulama Hücresi |
|:---|:---|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| AUGMENTIN 500 MG/125 MG FILM KAPLI TABLET, 14 ADET | KLACID 500 MG FİLM KAPLI TABLET, 14 ADET | amoksisilin (amoxicillin) | clarithromycin | J + J | DDInter83 | DDInter393 | **Etkileşim Var** | **Minor** | A | (NB04 Hücre [13]) |
| AUGMENTIN 500 MG/125 MG FILM KAPLI TABLET, 14 ADET | KLACID 500 MG FİLM KAPLI TABLET, 14 ADET | klavulanik asit (clavulanic acid) | clarithromycin | J + J | DDInter394 | DDInter393 | **Eksik Grup (Olası Kayıp)** | - | - | (NB04 Hücre [13]) |
| AUGMENTIN 500 MG/125 MG FILM KAPLI TABLET, 14 ADET | ASPIRIN 100 MG TABLET, 1000 ADET | amoksisilin (amoxicillin) | asetilsalisilik asit (acetylsalicylic acid) | J + N | DDInter83 | DDInter20 | **Etkileşim Var** | **Unknown** | A, B | (NB04 Hücre [13]) |
| AUGMENTIN 500 MG/125 MG FILM KAPLI TABLET, 14 ADET | ASPIRIN 100 MG TABLET, 1000 ADET | klavulanik asit (clavulanic acid) | asetilsalisilik asit (acetylsalicylic acid) | J + N | DDInter394 | DDInter20 | **Eksik Grup (Olası Kayıp)** | - | - | (NB04 Hücre [13]) |
| KLACID 500 MG FİLM KAPLI TABLET, 14 ADET | ASPIRIN 100 MG TABLET, 1000 ADET | clarithromycin | asetilsalisilik asit (acetylsalicylic acid) | J + N | DDInter393 | DDInter20 | **Etkileşim Var** | **Unknown** | A, B | (NB04 Hücre [13]) |

---

## 4. Senaryo 3: Kayıp / Eksik Ürün Senaryosu (Arveles + Parol + Cordarone) (NB04 Hücre [14])

*Şartname Sayfa 11 kuralı: "En az bir ilacı DDInter'da bulunmayan bir liste".* (NB04 Hücre [14])

Bu senaryoda hem DDInter kataloğunda bulunmayan bir molekül (`Arveles`: Deksketoprofen), hem de DDInter indirme dosyası bulunmayan eksik ATC sınıflarındaki ilaçlar (`Parol`: Parasetamol / N grubu; `Cordarone`: Amiodaron / C grubu) test edilmiştir ($3$ tekil ilaç = $3$ çift) (NB04 Hücre [14]).

| urun_1 | urun_2 | etken_1 | etken_2 | atc_gruplari | ddinter_id_1 | ddinter_id_2 | durum | siddet | kaynak_dosyalar | Doğrulama Hücresi |
|:---|:---|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| ARVELES 25 MG FİLM KAPLI TABLET, 20 ADET | PAROL 500 MG TABLET, 20 ADET | dexketoprofen | parasetamol (acetaminophen) | M + N | - | DDInter14 | **DDInter'da Yok** | - | - | (NB04 Hücre [14]) |
| ARVELES 25 MG FİLM KAPLI TABLET, 20 ADET | CORDARONE 200 MG BÖLÜNEBİLİR TABLET, 30 ADET | dexketoprofen | amiodarone | M + C | - | DDInter76 | **DDInter'da Yok** | - | - | (NB04 Hücre [14]) |
| PAROL 500 MG TABLET, 20 ADET | CORDARONE 200 MG BÖLÜNEBİLİR TABLET, 30 ADET | parasetamol (acetaminophen) | amiodarone | N + C | DDInter14 | DDInter76 | **Eksik Grup (Olası Kayıp)** | - | - | (NB04 Hücre [14]) |

---

## 5. Senaryo 4: Yol D Doğrulama ve Belge Bekleyen Ürün Senaryosu (BEDOXINAL, BENORAL, POLIVIT C)

Yol D entegrasyonu kapsamında manuel etken madde eşleştirmesi ve ürün belgesi doğrulama süreçleri test edilmiştir:
1. **BEDOXINAL (Bileşen Doğrulaması Bekleniyor):** Resmî ruhsat/KÜB belgesi henüz doğrulanmamış ürünlerde sistem ham otomatik ayrıştırmadaki hatalı parçalara geri dönmemekte; kullanıcıya açıkça `Bileşen doğrulaması bekleniyor` uyarısı üretmektedir.
2. **BENORAL ve POLIVIT C (Yol D Aktif Eşleşme):** Farklı ambalaj boyutlarında (BENORAL 30/50 tablet, POLIVIT C 30/500/1000 tablet) Yol D manuel eşleştirmeleri tüm ambalaj boyutlarına genişletilmiş ve DDInter eşleşmeleri (`DDInter1549`, `DDInter124`, `DDInter1289`, `DDInter771`) doğrulanmıştır.

| urun_1 | urun_2 | etken_1 | etken_2 | durum | siddet | Doğrulama |
|:---|:---|:---|:---|:---:|:---:|:---:|
| BEDOXINAL 50 TABLET | WARFMADIN 10 MG TABLET | Bileşen doğrulaması bekleniyor | warfarin | **Bileşen doğrulaması bekleniyor** | - | Yol D Kuralı |
| BENORAL 250 MG/250 MG (30 ADET) | KLACID 500 MG FİLM KAPLI TABLET | Piridoksin hidroklorür | clarithromycin | **Kayıt bulunamadı** | - | Yol D Eşleşmesi |
| POLIVIT C FİLM TABLET (1000 ADET) | WARFMADIN 10 MG TABLET | C vitamini (askorbik asit) | warfarin | **Etkileşim Var** | **Minor** | Yol D Eşleşmesi |

---

## 6. Olası Sorular ve Cevaplar

| Hoca Ne Sorabilir? | Vereceğin Net ve Güvenli Cevap | Doğrulama Hücresi |
|:---|:---|:---:|
| **1. "Arveles ile Warfmadin arasındaki etkileşimi sistem neden bulamadı?"** | Arveles'in etken maddesi *Deksketoprofen*'dir. Deksketoprofen Türkiye'de ve Avrupa'da çok yaygın bir molekül olmasına rağmen küresel DDInter kataloğunda tekil molekül olarak yer almamakta, sadece ana rasematı olan *Ketoprofen* bulunmaktadır. Sistemimiz varsayım yapmayıp veritabanında olmadığı için `DDInter'da Yok` uyarısı verdi. | (NB04 Hücre [12]) |
| **2. "Coumadin yerine neden Warfmadin ile test yapıldı?"** | Sağlık Bakanlığı ham verileri incelendiğinde `Coumadin` markasının TİTCK ruhsatlı güncel ürün listesinde yer almadığı, SKRS Pasif Ürünler Listesi'nde bulunduğu görülmüştür (5 mg 2022'de, 10 mg 2023'te pasife alınmıştır). Sistem yapay alias kuralları kullanmadan dürüstçe `Ürün Bulunamadı` demiştir. Ruhsatlı aktif varfarin ürünü olan `Warfmadin` ile klinik test gerçekleştirilmiş ve **Major** etkileşim yakalanmıştır. | (NB04 Hücre [10], [11] ve [12]) |
| **3. "Augmentin senaryosunda neyi kanıtladınız?"** | Augmentin kombine bir formülasyondur (Amoksisilin + Klavulanik Asit). Sistemimiz barkod üzerinden bunu iki ayrı bileşene ayırdı ve diğer iki ilaçla kartezyen eşleyerek $(2 \times 1) + (2 \times 1) + (1 \times 1) = 5$ çift üretti. Amoksisilin–Klaritromisin arasındaki **Minor** etkileşimi başarıyla yakaladı. | (NB04 Hücre [13]) |
| **4. "Parol ve Cordarone ikisi de DDInter'da varken neden sonuç çıkmadı?"** | DDInter 14 ATC grubundan sadece 8'i için dosya sunuyor. Parol **N (Sinir)** grubunda, Cordarone ise **C (Kardiyovasküler)** grubundadır. İki ilacın da indirme dosyası olmadığı için indirilen tablolarda yer alamazlar. Sistemimiz bunu `Eksik Grup (Olası Kayıp)` olarak etiketleyerek kayıp analizi modelimizi sahada ispatlamıştır. | (NB04 Hücre [14]) |
| **5. "Drugs.com, Medscape ve WebMD ile karşılaştırdığınızda ne gördünüz?"** | Araçlar şiddet konusunda anlaşmamaktadır: Drugs.com Varfarin–Klaritromisin etkileşimini **Major** olarak sınıflandırırken (Şekil 7), Medscape **Önemli – Yakından Takip Edin** (Şekil 14) ve WebMD **Yakından takip edin** (Şekil 20) şeklinde klinik takip kategorisinde vermektedir. Ayrıca Deksketoprofen hiçbir küresel araç tarafından (ABD pazarı odaklı oldukları için) tanınamamıştır (Şekil 9, 15, 21). | (Şekil 7, 9, 10, 14, 15, 20, 21) |

---

## 6. Hafta Sonu Teslim Kontrol Listesi Uygunluğu

- [x] **İP7 Fonksiyonu:** `etkilesim_kontrol` fonksiyonu genel arama kurallarıyla yazıldı ve test edildi (`src/etkilesim_kontrol.py`).
- [x] **Çıktı Formatı:** Her çift için bulundu/bulunmadı, şiddet, DDInter kimlikleri ve ATC grupları döndürüldü (NB04 Hücre [10]–[14]).
- [x] **Zorunlu Senaryolar:** Referans (Coumadin ve Warfmadin), Kombine Augmentin (5 çift) ve Kayıp Parol-Cordarone (3 çift) denendi (NB04 Hücre [10], [11], [12], [13], [14]).
- [x] **Araç Karşılaştırması:** Drugs.com, Medscape ve WebMD sonuçları canlı ekran görüntüsü referanslarıyla (`images/sekil*.png`) tabloya işlendi.
- [x] **Rapor:** `docs/uctan_uca_test.md` şartnamedeki tüm detaylarla ve notebook hücre atıflarıyla güncellendi.
- [x] **Notebook 04 Entegrasyonu:** Bölüm 10 altına tüm çıktılar ve assertion kontrolleri kaydedildi (NB04 Hücre [10]–[15]).
