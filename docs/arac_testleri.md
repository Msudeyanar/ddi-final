# İP8: Çevrimiçi Etkileşim Kontrol Araçları Test Sonuçları

**Test Senaryosu:** Arveles + Coumadin + Klacid
- **Arveles:** Deksketoprofen trometamol (ATC: M01AE17)
- **Coumadin:** Varfarin sodyum (ATC: B01AA03)
- **Klacid:** Klaritromisin (ATC: J01FA09)

---

## 1. Etkileşim Araçları Karşılaştırma Tablosu

| Araç | Ticari Ad Tanındı mı? | Etken Madde ile Giriş Gerekti mi? | Bulunan Çiftler | Şiddet Etiketi (Araca Özgü) | Açıklamanın Özeti | Ekran Görüntüsü Dosyası |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Drugs.com** | Kısmen (Coumadin tanındı; Arveles ve Klacid tanınmadı) | Evet (Dexketoprofen ve Clarithromycin olarak girildi) | 1. Warfarin – Clarithromycin<br>2. Warfarin – Dexketoprofen | 1. Major<br>2. Major | 1. Klaritromisin CYP3A4'ü inhibe ederek varfarin düzeyini ve INR'yi artırır, ciddi kanama riski oluşturur.<br>2. Deksketoprofen trombosit agregasyonunu bozar ve GI mukoza hasarı yaparak varfarinle kanama riskini katlar. | `docs/screenshots/drugs_com.png` |
| **Medscape** | Kısmen (Coumadin tanındı; Arveles tanınmadı) | Evet (Dexketoprofen ve Clarithromycin olarak girildi) | 1. Warfarin – Clarithromycin<br>2. Warfarin – Dexketoprofen | 1. Serious - Use Alternative<br>2. Serious - Monitor Closely | 1. Klaritromisin varfarinin hepatik klerensini düşürür, kanama riskini belirgin artırır.<br>2. NSAİİ ile antikoagülan kombinasyonu gastrointestinal ülserasyon ve kanama riskini sinerjistik artırır. | `docs/screenshots/medscape.png` |
| **WebMD** | Kısmen (Coumadin tanındı; Arveles tanınmadı) | Evet (Dexketoprofen ve Clarithromycin olarak girildi) | 1. Warfarin – Clarithromycin<br>2. Warfarin – Dexketoprofen | 1. Serious / Significant<br>2. Serious / Significant | 1. Varfarin etkisinin ve protrombin zamanının klaritromisin etkisiyle şiddetli artışı.<br>2. Trombosit fonksiyon bozukluğu ve mide kanaması ihtimali. | `docs/screenshots/webmd.png` |
| **BNF (British National Formulary)** | *(Danışman için boş bırakıldı)* | *(Danışman için boş bırakıldı)* | *(Danışman için boş bırakıldı)* | *(Danışman için boş bırakıldı)* | *(Danışman için boş bırakıldı)* | *(Danışman için boş bırakıldı)* |

---

## 2. Kurumsal Lisans ve Önemli Notlar

- **BNF Durumu:** Proje protokolü gereği BNF test sütunları akademik danışman değerlendirmesi için boş bırakılmıştır.
- **RxMediaPharma Durumu:** Fakülte ve üniversite hastanesi kütüphanesi / eczanesi nezdinde RxMediaPharma kurumsal erişim lisansının bulunup bulunmadığı sorgulanmış; lisans durumu toplantıda danışmana aktarılmak üzere not edilmiştir.
- **Ticari Ad Kısıtı:** Yabancı menşeili araçların neredeyse hiçbiri Türkiye'ye özgü ticari adları ("Arveles", "Klacid") doğrudan tanıyamamakta, mutlaka İngilizce etken maddeye köprü kurulması gerekmektedir. Bu durum projemizin yerelleştirilmiş ürün arayüzü motivasyonunu doğrudan desteklemektedir.