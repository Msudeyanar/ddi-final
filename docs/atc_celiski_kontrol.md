# ATC Çelişki Kontrol Raporu — 20 Ürünlük İnceleme

> **Sayısal kaynak:** İlk 20 kayıt [Notebook 01, `c9_ornek_20`](../notebooks/01_titck_temizlik.ipynb#cell-id=c9_ornek_20) çıktısından, Kural 8 sayımları [`c8_atc_celiski`](../notebooks/01_titck_temizlik.ipynb#cell-id=c8_atc_celiski) hücresinden alınır. Ürün bazındaki WHO kaynakları Bölüm 5’tedir.

- **Proje:** Türkiye'deki ilaç verilerinin TİTCK Ruhsatlı İlaçlar Listesi ve SKRS E-Reçete Listesi üzerinden birleştirilmesi
- **Görev:** İP1 — `farkli_grup` sınıfından 20 ürünün incelenmesi
- **Sorumlular:** Kişi A ve Kişi C — Ortak inceleme
- **İnceleme Tarihi:** 20 Ekim 2026 (Güncellendi: Kasım 2026)
- **İnceleme Kapsamı:** `notebooks/01_titck_temizlik.ipynb` `[In[10]: Bölüm 9]` kod hücresinde `farkli_grup` sınıfından çekilen 20 ürünün TİTCK ve SKRS kaynaklarındaki barkod, ürün adı, etkin madde ve ATC kodlarının karşılaştırılması
> **📌 Örneklem Notu:** İncelenen 20 ürün, Notebook 01'deki `farkli_grup` sınıfının dosya sırasındaki ilk 20 kaydıdır (`head(20)`). Pilot nitelikteki bu inceleme Kural 8'in doğruluğunu teyit etmekte olup, portföyde pilot dışında 187 çelişki (202 − 15) kalmıştır.

---

## 1. Yöntem ve Güncellenmiş Karar Kuralı (Kural 8)

Proje yönergesindeki Kural 8 doğrultusunda ve danışman kararıyla yürürlüğe giren plan değişikliği uyarınca:
1. Ürünler barkodları üzerinden Ruhsatlı ve SKRS listelerinde eşleştirilir.
2. Kodlardan biri diğerinin başlangıcı / ön eki ise `duzey_farki` kabul edilir ve uzun kod seçilir (`atc_celiski = 0`).
3. Kodlar farklı grupta ise (`farkli_grup` veya `ayni_grup_farkli_madde`):
   - **WHO Kümülatif Değişiklik Kuralı:** Eski kod WHO'nun kümülatif değişiklik listesinde (`config/who_atc_degisiklik.csv`) diğer koda dönüştürülmüşse, SKRS'in taşıdığı yeni kod `atc_final` olarak kabul edilir ve çelişki kaldırılır (`atc_celiski = 0`, `atc_who_guncellendi = 1`).
   - **Diğer Çelişkiler (SKRS Hataları ve Endikasyon Farkları):** WHO listesinde karşılığı bulunmayan tüm diğer çelişkilerde resmî Ruhsatlı kod korunur ve kayıt `atc_celiski = 1` olarak işaretlenir (`atc_who_guncellendi = 0`). Bu ürünler Yol A (ATC köprüsü) yerine doğrudan etkin madde metniyle (Yol C/D) eşlenir.
4. TİTCK'nın orijinal ATC kodu `atc_ruhsat` sütununda her durumda korunur.

---

## 2. Notebook 01'den Alınan 20 Ürünün İnceleme Tablosu

Aşağıdaki tablo, `notebooks/01_titck_temizlik.ipynb` (In[10]: Bölüm 9) çıktısındaki `farkli_grup` sınıfından listelenen 20 ürünün detaylı klinik ve sınıflandırma incelemesini içermektedir:

| # | Barkod | Ürün Adı | Etkin Madde / Ham Metin | TİTCK ATC | SKRS ATC | İnceleme ve Çelişki Nedeni | Güncellenmiş Kural 8 Kararı |
|---|---|---|---|---|---|---|---|
| 1 | 8685073367001 | FLAGYL 500 MG FİLM TABLET | metronidazol | P01AB01 | J01XD01 | Endikasyon/kullanım ayrımı: P01AB antiparaziter (protozoa), J01XD sistemik imidazol antibakteriyeldir. WHO değişikliği değildir. | Ruhsatlı kod korunur (`P01AB01`); `atc_celiski = 1` |
| 2 | 8699548095603 | Femoston 1 mg/10 mg Film Tablet | Estradiol hemihidrat, Didrogesteron | G03FA14 | G03FB08 | G03FA sabit kombinasyon, G03FB sıralı (ardışık) rejimdir. WHO değişikliği değildir. | Ruhsatlı kod korunur (`G03FA14`); `atc_celiski = 1` |
| 3 | 8699548095610 | Femoston 2 mg/10 mg Film Tablet | Estradiol hemihidrat, Didrogesteron | G03FA14 | G03FB08 | Sıralı/sabit rejim kodlaması farkı. WHO değişikliği değildir. | Ruhsatlı kod korunur (`G03FA14`); `atc_celiski = 1` |
| 4 | 8699074090509 | Admiraz 1 mg Film Kaplı Tablet | Siponimod fumarik asit | L04AE03 | C09DX04 | **SKRS VERİ GİRİŞ HATASI:** Çoklu skleroz (MS) ilacı olan siponimoda SKRS sisteminde hipertansiyon ilacı olan `C09DX04` (valsartan ve sakubitril) ATC'si girilmiştir! | Ruhsatlı kod korunur (`L04AE03`); `atc_celiski = 1` |
| 5 | 8699717150010 | ATOMINEX 10 MG KAPSÜL | amoksetin hidroklorür | N06BA09 | J01CA04 | **SKRS VERİ GİRİŞ HATASI:** DEHB tedavisinde kullanılan atomoksetine (`N06BA09`) SKRS'te penisilin grubu antibiyotik olan amoksisilin (`J01CA04`) atanmıştır! | Ruhsatlı kod korunur (`N06BA09`); `atc_celiski = 1` |
| 6 | 8680150570268 | PEDITUS SURUP, 100 ML | other cold preparations | R05X | N02BE51 | Sınıflandırma farkı: TİTCK soğuk algınlığı kombinasyonu (`R05X`), SKRS parasetamol kombinasyonu (`N02BE51`) kodlamıştır. | Ruhsatlı kod korunur (`R05X`); `atc_celiski = 1` |
| 7 | 8681801091378 | EMEDUR 200 MG FILM TABLET | trimetobenzamid hcl | A04AD | R06AA10 | TİTCK antiemetik (`A04AD`), SKRS antihistaminik/antiemetik (`R06AA10`) vermiştir. WHO değişikliği değildir. | Ruhsatlı kod korunur (`A04AD`); `atc_celiski = 1` |
| 8 | 8699624770028 | Rystiggo 280 mg/2 ml Çözelti | Rozanolixizumab | L04AG16 | L04AL02 | **WHO GÜNCELLEMESİ (2026):** WHO, FcRn inhibitörleri için yeni `L04AL` grubunu oluşturmuş ve rozanolixizumab'ı `L04AG16`'dan `L04AL02`'ye taşımıştır. | WHO yeni kodu alınır (`L04AL02`); `atc_celiski = 0`; `atc_who_guncellendi = 1` |
| 9 | 8680150350112 | Nimejel Plus %1+ %5 Jel | Nimesulid, Lidokain | M02AA26 | D10AF05 | **SKRS VERİ GİRİŞ HATASI:** Topikal antiinflamatuar jöleye SKRS'te akne tedavisinde kullanılan nadifloksasin antibiyotik kodu (`D10AF05`) verilmiştir. | Ruhsatlı kod korunur (`M02AA26`); `atc_celiski = 1` |
| 10 | 8699578040079 | Bio-sidoz 1000 mg Tablet | Sodyum bikarbonat | A02AX | A02AH | TİTCK diğer antasitler (`A02AX`), SKRS sodyum bikarbonatlı antasitler (`A02AH`) tanımlamıştır. | Ruhsatlı kod korunur (`A02AX`); `atc_celiski = 1` |
| 11 | 8681801571429 | KONGEST PEDİATRİK ŞURUP | parasetamol, fenilnefrin, klorfeniramin | R05X | N02BE51 | Soğuk algınlığı kombinasyonu (`R05X`) vs Parasetamol kombinasyonu (`N02BE51`). | Ruhsatlı kod korunur (`R05X`); `atc_celiski = 1` |
| 12 | 8680150350082 | Capcial % 0,075 Krem | Kapsaisin | M02AB01 | N01BX04 | Topikal kas-eklem ağrısı preparatı (`M02AB01`) vs Lokal anestezik (`N01BX04`). | Ruhsatlı kod korunur (`M02AB01`); `atc_celiski = 1` |
| 13 | 8699578190019 | Bio-Sidoz 500 mg Kapsül | Sodyum bikarbonat | B05XA02 | A02AH | TİTCK elektrolit çözeltisi (`B05XA02`), SKRS antasit (`A02AH`) kodlamıştır. | Ruhsatlı kod korunur (`B05XA02`); `atc_celiski = 1` |
| 14 | 8681880090101 | Coldason Film Tablet | Parasetamol, Klorfeniramin, Psödoefedrin | R05X | N02BE51 | Kombinasyon sınıflandırma farkı. WHO değişikliği değildir. | Ruhsatlı kod korunur (`R05X`); `atc_celiski = 1` |
| 15 | 8699786770935 | Saphnelo 300 mg/2 mL Çözelti | Anifrolumab | L04AA51 | L04AG11 | **WHO GÜNCELLEMESİ (2024):** İmmünsüpresifler (`L04AA`) yeniden düzenlenmiş, anifrolumab yeni monoklonal antikor grubu `L04AG11`'e taşınmıştır. | WHO yeni kodu alınır (`L04AG11`); `atc_celiski = 0`; `atc_who_guncellendi = 1` |
| 16 | 8699540019614 | CONTUBEL %10 + %0,04 + %1 JEL | Soğan ekstresi, Heparin sodyum, Allantoin | DO3AX | D03AX | **TİTCK HARF HATASI:** TİTCK Ruhsatlı listesinde sıfır (0) yerine İngilizce 'O' harfi girilmiştir (`DO3AX`). WHO kümülatif listesinde yer almadığı için Kural 8 gereği Ruhsatlı kod korunmuş, çelişki olarak kalmıştır. | Ruhsatlı kod korunur (`DO3AX`); `atc_celiski = 1` (Açık sorular #17 kapsamında danışman onayıyla düzeltilecektir) |
| 17 | 8683962383149 | Pedizero Şurup, 100 ML | Parasetamol, Klorfeniramin maleat | R05X | N02BE51 | Kombinasyon sınıflandırma tercihi (`R05X` vs `N02BE51`). | Ruhsatlı kod korunur (`R05X`); `atc_celiski = 1` |
| 18 | 8699726156102 | ZEPOSİA 0,23 MG VE 0,46 MG | Ozanimod | L04AA38 | L04AE02 | **WHO GÜNCELLEMESİ (2024):** Ozanimod, genel immünsüpresanlardan (`L04AA38`) yeni sfingozin-1-fosfat (S1P) modülatörleri grubuna (`L04AE02`) taşınmıştır. | WHO yeni kodu alınır (`L04AE02`); `atc_celiski = 0`; `atc_who_guncellendi = 1` |
| 19 | 8699726156201 | ZEPOSİA 0,92 MG SERT KAPSÜL | Ozanimod | L04AA38 | L04AE02 | **WHO GÜNCELLEMESİ (2024):** Ozanimod için WHO resmi geçişi. SKRS yeni kodu taşımaktadır. | WHO yeni kodu alınır (`L04AE02`); `atc_celiski = 0`; `atc_who_guncellendi = 1` |
| 20 | 8699511099218 | TOFANZİ 5 MG FİLM TABLET | Tofasitinib sitrat | L04AA29 | L04AF01 | **WHO GÜNCELLEMESİ (2024):** Tofasitinib, genel immünsüpresanlardan (`L04AA29`) yeni Janus kinaz (JAK) inhibitörleri grubuna (`L04AF01`) taşınmıştır. | WHO yeni kodu alınır (`L04AF01`); `atc_celiski = 0`; `atc_who_guncellendi = 1` |

---

## 3. Bulgular ve Analitik Değerlendirme

### 3.1. WHO Tarafından Belgelenmiş Yapısal Güncellemeler (SKRS'in Haklı Olduğu Durumlar)
İncelenen 20 kayıtta Zeposia (Ozanimod), Tofanzi (Tofasitinib), Saphnelo (Anifrolumab) ve Rystiggo (Rozanolixizumab) ürünlerinde SKRS'in WHO Collaborating Centre for Drug Statistics Methodology tarafından yayımlanan güncel kodları taşıdığı doğrulanmıştır. 
Portföy genelinde de benzer şekilde **Gabapentin (N03AX12 → N02BF01)**, **Pregabalin (N03AX16 → N02BF02)**, **Leflunomid (L04AA13 → L04AK01)** ve **Belimumab (L04AA26 → L04AG04)** gibi maddelerin 2023 ve 2024 yıllarında yeni alt gruplara aktarıldığı belgelenmiştir. 
Bu ürünler için SKRS'teki yeni kodun alınması klinik açıdan zorunludur ve toplam 167 çelişkili ürün bu kural ile çözülmüştür.

### 3.2. SKRS Veri Giriş Hataları (Ruhsatlı Kodun Korunmasını Zorunlu Kılan Durumlar)
Tablodaki **4. madde (Admiraz - Siponimod)**, **5. madde (ATOMINEX - Atomoksetin)** ve **9. madde (Nimejel Plus)** örnekleri SKRS'in otomatik olarak üstün tutulamayacağını kanıtlamaktadır:
- **Admiraz (Siponimod):** Bir MS ilacı olmasına karşın SKRS'te hipertansiyon kombinasyonu (`C09DX04`) atanmıştır.
- **ATOMINEX (Atomoksetin):** Bir DEHB ilacı (noradrenalin geri alım inhibitörü) olmasına karşın SKRS'te antibiyotik amoksisilin (`J01CA04`) atanmıştır.
- **Nimejel Plus:** Bir antiinflamatuar kas jeli olmasına karşın SKRS'te akne antibiyotiği (`D10AF05`) atanmıştır.

Bu ölümcül veri hataları, **"SKRS kodu her zaman günceldir" varsayımının geçersiz olduğunu** ve danışman kararıyla getirilen *"Yalnızca WHO kümülatif değişiklik listesinde belgelenmiş olan kodlar yeniye çevrilir, diğer tüm çelişkilerde resmî Ruhsatlı kod korunur"* kuralının doğruluğunu tartışmasız biçimde ortaya koymaktadır.

---

## 4. Sonuç ve Mutabakat

1. Notebook 01'den gelen 20 ürünün incelemesi sonucunda 5 ürünün WHO güncellemesi olduğu doğrulanmış ve yeni kod seçilerek çelişki kaldırılmıştır (`atc_celiski = 0`, `atc_who_guncellendi = 1`). Kalan 15 ürün ise SKRS veri giriş hataları (Admiraz, ATOMINEX, Nimejel Plus), endikasyon/kombinasyon farklılıkları veya TİTCK yazım hatası (`DO3AX`) nedeniyle resmî Ruhsatlı kodda korunmuş ve çelişki olarak (`atc_celiski = 1`) işaretlenmiştir.
2. Tüm portföyde 369 çelişkinin **167 adedi WHO kuralıyla çözülmüş**, kalan **202 ürün ise güvenli tarafta kalınarak `atc_celiski = 1` ile işaretlenmiş** ve Yol A köprüsünden çıkarılmıştır.
3. İP1 kalite kriterleri ve Kural 8 çalışma mantığı pilot incelemede doğrulanmış; pilot dışında 187 çelişki kalmıştır. [Notebook 01, nihai sayım](../notebooks/01_titck_temizlik.ipynb#cell-id=c10_save_summary).


---

## 5. Kişi C İnceleme Notu

Notebook 01’de `farkli_grup` filtresi uygulandıktan sonra `head(20)` ile listelenen 20 kaydın barkodları ve TİTCK/SKRS ATC kod çiftleri raporla aynı sırada eşleşiyor.

### SKRS kod uyuşmazlıkları

- **Admiraz 1 mg (`8699074090509`).** TİTCK kodu `L04AE03` siponimoda karşılık geliyor. SKRS alanındaki `C09DX04`, valsartan ve sakubitril kombinasyonuna ait. [Siponimod](https://atcddd.fhi.no/atc_ddd_index/?code=L04AE03) · [Valsartan ve sakubitril](https://atcddd.fhi.no/atc_ddd_index/?code=C09DX04)
- **Atominex 10 mg (`8699717150010`).** TİTCK kodu `N06BA09` atomoksetine karşılık geliyor. SKRS alanındaki `J01CA04`, amoksisiline ait. Yerel kayıttaki `amoksetin hidroklorür` yazımı ürün bilgisine göre `atomoksetin hidroklorür` olarak düzeltilmeli. [Ürün bilgisi](https://www.sanofi.com/assets/countries/turkey/docs/products/prescription-products/A/atominex-10-mg-kapsul-kub.pdf) · [Atomoksetin](https://atcddd.fhi.no/atc_ddd_index/?code=N06BA09) · [Amoksisilin](https://atcddd.fhi.no/atc_ddd_index/?code=J01CA04)
- **Nimejel Plus %1 + %5 jel (`8680150350112`).** Ürün nimesulid ve lidokain içeriyor. TİTCK kodu `M02AA26` topikal nimesulide karşılık geliyor. SKRS alanındaki `D10AF05`, nadifloksasine ait. [Ürün bilgisi](https://www.titck.gov.tr/storage/Archive/2025/kubKtAttachments/nimejek1312ktrevBruhsatkesimonayli_26_03_2025.pdf) · [Nimesulid](https://atcddd.fhi.no/atc_ddd_index/?code=M02AA26) · [Nadifloksasin](https://atcddd.fhi.no/atc_ddd_index/?code=D10AF05)

Bu üç kayıt için Kural 8 uyarınca TİTCK kodunun korunmasını ve `atc_celiski = 1` olarak işaretlenmesini uygun buldum. İncelenen yerel `urun.csv` kopyası bu kararla uyumlu.

### WHO kod güncellemeleri

Rystiggo (`L04AG16` → `L04AL02`, 2026), Saphnelo (`L04AA51` → `L04AG11`, 2024), Zeposia’nın iki kaydı (`L04AA38` → `L04AE02`, 2024) ve Tofanzi (`L04AA29` → `L04AF01`, 2024) için kod geçişlerini ve yıllarını resmî listeden doğruladım. [WHO ATC değişiklik listesi](https://atcddd.fhi.no/atc_ddd_alterations__cumulative/atc_alterations/)

Notebook 01, 14 Ekim 2026 tarihli TİTCK ve SKRS çalışma kitaplarıyla yeniden çalıştırıldı. Yukarıdaki beş ürünün tamamında `atc_final` yeni kodu taşıdı, `atc_celiski = 0` ve `atc_who_guncellendi = 1` olarak doğrulandı. Portföy sayıları Notebook 01’in `c8_atc_celiski` (In[9]) ve `c10_save_summary` (In[11]) kod hücre çıktılarından alınmıştır. [Notebook 01](../notebooks/01_titck_temizlik.ipynb)
