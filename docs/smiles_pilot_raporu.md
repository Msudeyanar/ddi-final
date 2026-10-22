# İP10: PubChem SMILES Pilot Test Raporu

- **Test Edilen İlaç Sayısı:** 100
- **SMILES Bulunan İlaç Sayısı:** 100 (%100.0)
- **SMILES Bulunamayan / Biyolojik:** 0
- **Birden Fazla CID Dönen (coklu_cid=1):** 0
- **100 İstek İçin Geçen Süre:** 54.69 saniye (Ortalama 0.55 sn/istek)
- **1.939 İlacın Tamamı İçin Tahmini Süre:** ~17.7 dakika

**Klinik ve Mimari Not:** 
PubChem rate limiter kuralı (5 istek/sn) ve önbellekleme (cache) mimarisi test edilmiştir. 
Tam kümenin çekilmesi yaklaşık 17.7 dakika süreceğinden, 2. hafta başında tek seferlik bir arka plan batch işlemi olarak çalıştırılması önerilmektedir.
