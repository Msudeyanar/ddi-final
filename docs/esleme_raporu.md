# İP3: DDInter İlaç Eşleşme Raporu

> **Rapor özeti:** Türkiye'deki kapsam içi etken maddelerin %48.1'i (1,418 / 2,945), kapsam içi ruhsatlı ürünlerin %80.5'inin (18,081 / 22,470) en az bir bileşeni DDInter'da bulunuyor.
> *(Tüm Bileşenler Bazında: %46.3 (1,420 / 3,065) — Tüm Ruhsatlı Ürünler Bazında: %80.6 (18,488 / 22,927))*

> **Notebook 03’ün ana daldaki kayıtlı özeti.** [Özet hücresi](../notebooks/03_kopru_ddinter.ipynb#cell-id=d9715d76), kapsam içi bileşenlerde **1.418 / 2.945**, kapsam içi ruhsatlı ürünlerde en az bir eşleşme için **18.081 / 22.470**, tüm bileşenlerde **1.420 / 3.065**, tüm ruhsatlı ürünlerde en az bir eşleşme için **18.488 / 22.927** verir. Bu değerler yukarıdaki özetle eşleşir. Bölüm 4 eldeki yerel CSV’ye dayanır.

## 1. Yol Bazında Bileşen Sayısı ve DDInter Eşleşme Dağılımı

Bu bölüm Notebook 03’ün kayıtlı çalıştırmasındaki eşleme tablosunu özetler. Sorgu motorundaki daha sonraki Yol D kuralları bu sayıma dahil edilmemiştir.
| Eşleşme Yolu | Toplam Bileşen | DDInter Eşleşen | Eşleşme Oranı (%) | Açıklama |
| :--- | :---: | :---: | :---: | :--- |
| **Yol A (Tek Bileşenli ATC)** | 1,904 | 1,234 | %64.8 | Tek bileşenli ürünlerin SKRS ATC sözlüğünden İngilizce adı |
| **Yol B (Kombine Bölme & RapidFuzz)** | 68 | 37 | %54.4 | Kombine ürünlerin ATC adından ayrıştırılan bileşenler |
| **Yol C (Kural Tabanlı - tr_en_kurallar)** | 92 | 92 | %100.0 | Türkçe kural tabanlı çeviri motoru ile eşleşenler |
| **SKRS (Kural 5/6)** | 90 | 32 | %35.6 | SKRS'ten doğrudan İngilizce gelen ürünler |
| **Yol D (Kişi C - Uzman Manuel İnceleme)** | 24 | 24 | %100.0 | Kişi C tarafından en sık eşleşmeyenlerden doğrulanarak bağlanan bileşenler |
| **Eşleşmedi (Kalan)** | 887 | 1 | %0.1 | Kural motoru ve Yol D sonrasında eşleşmeyen bileşenler |
| **TOPLAM** | **3,065** | **1,420** | **%46.3** | TİTCK ruhsatlı listedeki tüm benzersiz bileşenler |
> **Not (Yol D ve PubChem Doğrulaması):** Adım 4 kapsamında en sık 100 eşleşmeyen kapsam içi bileşenden 17 tanesi PubChem eş anlamlılarıyla doğrudan DDInter kimliğine bağlanmış ve 24 satıra yayılmıştır. Örneğin 376 ürünlü parasetamol → DDInter14 (acetaminophen). Adım 5 kapsamında ise Kişi C tarafından en sık 100 eşleşmeyen bileşen incelenmiş; 23 bileşen DDInter kimliklerine bağlanmış ve 20 İngilizce ad düzeltmesi yapılarak toplam 24 bileşen Yol D statüsüne kavuşturulmuştur. Kalan 887 bileşen sonraki aşamalara devredilmiştir.

## 2. DDInter Eşleşme Oranı Özeti
| Metrik Düzeyi | Toplam Büyüklük | DDInter'da Bulunan | Kapsama Oranı (%) |
| :--- | :---: | :---: | :--- |
| **Kapsam İçi Etken Madde Bazında** | 2,945 | 1,418 | %48.1 |
| **Kapsam İçi Ruhsatlı Ürün Bazında (En Az 1 Bileşen)** | 22,470 | 18,081 | %80.5 |
| **Tüm Etken Maddeler Bazında** | 3,065 | 1,420 | %46.3 |
| **Tüm Ruhsatlı Ürünler Bazında (En Az 1 Bileşen)** | 22,927 | 18,488 | %80.6 |

> **Not (Benzersiz İlaç Kimliği):** DDInter ile eşleşen 1,420 etken madde kaydı, toplam **898 benzersiz DDInter kimliğine** (`ddinter_id`) karşılık gelmektedir (örn. `vitamin d3` ve `kolekalsiferol` her ikisi de `DDInter367` kimliğine bağlanmıştır).

## 3. ATC Ana Grubuna Göre DDInter Eşleşme Oranı (14 Satır - Kapsam İçi)
| ATC Ana Grubu | Grup Açıklaması | Toplam Bileşen | DDInter Eşleşen | Eşleşme Oranı (%) |
| :---: | :--- | :---: | :--- | :---: |
| **A** | Sindirim Sistemi ve Metabolizma | 468 | 155 | %33.1 |
| **B** | Kan ve Kan Yapıcı Organlar | 249 | 89 | %35.7 |
| **C** | Kardiyovasküler Sistem | 215 | 122 | %56.7 |
| **D** | Dermatolojik İlaçlar | 192 | 62 | %32.3 |
| **G** | Genito-Üriner Sistem ve Cinsiyet Hormonları | 119 | 62 | %52.1 |
| **H** | Sistemik Hormonal Preparatlar | 56 | 33 | %58.9 |
| **J** | Sistemik Antiinfektifler (Antibiyotikler vb.) | 442 | 183 | %41.4 |
| **L** | Antineoplastik ve İmmünomodülatör Ajanlar | 299 | 254 | %84.9 |
| **M** | Kas-İskelet Sistemi | 173 | 68 | %39.3 |
| **N** | Sinir Sistemi | 284 | 204 | %71.8 |
| **P** | Antiparaziter Ürünler | 31 | 19 | %61.3 |
| **R** | Solunum Sistemi | 219 | 89 | %40.6 |
| **S** | Duyu Organları | 90 | 38 | %42.2 |
| **V** | Çeşitli (Various) | 108 | 40 | %37.0 |

> **Not (ATC Dağılımı):** Tablo kapsam içi 2,945 etken maddeyi içerir. Kapsam dışı veya ATC atanmamış 120 bileşen tablodan hariç tutulmuştur; toplam etken madde 3,065'dir.

> **Önemli Not (Eşleşme Oranı vs. Etkileşim Kapsamı):** Tablodaki yüksek eşleşme oranları (örn. Sinir Sistemi %71.8), bu ilaçların DDInter kütüphanesinde kimlik olarak geçtiğini gösterir. Ancak DDInter indirme paketlerinde C, G, J, M, N, S gibi ana grupların bağımsız etkileşim dosyaları bulunmamaktadır. Bağımsız bir grup dosyasının bulunmaması, o gruptaki iki ilacın diğer kaynak dosyalarda birlikte yer almasını engellemez. Güncel yerel D05 sayımında N–N grubunda 481 benzersiz çift bulunuyor. Bu sayı, yukarıdaki tarihsel eşleme oranlarından farklı bir veri çıktısına dayanır. [D05 tam sayımı](IP6_Tablo20_ATC_Ciftleri.csv)

## 4. Yerel CSV’de eşleşmeyen ilk 30 kapsam içi bileşen

Yerel `data/interim/etken_madde.csv` dosyasında `kapsam_ici=1` ve `ddinter_id` boş olan satırlar seçildi. `urun_sayisi` azalan, eşitlikte `bilesen_tr` artan sırada ilk 30 satır alındı. İngilizce ad ve ATC alanları CSV’deki kayıtları gösterir. [Sayım CSV’si](IP3_Ilk30_Yerel_Sayim.csv)

| Sıra | Bileşen | Ürün sayısı | İngilizce ad | ATC |
|---:|---|---:|---|---|
| 1 | `dekstroz` | 720 | carbohydrates | B05BA03 |
| 2 | `sodyum laktat` | 315 | — | — |
| 3 | `glukoz` | 180 | carbohydrates | B05BA03 |
| 4 | `tiyokolsikosid` | 155 | thiocolchicoside | M03BX05 |
| 5 | `deksketoprofen` | 131 | dexketoprofen | M01AE17 |
| 6 | `kandesartan` | 103 | candesartan | C09CA06 |
| 7 | `glisin` | 100 | glycine | B05CX03 |
| 8 | `vildagliptin` | 87 | vildagliptin | A10BH02 |
| 9 | `l-losin` | 76 | — | — |
| 10 | `simetikon` | 63 | silicones | A03AX13 |
| 11 | `sulbaktam` | 62 | sulbactam | J01CG01 |
| 12 | `benzidamin` | 60 | benzydamine | A01AD02 |
| 13 | `metamizol` | 55 | metamizole sodium | N02BB02 |
| 14 | `gliklazid` | 54 | gliclazide | A10BB09 |
| 15 | `levotiroksin` | 54 | levothyroxine sodium | H03AA01 |
| 16 | `allergen extracts` | 53 | allergen extracts | — |
| 17 | `diuretics` | 51 | diuretics | C09BA04 |
| 18 | `glikoz` | 48 | — | — |
| 19 | `peritoneal dialytics` | 48 | peritoneal dialytics | — |
| 20 | `dapoksetin` | 47 | dapoxetine | G04BX14 |
| 21 | `mometazon` | 47 | mometasone | R01AD09 |
| 22 | `other cold preparations` | 47 | codeine and paracetamol | N02AJ06 |
| 23 | `carbohydrates` | 44 | carbohydrates | B05BA03 |
| 24 | `nimesulid` | 43 | nimesulide | M02AA26 |
| 25 | `aljinik asit` | 41 | alginic acid | A02BX13 |
| 26 | `enzyme inhibitor` | 41 | enzyme inhibitor | J01CR02 |
| 27 | `fusidik asit` | 41 | fusidic acid | D06AX01 |
| 28 | `beklometazon` | 40 | beclometasone | R01AD01 |
| 29 | `electrolytes with carbohydrates` | 40 | electrolytes with carbohydrates | B05BB02 |
| 30 | `tenofovir disoproksil` | 38 | tenofovir disoproxil | J05AF07 |
