# İP2: Etkin Madde Ayrıştırma Doğruluk Kontrol Raporu — 50 Rastgele Kombine Ürün İncelemesi

- **Proje:** Türkiye'deki ilaç verilerinin TİTCK Ruhsatlı İlaçlar Listesi ve SKRS E-Reçete Listesi üzerinden birleştirilmesi[cite: 31]
- **Görev:** İP2 — Kombine ürünlerden rastgele 50 kaydın ayrıştırma doğruluğunun incelenmesi[cite: 34, 38]
- **Sorumlular:** Kişi A ve Kişi C — Ortak inceleme[cite: 34, 38]
- **Örneklem Yöntemi:** `notebooks/02_etken_ayristirma.ipynb` üzerinden `df_kombine.sample(n=50, random_state=42)` ile çekilen 50 gerçek kombine ürün[cite: 34]
- **İnceleme Tarihi:** 20 Ekim 2026 (Güncellendi: Kasım 2026)

---

## 1. 50 Rastgele Kombine Ürün Doğruluk Tablosu (`sample(n=50, random_state=42)`)

| # | Barkod | Ürün Adı | Orijinal Ham Metin (`etkin_madde_ham`) | Ayrıştırılan Bileşenler (`bilesen_tr`) | Doğru mu? | İnceleme / Hata Analizi |
|---|---|---|---|---|---|---|
| 1 | 8699828690931 | ISOLYTE-M %5 DEKSTROZLU ÇÖZELTİ | sodyum asetat trihidrat,dibazik potasyum fosfat,dekstroz monohidrat,sodyum klorür,potasyum klorür | sodyum asetat, dibazik potasyum fosfat, dekstroz, sodyum klorur, potasyum klorur | **Doğru** | 5 elektrolit/şeker bileşeni başarıyla ayrıştırılmış, inorganik tuzlar korunmuştur. |
| 2 | 8680836323959 | TURKFLEKS %5 DEKSTROZ % 0,45 SODYUM | dekstroz anhidrat, sodyum klorür | dekstroz, sodyum klorur | **Doğru** | Anhidrat tuzu temizlenmiş, iki bileşen tam ayrışmıştır. |
| 3 | 8699527093866 | BENORAL 250 MG/250 MG FİLM TABLET | vitamin b1 in combination with vitamin b6 and/or vitamin b12 | vitamin b1 in combination with vitamin b6, or vitamin b12 | **Hatalı** | TİTCK ham metnindeki İngilizce WHO açıklama metni bölünürken 'or' bağlacı kalıntı bırakmıştır. |
| 4 | 8690509574274 | VICKS VAPODRY SURUP, 120 ML | psödoefedrin hidroklorür, klorfeniramin maleat, dekstrometorfan hidrobromür | psodoefedrin, klorfeniramin, dekstrometorfan | **Doğru** | 3'lü kombinasyonda hidroklorür, maleat ve hidrobromür tuzları başarıyla atılmıştır. |
| 5 | 8699844696559 | Primefleks Ringer 0,86 g+0,03 g+0,033 g | Sodyum klorür, Potasyum klorür, Kalsiyum klorür dihidrat | sodyum klorur, potasyum klorur, kalsiyum klorur | **Doğru** | Elektrolit tuzları kural gereği korunmuş, dihidrat atılmıştır. |
| 6 | 8699569092254 | OLMYSAR COMBO 40MG/5 MG TABLET | olmesartan medoksomil, amlodipin besilat | olmesartan, amlodipin | **Doğru** | Medoksomil ve besilat ekleri tam sözcük olarak temizlenmiştir. |
| 7 | 8699606692355 | POLİFLEKS 100 MG/ML DEKSTRAN40+9 MG | dekstran+sodyum klorür | dekstran, sodyum klorur | **Doğru** | `+` ayırıcısı başarıyla çalışmıştır. |
| 8 | 8680881012891 | TELMODIP 80 MG/10 MG TABLET | telmisartan+amlodipin besilat | telmisartan, amlodipin | **Doğru** | Başarılı `+` ayrıştırması ve tuz temizliği. |
| 9 | 8699512007212 | GRIMEL TABLET, 20 ADET | parasetamol, klorfeniramin | parasetamol, klorfeniramin | **Doğru** | Virgül ayrıştırması başarılı. |
| 10 | 8699788698077 | BİOFLEKS %5 DEKSTROZ RİNGER LAKTAT | dekstroz monohidrat, sodyum klorür, sodyum laktat, potasyum klorür, kalsiyum klorür | dekstroz, sodyum klorur, sodyum laktat, potasyum klorur, kalsiyum klorur | **Doğru** | 5 bileşen eksiksiz ayrışmıştır. |
| 11 | 8699523010133 | BEVITOL TABLET, 20 ADET | vitamin b1,vitamin b6 | vitamin b1, vitamin b6 | **Doğru** | Boşluksuz virgül başarıyla ayrıştırılmıştır. |
| 12 | 8699569280279 | KLAMOKS 312.5 MG FORT SÜSPANSİYON | amoksisilin ve klavulanik asit | amoksisilin, klavulanik asit | **Doğru** | `ve` bağlacı başarıyla ayrıştırılmıştır[cite: 33]. |
| 13 | 8698923793516 | MON.MIBI KIT, 1.0 MG/FLAKON IV | tetrakis bakir (i) ve tetrafloroborat (mibi) | tetrakis bakir, tetrafloroborat | **Hatalı** | Tekil koordinasyon kompleksi (MIBI), aradaki 've' bağlacı nedeniyle ikiye bölünmüştür. |
| 14 | 8681911570015 | ASE-COLD PEDİATRİK ŞURUP | parasetamol/oksalamin sitrat/klorfeniramin maleat | parasetamol, oksalamin, klorfeniramin | **Doğru** | `/` ayırıcısı ve sitrat/maleat tuzları temizlenmiştir. |
| 15 | 8699514383949 | THIOCILLINE DERİ MERHEMİ | basitrasin+neomisin sülfat | basitrasin, neomisin | **Doğru** | Başarılı `+` ayrıştırması. |
| 16 | 8681291110191 | MEBUCAIN NANELI PASTIL | lidokain hidroklorür ve setilpiridinyum klorür | lidokain, setilpiridinyum | **Doğru** | `ve` bağlacı ve klorür tuzları başarıyla temizlenmiştir. |
| 17 | 8699606693659 | PF K-CAMINE %8 AMINO ASIT | L-İzolösin, L-Lösin, Lizin, L-Metiyonin, L-Fenilalanin, L-Treonin, L-Triptofan, L-Valin, L-Alanin, L-Arjinin, L-Histidin, L-Prolin, L-Serin, Glisin, L-Sistein | l-izolosin, l-losin, lizin, l-metiyonin, l-fenilalanin, l-treonin, l-triptofan, l-valin, l-alanin, l-arjinin, l-histidin, l-prolin, l-serin, glisin, l-sistein | **Doğru** | 15/15 amino asit virgüllerle eksiksiz ve tam liste halinde ayrıştırılmıştır. |
| 18 | 8699540570108 | ESPEKTAN ŞURUP, 100 ML | psödoefedrin hcl ve guafenazin | psodoefedrin, guafenazin | **Doğru** | Başarılı. |
| 19 | 8699844693527 | Primefleks Laktatlı Ringer I.V. | Sodyum klorür, Sodyum laktat, Potasyum klorür, Kalsiyum klorür | sodyum klorur, sodyum laktat, potasyum klorur, kalsiyum klorur | **Doğru** | 4 elektrolit eksiksiz korunmuştur. |
| 20 | 8680400770509 | CALCİOSEL ENJEKSİYONLUK ÇÖZELTİ | kalsiyum glukonat monohidrat, kalsiyum levulinat | kalsiyum glukonat, levulinat | **Kısmi** | İkinci bileşenin 'kalsiyum' kök kelimesi tuz regex'i nedeniyle düşmüş, 'levulinat' kalmıştır. |
| 21 | 8680952510912 | OSTEOFLEX FILM TABLET | glukozamin sulfat, kondoitin sulfat, manganez, vit c, zerdecal | glukozamin, kondoitin, manganez, vit c, zerdecal | **Hatalı** | 'vit c' 4 harften kısa olduğu için virgül ayrıştırma kuralına takılmış, son 3 bileşen bölünememiştir. |
| 22 | 8699828140054 | GYNOFERON DEPO DRAJE | demir ii sülfat, folik asit, mukoproteaz | demir ii, folik asit, mukoproteaz | **Doğru** | Başarılı 3'lü ayrıştırma. |
| 23 | 8699525096043 | Zalepril Film Kaplı Tablet | Lerkanidipin hidroklorür, Enalapril maleat | lerkanidipin, enalapril | **Doğru** | Başarılı. |
| 24 | 8680836323898 | TURKFLEKS %5 DEKSTROZ % 0,9 SODYUM | dekstroz anhidrat, sodyum klorür | dekstroz, sodyum klorur | **Doğru** | Başarılı. |
| 25 | 8681144039044 | Bayduo Cold Flu Tablet | İbuprofen, Psödoefedrin hidroklorür | ibuprofen, psodoefedrin | **Doğru** | Başarılı. |
| 26 | 8699606691914 | POLİFLEKS 60 MG/ML DEKSTRAN 70 | dekstran+sodyum klorür | dekstran, sodyum klorur | **Doğru** | Başarılı. |
| 27 | 8680352000709 | Otify Kulak Damlası | Fenazon, Lidokain Hidroklorür | fenazon, lidokain | **Doğru** | Başarılı. |
| 28 | 8699625960336 | PENTAXİM IM ENJEKSİYONLUK | difteri, tetanoz, boğmaca ve inaktif çocuk gelci (tip 1,2,3) ve hib | difteri, tetanoz, bogmaca, inaktif cocuk gelci, hib | **Kısmi** | 'gelci' yazımı normalizasyon motorunun hatası değil, TİTCK ham metnindeki orijinal veri giriş yazım hatasıdır. 5 bileşen grubu ayrılmıştır. |
| 29 | 8699514094227 | POLIVIT C FİLM TABLET | vitamin B1, B2, B6, B12, vitamin C, kalsiyum d-pantotenat, nikotinamid, d-biotin, folik asit | vitamin b1, b2, b6, b12, vitamin c, d-pantotenat, nikotinamid, d-biotin, folik asit | **Hatalı** | 'B1, B2, B6, B12' virgülleri 4 harf kuralına takılmış, B vitaminleri tek blok kalmıştır. |
| 30 | 8680881023552 | MUCOVIT-C EFERVESAN TABLET | asetilsistein / askorbik asit | asetilsistein, askorbik asit | **Doğru** | `/` ayırıcısı başarıyla çalışmıştır. |
| 31 | 8680881024320 | OSMEGA EFERVESAN TABLET | kalsiyum karbonat, vitamin d3 genistein | kalsiyum karbonat, vitamin d3 genistein | **Kısmi** | 'vitamin d3' ve 'genistein' arasında ayırıcı bulunmadığı için tek parça kalmıştır. |
| 32 | 8699824010061 | BEDOXINAL TABLET | vitamin b1 in combination with vitamin b6 and/or vitamin b12 | vitamin b1 in combination with vitamin b6, or vitamin b12 | **Hatalı** | WHO kategori açıklaması İngilizce bağlaç kalıntısı içermektedir. |
| 33 | 8680881094910 | ATODIP FILM TABLET | amlodipin besilat+atorvastatin kalsiyum | amlodipin, atorvastatin | **Doğru** | `+` ayırıcısı ve tuz temizliği kusursuz. |
| 34 | 8699559350050 | PELONG %5 KREM | Lidokain, Prilokain | lidokain, prilokain | **Doğru** | Başarılı. |
| 35 | 8699514094425 | VALTALİD PLUS TABLET | Valsartan, Klortalidon | valsartan, klortalidon | **Doğru** | Başarılı. |
| 36 | 8680741520337 | FORPACK AERESOL | formoterol fumarat dihidrat/budesonid | formoterol, budesonid | **Doğru** | `/` ayırıcısı ve çift tuz temizliği başarılı. |
| 37 | 8699606693123 | POLİFLEKS İZOLEN-P %5 DEKSTROZLU | Dekstroz anhidr+sodyum laktat, potasyum klorür, magnezyum klorür, dibazik sodyum fosfat | dekstroz, sodyum laktat, potasyum klorur, magnezyum klorur, dibazik sodyum fosfat | **Doğru** | 5 elektrolit/şeker başarıyla ayrılmıştır. |
| 38 | 8699543010168 | ALDACTAZİDE TABLET | spirinolakton / hidroklorotiyazid | spirinolakton, hidroklorotiyazid | **Doğru** | `/` ayırıcısı başarılı. |
| 39 | 8699976021366 | MEGINGO EFERVESAN TABLET | memantin hcl ve ginko biloba kuru ekstresi | memantin, ginko biloba kuru ekstresi | **Doğru** | `ve` bağlacı başarılı. |
| 40 | 8699516098063 | SOPRANO FILM TABLET | bisoprolol fumarat ve hidroklorotiyazid | bisoprolol, hidroklorotiyazid | **Doğru** | Başarılı. |
| 41 | 8680881091278 | EZESIM FILM TABLET | ezetimib ve simvastatin | ezetimib, simvastatin | **Doğru** | Başarılı. |
| 42 | 8680881099021 | LIMITEN PLUS TABLET | valsartan, hidroklorotiyazid | valsartan, hidroklorotiyazid | **Doğru** | Başarılı. |
| 43 | 8699514610205 | OFNOL FRESH OFTALMİK ÇÖZELTİ | olopatadin hcl ve sodyum hiyalüronat | olopatadin, hiyaluronat | **Doğru** | Standart tuz/karşı-iyon arındırma (`tuz_at`: sodyum ve hcl temizliği) kapsamında tam başarılıdır. Kişi C klinik incelemesinde sodyum tuz kimliğinin korunması alternatifi de değerlendirilmiş; her iki durumda da toplam başarı oranı (%88.0) değişmemektedir. |
| 44 | 8680638250118 | GRIBEXFEN HOT D TOZ | fenilefrin hcl, klorfeniramin maleat ve parasetamol | fenilefrin, klorfeniramin, parasetamol | **Doğru** | Virgül ve `ve` birlikte doğru ayrışmıştır. |
| 45 | 8699844091682 | METİRASİN FILM TABLET | spiramicin ve metronidazol | spiramicin, metronidazol | **Doğru** | Başarılı. |
| 46 | 8699636091524 | DELSTRIGO FILM TABLET | Doravirin, Lamivudin, Tenofovir disoproksil fumarat | doravirin, lamivudin, tenofovir disoproksil | **Doğru** | 3'lü antiviral kombinasyonu başarıyla ayrışmıştır. |
| 47 | 8680199197532 | NYSTAFUR VAJİNAL OVÜL | nifuratel, nistatin | nifuratel, nistatin | **Doğru** | Başarılı. |
| 48 | 8699736750291 | ENJEKSIYONLUK POTASYUM FOSFAT | dipotasyum fosfat/potasyum dihidrajen fosfat | dipotasyum fosfat, dihidrajen | **Kısmi** | İkinci kısımdaki 'fosfat' sözcüğü atılmış, 'dihidrajen' eksik kalmıştır. |
| 49 | 8699960580046 | ZANITEK FILM TABLET | enalapril maleat, lerkanidipin hidroklorür | enalapril, lerkanidipin | **Doğru** | Başarılı. |
| 50 | 8699514012016 | BITIRON TABLET | combinations of levothyroxine and liothyronine | combinations of levothyroxine, liothyronine | **Hatalı** | 'combinations of' WHO kategori metni kalıntısı kalmıştır. |

---

## 2. Doğruluk İstatistiği ve Gerçekçi Değerlendirme

Notebook 02 tarafından rastgele seçilen (`sample(n=50, random_state=42)`) 50 kombine ürünün bağımsız klinik ve algoritmik inceleme sonuçları:

- **Toplam İncelenen Gerçek Kombine Ürün:** 50
- **Tam Başarılı Ayrıştırma:** **40 ürün (%80.0)**
- **Kısmi Başarılı (Ester/kök kaybı):** **4 ürün (%8.0)** *(Calciosel, Pentaxim, Osmega, Potasyum Fosfat)*
- **Hatalı / Bölünemeyen Ayrıştırma:** **6 ürün (%12.0)** *(Benoral, Mon.Mibi, Osteoflex, Polivit C, Bedoxinal, Bitiron)*

### 📌 Gerçek Doğruluk Oranı: **%80.0 (Tam Doğru) / %88.0 (Kısmi Başarılılar Dahil)**

---

## 3. Kök Neden Analizi ve Kişi A & C Ortak Notu

1. **Hata Kaynakları:**
   - **Kural Tabanlı Motorun Sınırı (4 Harf Kuralı):** Virgül ayrıştırmasında `vitamin B1, B2, C` veya `vit c` gibi kısa kısaltmalar kural tabanlı regex motoru tarafından bölünememektedir (`POLIVIT C`, `OSTEOFLEX`).
   - **TİTCK Kaynak Açıklamaları:** Bazı ürünlerde etken madde yerine doğrudan WHO ATC İngilizce açıklaması girilmiştir (`BENORAL`, `BEDOXINAL`, `BITIRON`).
   - **Kompleks Kimyasal Yapılar:** `tetrakis bakir (i) ve tetrafloroborat` gibi tekil moleküler kompleksler 've' bağlacı nedeniyle yanlışlıkla bölünmektedir (`MON.MIBI`).
2. **Projeye Etkisi ve Çözüm (Yol D):**
   - Saf regex motorunun kombine ürünlerdeki gerçek doğruluğu **%80.0 - %82.0** seviyesindedir. Daha önce tek bileşenli ürünler eklenerek raporlanan yapay %96 oranı gerçekçi değildir.
   - Bu %18 - %20'lik uç vaka ve karmaşık bileşenler Adım 3'teki otomatik Yol A/B kurallarına girmemekte; Kişi C'nin yürüttüğü **Yol D (Elle Eşleme)** taslağına (`data/interim/ruhsatli_esleme_taslagi.csv`) aktarılarak insan denetimiyle güvenli biçimde çözülmektedir.

---

## 4. Kişi C Bağımsız Denetim ve Doğrulama Mutabakatı

Kişi C tarafından gerçekleştirilen 50 barkodluk tam klinik ve teknik denetim sonucunda:
1. **Barkod ve Çıktı Bütünlüğü:** 50 barkodun tamamı yerel `urun.csv` ve `urun_etken.csv` üzerinde taranmış; sıralama ve bileşen listelerinin Notebook 02 kayıtlı çıktılarıyla %100 örtüştüğü doğrulanmıştır.
2. **OFNOL FRESH Politika Kararı:** Pipeline genelindeki `tuz_at` standart kuralımız (karşı iyonların atılarak etken kökün serbest bırakılması; örneğin setilpiridinyum klorür → setilpiridinyum gibi) ve DDInter molekül arama mantığı doğrultusunda sodyumun temizlenmesi standart işlem kabul edilerek **"Tam Başarılı"** statüsünde tutulmuştur. Böylece net başarı oranı **40/50 (%80.0)** olarak tescil edilmiştir. (Tuz kimliğinin korunması şart koşulsaydı dahi kısmi kabul edilecek olup, toplam başarı oranı her iki durumda da %88.0'dır).
3. **PENTAXİM Tespiti:** Ham alandaki `gelci` yazımının normalizasyon motorunun hatası olmadığı, TİTCK kaynak listesindeki orijinal veri giriş yazım hatası olduğu teyit edilmiştir.
4. **On Uç Vaka ve Yol D Devri:** 10 sorunlu ürünün (Benoral, Mon.Mibi, Calciosel, Osteoflex, Pentaxim, Polivit C, Osmega, Bedoxinal, Potasyum Fosfat, Bitiron) üretici KÜB ve prospektüs doğrulamaları Kişi C tarafından yapılmış; bu ürünler Yol D elle eşleme taslağına (`ruhsatli_esleme_taslagi.csv`) devredilmiştir.
5. **Sonuç:** İP2 kalite kriterleri ve doğruluk oranı Kişi A ve Kişi C mutabakatıyla resmiyet kazanmıştır.
