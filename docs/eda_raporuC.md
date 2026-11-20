# TDC DrugBank EDA Raporu ve Yorumları (Kişi C Bölümü)

Kaynak: [Notebook 07](../notebooks/07_eda_tdc.ipynb) kayıtlı çıktıları. Aşağıdaki hücre numaraları notebook’taki `In [n]` etiketleridir.

## Özet Tablo (In [4])
- **Toplam Çift Sayısı:** 191,808
- **Toplam Benzersiz İlaç Sayısı:** 1,706
- **Toplam Etkileşim Tipi Sayısı:** 86
- **RDKit ile Okunamayan Hatalı SMILES Sayısı:** 1

---

## Grafik Değerlendirmeleri (3 Cümle Kuralı)

### T01 (In [5]): 86 Etkileşim Tipine Göre Çift Sayısı Dağılımı
- **Ne görülüyor:** 86 tip arasında belirgin bir sınıf dengesizliği olduğu, çiftlerin ilk birkaç tipte yoğunlaştığı görülmektedir.
- **Projeye etkisi:** Nadir tiplerde modelin öğrenme başarısı düşebileceğinden, sınıf ağırlıklandırma veya eşik değer filtreleme stratejileri uygulanmalıdır.

### T02 (In [8]): Frekans Grupları Oran Karşılaştırması (Bizim Hesap vs MRCGNN)
- **Ne görülüyor:** TDC DrugBank verisinin frekans grupları dağılımı ile literatürdeki MRCGNN/Ryu oranları karşılaştırılmıştır.
- Notebook frekansları `[1, 10]` ve `(300, +∞)` dahil beş aralığa ayırır. %5,8 ve %47,6 literatür karşılaştırması için kodda tanımlanan referans değerlerdir.

### T03 (In [9]): TDC DrugBank İlaç Başına Farklı Eş Sayısı Dağılımı
- **Ne görülüyor:** İlaçların büyük bir bölümünün orta ve yüksek eş sayısına sahip olduğu, çok az ilacın tekil kaldığı görülmektedir.
- **En önemli sayı:** İlaç başına ortalama eş sayısı 224.4, medyan eş sayısı ise 182.0'dir.
- **Projeye etkisi:** Çok az etkileşim çiftine sahip olan ilaçlar model eğitimi sırasında fiilen cold-start (yeni ilaç) davranışı sergileyecektir.

### T04 (In [10]): İlaçların SMILES Karakter Uzunluğu Dağılımı
- **Ne görülüyor:** Moleküllerin neredeyse tamamının küçük molekül yapısında olduğu ve SMILES uzunluklarının 1.000 karakterin altında kaldığı görülmektedir.
- **En önemli sayı:** 1.000 karakter sınırını aşan yalnızca 1 adet ilaç bulunmaktadır.
- **Projeye etkisi:** Modelin girdi boyutunu belirlerken maksimum dizi uzunluğu (max length) 1.000 karakter olarak sınırlandırılabilir.

### T06 (In [11]): Cold-Start S0 / S1 / S2 Bölme Protokolü Test Çifti Dağılımı
- **Ne görülüyor:** %80/%10/%10 ayrımında test kümesine düşen çift sayılarının S0, S1 ve S2 senaryolarındaki dağılımı 5 farklı seed ile hesaplanmıştır.
- **En önemli sayı:** S0 test kümesinde ortalama 12,267, S1'de 30,370 ve en zor senaryo olan S2'de 1,848 çift oluşmaktadır.
- **Projeye etkisi:** 3. haftadaki model test protokolü bu standart sapması düşük ve tekrarlanabilir sayılar referans alınarak kurgulanacaktır.
