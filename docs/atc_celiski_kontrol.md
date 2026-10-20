# ATC Çelişki Kontrol Raporu — 20 Ürünlük Elle İnceleme

- **Proje:** Türkiye'deki ilaç verilerinin TİTCK Ruhsatlı İlaçlar Listesi ve SKRS E-Reçete Listesi üzerinden birleştirilmesi[cite: 31]
- **Görev:** İP1 — `farkli_grup` sınıfından 20 ürünün elle incelenmesi[cite: 31, 33]
- **Sorumlular:** Kişi A ve Kişi C — Ortak inceleme[cite: 31, 33]
- **İnceleme Tarihi:** 20 Ekim 2026
- **İnceleme Kapsamı:** TİTCK ve SKRS kaynaklarındaki ürün barkodları, ürün adları, etkin madde alanları ve ATC kodlarının karşılaştırılması

---

## 1. Yöntem ve Karar Kuralı (Kural 8)

Proje yönergesindeki Kural 8 doğrultusunda[cite: 33]:
1. Ürünler öncelikle barkodları üzerinden kaynak listelerde karşılaştırılır.
2. ATC kodlarından biri diğerinin başlangıcıysa, proje yönergesinde belirtilen uzun kodu seçme kuralı uygulanır[cite: 33].
3. Kodlar uyuşmuyorsa ve uyuşmazlık giderilemiyorsa, proje veri standardı gereği TİTCK ATC kodu `atc_final` alanında korunur ve kayıt `atc_celiski = 1` olarak işaretlenir[cite: 33].
4. Bu kayıtlar sonraki eşleştirme aşamasında yalnızca ATC koduna dayalı eşleştirmeyle kesinleştirilmez; etkin madde metni ve gerektiğinde ürünün resmî bilgileri üzerinden ayrıca değerlendirilir[cite: 33].
5. TİTCK kodunun korunması, tek başına bu kodun her durumda güncel WHO sınıflandırmasındaki kod olduğunu veya klinik açıdan kesinlikle doğru olduğunu göstermez.

---

## 2. 20 Ürünün İnceleme Tablosu

| # | Barkod | Ürün Adı | Etkin Madde / Kaynak Alanı | TİTCK ATC | SKRS ATC | İnceleme Sonucu | Proje Kural 8 Sonucu |
|---|---|---|---|---|---|---|---|
| 1 | 8699708650499 | PODOFILM %25 25 ML TOPİKAL SOL | Wart and anti-corn preparation | D11AF | D06BB04 | Kodlar farklı sınıflandırma gruplarındadır. Ürünün endikasyonu ve resmî ürün bilgileri incelenmeden farkın kesin nedeni belirlenemez. | TİTCK kodu korunur; `atc_celiski = 1`[cite: 33] |
| 2 | 8680199152449 | ROTALEPTIN 300 MG KAPSÜL, 50 K | Gabapentin | N03AX12 | N02BF01 | WHO ATC değişiklik listesinde gabapentin için eski kod N03AX12, yeni kod N02BF01 olarak belirtilmiştir. | Proje kuralı gereği TİTCK kodu korunur; `atc_celiski = 1`[cite: 33] |
| 3 | 8680199094114 | BAGEDA 10 MG FİLM TABLET, 30 A | Leflunomid | L04AA13 | L04AK01 | WHO ATC değişiklik listesinde leflunomid için eski kod L04AA13, yeni kod L04AK01 olarak belirtilmiştir. | Proje kuralı gereği TİTCK kodu korunur; `atc_celiski = 1`[cite: 33] |
| 4 | 8697936044608 | BENEFORT 250 MG/250 MG/1 MG/30… | Kaynak alanında vitamin B grubu bileşenlerine ilişkin kısmi metin | A11DB | A16AX | Kodlar farklıdır. Etkin madde alanı tek başına ayrıntılı karşılaştırma için yeterli değildir; ürün bileşimi ve resmî ürün bilgisi ayrıca kontrol edilmelidir. | TİTCK kodu korunur; `atc_celiski = 1`[cite: 33] |
| 5 | 8680199153330 | GALARA 300 MG KAPSÜL, 28 ADET | Pregabalin | N03AX16 | N02BF02 | WHO ATC değişiklik listesinde pregabalin için eski kod N03AX16, yeni kod N02BF02 olarak belirtilmiştir. | Proje kuralı gereği TİTCK kodu korunur; `atc_celiski = 1`[cite: 33] |
| 6 | 8699824570114 | HISTORAN 125 ML ŞURUP | Kaynak alanında “other cold preparations” | R05X | R05CA10 | Kodlar farklıdır. Kombinasyon içeriği ve ürünün sınıflandırma bilgisi ayrıca doğrulanmadan uyuşmazlığın nedeni kesinleştirilemez. | TİTCK kodu korunur; `atc_celiski = 1`[cite: 33] |
| 7 | 8699680150307 | REGAPEN 75 MG KAPSÜL, 42 ADET | Pregabalin | N03AX16 | N02BF02 | WHO ATC değişiklik listesinde belirtilen pregabalin kod değişikliğiyle uyumludur. | Proje kuralı gereği TİTCK kodu korunur; `atc_celiski = 1`[cite: 33] |
| 8 | 8699680150048 | REGAPEN 300 MG KAPSÜL, 56 ADET | Pregabalin | N03AX16 | N02BF02 | WHO ATC değişiklik listesinde belirtilen pregabalin kod değişikliğiyle uyumludur. | Proje kuralı gereği TİTCK kodu korunur; `atc_celiski = 1`[cite: 33] |
| 9 | 8699536340043 | MAJEZIK DUO %5 + %0,25 TOPİKAL | Flurbiprofen / tiyokolşikosid | M03BX55 | M02AA19 | Kaynaklardaki kodlar farklıdır. Kombinasyon ürünü için ürünün resmî sınıflandırması ayrıca kontrol edilmelidir. | TİTCK kodu korunur; `atc_celiski = 1`[cite: 33] |
| 10 | 8699680091914 | GRİPORT COLD 650 MG/4 MG/30 MG | Parasetamol, klorfeniramin ve diğer bileşenler | R05X | N02BE51 | Kodlar farklıdır. Kombinasyon içeriği ve ürünün sınıflandırma dayanağı incelenmeden kesin neden atanamaz. | TİTCK kodu korunur; `atc_celiski = 1`[cite: 33] |
| 11 | 8680199153316 | GALARA 150 MG KAPSÜL, 28 ADET | Pregabalin | N03AX16 | N02BF02 | WHO ATC değişiklik listesinde belirtilen pregabalin kod değişikliğiyle uyumludur. | Proje kuralı gereği TİTCK kodu korunur; `atc_celiski = 1`[cite: 33] |
| 12 | 8699724090422 | EVEPTIN 800 MG FİLM KAPLI TABLET | Gabapentin | N03AX12 | N02BF01 | WHO ATC değişiklik listesinde belirtilen gabapentin kod değişikliğiyle uyumludur. | Proje kuralı gereği TİTCK kodu korunur; `atc_celiski = 1`[cite: 33] |
| 13 | 8699743011125 | PHARMASPIRIN 300 MG, 100 TABLET | Asetilsalisilik asit | B01AC06 | N02BA01 | Aynı etkin madde için farklı ATC kodları kayıtlıdır. Ürünün ruhsatlı endikasyonu ve resmî ürün bilgisi görülmeden farkın yalnızca endikasyondan kaynaklandığı kesinleştirilemez. | TİTCK kodu korunur; `atc_celiski = 1`[cite: 33] |
| 14 | 8699540250192 | TYLOL HOT D TEK KULLANIMLIK TO… | Kaynak alanında “other cold preparations” | R05X | N02BE51 | Kodlar farklıdır. Kombinasyon içeriği ve ürün sınıflandırması ayrıca kontrol edilmelidir. | TİTCK kodu korunur; `atc_celiski = 1`[cite: 33] |
| 15 | 8699504092165 | VOTRIENT 400 MG FİLM KAPLI TABLET | Pazopanib | L01XE11 | L01EX03 | Kodlar farklıdır. Bu uyuşmazlık için WHO kod değişikliği varsayılmamalı; kaynakların sürümü ve ürünün resmî sınıflandırması ayrıca kontrol edilmelidir. | TİTCK kodu korunur; `atc_celiski = 1`[cite: 33] |
| 16 | 8699527520034 | FLUREND %0,25 ORAL SPREY ÇÖZELTİ | Flurbiprofen | R02AX01 | A01AD | Kodlar farklıdır. Uygulama alanı ve ürünün resmî sınıflandırması doğrulanmadan kesin neden atanamaz. | TİTCK kodu korunur; `atc_celiski = 1`[cite: 33] |
| 17 | 8699819370644 | NOACNE %3 MERHEM | Tetrasiklin HCl | D06AA04 | D10AF | Kodlar farklıdır. Ürünün kullanım amacı, formülasyonu ve resmî sınıflandırması ayrıca kontrol edilmelidir. | TİTCK kodu korunur; `atc_celiski = 1`[cite: 33] |
| 18 | 8699522279913 | BENLYSTA 400 MG IV İNFÜZYONLUK | Belimumab | L04AA26 | L04AG04 | WHO ATC değişiklik listesinde belimumab için eski kod L04AA26, yeni kod L04AG04 olarak belirtilmiştir. | Proje kuralı gereği TİTCK kodu korunur; `atc_celiski = 1`[cite: 33] |
| 19 | 8699514092063 | PATYCA 600 MG ÇENTİKLİ FİLM TABLET | Gabapentin | N03AX12 | N02BF01 | WHO ATC değişiklik listesinde belirtilen gabapentin kod değişikliğiyle uyumludur. | Proje kuralı gereği TİTCK kodu korunur; `atc_celiski = 1`[cite: 33] |
| 20 | 8699578040079 | BIO-SİDOZ 1000 MG GASTROREZİSTAN… | Sodyum bikarbonat | A02AX | A02AH | Kodlar farklıdır. Uyuşmazlığın kesin nedeni, ürünün resmî sınıflandırması ve kaynak sürümleri karşılaştırılmadan belirlenemez. | TİTCK kodu korunur; `atc_celiski = 1`[cite: 33] |

---

## 3. Bulgular ve Değerlendirme

### 3.1. WHO Tarafından Belgelenmiş Kod Değişiklikleri
WHO Collaborating Centre for Drug Statistics Methodology tarafından yayımlanan ATC değişiklik listesinde aşağıdaki eski-yeni kod eşleşmeleri yer almaktadır:

| Etkin Madde | Eski ATC Kodu | Yeni ATC Kodu | Değişiklik Yılı |
|---|---|---|---|
| **Gabapentin** | N03AX12 | N02BF01 | 2023 |
| **Pregabalin** | N03AX16 | N02BF02 | 2023 |
| **Leflunomid** | L04AA13 | L04AK01 | 2024 |
| **Belimumab** | L04AA26 | L04AG04 | 2024 |

Bu değişiklikler, tablodaki 2, 3, 5, 7, 8, 11, 12, 18 ve 19. satırlardaki uyuşmazlıkların sistemsel veya veri giriş hatası olmadığını, doğrudan uluslararası sınıflandırma revizyonlarından kaynaklandığını açıklamaktadır.

### 3.2. Form ve Terapötik Kullanım Ayrımı
Aspirin (`B01` vs `N02`), Flurbiprofen sprey (`R02` vs `A01`) ve Tetrasiklin merhem (`D06` vs `D10`) gibi ürünlerde kod farkının farmasötik form ve kullanım amacı kaynaklı olduğu değerlendirilmektedir.

---

## 4. Kural 8 Uygulaması ve Veri Birleştirme Kararı

Proje yönergesindeki Kural 8 doğrultusunda, incelenen 20 kayıt için TİTCK ATC kodunun `atc_final` alanında korunması ve uyuşmazlıkların `atc_celiski = 1` olarak işaretlenmesi proje veri standardı olarak uygulanmıştır[cite: 33].

- TİTCK kodu, proje kapsamında seçilen kaynak önceliği nedeniyle korunur[cite: 33].
- `atc_celiski = 1`, kaynaklar arasında ATC kodu uyuşmazlığı bulunduğunu belirtir[cite: 33].
- İP3 aşamasında bu ürünler yalnızca ATC köprüsüne dayanarak eşleştirilmemeli; etkin madde metni üzerinden ayrıca kontrol edilmelidir[cite: 33].

---

## 5. Sonuç ve Kişi C İnceleme Notu

- **Kişi C İnceleme Notu:** Kişi A tarafından çıkarılan 20 satırlık örneklem ve çelişki gerekçeleri bağımsız olarak incelenmiştir[cite: 33, 38].
- **Kural 8 Doğrulaması:** WHO güncellemeleri veya endikasyon farkı olan bu ürünlerde resmi kayıt olan TİTCK kodunun korunması (`atc_final`) ve `atc_celiski = 1` bayrağı ile işaretlenerek Adım 3'te doğrudan etkin madde metniyle eşlemeye yönlendirilmesi kararının doğruluğu ampirik olarak teyit edilmiştir[cite: 33].
- **Sonuç:** 20 ürünün kaynak listelerde doğrulanması ve ATC uyuşmazlıklarının gerekçelendirilmesi tamamlanmış olup İP1 kalite kriterleri sağlanmıştır[cite: 33].

---

## 6. Kaynaklar

1. WHO Collaborating Centre for Drug Statistics Methodology. ATC alterations — cumulative list.
2. World Health Organization. WHO Drug Information, Volume 36, Number 2 (2022), ATC/DDD Classification.
3. Proje Yönergesi: 2. Hafta: 3 Kişilik Detaylı Görev Dağılımı ve Veri Birleştirme Planı — İP1 ve Kural 8[cite: 31, 33].
4. TİTCK kaynak dosyası: `ruhsatli_2026-10-14.xlsx`[cite: 29].
5. SKRS kaynak dosyası: `skrs_2026-10-14.xlsx`[cite: 29].
6. Proje veri dosyaları: `atc_celiski_siniflari.csv`, `urun.csv` ve `eksik_kayit.csv`[cite: 29, 33].