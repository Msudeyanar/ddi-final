# DDInter Veri Dağılımı, Birleştirme ve Kayıp Analizi Raporu

**Tarih:** 2026-10-15  
**İlgili İş Paketi:** İP4 (DDInter Birleştirme ve Kayıp Analizi)  
**Notebook:** `notebooks/04_ddinter_birlestirme.ipynb`  
**Üretilen Veriler:** `data/interim/ddinter_ilac.csv`, `data/interim/etkilesim.csv`  

---

## 1. Yönetici Özeti ve Temel Çıktılar

Bu rapor, DDInter veritabanından indirilen 8 ayrı ATC kategorisine ait ham CSV dosyalarının (`ddinter_downloads_code_[A,B,D,H,L,P,R,V].csv`) tekilleştirilmesini, sayısal ID sıralamasıyla çiftlerin birleştirilmesini, Kural 9 uyarınca şiddet çelişkisi analizini, 10 kritik klinik çiftin web/dosya karşılaştırmasını ve eksik ATC gruplarından kaynaklanan veri kayıp analizini kapsamaktadır.

### Temel Metrikler Tablosu (Tekrar Sonrası Sayılar)

Aşağıdaki sayılar, 1. hafta raporundaki tekrar öncesi sayıların yerine geçen nihai doğrulanmış değerlerdir:

| Metrik | Ham / Tekrar Öncesi Değer | Tekrar Sonrası (Nihai) Değer | Açıklama |
| :--- | :---: | :---: | :--- |
| **Toplam Okunan Satır** | 222.383 | — | 8 ham CSV dosyasının toplam satır sayısı |
| **Benzersiz İlaç Sayısı** | 1.939 | **1.939** | `ddinter_id` bazında tekilleştirilmiş ilaç sayısı |
| **Benzersiz Etkileşim Çifti** | — | **160.235** | Sayısal sıralanmış ve Kural 9 ile tekilleştirilmiş çift sayısı |
| **Elenen Mükerrer Kayıt** | — | **62.148** | Birden fazla dosyada yer alan veya yönü ters olan kayıtlar |
| **Birden Fazla Dosyada Geçen Çift** | — | **43.826** | En az iki farklı ATC grubunda ortak listelenen çiftler |
| **Şiddet Çelişkisi (`siddet_celiski = 1`)**| — | **0** | Farklı dosyalarda farklı şiddetle listelenen çift sayısı |
| **İlaç Başına Ortalama Eş Sayısı** | — | **165,28** | Bir ilacın etkileştiği ortalama diğer ilaç sayısı |
| **İlaç Başına Medyan Eş Sayısı** | — | **125,0** | Min: 1, Maks: 910 (Dexamethasone) |

---

## 2. Şiddet Dağılımı ve Kural 9 Analizi

### A. Kural 9 Önceliği
Bir çift birden fazla dosyada yer aldığında şiddet seviyeleri şu hiyerarşiye göre belirlenmiştir:
$$\text{Major (0)} > \text{Moderate (1)} > \text{Minor (2)} > \text{Unknown (3)}$$
Farklı dosyalarda farklı şiddet etiketine sahip olan kayıtlar için `siddet_celiski = 1` bayrağı konulması kurala bağlanmıştır.

### B. Şiddet Dağılım Tablosu

| Şiddet Düzeyi (*Severity Level*) | Etkileşim Çifti Sayısı | Oran (%) | Kümülatif Oran (%) |
| :--- | :---: | :---: | :---: |
| **Moderate** | 96.675 | %60,33 | %60,33 |
| **Unknown** | 29.813 | %18,61 | %78,94 |
| **Major** | 26.914 | %16,80 | %95,74 |
| **Minor** | 6.833 | %4,26 | %100,00 |
| **Toplam** | **160.235** | **%100,00** | — |

> **Önemli Bulgu (`siddet_celiski`):**  
> Veri setinde 43.826 çift birden fazla dosyada tekrar etmesine rağmen, hiçbir çiftte şiddet uyuşmazlığı tespit edilmemiştir (`siddet_celiski = 0`). Bu durum, DDInter veritabanının farklı ATC kategorileri arasında tutarlı bir şiddet etiketleme protokolü kullandığını kanıtlamaktadır.

---

## 3. En Çok Etkileşen 20 İlaç Tablosu

Veritabanında en yüksek dereceye (en fazla partner/eş sayısına) sahip ilk 20 ilaç aşağıda listelenmiştir. Bu ilaçlar klinik pratikte sıklıkla polifarmasi hastalarında yer alan kortikosteroidler, immünsüpresanlar ve dar terapötik indeksli ajanlardır:

| Sıra | DDInter ID | İlaç Adı (*Drug Name*) | Eş (Partner) Sayısı | Birincil Klinik Kullanım Alanı |
| :---: | :---: | :--- | :---: | :--- |
| 1 | `DDInter513` | **Dexamethasone** | 910 | Kortikosteroid / Enflamasyon / İmmünsüpresyon |
| 2 | `DDInter1735` | **Tacrolimus** | 866 | İmmünsüpresif (Organ nakli) |
| 3 | `DDInter1951` | **Warfarin** | 864 | Antikoagülan (Dar terapötik indeks) |
| 4 | `DDInter1533` | **Promethazine** | 832 | Antihistaminik / Sedatif |
| 5 | `DDInter393` | **Clarithromycin** | 822 | Makrolid Antibiyotik (Güçlü CYP3A4 inhibitörü) |
| 6 | `DDInter458` | **Cyclosporine** | 816 | İmmünsüpresif / Kalsinörin inhibitörü |
| 7 | `DDInter1515` | **Prednisone** | 805 | Sistemik Glukokortikoid |
| 8 | `DDInter1789` | **Thalidomide** | 785 | İmmünomodülatör / Antineoplastik |
| 9 | `DDInter743` | **Fluconazole** | 783 | Antifungal (CYP2C9/CYP3A4 inhibitörü) |
| 10 | `DDInter1174` | **Methotrexate** | 781 | Antimetabolit / Antineoplastik / İmmünsüpresif |
| 11 | `DDInter670` | **Erythromycin** | 754 | Makrolid Antibiyotik |
| 12 | `DDInter1632` | **Salbutamol** | 753 | Beta-2 Agonist (Bronkodilatör) |
| 13 | `DDInter1513` | **Prednisolone** | 751 | Sistemik Glukokortikoid |
| 14 | `DDInter593` | **Doxepin** | 734 | Trisiklik Antidepresan |
| 15 | `DDInter1376` | **Ozanimod** | 733 | Sfingozin-1-fosfat reseptör modülatörü (MS) |
| 16 | `DDInter885` | **Hydrocortisone** | 722 | Kortikosteroid |
| 17 | `DDInter1244` | **Morphine** | 718 | Opioid Analjezik |
| 18 | `DDInter1675` | **Simvastatin** | 695 | HMG-CoA Redüktaz İnhibitörü (Statin) |
| 19 | `DDInter1855` | **Triamcinolone** | 695 | Kortikosteroid |
| 20 | `DDInter905` | **Idelalisib** | 693 | Antineoplastik (PI3K inhibitörü) |

---

## 4. 10 Çiftlik Web Kontrolü ve Dosya Karşılaştırması

DDInter web platformu (`http://ddinter.scbdd.com/`) ve indirilen 8 dosyanın kapsamını test etmek amacıyla belirlenen 10 kritik klinik çift incelenmiştir.

### Karşılaştırma Tablosu

| # | İlaç 1 | İlaç 2 | ATC Sınıfları | İlaç 1 ID | İlaç 2 ID | İndirilen Dosyalarda Durum | Şiddet | Kaynak Dosya(lar) | Web Kontrolü / Nedeni |
| :---: | :---| :---| :---: | :---: | :---: | :---: | :---: | :---: | :---|
| 1 | **dexketoprofen** | **clarithromycin** | M + J | *YOK* | DDInter393 | **HAYIR** | — | — | **DDInter'da Yok:** Dexketoprofen etken maddesi DDInter veritabanında kayıtlı değildir (yalnızca rasemik *ketoprofen* mevcuttur). Sitede "No record found". |
| 2 | **simvastatin** | **clarithromycin** | C + J | DDInter1675 | DDInter393 | **EVET** | Major | `A` | **Dosyada Bulundu:** Her iki ilaç da eksik dosya grubunda (C ve J) olmasına rağmen simvastatin A grubundaki ilaçlarla paylaşıldığı için `code_A.csv` içine girmiştir. |
| 3 | **amlodipine** | **simvastatin** | C + C | DDInter79 | DDInter1675 | **EVET** | Major | `A` | **Dosyada Bulundu:** İki kardiyovasküler ilaç (C+C). Simvastatin'in A dosyasında yer alması sayesinde çift `code_A.csv` dosyasında korunmuştur. |
| 4 | **ibuprofen** | **sertraline** | M + N | DDInter900 | DDInter1662 | **EVET** | Moderate | `R` | **Dosyada Bulundu:** İkisi de eksik grupta (M+N). İbuprofen'in solunum grubu dosyasında (`code_R.csv`) listelenmesi sayesinde etkileşim yakalanmıştır. |
| 5 | **digoxin** | **amiodarone** | C + C | DDInter554 | DDInter76 | **HAYIR** | — | — | **Eksik Grup Kaybı:** İki ilaç da DDInter'da mevcuttur ancak ikisi de C sınıfındadır ve mevcut 8 dosyadaki hiçbir ilaçla köprü kuramadığı için 8 CSV'de yer almamaktadır. Web motorunda da indirme havuzuyla aynı kısıt geçerlidir. |
| 6 | **warfarin** | **clarithromycin** | B + J | DDInter1951 | DDInter393 | **EVET** | Major | `A, B` | **Dosyada Bulundu:** Warfarin B grubunda yer aldığı için hem B hem de A dosyalarında Major şiddetle yer almaktadır. |
| 7 | **warfarin** | **dexketoprofen** | B + M | DDInter1951 | *YOK* | **HAYIR** | — | — | **İlaç Eksikliği:** Warfarin mevcuttur ancak Dexketoprofen DDInter fihristinde tanımlı değildir. |
| 8 | **ciprofloxacin** | **tizanidine** | J + M | DDInter384 | DDInter1821 | **HAYIR** | — | — | **Eksik Grup Kaybı:** Ciprofloxacin (J) ve Tizanidine (M) veritabanında bağımsız ilaç olarak vardır ancak ikisi de eksik grupta kaldığı için ikili etkileşimleri 8 dosyaya girmemiştir. |
| 9 | **tramadol** | **sertraline** | N + N | DDInter1841 | DDInter1662 | **HAYIR** | — | — | **Eksik Grup Kaybı:** İki merkezi sinir sistemi ilacı (N+N). İndirme dosyalarında N grubu bulunmadığı için serotonin sendromu riski taşıyan bu kritik çift dosyalarda eksiktir. |
| 10 | **metformin** | **furosemide** | A + C | DDInter1164 | DDInter790 | **EVET** | Moderate | `A` | **Dosyada Bulundu:** Metformin A sınıfı indirme dosyasında (`code_A.csv`) Furosemide (C) ile birlikte yer almaktadır. |

### Web Kontrolü Çıkarımları
1. **İlaç Varlığı Sorunu (2/10):** Dexketoprofen gibi bazı yaygın Türkiye/Avrupa molekülleri DDInter'da enantiomer bazında yer almamakta, sadece ana molekül (Ketoprofen) bulunmaktadır.
2. **Eksik Grup Kaybı (3/10):** Digoxin–Amiodarone (C+C), Ciprofloxacin–Tizanidine (J+M) ve Tramadol–Sertraline (N+N) gibi hayati klinik çiftler, her iki ajan da eksik dosya gruplarında kaldığı için indirilen 8 dosyada yer almamaktadır.
3. **Çapraz Geçiş Kurtarması (5/10):** Eksik gruplarda yer alan bazı ilaçlar (ör. Simvastatin, Amlodipine, Ibuprofen), A veya R dosyalarındaki genişletilmiş partner listeleri sayesinde yakalanabilmiştir.

---

## 5. Eksik ATC Grupları ve Kayıp Analizi Metodolojisi

### A. Eksik Dosya Grupları
DDInter indirme sayfasında Dünya Sağlık Örgütü'nün (WHO) 14 ana ATC grubundan yalnızca 8 tanesi için dosya sunulmaktadır:
- **İndirilen Gruplar (8 Adet):** `A` (Sindirim), `B` (Kan), `D` (Dermatoloji), `H` (Hormonlar), `L` (Antineoplastik), `P` (Antiparaziter), `R` (Solunum), `V` (Çeşitli).
- **İndirme Dosyası Bulunmayan Eksik Gruplar (6 Adet):**
  - **C:** Kalp ve Damar Sistemi (*Cardiovascular*)
  - **G:** Ürogenital ve Cinsiyet Hormonları
  - **J:** Sistemik Antiinfektifler (Antibiyotikler, Antiviraller)
  - **M:** Kas-İskelet Sistemi
  - **N:** Sinir Sistemi (Analjezikler, Psikiyatrik ilaçlar)
  - **S:** Duyu Organları (Göz, Kulak)

### B. Kayıp Analizi Algoritması (Kişi A `etken_madde.csv` Hazır Olunca)
Kişi A tarafından üretilecek olan `data/interim/etken_madde.csv` tablosu geldiğinde uygulanacak standart hesaplama protokolü:

1. DDInter'da bulunan Türk etken maddelerinin kümesi filtrelenir ($N_{\text{eslesen}}$).
2. Olası tüm ikili kombinasyonlar üretilir:
   $$N_{\text{toplam\_cift}} = \binom{N_{\text{eslesen}}}{2} = \frac{N_{\text{eslesen}} \times (N_{\text{eslesen}} - 1)}{2}$$
3. Her çift $(i, j)$ için bileşenlerin ATC 1. düzey ana gruplarına bakılır ($\text{ATC}_i, \text{ATC}_j$).
4. Eğer $\text{ATC}_i \in \{C, G, J, M, N, S\}$ **ve** $\text{ATC}_j \in \{C, G, J, M, N, S\}$ ise çift `kapsam_disi_grup = 1` olarak işaretlenir.
5. **Kayıp Oranı:**
   $$\text{Kayip Orani (\%)} = \frac{\sum \text{kapsam\_disi\_grup}}{N_{\text{toplam\_cift}}} \times 100$$

### C. Teorik ve Yaklaşık Kayıp Oranı Tahmini
1. **Eşit Dağılım Varsayımı:**  
   14 gruptan 6'sı eksiktir ($p = 6/14 \approx 0,4286$).  
   İki tarafın da eksik grupta olma teorik olasılığı:
   $$P(\text{Kayıp}) = p^2 = (0,4286)^2 \approx \mathbf{\%18,37}$$

2. **Klinik / Reçete Ağırlıklı Gerçeklik:**  
   Türkiye'de TİTCK ruhsatlı ve en çok reçete edilen ilaçların yaklaşık **%50–%55'i** C (Kalp), N (Sinir), J (Antibiyotik) ve M (Ağrı/Kas) gruplarında yoğunlaşmaktadır. Bu durumda beklenen gerçek ikili çift kaybı:
   $$P(\text{Klinik Kayıp}) \approx (0,50)^2 \approx \mathbf{\%25,0} \quad \text{ile} \quad (0,55)^2 \approx \mathbf{\%30,25}$$
   aralığında gerçekleşecektir.
   Nitekim 10 çiftlik klinik test örneğimizde de 10 çiftten 3 tanesi (%30) doğrudan eksik grup kombinasyonu nedeniyle indirilen dosyalarda bulunamamıştır.

---

## 6. Zorunlu Metodolojik Rapor Notu

> **⚠️ ZORUNLU METODOLOJİK NOT:**  
> Bu bir yaklaşık hesaptır; çünkü DDInter bir ilaca birden fazla ATC kodu atayabilir (örneğin *Acetaminophen* sayfasında birden fazla farklı ATC kodu listelenmektedir) ve bu durum çapraz dosya geçişleriyle bazı çiftlerin kurtarılmasını sağladığından gerçek kayıp hesaplanandan daha düşük olabilir. 10 çiftlik web kontrolü bu yaklaşımın ne kadar tuttuğunu ve klinik açıdan hangi çiftlerin kaybolduğunu açıkça göstermektedir.

---

## 7. Sonuç ve Proje Tavsiyeleri (Karar Zemin Notu)

1. **İlaç Fihristi Açısından:** 8 dosyanın birleşimi, eksik gruplardaki ilaçlar da `Drug_B` olarak dahil edildiğinden 1.939 benzersiz ilaçla geniş bir kapsayıcılık sağlamaktadır.
2. **Etkileşim Çiftleri Açısından:** İki tarafı da `C, G, J, M, N, S` gruplarında kalan etkileşimler indirilen tablolarda bulunmamaktadır.
3. **Uygulama Mimarisi Kararı:**
   - Türkiye pazarında en sık kullanılan 200–300 etken madde baz alındığında bu eksiklik kullanıcı deneyiminde "etkileşim bulunamadı" uyarısı üretme riskini artırır.
   - Bu nedenle sistemin kural tabanlı olarak veya harici bir açık kaynak kaynaktan (ör. DrugBank / TDC) bu eksik grupları desteklemesi 3. hafta kapsam toplantısında önerilmelidir.
