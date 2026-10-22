# TDC DrugBank EDA Raporu ve Yorumları (Kişi C Bölümü)

## Özet Tablo
- **Toplam Çift Sayısı:** 191,808
- **Toplam Benzersiz İlaç Sayısı:** 1,706
- **Toplam Etkileşim Tipi Sayısı:** 86
- **RDKit ile Okunamayan Hatalı SMILES Sayısı:** 1

---

## Grafik Değerlendirmeleri (3 Cümle Kuralı)

### T01: 86 Etkileşim Tipine Göre Çift Sayısı Dağılımı
- **Ne görülüyor:** 86 tip arasında belirgin bir sınıf dengesizliği olduğu, çiftlerin ilk birkaç tipte yoğunlaştığı görülmektedir.
- **En önemli sayı:** En sık 5 tip tüm verinin büyük çoğunluğunu oluştururken, 10'dan az örneğe sahip 5 nadir tip bulunmaktadır.
- **Projeye etkisi:** Nadir tiplerde modelin öğrenme başarısı düşebileceğinden, sınıf ağırlıklandırma veya eşik değer filtreleme stratejileri uygulanmalıdır.

### T02: Frekans Grupları Oran Karşılaştırması (Bizim Hesap vs MRCGNN)
- **Ne görülüyor:** TDC DrugBank verisinin frekans grupları dağılımı ile literatürdeki MRCGNN/Ryu oranları karşılaştırılmıştır.
- **En önemli sayı:** 86 tipin %47,6'sının 300'den fazla örneğe, %5,8'inin ise 10'dan az örneğe sahip olduğu hesaplanmıştır.
- **Projeye etkisi:** Veri setinin literatür ile birebir örtüştüğü ve kıyaslama (benchmark) deneyleri için güvenle kullanılabileceği doğrulanmıştır.

### T03: TDC DrugBank İlaç Başına Farklı Eş Sayısı Dağılımı
- **Ne görülüyor:** İlaçların büyük bir bölümünün orta ve yüksek eş sayısına sahip olduğu, çok az ilacın tekil kaldığı görülmektedir.
- **En önemli sayı:** İlaç başına ortalama eş sayısı 224.4, medyan eş sayısı ise 182.0'dir.
- **Projeye etkisi:** Çok az etkileşim çiftine sahip olan ilaçlar model eğitimi sırasında fiilen cold-start (yeni ilaç) davranışı sergileyecektir.

### T04: İlaçların SMILES Karakter Uzunluğu Dağılımı
- **Ne görülüyor:** Moleküllerin neredeyse tamamının küçük molekül yapısında olduğu ve SMILES uzunluklarının 1.000 karakterin altında kaldığı görülmektedir.
- **En önemli sayı:** 1.000 karakter sınırını aşan yalnızca 1 adet ilaç bulunmaktadır.
- **Projeye etkisi:** Modelin girdi boyutunu belirlerken maksimum dizi uzunluğu (max length) 1.000 karakter olarak sınırlandırılabilir.

### T06: Cold-Start S0 / S1 / S2 Bölme Protokolü Test Çifti Dağılımı
- **Ne görülüyor:** %80/%10/%10 ayrımında test kümesine düşen çift sayılarının S0, S1 ve S2 senaryolarındaki dağılımı 5 farklı seed ile hesaplanmıştır.
- **En önemli sayı:** S0 test kümesinde ortalama 12,267, S1'de 30,370 ve en zor senaryo olan S2'de 1,848 çift oluşmaktadır.
- **Projeye etkisi:** 3. haftadaki model test protokolü bu standart sapması düşük ve tekrarlanabilir sayılar referans alınarak kurgulanacaktır.
