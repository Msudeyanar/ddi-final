# Keşifsel Veri Analizi (EDA) Raporu

> **Hesap kaynakları:** [Notebook 05](../notebooks/05_eda_titck.ipynb) içinde E01 [`5d307533`](../notebooks/05_eda_titck.ipynb#cell-id=5d307533), E02 [`174eb525`](../notebooks/05_eda_titck.ipynb#cell-id=174eb525), E03 [`9b040e10`](../notebooks/05_eda_titck.ipynb#cell-id=9b040e10), E04 [`a4b481d5`](../notebooks/05_eda_titck.ipynb#cell-id=a4b481d5) ve E07 [`d11de057`](../notebooks/05_eda_titck.ipynb#cell-id=d11de057) hücreleri ilgili grafiklerin hesabını gösterir.

*Bu rapor, TİTCK Ruhsatlı İlaçlar ve SKRS verilerinin temizlik ve birleştirme çıktıları (`data/interim/`) üzerinden PDF şartnamesine tam uyumlu olarak üretilmiştir.*

## A. Türk İlaç Verisi (TİTCK + SKRS) EDA

### 1. Özet Profil Tabloları

#### Tablo 1: urun.csv Özet Profili (Toplam Satır: 23,801, Sütun: 15)

| Sütun Adı                    | Veri Tipi   |   Boş Sayısı | Boş Oranı (%)   |   Benzersiz Sayısı | Örnek Değer                         |
|:-----------------------------|:------------|-------------:|:----------------|-------------------:|:------------------------------------|
| barkod                       | object      |           24 | %0.10           |             23,777 | 8685276183408                       |
| urun_adi                     | object      |            0 | %0.00           |             23,741 | GLİMATİNE 400 MG FİLM KAPLI TABL... |
| etkin_madde_ham              | object      |            0 | %0.00           |              4,617 | İmatinib mesilat                    |
| atc_ruhsat                   | object      |          864 | %3.63           |              1,919 | L01EA01                             |
| atc_skrs                     | object      |       11,297 | %47.46          |              1,605 | M03BX05                             |
| atc_adi_skrs                 | object      |       11,297 | %47.46          |              1,498 | thiocolchicoside                    |
| durum                        | object      |            0 | %0.00           |                  2 | Aktif                               |
| kaynak                       | object      |            0 | %0.00           |                  2 | Ruhsatlı                            |
| atc_final                    | object      |            0 | %0.00           |              1,938 | L01EA01                             |
| atc_celiski                  | object      |            0 | %0.00           |                  2 | 0                                   |
| kapsam_disi                  | object      |            0 | %0.00           |                  2 | 0                                   |
| barkod_gecersiz              | object      |            0 | %0.00           |                  2 | 0                                   |
| kural_6_skrs_tamamlandi      | object      |            0 | %0.00           |                  2 | 0                                   |
| atc_kaynak_hatasi_duzeltildi | object      |            0 | %0.00           |                  2 | 0                                   |
| atc_who_guncellendi          | object      |            0 | %0.00           |                  2 | 0                                   |

#### Tablo 2: urun_etken.csv Özet Profili (Toplam Satır: 32,076, Sütun: 4)

| Sütun Adı   | Veri Tipi   |   Boş Sayısı | Boş Oranı (%)   |   Benzersiz Sayısı | Örnek Değer      |
|:------------|:------------|-------------:|:----------------|-------------------:|:-----------------|
| barkod      | object      |           29 | %0.09           |             23,714 | 8685276183408    |
| sira        | object      |            0 | %0.00           |                 29 | 1                |
| bilesen_ham | object      |            0 | %0.00           |              3,698 | imatinib mesilat |
| bilesen_tr  | object      |            0 | %0.00           |              3,065 | imatinib         |

Tablo 1–2, yerel `urun_guncel.csv` ve `urun_etken.csv` üzerinden metin tipinde yeniden sayıldı. Boş değerler benzersiz değer hesabına alınmadı.

#### Tablo 3: Veri Entegrasyonu ve Ayrıştırma Mutabakat Tablosu

Kaynaklar: [Notebook 01 nihai sayımlar](../notebooks/01_titck_temizlik.ipynb#cell-id=c10_save_summary), [Kural 6](../notebooks/01_titck_temizlik.ipynb#cell-id=c6_kural6_eksik) ve [Notebook 02 bileşen çıktısı](../notebooks/02_etken_ayristirma.ipynb#cell-id=a55eea71). Kapsam dışı ve geçersiz barkod sayıları nihai yerel ürün tablosundaki ilgili bayrakların toplamıdır.

| Metrik                                             |   Değer |
|:---------------------------------------------------|--------:|
| Başlangıç TİTCK satır sayısı | 23.105 |
| Eklenen aktif SKRS ürünü (Kural 5) | 851 |
| Kapsam Dışı Ürünler (kapsam_disi=1)                |     895 |
| Geçersiz Barkodlar (barkod_gecersiz=1)             |     184 |
| SKRS ile Tamamlanan Kayıtlar (Kural 6)             |      14 |
| Analizden çıkarılan eksik kayıt (`eksik_kayit.csv`) | 103 |
| ATC Çelişkili Ürünler (atc_celiski=1)              |     202 |
| Nihai Ürün Sayısı (urun.csv)                       |  23,801 |
| Nihai Ayrıştırılmış Bileşen Kaydı (urun_etken.csv) |  32,076 |
| Tekil Normalize Etken Madde Sayısı                 |   3,065 |

### Özet Tablolar Analitik Değerlendirmesi (3 Cümle Kuralı):

1. **Ne Görülüyor?** `urun.csv` tablosunda kritik operasyonel sütunlar (`urun_adi`, `etkin_madde_ham`, `atc_final`, `durum`, `kaynak`) %100 doluluk oranına sahipken, SKRS eşleşmesi bulunmayan ruhsatlı ürünlerden kaynaklı olarak `atc_skrs` ve `atc_adi_skrs` alanlarında beklenen şekilde %47,46 boşluk gözlenmektedir.
2. **En Önemli Sayı:** 23.801 ürünün ham etkin madde metinleri `urun_etken.csv` tablosunda 32,076 bileşen satırına ayrıştırılmış ve uygulanan kimyasal temizlik/normalizasyon neticesinde **3,065 tekil etken maddeye** indirgenmiştir.
3. **Projeye etkisi:** Notebook 01, analizden çıkarılan eksik kayıtları `eksik_kayit.csv` dosyasında saklar. Ürün ve bileşen tabloları eşleme adımlarının girdisidir.

### 2. Grafik E01: Bileşen Sayısı Dağılımı

![Grafik E01](../figs/E01_bilesen_sayisi.png)

#### Tablo 4: Bileşen Sayısı Dağılımı ve Kapsam Durumu

| Bileşen Sayısı   |   Kapsam İçi Ürün |   Kapsam Dışı Ürün |   Toplam Ürün | Genel Oran (%)   |
|:-----------------|------------------:|-------------------:|--------------:|:-----------------|
| 1                |            18,960 |                446 |        19,406 | %81.53           |
| 2                |             3,239 |                 10 |         3,249 | %13.65           |
| 3                |               518 |                  0 |           518 | %2.18            |
| 4                |               154 |                  0 |           154 | %0.65            |
| 5                |                16 |                226 |           242 | %1.02            |
| 6                |                 5 |                 93 |            98 | %0.41            |
| 7+               |                14 |                120 |           134 | %0.56            |

#### 📌 Grafik E01 Analitik Değerlendirmesi (3 Cümle Kuralı):

1. **Bileşen dağılımı.** E01’in sayım kuralıyla 23.801 ürün kaydının 19.406’sı tek bileşenli (%81,53), 4.395’i kombine (%18,47).
2. **Sayım yöntemi.** E01 bileşenleri barkoda göre sayar. Barkodu boş kayıtlarda ham maddeden bileşen sayısını hesaplar ve eşleşmeyen diğer kayıtlarda varsayılan sayı olarak 1 kullanır. Yüzdelerin paydası tüm ürün kayıtlarıdır.
3. **Kapsam içi dağılım.** E01 çapraz tablosuna göre kapsam içinde 18.960 tek bileşenli ve 3.946 kombine ürün kaydı var. Yol A uygunluğu ayrıca ATC ve eşleme koşullarıyla belirlenir.

[Notebook 05, E01 hücresi](../notebooks/05_eda_titck.ipynb#cell-id=5d307533)

### 3. Grafik E02: 14 ATC Ana Grubu ve SKRS Durumu Dağılımı

![Grafik E02](../figs/E02_atc_ana_grup.png)

#### Tablo 5: 14 ATC Ana Grubu Dağılımı ve DDInter Kapsamı

| ATC Grubu Adı                              |   SKRS Aktif |   SKRS Pasif |   SKRS'te Yok |   Toplam | Oran (%)   | DDInter Durumu      |
|:-------------------------------------------|-------------:|-------------:|--------------:|---------:|:-----------|:--------------------|
| N – Sinir Sistemi*                         |         1079 |          670 |          1779 |     3528 | %14.82     | Dosyası Yok (Eksik) |
| A – Sindirim Sistemi & Metabolizma         |          853 |          592 |          1624 |     3069 | %12.89     | Dosyası Var         |
| J – Sistemik Antienfektifler*              |          770 |          793 |          1417 |     2980 | %12.52     | Dosyası Yok (Eksik) |
| B – Kan & Kan Yapıcı Organlar              |         1265 |          327 |          1283 |     2875 | %12.08     | Dosyası Var         |
| C – Kardiyovasküler Sistem*                |          656 |          596 |          1423 |     2675 | %11.24     | Dosyası Yok (Eksik) |
| R – Solunum Sistemi                        |          506 |          379 |           911 |     1796 | %7.55      | Dosyası Var         |
| L – Antineoplastikler & İmmünomodülatörler |          718 |          279 |           612 |     1609 | %6.76      | Dosyası Var         |
| M – Kas-İskelet Sistemi*                   |          407 |          344 |           788 |     1539 | %6.47      | Dosyası Yok (Eksik) |
| V – Çeşitli                                |          645 |          139 |           362 |     1146 | %4.81      | Dosyası Var         |
| D – Dermatolojikler                        |          371 |          159 |           368 |      898 | %3.77      | Dosyası Var         |
| G – Genito-Üriner Sistem*                  |          297 |          131 |           396 |      824 | %3.46      | Dosyası Yok (Eksik) |
| S – Duyu Organları*                        |          186 |           69 |           125 |      380 | %1.60      | Dosyası Yok (Eksik) |
| H – Sistemik Hormonlar                     |          137 |           53 |           147 |      337 | %1.42      | Dosyası Var         |
| P – Antiparaziter Ürünler                  |           59 |           24 |            62 |      145 | %0.61      | Dosyası Var         |

#### 📌 Grafik E02 Analitik Değerlendirmesi (3 Cümle Kuralı):

1. **Ne Görülüyor?** Türkiye ruhsatlı ilaç portföyü ağırlıklı olarak Sinir Sistemi (N, %14,8), Sindirim/Metabolizma (A, %12,9), Antienfektifler (J, %12,5), Kan (B, %12,1) ve Kardiyovasküler (C, %11,2) olmak üzere 5 ana grupta (%63,55) yoğunlaşmaktadır.
2. **En Önemli Sayı:** DDInter veri tabanında bağımsız etkileşim dosyası bulunmayan 6 kritik ATC ana grubu (N, J, C, M, G, S), toplam 11,926 ürün ile tüm Türk ilaç pazarının **%50.11'sini (yarısından fazlasını)** oluşturmaktadır.
3. **Projeye Etkisi:** Pazarın yarısını oluşturan bu eksik grupların varlığı, DDInter doğrudan birleştirmesinde ciddi bir kapsama kaybı riski doğurmakta; bu nedenle İP5/İP6 hattındaki TDC DrugBank entegrasyonu ve Yol C/D genişletmelerinin ne denli hayati olduğunu ortaya koymaktadır.

### 4. Grafik E03: ATC Kod Uzunluğu (Granülarite) Dağılımı

![Grafik E03](../figs/E03_atc_uzunluk.png)

#### Tablo 6: ATC Kod Uzunluğu ve Yol A (ATC Köprüsü) Uygunluğu

| Hane Sayısı   | WHO ATC Düzey Tanımı                 |   Ürün Sayısı | Oran (%)   | Yol A (ATC Köprüsü) Durumu   |
|:--------------|:-------------------------------------|--------------:|:-----------|:-----------------------------|
| 1             | 1. Düzey (Anatomik Ana Grup)         |             0 | %0.00      | Kullanamaz (Yol C/D)         |
| 3             | 2. Düzey (Terapötik Ana Grup)        |             9 | %0.04      | Kullanamaz (Yol C/D)         |
| 4             | 3. Düzey (Farmakolojik Grup)         |           418 | %1.76      | Kullanamaz (Yol C/D)         |
| 5             | 4. Düzey (Kimyasal / Terapötik Grup) |         1,133 | %4.76      | Kullanamaz (Yol C/D)         |
| 7             | 5. Düzey (Kimyasal Madde Düzeyi)     |        22,237 | %93.43     | Kullanabilir (Yol A / B)     |
| Diğer         | Diğer (Çoklu / Boşluklu Kodlar)      |             4 | %0.02      | Kullanamaz (Yol C/D)         |

#### 📌 Grafik E03 Analitik Değerlendirmesi (3 Cümle Kuralı):

1. **Ne Görülüyor?** Ruhsatlı ilaçların ezici bir çoğunluğu (%93,43, n=22.237) tam kimyasal madde düzeyini temsil eden 7 haneli ATC koduna sahipken, 1 hane düzeyinde bırakılmış hiçbir ürün bulunmamaktadır.
2. **En Önemli Sayı:** Toplam 1,560 üründe (%6.55, n=23.801) ATC kodları yalnızca 3, 4 veya 5 haneli terapötik/farmakolojik grup düzeyinde kalmıştır (özellikle 1.133 adet 5 haneli kimyasal alt grup).
3. **Projeye Etkisi:** Yalnızca grup düzeyinde ATC'si bulunan bu 1.560 ürün, spesifik kimyasal karşılığı olmadığından Yol A (ATC Köprüsü) üzerinden doğrudan eşleştirilemeyecek olup, Yol B ve Yol C/D (etkin madde metin madenciliği ve fuzzy matching) hattına yönlendirilmek zorundadır.

### 5. Grafik E04: Etken Madde Normalizasyon Hunisi

![Grafik E04](../figs/E04_normalizasyon_hunisi.png)

#### Tablo 7: İP2 Normalizasyon Aşamaları ve İndirgeme Oranları

| Aşama Sırası               |   Benzersiz Değer Sayısı | Adım İndirgemesi (Adet)   | Adım İndirgemesi (%)   | Kümülatif İndirgeme (%)   |
|:---------------------------|-------------------------:|:--------------------------|:-----------------------|:--------------------------|
| 1. Ham Metin               |                    4,617 | -                         | -                      | %0.00                     |
| 2. Küçük Harf & Boşluk     |                    4,134 | -483                      | %10.46                 | %10.46                    |
| 3. Tuz ve Hidrat Arındırma |                    3,270 | -864                      | %20.90                 | %29.17                    |
| 4. Bileşen Ayrıştırma      |                    3,065 | -205                      | %6.27                  | %33.61                    |

#### 📌 Grafik E04 Analitik Değerlendirmesi (3 Cümle Kuralı):

1. **Ne Görülüyor?** İP2 normalizasyon hattında 4.617 ham etkin madde metni; küçük harf dönüşümü, tuz/hidrat temizliği ve bileşen ayrıştırma aşamalarından geçerek kademeli olarak konsolide edilmiştir.
2. **En Önemli Sayı:** En büyük tekil indirgemeyi **864 farklı metni (%20.90)** tekilleştiren tuz ve hidrat arındırma adımı sağlarken, 4 aşama sonunda toplamda **1,552 metin elenerek (%33.61 genel indirgeme)** veri kümesi net 3,065 tekil etken maddeye indirgenmiştir.
3. **Projeye Etkisi:** Yüzde 33'lük bu devasa indirgeme, downstream aşamalarda yapılacak bulanık eşleştirme (rapidfuzz) ve PubChem/DDInter sorgularının arama uzayını üçte bir oranında daraltarak hem işlem hızını hem de eşleşme doğruluğunu maksimize etmiştir.

### 6. Grafik E07: ATC Çelişki Sınıfları Dağılımı ve Güncellenmiş Kural 8 Analizi

![Grafik E07](../figs/E07_celiski_siniflari.png)

#### Tablo 8: ATC Çelişki Sınıfları ve Güncellenmiş Kural 8 Dağılımı

Sınıf toplamları ve WHO geçişleri Notebook 01’in `c8_atc_celiski` ve `c10_save_summary` hücrelerine dayanır. Yeniden çalıştırılan `urun.csv` çıktısı `atc_celiski_siniflari.csv` ile barkod üzerinden birleştirildiğinde 167 geçişin tamamı `farkli_grup` sınıfında yer alır. [Notebook 01](https://github.com/Msudeyanar/ddi-final/blob/main/notebooks/01_titck_temizlik.ipynb)

| Çelişki Sınıfı         | Tanım / Kriter                                              |   Ürün Sayısı | Portföy Oranı (%)   | İki Kaynaklı Ürün Oranı (%)   | Çelişki Durumu (atc_celiski)              | Uygulanan Çözüm Kuralı                                          |
|:-----------------------|:------------------------------------------------------------|--------------:|:--------------------|:------------------------------|:------------------------------------------|:----------------------------------------------------------------|
| bosluk                 | Boşluk/karakter temizliği sonrası tam eşit kodlar           |        11,222 | %47.15              | %96.41                        | Çelişki Yok (0)                           | Ruhsatlı kod onaylandı                                          |
| duzey_farki            | Biri diğerinin başlangıcı / ön eki (örn. N02B vs N02BE01)   |            49 | %0.21               | %0.42                         | Sahte Çelişki (0)                         | Kural 8: Uzun olan (ayrıntılı) kod seçildi                      |
| ayni_grup_farkli_madde | İlk 5 hane aynı, son 2 hane farklı (kimyasal alt grup aynı) |            27 | %0.11               | %0.23                         | WHO ile Çözülen: 0 / Kalan Çelişki: 27  | WHO listesinde varsa yeni kod; yoksa ruhsatlı kod, Yol A kapalı |
| farkli_grup            | İlk 5 hane tamamen farklı grup                              |           342 | %1.44               | %2.94                         | WHO ile Çözülen: 167 / Kalan Çelişki: 175 | WHO listesinde varsa yeni kod; yoksa ruhsatlı kod, Yol A kapalı |
| bos                    | Kaynakların en az birinde ATC kodu eksik                    |        12,161 | %51.09              | -                             | Karşılaştırılamaz (0)                     | Kural 6/7: Mevcut olan kod veya boş atandı                      |

> **🎯 Güncellenmiş Kural 8 Çelişki Çözüm Kararı:**
> - **İki Kaynakta da Kod Olup Farklı Olan Toplam Ürün:** **418** (1. Hafta Kaba Tahmini: 411)
> - **Granülarite Farkı (Sahte Çelişki):** **49** → `duzey_farki`, Kural 8 ile uzun kod alınarak çözülmüştür.
> - **WHO Kümülatif Listesiyle Çözülen:** **167** ürün → Eski kod WHO listesinde yeni koda dönüştürülmüş; yeni kod alınmıştır (`atc_celiski = 0`).
> - **Kalan Gerçek Çelişki:** **202** ürün → Ruhsatlı kod korunmuş, `atc_celiski = 1`, Yol A köprüsü kapatılmıştır.

#### 📌 Grafik E07 Analitik Değerlendirmesi (3 Cümle Kuralı):

1. **Ne Görülüyor?** TİTCK Ruhsatlı İlaçlar Listesi ile SKRS E-Reçete Listesi karşılaştırıldığında, her iki kaynakta da ATC kodu bulunan 11.640 ürünün %96,4'ü (11.222 ürün) boşluk temizliği sonrası birebir tam uyumludur.
2. **En Önemli Sayı:** 418 kod farklılığının 49'i granülarite farkı (sahte çelişki), 167'si WHO kümülatif listesiyle çözülmüş olup yalnızca **202 ürün** gerçek çelişki olarak kalmıştır (tüm portföyün %0.85'i).
3. **Projeye Etkisi:** Kalan 202 çelişkili ürün için ruhsatlı kod korunarak Yol A (ATC köprüsü) devre dışı bırakılmış, doğrudan etkin madde metin madenciliği (Yol C/D) zorunlu kılınmıştır. WHO güncellemesiyle çözülen 167 ürün ise artık `atc_celiski = 0` olduğu için Yol A/B eşleştirmesine dahil edilmiştir.
