# İP3: DDInter İlaç Eşleşme Raporu

> **Özet:** Türkiye'deki kapsam içi etken maddelerin %48.1'i (1,416 / 2,945), kapsam içi ruhsatlı ürünlerin %80.4'inin (18,067 / 22,470) en az bir bileşeni DDInter'da bulunuyor.
> *(Tüm Bileşenler Bazında: %46.3 (1,418 / 3,065) — Tüm Ruhsatlı Ürünler Bazında: %80.6 (18,474 / 22,927))*

## 1. Yol Bazında Bileşen Sayısı ve DDInter Eşleşme Dağılımı
| Eşleşme Yolu | Toplam Bileşen | DDInter Eşleşen | Eşleşme Oranı (%) | Açıklama |
| :--- | :---: | :---: | :---: | :--- |
| **Yol A (Tek Bileşenli ATC)** | 1,887 | 1,219 | %64.6 | Tek bileşenli ürünlerin SKRS ATC sözlüğünden İngilizce adı |
| **Yol B (Kombine Bölme & RapidFuzz)** | 66 | 36 | %54.5 | Kombine ürünlerin ATC adından ayrıştırılan bileşenler |
| **Yol C (Kural Tabanlı - tr_en_kurallar)** | 106 | 106 | %100.0 | Türkçe kural tabanlı çeviri motoru ile eşleşenler |
| **SKRS (Kural 5/6)** | 90 | 32 | %35.6 | SKRS'ten doğrudan İngilizce gelen ürünler |
| **Yol D (Kişi C - Uzman Manuel İnceleme)** | 24 | 24 | %100.0 | Kişi C tarafından en sık eşleşmeyenlerden doğrulanarak bağlanan bileşenler |
| **Eşleşmedi (Kalan)** | 892 | 1 | %0.1 | Kural motoru ve Yol D sonrasında eşleşmeyen bileşenler |
| **TOPLAM** | **3,065** | **1,418** | **%46.3** | TİTCK ruhsatlı listedeki tüm benzersiz bileşenler |
> **Not (Yol D ve PubChem Doğrulaması):** Adım 4 kapsamında en sık 100 eşleşmeyen kapsam içi bileşenden 17 tanesi PubChem eş anlamlılarıyla doğrudan DDInter kimliğine bağlanmış ve 24 satıra yayılmıştır. Örneğin 376 ürünlü parasetamol → DDInter14 (acetaminophen). Adım 5 kapsamında ise Kişi C tarafından en sık 100 eşleşmeyen bileşen incelenmiş; 23 bileşen DDInter kimliklerine bağlanmış ve 20 İngilizce ad düzeltmesi yapılarak toplam 24 bileşen Yol D statüsüne kavuşturulmuştur. Kalan 892 bileşen sonraki aşamalara devredilmiştir.

## 2. DDInter Eşleşme Oranı Özeti
| Metrik Düzeyi | Toplam Büyüklük | DDInter'da Bulunan | Kapsama Oranı (%) |
| :--- | :---: | :---: | :--- |
| **Kapsam İçi Etken Madde Bazında** | 2,945 | 1,416 | %48.1 |
| **Kapsam İçi Ruhsatlı Ürün Bazında (En Az 1 Bileşen)** | 22,470 | 18,067 | %80.4 |
| **Tüm Etken Maddeler Bazında** | 3,065 | 1,418 | %46.3 |
| **Tüm Ruhsatlı Ürünler Bazında (En Az 1 Bileşen)** | 22,927 | 18,474 | %80.6 |

> **Not (Benzersiz İlaç Kimliği):** DDInter ile eşleşen 1,418 etken madde kaydı, toplam **896 benzersiz DDInter kimliğine** (`ddinter_id`) karşılık gelmektedir (örn. `vitamin d3` ve `kolekalsiferol` her ikisi de `DDInter367` kimliğine bağlanmıştır).

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
| **L** | Antineoplastik ve İmmünomodülatör Ajanlar | 299 | 252 | %84.3 |
| **M** | Kas-İskelet Sistemi | 173 | 68 | %39.3 |
| **N** | Sinir Sistemi | 284 | 204 | %71.8 |
| **P** | Antiparaziter Ürünler | 31 | 19 | %61.3 |
| **R** | Solunum Sistemi | 219 | 89 | %40.6 |
| **S** | Duyu Organları | 90 | 38 | %42.2 |
| **V** | Çeşitli (Various) | 108 | 40 | %37.0 |

> **Not (ATC Dağılımı):** Tablo kapsam içi 2,945 etken maddeyi içerir. Kapsam dışı veya ATC atanmamış 120 bileşen tablodan hariç tutulmuştur; toplam etken madde 3,065'dir.

> **Önemli Not (Eşleşme Oranı vs. Etkileşim Kapsamı):** Tablodaki yüksek eşleşme oranları (örn. Sinir Sistemi %71.8), bu ilaçların DDInter kütüphanesinde kimlik olarak geçtiğini gösterir. Ancak DDInter indirme paketlerinde C, G, J, M, N, S gibi ana grupların bağımsız etkileşim dosyaları bulunmamaktadır. Dolayısıyla bu gruptaki ilaçlar yalnızca diğer mevcut gruplarla (A, B, D, H, L, P, R, V) olan etkileşimlerde yer alabilir; iki N grubu ilacının kendi arasındaki etkileşim DDInter dosyalarında bulunamaz.

## 4. Eşleşmeyen En Sık 30 Bileşen Tablosu (Kişi C Öncelik Listesi - Kapsam İçi)
| Sıra | Türkçe Bileşen Adı | Ürün Sayısı | Önerilen İngilizce / ATC | Durum |
| :---: | :--- | :---: | :--- | :--- |
| 1 | `sodyum laktat` | 315 | - (-) | Eşleşmedi |
| 2 | `tiyokolsikosid` | 155 | thiocolchicoside (M03BX05) | Eşleşmedi |
| 3 | `deksketoprofen` | 131 | dexketoprofen (M01AE17) | Eşleşmedi |
| 4 | `kandesartan` | 103 | candesartan (C09CA06) | Eşleşmedi |
| 5 | `glisin` | 100 | glycine (B05CX03) | Eşleşmedi |
| 6 | `vildagliptin` | 87 | vildagliptin (A10BH02) | Eşleşmedi |
| 7 | `l-losin` | 76 | - (-) | Eşleşmedi |
| 8 | `sulbaktam` | 62 | sulbactam (J01CG01) | Eşleşmedi |
| 9 | `benzidamin` | 60 | benzydamine (A01AD02) | Eşleşmedi |
| 10 | `metamizol` | 55 | metamizole (N02BB02) | Eşleşmedi |
| 11 | `gliklazid` | 54 | gliclazide (A10BB09) | Eşleşmedi |
| 12 | `allergen extracts` | 53 | allergen extracts (-) | Eşleşmedi |
| 13 | `diuretics` | 51 | diuretics (C09BA04) | Eşleşmedi |
| 14 | `peritoneal dialytics` | 48 | peritoneal dialytics (-) | Eşleşmedi |
| 15 | `dapoksetin` | 47 | dapoxetine (G04BX14) | Eşleşmedi |
| 16 | `mometazon` | 47 | mometasone (R01AD09) | Eşleşmedi |
| 17 | `other cold preparations` | 47 | codeine and paracetamol (N02AJ06) | Eşleşmedi |
| 18 | `carbohydrates` | 44 | carbohydrates (B05BA03) | Eşleşmedi |
| 19 | `nimesulid` | 43 | nimesulide (M02AA26) | Eşleşmedi |
| 20 | `aljinik asit` | 41 | alginic acid (A02BX13) | Eşleşmedi |
| 21 | `enzyme inhibitor` | 41 | enzyme inhibitor (J01CR02) | Eşleşmedi |
| 22 | `fusidik asit` | 41 | fusidic acid (D06AX01) | Eşleşmedi |
| 23 | `electrolytes with carbohydrates` | 40 | electrolytes with carbohydrates (B05BB02) | Eşleşmedi |
| 24 | `tenofovir disoproksil` | 38 | tenofovir disoproxil (J05AF07) | Eşleşmedi |
| 25 | `sultamicillin` | 35 | sultamicillin (J01CR04) | Eşleşmedi |
| 26 | `butamirat` | 32 | butamirate (R05DB13) | Eşleşmedi |
| 27 | `pinaveryum` | 32 | pinaverium (A03AX04) | Eşleşmedi |
| 28 | `hypertonic solutions` | 29 | - (-) | Eşleşmedi |
| 29 | `dekspantenol` | 28 | dexpanthenol (D03AX03) | Eşleşmedi |
| 30 | `karbidopa` | 28 | - (-) | Eşleşmedi |
