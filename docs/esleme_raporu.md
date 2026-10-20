# Eşleme Raporu (İP3 — İngilizce köprü ve DDInter eşleme)

> Bu rapor `etken_madde.csv` (Yol A/B/C, tam eşleşme, PubChem sonrası hâli) ile Kişi C'nin Yol D sonuçlarının (`yol_d_sonuclari.csv`) birleştirilmesiyle hazırlandı. Yol D bölümü (1) Kişi C'ye, genel tablolar (2) Kişi B'ye aittir.

## Ana sonuç

**Türkiye'de ruhsatlı/SKRS'li ürünlerde geçen 3.073 benzersiz etken maddenin 1.392'i (%45,3) DDInter'da bulunuyor** (kapsam içi 2.958 bileşende %47,1). **Kapsam içi 22.906 ürünün 18.171'i (%79,3) en az bir DDInter'lı bileşen içeriyor** (yalnız ruhsatlı ürünlerde 17.976 / 22.493 = %79,9).

Yol D'nin katkısı: +27 bileşen (1.365 → 1.392), ürün bazında +789 ürün (17.382 → 18.171; %75,9 → %79,3).

DDInter'da bulunmayan bileşenler hata değil, raporlanacak sonuçtur (`ddinter_id` boş bırakıldı).

## 1. Yol D — elle eşleme (Kişi C)

### Yöntem

- Girdi: `ruhsatli_esleme_taslagi.csv` (1.708 eşleşmemiş bileşen). 115 satır `kapsam_ici=0` (V06/V07 ve 5+ bileşenli B05 ürünleri) olup dosyanın sonunda sırasız durduğu ve kapsam dışı olduğu için elemeye alınmadı. Kalan 1.593 bileşen `urun_sayisi`'na göre azalan sıralandı, **ilk 100'ü** incelendi (en küçük ürün sayısı 15).
- Her bileşen için etken madde Türkçe adı, ürün örneği ve ATC ipucuyla İngilizce karşılığı belirlendi ve `ddinter_ilac.csv` içinde (ad, tuz/ester yazımı, eş anlamlı) arandı. Bulunamayanlarda yakın adlar (ör. farklı tuz) **eşleştirilmedi**.
- Her satıra `yol` (D / eslesmedi), `ddinter_id`, `durum`, `guven` ve açıklama yazıldı. Kurallara uymayan durumlar varsayım yapılmadan `docs/acik_sorular.md`'ye alındı.
- Sınır notu: 15 ürünlük eşitlik grubunda 3 bileşen listeye girdi, 3'ü (rafine soya yağı, rokuronyum, sulpiride) dışarıda kaldı; bunlar ve 100–300 arası 3. haftaya devredilir.

### Sonuç özeti

| Sonuç | Bileşen | Ürün sayısı toplamı* |
|---|---:|---:|
| DDInter'da bulundu (Yol D) | 27 | 2742 |
| DDInter'da yok | 58 | 2378 |
| Madde değil (ATC grup adı / kaynak artefaktı) | 14 | 504 |
| Belirsiz (açık soru) | 1 | 21 |
| **Toplam** | **100** | **5645** |

*Ürün sayısı toplamı bileşen–ürün çifti sayısıdır; bir ürün birden çok bileşen taşıdığından benzersiz ürün sayısı değildir.

### Yol D ile eşleşen 27 bileşen

| Bileşen (TR) | Ürün | DDInter kimliği | DDInter adı | Güven |
|---|---:|---|---|---|
| dekstroz | 720 | DDInter529 | Dextrose, unspecified form | yuksek |
| kalsiyum klorur | 409 | DDInter272 | Calcium chloride | yuksek |
| hidroklorotiyazid | 379 | DDInter883 | Hydrochlorothiazide | yuksek |
| magnezyum klorur | 300 | DDInter1114 | Magnesium chloride | yuksek |
| glukoz | 180 | DDInter529 | Dextrose, unspecified form | yuksek |
| klavulanik asit | 105 | DDInter394 | Clavulanic acid | yuksek |
| simetikon | 63 | DDInter1674 | Simethicone | yuksek |
| klorheksidin | 57 | DDInter356 | Chlorhexidine | yuksek |
| levotiroksin | 54 | DDInter1064 | Levothyroxine | yuksek |
| sodyum iyodur | 53 | DDInter1689 | Sodium iodide | yuksek |
| glikoz | 48 | DDInter529 | Dextrose, unspecified form | yuksek |
| magnezyum karbonat | 41 | DDInter1113 | Magnesium carbonate | yuksek |
| beklometazon | 40 | DDInter168 | Beclomethasone dipropionate | orta |
| sodyum sitrat | 35 | DDInter1686 | Sodium citrate | yuksek |
| glutamik asit | 29 | DDInter830 | Glutamic acid | yuksek |
| dimetil | 22 | DDInter564 | Dimethyl fumarate | orta |
| entakapon | 22 | DDInter646 | Entacapone | yuksek |
| insan normal immunoglobulini | 22 | DDInter873 | Human immunoglobulin G (intravenous) | orta |
| benzoil peroksit | 21 | DDInter186 | Benzoyl peroxide (topical) | yuksek |
| glikopironyum | 21 | DDInter834 | Glycopyrronium | yuksek |
| somatropin | 21 | DDInter1699 | Somatotropin | yuksek |
| ginkgo biloba kuru ekstresi | 18 | DDInter819 | Ginkgo biloba | orta |
| brivarasetam | 17 | DDInter239 | Brivaracetam | yuksek |
| folinik asit | 17 | DDInter1041 | Leucovorin | yuksek |
| ksilometazolin | 17 | DDInter1952 | Xylometazoline (nasal) | yuksek |
| insulin aspart | 16 | DDInter929 | Insulin aspart (aspart) | yuksek |
| piperasilin | 15 | DDInter1474 | Piperacillin | yuksek |

Orta güvenli 4 eşleme (beklometazon, dimetil, insan normal immünoglobulini, ginkgo biloba) toplantıda onaylanmalıdır. Dekstroz, glukoz ve glikoz aynı kayda (DDInter529) gitti.

### DDInter'da bulunmayanlar (58 bileşen)

sodyum laktat (315), tiyokolsikosid (155), deksketoprofen (131), kandesartan (103), glisin (100), vildagliptin (87), l-losin (76), sulbaktam (62), benzidamin (60), metamizol (55), gliklazid (54), dapoksetin (47), mometazon (47), nimesulid (43), aljinik asit (41), fusidik asit (41), tenofovir disoproksil (38), sultamicillin (35), butamirat (32), pinaveryum (32), rafine zeytinyagi (32), rafine soya fasulyesi yagi (30), dekspantenol (28), karbidopa (28), ornidazol (28), izokonazol (27), naftifin (27), trimebutin (27), teikoplanin (26), tiamin (26), levodropropizin (25), ambroksol (24), dibazik sodyum fosfat heptahidrat (24), etofenamat (24), lerkanidipin (24), otilonyum (24), tirzepatid (24), diflukortolon (23), tenoksikam (23), demir iii hidroksit polimaltoz kompleksi (22), sultamisilin (21), insan albumini (20), polistiren sulfonat (20), iomeprol (19), lornoksikam (18), molibdat (18), trimetazidin (17), vitamin b1 (17), aspartam (16), betahistin (16), dexketoprofen (16), dobesilik asit (16), erdostein (16), fentikonazol (16), pertetnetat (16), pirasetam (16), gliclazide (15), mentol (15).

### Madde olmayan kayıtlar (14 bileşen, bileşen değil)

combinations (62), allergen extracts (53), diuretics (51), peritoneal dialytics (48), other cold preparations (47), carbohydrates (44), enzyme inhibitor (41), electrolytes with carbohydrates (40), hypertonic solutions (29), hemofiltrates (21), amino acids (20), combinations excl. psycholeptics (16), electrolytes (16), hemodialytics (16).

Bunlar gerçek madde değil, ATC grup adlarıdır. Ruhsat/SKRS etkin madde metnine ATC adı yazıldığı için bileşen olarak ayrılmışlardır. Etkilerinden biri, bazı ürünlerin gerçek bileşeninin (ör. olmesartan+**diüretik**, piperasilin+**enzim inhibitörü**) hiç aranamamasıdır; önerisi A'ya iletilen aşağıdaki listededir.

### Yol D'nin ortaya çıkardığı veri sorunları (A ve B'ye iade)

1. **`tuz_at()` hatası (A, İP2):** `dimetil fumarat` → `dimetil` olmuş (22 ürün, TECFIDERA). `fumarat` tuz listesinde olduğundan atılmış; geriye kalan metin etken maddenin kendisi olduğu için orijinal korunmalıydı.
2. **Yazım varyantları ayrı bileşen sayılmış (B ve A):** deksketoprofen/dexketoprofen (131+16), gliklazid/gliclazide (54+15), sultamisilin/sultamicillin (21+35), glukoz/glikoz/dekstroz (180+48+720), tiamin/vitamin b1 (26+17). Birleştirilirse bileşen sayısı ve ürün bazlı sayılar değişir.
3. **ATC grup adları bileşen olarak girmiş (A):** 14 kayıt (yukarıdaki liste). `Yol B`'nin `enzyme inhibitor` ve `diuretics` parçaları da bu sınıfta.
4. **Kaynak veri hataları:** `dekstran monohidrat` ("%5 dekstroz" ürünlerinde, muhtemelen dekstroz); `tirzepatid` için taslakta `ad_en = tirzepadite` yazım hatası; `aspartam` (SANPA tabletleri, ATC A10X) etken maddesi doğrulanmalı.
5. **Taslak dosyası sıralaması:** `kapsam_ici=0` satırlar dosyanın sonunda ve sırasız (ör. `other non therapeutic auxiliary products` 258 ürünle sonda). Sıralama yapılırken kapsam filtresi uygulanmalı.

## 2. Yol bazında bileşen sayısı (Yol D sonrası)

| Yol | Bileşen | DDInter'lı | Oran |
|---|---:|---:|---:|
| A | 1893 | 1219 | %64,4 |
| B | 66 | 36 | %54,5 |
| C | 78 | 78 | %100,0 |
| D | 27 | 27 | %100,0 |
| SKRS | 90 | 32 | %35,6 |
| eslesmedi | 919 | 0 | %0,0 |
| **Toplam** | **3073** | **1392** | **%45,3** |

A ve B'de İngilizce ad bulunup DDInter'da yer almayan bileşenler eşleşmemiş sayılır. Yol C'nin 78 bileşeninin tamamı DDInter'lıdır, çünkü kural motoru yalnızca birebir bulunan sonuçları kabul eder. 24+16 bileşen PubChem eş anlamlısıyla bulundu.

## 3. DDInter eşleşme oranı

| Ölçüt | Payda | DDInter'lı | Oran | Yol D öncesi |
|---|---:|---:|---:|---:|
| Benzersiz etken madde (tümü) | 3073 | 1392 | %45,3 | %44,4 |
| Benzersiz etken madde (kapsam içi) | 2958 | 1392 | %47,1 | %46,1 |
| Ürün (kapsam içi, ≥1 DDInter'lı bileşen) | 22906 | 18171 | %79,3 | %75,9 |
| Ruhsatlı ürün (kapsam içi) | 22493 | 17976 | %79,9 | %76,4 |

Ürün bazında hesap `urun.csv` (`kapsam_disi=0`) ve `urun_etken.csv` ile yapıldı; ürünün **en az bir** bileşeni DDInter'daysa sayıldı. Çok bileşenli ürünlerde bu oran, tüm bileşenlerinin bulunduğu ürünlerin oranından yüksektir.

## 4. ATC ana grubuna göre eşleşme oranı

| ATC ana | Bileşen | DDInter'lı | Oran | Yol D öncesi |
|---|---:|---:|---:|---:|
| A | 470 | 149 | %31,7 | %30,9 |
| B | 356 | 86 | %24,2 | %22,2 |
| C | 215 | 121 | %56,3 | %55,8 |
| D | 192 | 62 | %32,3 | %31,8 |
| G | 119 | 60 | %50,4 | %50,4 |
| H | 56 | 32 | %57,1 | %53,6 |
| J | 443 | 182 | %41,1 | %40,4 |
| L | 299 | 252 | %84,3 | %83,9 |
| M | 173 | 64 | %37,0 | %37,0 |
| N | 285 | 201 | %70,5 | %69,5 |
| P | 31 | 19 | %61,3 | %61,3 |
| R | 220 | 88 | %40,0 | %38,6 |
| S | 90 | 38 | %42,2 | %42,2 |
| V | 124 | 38 | %30,6 | %29,0 |

`atc_ana` `etken_madde.csv` içindeki hâliyle alındı. DDInter, L (antineoplastik) ve N (sinir sistemi) grubunda güçlü, B (kan ve sıvılar), A ve V'de zayıftır.

## 5. Eşleşmeyen en sık 30 bileşen (kapsam içi)

| # | Bileşen | Ürün | ATC | Neden |
|---:|---|---:|---|---|
| 1 | sodyum laktat | 315 |  | DDInter'da yok |
| 2 | tiyokolsikosid | 155 | M03BX05 | DDInter'da yok |
| 3 | deksketoprofen | 131 | M01AE17 | DDInter'da yok |
| 4 | kandesartan | 103 | C09CA06 | DDInter'da yok |
| 5 | glisin | 100 | B05CX03 | DDInter'da yok |
| 6 | vildagliptin | 87 | A10BH02 | DDInter'da yok |
| 7 | l-losin | 76 |  | DDInter'da yok |
| 8 | combinations | 62 | D01AC20 | Madde değil |
| 9 | sulbaktam | 62 | J01CG01 | DDInter'da yok |
| 10 | benzidamin | 60 | A01AD02 | DDInter'da yok |
| 11 | metamizol | 55 | N02BB02 | DDInter'da yok |
| 12 | gliklazid | 54 | A10BB09 | DDInter'da yok |
| 13 | allergen extracts | 53 |  | Madde değil |
| 14 | diuretics | 51 | C09BA04 | Madde değil |
| 15 | peritoneal dialytics | 48 |  | Madde değil |
| 16 | dapoksetin | 47 | G04BX14 | DDInter'da yok |
| 17 | mometazon | 47 | R01AD09 | DDInter'da yok |
| 18 | other cold preparations | 47 | N02AJ06 | Madde değil |
| 19 | carbohydrates | 44 | B05BA03 | Madde değil |
| 20 | nimesulid | 43 | M02AA26 | DDInter'da yok |
| 21 | aljinik asit | 41 | A02BX13 | DDInter'da yok |
| 22 | enzyme inhibitor | 41 | J01CR02 | Madde değil |
| 23 | fusidik asit | 41 | D06AX01 | DDInter'da yok |
| 24 | electrolytes with carbohydrates | 40 | B05BB02 | Madde değil |
| 25 | tenofovir disoproksil | 38 | J05AF07 | DDInter'da yok |
| 26 | sultamicillin | 35 | J01CR04 | DDInter'da yok |
| 27 | butamirat | 32 | R05DB13 | DDInter'da yok |
| 28 | pinaveryum | 32 | A03AX04 | DDInter'da yok |
| 29 | rafine zeytinyagi | 32 |  | DDInter'da yok |
| 30 | rafine soya fasulyesi yagi | 30 |  | DDInter'da yok |

Kapsam içi 1.566 bileşen DDInter'sız kaldı; bunun 1.493'i Yol D'de henüz incelenmedi (ürün sayısı ≤15, 3. haftaya devredilir). Kapsam dışı 115 bileşen bu tablolara girmez.

## Dosyalar
- `yol_d_sonuclari.csv`: 100 satır, Kişi C → Kişi B (Gün 6).
- `etken_madde_yol_d_birlesik.csv`: B'nin `etken_madde.csv`'sine Yol D uygulanmış hâli (27 satırda `yol=D`, `eslesme_kaynagi=yol_d_elle`).
- `docs/acik_sorular.md`: toplantıda sorulacak durumlar.
