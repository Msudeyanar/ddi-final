# İP2 — 50 ürünün elle ayrıştırma kontrolü

Kişi A ve Kişi C’nin ortak kontrolünde Notebook 02’nin `sample(n=50, random_state=42)` çıktısındaki barkodlar, yerel ham etkin madde ve bileşen listeleriyle tek tek karşılaştırıldı. Örneklem, ayrıştırıcının en az iki bileşen çıkardığı ürünlerle sınırlıdır. [Notebook 02, örneklem ve elle kontrol hücresi](../notebooks/02_etken_ayristirma.ipynb)

**Sonuç:** 40/50 tam (%80), 4/50 kısmi (%8), 6/50 hatalı (%12). Kısmi kayıtlar dahil edildiğinde 44/50 (%88). Oranlar aşağıdaki elle kontrol tablosundan ve Notebook 02’nin `62e06900` hücresindeki aynı barkod etiketlerinden hesaplandı.

| # | Barkod | Ürün | Yerel ham etkin madde | Notebook bileşen listesi | Elle karar | Açıklama |
|---:|---|---|---|---|---|---|
| 1 | 8699828690931 | ISOLYTE-M %5 DEKSTROZLU ÇÖZELTİ | sodyum asetat trihidrat,dibazik potasyum fosfat,dekstroz monohidrat,sodyum klorür,potasyum klorür | `sodyum asetat` + `dibazik potasyum fosfat` + `dekstroz` + `sodyum klorur` + `potasyum klorur` | **Doğru** | 5 elektrolit/şeker bileşeni başarıyla ayrıştırılmış, inorganik tuzlar korunmuştur. |
| 2 | 8680836323959 | TURKFLEKS %5 DEKSTROZ % 0,45 SODYUM | dekstroz anhidrat, sodyum klorür | `dekstroz` + `sodyum klorur` | **Doğru** | Anhidrat tuzu temizlenmiş, iki bileşen tam ayrışmıştır. |
| 3 | 8699527093866 | BENORAL 250 MG/250 MG FİLM TABLET | vitamin b1 in combination with vitamin b6 and/or vitamin b12 | `vitamin b1 in combination with vitamin b6` + `or vitamin b12` | **Hatalı** | TİTCK ham metnindeki İngilizce WHO açıklama metni bölünürken 'or' bağlacı kalıntı bırakmıştır. |
| 4 | 8690509574274 | VICKS VAPODRY SURUP, 120 ML | psödoefedrin hidroklorür, klorfeniramin maleat, dekstrometorfan hidrobromür | `psodoefedrin` + `klorfeniramin` + `dekstrometorfan` | **Doğru** | 3'lü kombinasyonda hidroklorür, maleat ve hidrobromür tuzları başarıyla atılmıştır. |
| 5 | 8699844696559 | Primefleks Ringer 0,86 g+0,03 g+0,033 g | Sodyum klorür, Potasyum klorür, Kalsiyum klorür dihidrat | `sodyum klorur` + `potasyum klorur` + `kalsiyum klorur` | **Doğru** | Elektrolit tuzları kural gereği korunmuş, dihidrat atılmıştır. |
| 6 | 8699569092254 | OLMYSAR COMBO 40MG/5 MG TABLET | olmesartan medoksomil, amlodipin besilat | `olmesartan` + `amlodipin` | **Doğru** | Medoksomil ve besilat ekleri tam sözcük olarak temizlenmiştir. |
| 7 | 8699606692355 | POLİFLEKS 100 MG/ML DEKSTRAN40+9 MG | dekstran+sodyum klorür | `dekstran` + `sodyum klorur` | **Doğru** | `+` ayırıcısı başarıyla çalışmıştır. |
| 8 | 8680881012891 | TELMODIP 80 MG/10 MG TABLET | telmisartan+amlodipin besilat | `telmisartan` + `amlodipin` | **Doğru** | Başarılı `+` ayrıştırması ve tuz temizliği. |
| 9 | 8699512007212 | GRIMEL TABLET, 20 ADET | parasetamol, klorfeniramin | `parasetamol` + `klorfeniramin` | **Doğru** | Virgül ayrıştırması başarılı. |
| 10 | 8699788698077 | BİOFLEKS %5 DEKSTROZ RİNGER LAKTAT | dekstroz monohidrat, sodyum klorür, sodyum laktat, potasyum klorür, kalsiyum klorür | `dekstroz` + `sodyum klorur` + `sodyum laktat` + `potasyum klorur` + `kalsiyum klorur` | **Doğru** | 5 bileşen eksiksiz ayrışmıştır. |
| 11 | 8699523010133 | BEVITOL TABLET, 20 ADET | vitamin b1,vitamin b6 | `vitamin b1` + `vitamin b6` | **Doğru** | Boşluksuz virgül başarıyla ayrıştırılmıştır. |
| 12 | 8699569280279 | KLAMOKS 312.5 MG FORT SÜSPANSİYON | amoksisilin ve klavulanik asit | `amoksisilin` + `klavulanik asit` | **Doğru** | `ve` bağlacı başarıyla ayrıştırılmıştır. |
| 13 | 8698923793516 | MON.MIBI KIT, 1.0 MG/FLAKON IV | tetrakis bakir (i) ve tetrafloroborat (mibi) | `tetrakis bakir` + `tetrafloroborat` | **Hatalı** | Tekil koordinasyon kompleksi (MIBI), aradaki 've' bağlacı nedeniyle ikiye bölünmüştür. |
| 14 | 8681911570015 | ASE-COLD PEDİATRİK ŞURUP | parasetamol/oksalamin sitrat/klorfeniramin maleat | `parasetamol` + `oksalamin` + `klorfeniramin` | **Doğru** | `/` ayırıcısı ve sitrat/maleat tuzları temizlenmiştir. |
| 15 | 8699514383949 | THIOCILLINE DERİ MERHEMİ | basitrasin+neomisin sülfat | `basitrasin` + `neomisin` | **Doğru** | Başarılı `+` ayrıştırması. |
| 16 | 8681291110191 | MEBUCAIN NANELI PASTIL | lidokain hidroklorür ve setilpiridinyum klorür | `lidokain` + `setilpiridinyum` | **Doğru** | `ve` bağlacı ve klorür tuzları başarıyla temizlenmiştir. |
| 17 | 8699606693659 | PF K-CAMINE %8 AMINO ASIT | L-İzolösin, L-Lösin, Lizin (L-Lizin asetat 0,86 g olarak), L-Metiyonin, L-Fenilalanin, L-Treonin, L-Triptofan, L-Valin, L-Alanin, L-Arjinin, L-Histidin, L-Prolin, L-Serin, Glisin (Amino asetik asit), L-Sistein. HCl. H2O | `l-izolosin` + `l-losin` + `lizin` + `l-metiyonin` + `l-fenilalanin` + `l-treonin` + `l-triptofan` + `l-valin` + `l-alanin` + `l-arjinin` + `l-histidin` + `l-prolin` + `l-serin` + `glisin` + `l-sistein` | **Doğru** | 15 amino asit virgüllerle eksiksiz ayrıştırılmıştır. |
| 18 | 8699540570108 | ESPEKTAN ŞURUP, 100 ML | psödoefedrin hcl ve guafenazin | `psodoefedrin` + `guafenazin` | **Doğru** | Başarılı. |
| 19 | 8699844693527 | Primefleks Laktatlı Ringer I.V. | Sodyum klorür, Sodyum laktat, Potasyum klorür, Kalsiyum klorür dihidrat | `sodyum klorur` + `sodyum laktat` + `potasyum klorur` + `kalsiyum klorur` | **Doğru** | 4 elektrolit eksiksiz korunmuştur. |
| 20 | 8680400770509 | CALCİOSEL ENJEKSİYONLUK ÇÖZELTİ | kalsiyum glukonat monohidrat, kalsiyum levulinat dihidrat | `kalsiyum glukonat` + `levulinat` | **Kısmi** | İkinci bileşenin 'kalsiyum' kök kelimesi tuz regex'i nedeniyle düşmüş, 'levulinat' kalmıştır. |
| 21 | 8680952510912 | OSTEOFLEX FILM TABLET | glukozamin sulfat, kondoitin sulfat, manganez, vit c, zerdecal | `glukozamin` + `kondoitin` + `manganez, vit c, zerdecal` | **Hatalı** | 'vit c' 4 harften kısa olduğu için virgül ayrıştırma kuralına takılmış, son 3 bileşen bölünememiştir. |
| 22 | 8699828140054 | GYNOFERON DEPO DRAJE | demir ii sülfat, folik asit, mukoproteaz | `demir ii` + `folik asit` + `mukoproteaz` | **Doğru** | Başarılı 3'lü ayrıştırma. |
| 23 | 8699525096043 | Zalepril Film Kaplı Tablet | Lerkanidipin hidroklorür, Enalapril maleat | `lerkanidipin` + `enalapril` | **Doğru** | Başarılı. |
| 24 | 8680836323898 | TURKFLEKS %5 DEKSTROZ % 0,9 SODYUM | dekstroz anhidrat, sodyum klorür | `dekstroz` + `sodyum klorur` | **Doğru** | Başarılı. |
| 25 | 8681144039044 | Bayduo Cold Flu Tablet | İbuprofen, Psödoefedrin hidroklorür | `ibuprofen` + `psodoefedrin` | **Doğru** | Başarılı. |
| 26 | 8699606691914 | POLİFLEKS 60 MG/ML DEKSTRAN 70 | dekstran+sodyum klorür | `dekstran` + `sodyum klorur` | **Doğru** | Başarılı. |
| 27 | 8680352000709 | Otify Kulak Damlası | Fenazon, Lidokain Hidroklorür | `fenazon` + `lidokain` | **Doğru** | Başarılı. |
| 28 | 8699625960336 | PENTAXİM IM ENJEKSİYONLUK | difteri, tetanoz, boğmaca ve inaktif çocuk gelci (tip 1,2,3) ve hib | `difteri` + `tetanoz` + `bogmaca` + `inaktif cocuk gelci` + `hib` | **Kısmi** | gelci yerel ham ürün metninde zaten mevcut. |
| 29 | 8699514094227 | POLIVIT C FİLM TABLET | vitamin B1, B2, B6, B12, vitamin C, kalsiyum D-pantotenat,nikotinamid, D-biotin, folik asit. | `vitamin b1, b2, b6, b12, vitamin c` + `d-pantotenat` + `nikotinamid` + `d-biotin` + `folik asit` | **Hatalı** | 'B1, B2, B6, B12' virgülleri 4 harf kuralına takılmış, B vitaminleri tek blok kalmıştır. |
| 30 | 8680881023552 | MUCOVIT-C EFERVESAN TABLET | asetilsistein / askorbik asit | `asetilsistein` + `askorbik asit` | **Doğru** | `/` ayırıcısı başarıyla çalışmıştır. |
| 31 | 8680881024320 | OSMEGA EFERVESAN TABLET | kalsiyum karbonat, vitamin d3 genistein | `kalsiyum karbonat` + `vitamin d3 genistein` | **Kısmi** | 'vitamin d3' ve 'genistein' arasında ayırıcı bulunmadığı için tek parça kalmıştır. |
| 32 | 8699824010061 | BEDOXINAL TABLET | vitamin b1 in combination with vitamin b6 and/or vitamin b12 | `vitamin b1 in combination with vitamin b6` + `or vitamin b12` | **Hatalı** | WHO kategori açıklaması İngilizce bağlaç kalıntısı içermektedir. |
| 33 | 8680881094910 | ATODIP FILM TABLET | amlodipin besilat+atorvastatin kalsiyum | `amlodipin` + `atorvastatin` | **Doğru** | `+` ayırıcısı ve tuz temizliği kusursuz. |
| 34 | 8699559350050 | PELONG %5 KREM | Lidokain, Prilokain | `lidokain` + `prilokain` | **Doğru** | Başarılı. |
| 35 | 8699514094425 | VALTALİD PLUS TABLET | Valsartan, Klortalidon | `valsartan` + `klortalidon` | **Doğru** | Başarılı. |
| 36 | 8680741520337 | FORPACK AERESOL | formoterol fumarat dihidrat/budesonid | `formoterol` + `budesonid` | **Doğru** | `/` ayırıcısı ve çift tuz temizliği başarılı. |
| 37 | 8699606693123 | POLİFLEKS İZOLEN-P %5 DEKSTROZLU | Dekstroz anhidr+sodyum laktat, potasyum klorür, magnezyum klorür hekzahidrat, dibazik sodyum fosfat | `dekstroz` + `sodyum laktat` + `potasyum klorur` + `magnezyum klorur` + `dibazik sodyum fosfat` | **Doğru** | 5 elektrolit/şeker başarıyla ayrılmıştır. |
| 38 | 8699543010168 | ALDACTAZİDE TABLET | spirinolakton / hidroklorotiyazid | `spirinolakton` + `hidroklorotiyazid` | **Doğru** | `/` ayırıcısı başarılı. |
| 39 | 8699976021366 | MEGINGO EFERVESAN TABLET | memantin hcl ve ginko biloba kuru ekstresi | `memantin` + `ginko biloba kuru ekstresi` | **Doğru** | `ve` bağlacı başarılı. |
| 40 | 8699516098063 | SOPRANO FILM TABLET | bisoprolol fumarat ve hidroklorotiyazid | `bisoprolol` + `hidroklorotiyazid` | **Doğru** | Başarılı. |
| 41 | 8680881091278 | EZESIM FILM TABLET | ezetimib ve simvastatin | `ezetimib` + `simvastatin` | **Doğru** | Başarılı. |
| 42 | 8680881099021 | LIMITEN PLUS TABLET | valsartan, hidroklorotiyazid | `valsartan` + `hidroklorotiyazid` | **Doğru** | Başarılı. |
| 43 | 8699514610205 | OFNOL FRESH OFTALMİK ÇÖZELTİ | olopatadin hcl ve sodyum hiyalüronat | `olopatadin` + `hiyaluronat` | **Doğru** | İki bileşen ayrıldı. Projenin karşı iyon sadeleştirme ölçütüyle tam doğru. |
| 44 | 8680638250118 | GRIBEXFEN HOT D TOZ | fenilefrin hcl, klorfeniramin maleat ve parasetamol | `fenilefrin` + `klorfeniramin` + `parasetamol` | **Doğru** | Virgül ve `ve` birlikte doğru ayrışmıştır. |
| 45 | 8699844091682 | METİRASİN FILM TABLET | spiramicin ve metronidazol | `spiramicin` + `metronidazol` | **Doğru** | Başarılı. |
| 46 | 8699636091524 | DELSTRIGO FILM TABLET | Doravirin, Lamivudin, Tenofovir disoproksil fumarat | `doravirin` + `lamivudin` + `tenofovir disoproksil` | **Doğru** | 3'lü antiviral kombinasyonu başarıyla ayrışmıştır. |
| 47 | 8680199197532 | NYSTAFUR VAJİNAL OVÜL | nifuratel, nistatin | `nifuratel` + `nistatin` | **Doğru** | Başarılı. |
| 48 | 8699736750291 | ENJEKSIYONLUK POTASYUM FOSFAT | dipotasyum fosfat/potasyum dihidrajen fosfat | `dipotasyum fosfat` + `dihidrajen` | **Kısmi** | İkinci kısımdaki 'fosfat' sözcüğü atılmış, 'dihidrajen' eksik kalmıştır. |
| 49 | 8699960580046 | ZANITEK FILM TABLET | enalapril maleat, lerkanidipin hidroklorür | `enalapril` + `lerkanidipin` | **Doğru** | Başarılı. |
| 50 | 8699514012016 | BITIRON TABLET | combinations of levothyroxine and liothyronine | `combinations of levothyroxine` + `liothyronine` | **Hatalı** | 'combinations of' WHO kategori metni kalıntısı kalmıştır. |

Bileşim kaynakları ve ayrıntılı Yol D kararları [barkod bazlı eşleme tablosunda](../config/yol_d_urun_esleme.csv) yer alır.


## Kişi C inceleme notu

Notebook 02’deki 50 barkodu ham ürün metni ve ayrıştırılmış bileşen listeleriyle karşılaştırdım. Kişi A ile mutabakatımıza göre OFNOL FRESH, `tuz_at` kuralının karşı iyonları sadeleştirdiği değerlendirme kapsamında tam doğru sayıldı. Ürün belgesinde ikinci etkin madde **sodyum hiyalüronat**, eşleme çıktısında **hiyaluronat** olarak yer alır. Bu ayrım, tam tuz kimliği gereken kullanımlar için kaydedildi. [OFNOL FRESH KÜB](https://www.abdiibrahim.com.tr/Uploads/Product/prospektus/ofnol/ofnol-fresh-01-015-goz-damlasi-cozelti.pdf)

PF K-CAMINE satırında 15 amino asidin tamamı gösterildi. PENTAXİM’de `gelci` yazımı, 14 Ekim 2026 tarihli TİTCK ham Excel dosyasının `RUHSATLI ÜRÜNLER LİSTESİ` sayfasında, 11795. satırda zaten mevcut. Ayrıştırma çıktısında beş bileşen grubu bulunuyor. [PF K-CAMINE KÜB](https://www.polifarma.com.tr/media/3617/pf-k-camine-8-057_kub_02-11-06-2020.pdf) · [Notebook 02](../notebooks/02_etken_ayristirma.ipynb)

On uç vakanın sorunlu bileşenleri yerel Yol D taslağında doğrulandı. Bileşim incelemesinde erişilebilen ürün belgeleri kullanıldı. BEDOXINAL için özgün ürün belgesi bekleniyor. [Yol D eşleme kararları](../config/yol_d_urun_esleme.csv)
