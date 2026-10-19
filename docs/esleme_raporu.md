# İP3: DDInter İlaç Eşleşme Raporu

> **Özet:** Türkiye'deki kapsam içi etken maddelerin %46.1'i (1,378 / 2,988), kapsam içi ruhsatlı ürünlerin %76.5'inin (17,180 / 22,470) en az bir bileşeni DDInter'da bulunuyor.
> *(Tüm Bileşenler Bazında: %44.3 (1,378 / 3,111) — Tüm Ruhsatlı Ürünler Bazında: %76.7 (17,578 / 22,927))*

## 1. Yol Bazında Bileşen Sayısı ve DDInter Eşleşme Dağılımı
| Eşleşme Yolu | Toplam Bileşen | DDInter Eşleşen | Eşleşme Oranı (%) | Açıklama |
| :--- | :---: | :---: | :---: | :--- |
| **Yol A (Tek Bileşenli ATC)** | 1,922 | 1,232 | %64.1 | Tek bileşenli ürünlerin SKRS ATC sözlüğünden İngilizce adı |
| **Yol B (Kombine Bölme & RapidFuzz)** | 66 | 36 | %54.5 | Kombine ürünlerin ATC adından ayrıştırılan bileşenler |
| **Yol C (Kural Tabanlı - tr_en_kurallar)** | 78 | 78 | %100.0 | Türkçe kural tabanlı çeviri motoru ile eşleşenler |
| **SKRS (Kural 5/6)** | 90 | 32 | %35.6 | SKRS'ten doğrudan İngilizce gelen ürünler |
| **Eşleşmedi (Kişi C - Yol D Adayları)** | 955 | 0 | %0.0 | Kural motoru ve PubChem ile eşleşmeyip Kişi C uzman incelemesine kalanlar |
| **TOPLAM** | **3,111** | **1,378** | **%44.3** | TİTCK ruhsatlı listedeki tüm benzersiz bileşenler |

> **Not (PubChem Doğrulaması ve Dağılımı):** Adım 4 kapsamında en sık 100 eşleşmeyen kapsam içi bileşenden 16 tanesi PubChem eş anlamlılarıyla doğrudan DDInter kimliğine bağlanmış ve 24 satıra yayılmıştır. Örneğin 377 ürünlü parasetamol → DDInter14 (acetaminophen). Kurtarılan bu bileşikler resmi ATC adı ile DDInter adı farklılaşan Yol A ve Yol B satırlarıdır (bu nedenle Yol A/B altında DDInter kimliği kazanmışlardır). Kural motoruna girmeyip `eslesmedi` yolunda kalan 955 bileşenin en sık olanları (dekstroz, kalsiyum klorur, sodyum laktat, magnezyum klorur, tiyokolsikosid vb.) DDInter kütüphanesinde hiç yer almadığından bu gruptan yeni DDInter eşleşmesi çıkmamış ve tümü Kişi C'nin Yol D taslağına devredilmiştir.

## 2. DDInter Eşleşme Oranı Özeti
| Metrik Düzeyi | Toplam Büyüklük | DDInter'da Bulunan | Kapsama Oranı (%) |
| :--- | :---: | :---: | :--- |
| **Kapsam İçi Etken Madde Bazında** | 2,988 | 1,378 | %46.1 |
| **Kapsam İçi Ruhsatlı Ürün Bazında (En Az 1 Bileşen)** | 22,470 | 17,180 | %76.5 |
| **Tüm Etken Maddeler Bazında** | 3,111 | 1,378 | %44.3 |
| **Tüm Ruhsatlı Ürünler Bazında (En Az 1 Bileşen)** | 22,927 | 17,578 | %76.7 |

> **Not (Benzersiz İlaç Kimliği):** DDInter ile eşleşen 1,378 etken madde kaydı, toplam **852 benzersiz DDInter kimliğine** (`ddinter_id`) karşılık gelmektedir (örn. `vitamin d3` ve `kolekalsiferol` her ikisi de `DDInter367` kimliğine bağlanmıştır).

## 3. ATC Ana Grubuna Göre DDInter Eşleşme Oranı (14 Satır - Kapsam İçi)
| ATC Ana Grubu | Grup Açıklaması | Toplam Bileşen | DDInter Eşleşen | Eşleşme Oranı (%) |
| :---: | :--- | :---: | :--- | :---: |
| **A** | Sindirim Sistemi ve Metabolizma | 483 | 153 | %31.7 |
| **B** | Kan ve Kan Yapıcı Organlar | 260 | 79 | %30.4 |
| **C** | Kardiyovasküler Sistem | 215 | 120 | %55.8 |
| **D** | Dermatolojik İlaçlar | 198 | 61 | %30.8 |
| **G** | Genito-Üriner Sistem ve Cinsiyet Hormonları | 119 | 60 | %50.4 |
| **H** | Sistemik Hormonal Preparatlar | 57 | 31 | %54.4 |
| **J** | Sistemik Antiinfektifler (Antibiyotikler vb.) | 442 | 178 | %40.3 |
| **L** | Antineoplastik ve İmmünomodülatör Ajanlar | 299 | 251 | %83.9 |
| **M** | Kas-İskelet Sistemi | 178 | 66 | %37.1 |
| **N** | Sinir Sistemi | 288 | 201 | %69.8 |
| **P** | Antiparaziter Ürünler | 31 | 19 | %61.3 |
| **R** | Solunum Sistemi | 220 | 85 | %38.6 |
| **S** | Duyu Organları | 90 | 38 | %42.2 |
| **V** | Çeşitli (Various) | 108 | 36 | %33.3 |

> **Not (ATC Dağılımı):** Tablo kapsam içi 2,988 etken maddeyi içerir. Kapsam dışı veya ATC atanmamış 123 bileşen tablodan hariç tutulmuştur; toplam etken madde 3,111'dir.

> **Önemli Not (Eşleşme Oranı vs. Etkileşim Kapsamı):** Tablodaki yüksek eşleşme oranları (örn. Sinir Sistemi %69.8), bu ilaçların DDInter kütüphanesinde kimlik olarak geçtiğini gösterir. Ancak DDInter indirme paketlerinde C, G, J, M, N, S gibi ana grupların bağımsız etkileşim dosyaları bulunmamaktadır. Dolayısıyla bu gruptaki ilaçlar yalnızca diğer mevcut gruplarla (A, B, D, H, L, P, R, V) olan etkileşimlerde yer alabilir; iki N grubu ilacının kendi arasındaki etkileşim DDInter dosyalarında bulunamaz.

## 4. Eşleşmeyen En Sık 30 Bileşen Tablosu (Kişi C Öncelik Listesi - Kapsam İçi)
| Sıra | Türkçe Bileşen Adı | Ürün Sayısı | Önerilen İngilizce / ATC | Durum |
| :---: | :--- | :---: | :--- | :--- |
| 1 | `dekstroz` | 720 | carbohydrates (B05BA03) | Yol D Adayı |
| 2 | `kalsiyum klorur` | 400 | - (-) | Yol D Adayı |
| 3 | `hidroklorotiyazid` | 379 | - (-) | Yol D Adayı |
| 4 | `sodyum laktat` | 315 | - (-) | Yol D Adayı |
| 5 | `magnezyum klorur` | 293 | - (-) | Yol D Adayı |
| 6 | `glukoz` | 177 | carbohydrates (B05BA03) | Yol D Adayı |
| 7 | `tiyokolsikosid` | 155 | thiocolchicoside (M03BX05) | Yol D Adayı |
| 8 | `deksketoprofen` | 131 | dexketoprofen (M01AE17) | Yol D Adayı |
| 9 | `klavulanik asit` | 105 | - (-) | Yol D Adayı |
| 10 | `kandesartan` | 103 | candesartan (C09CA06) | Yol D Adayı |
| 11 | `glisin` | 100 | glycine (B05CX03) | Yol D Adayı |
| 12 | `vildagliptin` | 87 | vildagliptin (A10BH02) | Yol D Adayı |
| 13 | `l-losin` | 76 | - (-) | Yol D Adayı |
| 14 | `simetikon` | 63 | silicones (A03AX13) | Yol D Adayı |
| 15 | `combinations` | 62 | imidazoles/triazoles in combination with corticosteroids (D01AC20) | Yol D Adayı |
| 16 | `sulbaktam` | 62 | sulbactam (J01CG01) | Yol D Adayı |
| 17 | `benzidamin` | 60 | benzydamine (A01AD02) | Yol D Adayı |
| 18 | `klorheksidin` | 57 | - (-) | Yol D Adayı |
| 19 | `metamizol` | 55 | metamizole sodium (N02BB02) | Yol D Adayı |
| 20 | `gliklazid` | 54 | gliclazide (A10BB09) | Yol D Adayı |
| 21 | `levotiroksin` | 54 | levothyroxine sodium (H03AA01) | Yol D Adayı |
| 22 | `allergen extracts` | 53 | allergen extracts (-) | Yol D Adayı |
| 23 | `sodyum iyodur` | 53 | - (-) | Yol D Adayı |
| 24 | `diuretics` | 51 | diuretics (C09BA04) | Yol D Adayı |
| 25 | `glikoz` | 48 | - (-) | Yol D Adayı |
| 26 | `peritoneal dialytics` | 48 | peritoneal dialytics (-) | Yol D Adayı |
| 27 | `dapoksetin` | 47 | dapoxetine (G04BX14) | Yol D Adayı |
| 28 | `mometazon` | 47 | mometasone (R01AD09) | Yol D Adayı |
| 29 | `other cold preparations` | 47 | codeine and paracetamol (N02AJ06) | Yol D Adayı |
| 30 | `carbohydrates` | 44 | carbohydrates (B05BA03) | Yol D Adayı |
