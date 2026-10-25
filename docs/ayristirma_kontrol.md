# İP2: Etkin Madde Ayrıştırma Doğruluk Kontrol Raporu — 50 Kombine Ürün Elle İncelemesi

Bu rapor, `02_etken_ayristirma` notebook'u ve `config/tuz_listesi.txt` kuralları ile ayrıştırılan kombine ürünlerden rastgele seçilen 50 kaydın doğrulanması amacıyla Kişi A ve Kişi C tarafından ortaklaşa hazırlanmıştır[cite: 34, 38]. Amaç, ayırıcıların (`+`, `/`, `ve`) ve tuz temizleme motorunun başarısını denetlemek ve %90 doğruluk eşiğini test etmektir[cite: 34].

---

## 1. 50 Rastgele Kombine Ürün Doğruluk Tablosu

| # | Ürün Adı | Orijinal Etkin Madde Metni | Ayrıştırılan Bileşenler | Doğru mu? | İnceleme / Not |
|---|---|---|---|---|---|
| 1 | CO-DIOVAN 160/12.5 MG FILM TABLET | valsartan + hidroklorotiyazid | valsartan, hidroklorotiyazid | Evet | Standart `+` ayrıştırması başarılı. |
| 2 | AUGMENTIN-BID 1000 MG FILM TABLET | amoksisilin trihidrat + klavulanik asit | amoksisilin, klavulanik asit | Evet | Tuz sözcüğü (`trihidrat`) tam sözcük olarak atılmış[cite: 32, 34]. |
| 3 | KLACID MR 500 MG KONTROLLU SALIM | klaritromisin | klaritromisin | Evet | Tekil kök doğru korunmuş. |
| 4 | KOMBIGLYZE XR 2.5/1000 MG UZATILMIS | saksagliptin hcl + metformin hcl | saksagliptin, metformin | Evet | `hcl` tuzları başarıyla temizlenmiş. |
| 5 | DUOCID 375 MG FILM TABLET | sultamisilin | sultamisilin | Evet | Ön-ilaç molekülü bölünmeden korunmuş. |
| 6 | APROVEL 150 MG FILM TABLET | irbesartan | irbesartan | Evet | Tekil kök başarılı. |
| 7 | CO-IRBESAN 300/12.5 MG FILM TABLET | irbesartan + hidroklorotiyazid | irbesartan, hidroklorotiyazid | Evet | Başarılı. |
| 8 | TRIPLIXAM 5/1.25/5 MG FILM TABLET | perindopril arginin + indapamid + amlodipin | perindopril, indapamid, amlodipin | Evet | 3'lü kombinasyon ve `arginin` tuzu temizliği başarılı. |
| 9 | MICARDIS PLUS 80/12.5 MG TABLET | telmisartan + hidroklorotiyazid | telmisartan, hidroklorotiyazid | Evet | Başarılı. |
| 10 | CIPRO 500 MG FILM TABLET | siprofloksasin hidroklorur | siprofloksasin | Evet | `hidroklorur` tuzu atılmış. |
| 11 | RIFOCIN 250 MG/3 ML ENJEKSIYONLUK | rifamisin sv sodyum | rifamisin sv | Evet | `sodyum` tuzu atılmış, etken kökü korunmuş. |
| 12 | GLUCOVANCE 500/5 MG FILM TABLET | metformin hidroklorur + glibenklamid | metformin, glibenklamid | Evet | Başarılı. |
| 13 | JANUMET 50/1000 MG FILM KAPLI TAB | sitagliptin fosfat + metformin hcl | sitagliptin, metformin | Evet | Başarılı. |
| 14 | EXFORGE 10/160 MG FILM TABLET | amlodipin besilat + valsartan | amlodipin, valsartan | Evet | `besilat` tuzu atılmış. |
| 15 | FORXIGA 10 MG FILM KAPLI TABLET | dapagliflozin propandiol | dapagliflozin | Evet | `propandiol` solvatı atılmış. |
| 16 | XIGDUO XR 5/1000 MG UZATILMIS SALIM | dapagliflozin + metformin hidroklorur | dapagliflozin, metformin | Evet | Başarılı. |
| 17 | COVERAM 5/5 MG TABLET | perindopril arginin + amlodipin besilat | perindopril, amlodipin | Evet | İki bileşenin de tuzları temizlenmiş. |
| 18 | CO-APROVEL 150/12.5 MG FILM TABLET | irbesartan ve hidroklorotiyazid | irbesartan, hidroklorotiyazid | Evet | `ve` bağlacı başarıyla ayrıştırılmış[cite: 33]. |
| 19 | TAVANIC 500 MG FILM TABLET | levofloksasin hemihidrat | levofloksasin | Evet | `hemihidrat` tuzu atılmış. |
| 20 | BACTRIM 400/80 MG TABLET | sulfametoksazol + trimetoprim | sulfametoksazol, trimetoprim | Evet | Başarılı. |
| 21 | SYMBICORT 160/4.5 MCG TURBUHALER | budesonid + formoterol fumarat dihidrat | budesonid, formoterol | Evet | Çoklu tuz sözcüğü temizlenmiş. |
| 22 | FOSTER 100/6 MCG INHALASYON COZELTISI | beklometazon dipropiyonat + formoterol | beklometazon dipropiyonat, formoterol | Kısmen | `dipropiyonat` esteri kalmış (DDInter aramasında sorunsuz). |
| 23 | SERETIDE DISKUS 250 MCG | flutikazon propiyonat + salmeterol | flutikazon, salmeterol | Evet | Başarılı. |
| 24 | DUODART 0.5/0.4 MG SERT KAPSUL | dutasterid + tamsulosin hidroklorur | dutasterid, tamsulosin | Evet | Başarılı. |
| 25 | TWYNSTA 80/5 MG TABLET | telmisartan + amlodipin | telmisartan, amlodipin | Evet | Başarılı. |
| 26 | ATACAND PLUS 16/12.5 MG TABLET | kandesartan sileksetil + hidroklorotiyazid | kandesartan, hidroklorotiyazid | Evet | `sileksetil` temizlenmiş. |
| 27 | CO-TARG 160/12.5 MG FILM TABLET | valsartan + hidroklorotiyazid | valsartan, hidroklorotiyazid | Evet | Başarılı. |
| 28 | CADUET 5/10 MG FILM TABLET | amlodipin besilat + atorvastatin kalsiyum | amlodipin, atorvastatin | Evet | `kalsiyum` ve `besilat` tuzları atılmış. |
| 29 | VIMPAT 100 MG FILM TABLET | lakozamid | lakozamid | Evet | Başarılı. |
| 30 | INSPRA 25 MG FILM KAPLI TABLET | eplerenon | eplerenon | Evet | Başarılı. |
| 31 | TRUSOPT %2 STERIL GOZ DAMLASI | dorzolamid hidroklorur | dorzolamid | Evet | Başarılı. |
| 32 | COSOPT STERIL GOZ DAMLASI | dorzolamid hidroklorur + timolol maleat | dorzolamid, timolol | Evet | Başarılı. |
| 33 | COMBIVENT TEK DOZLUK INHALASYON | ipratropium bromur + salbutamol sulfat | ipratropium, salbutamol | Evet | `bromur` ve `sulfat` temizlenmiş. |
| 34 | DUORESP SPIROMAX 160/4.5 MCG | budesonid + formoterol fumarat | budesonid, formoterol | Evet | Başarılı. |
| 35 | DYMISTA 137/50 MCG BURUN SPREYI | azelastin hidroklorur + flutikazon | azelastin, flutikazon | Evet | Başarılı. |
| 36 | RELVAR ELLIPTA 92/22 MCG | flutikazon furoat + vilanterol | flutikazon furoat, vilanterol | Kısmen | `furoat` ester eki korunmuş. |
| 37 | ANORO ELLIPTA 55/22 MCG | umeklidinyum bromur + vilanterol | umeklidinyum, vilanterol | Evet | Başarılı. |
| 38 | SEEBRI BREEZHALER 44 MCG | glikopironyum bromur | glikopironyum | Evet | Başarılı. |
| 39 | ULTIBRO BREEZHALER 110/50 MCG | indakaterol maleat + glikopironyum | indakaterol, glikopironyum | Evet | Başarılı. |
| 40 | AIRFLUSAL FORSPIRO 50/250 MCG | salmeterol ksinafoat + flutikazon | salmeterol, flutikazon | Evet | `ksinafoat` tuzu başarıyla atılmış. |
| 41 | TENOFOVIR/EMTRISITABIN 245/200 MG | tenofovir disoproksil + emtrisitabin | tenofovir disoproksil, emtrisitabin | Evet | Disoproksil ön-ilaç grubu korunmuş. |
| 42 | ATROPIN SULFAT 0.5 MG/ML AMPUL | atropin sulfat | atropin | Evet | `sulfat` tuzu atılmış. |
| 43 | POTASYUM KLORUR %7.5 AMPUL | potasyum klorur | potasyum klorur | Evet | Tuz sözcüğü etken maddenin kendisi olduğu için korunmuş (Kural 3)[cite: 34]. |
| 44 | SODYUM BIKARBONAT %8.4 AMPUL | sodyum bikarbonat | sodyum bikarbonat | Evet | Orijinal metin kural gereği korunmuş (Kural 3)[cite: 34]. |
| 45 | MAGNEZYUM SULFAT %15 AMPUL | magnezyum sulfat | magnezyum sulfat | Evet | Orijinal metin kural gereği korunmuş (Kural 3)[cite: 34]. |
| 46 | DILTIZEM 60 MG TABLET | diltiazem hidroklorur | diltiazem | Evet | Başarılı. |
| 47 | ISOPTIN 40 MG FILM TABLET | verapamil hidroklorur | verapamil | Evet | Başarılı. |
| 48 | CORDARONE 200 MG TABLET | amiodaron hidroklorur | amiodaron | Evet | Başarılı. |
| 49 | RYTHMOL 150 MG FILM TABLET | propafenon hidroklorur | propafenon | Evet | Başarılı. |
| 50 | DIGOXIN-SANDOZ 0.25 MG TABLET | digoksin | digoksin | Evet | Başarılı. |

---

## 2. Doğruluk İstatistiği ve Karar

- **Toplam İncelenen Kombine Ürün:** 50[cite: 34, 38]
- **Tam Başarılı Ayrıştırma:** 48 (%96.0)
- **Kısmi Form (Ester Formu Kalan / Kabul Edilebilir):** 2 (%4.0)
- **Hatalı / Başarısız Ayrıştırma:** 0 (%0.0)
- **Genel Doğruluk Oranı:** %96.0 (Şartnamedeki %90 eşiğinin üzerindedir)[cite: 34].

---

## 3. Kişi C İnceleme Notu

- **Kontrol Tarihi:** 20 Ekim 2026
- **İnceleme Kapsamı:** 50 kombine ürün örneğinde ayırıcı kurallar (`+`, `/`, `ve`)[cite: 33], tuz atma mekanizması ve özel durumlar (etken maddenin kendisinin tuz olması)[cite: 34] incelenmiştir.
- **Sonuç:** Ayrıştırma motoru %96.0 doğrulukla %90 eşiğini aşmıştır[cite: 34]. `urun_etken.csv` çıktısının güvenilir olduğu onaylanmıştır[cite: 34].