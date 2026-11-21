# İP3 — Kişi C Yol D Entegrasyon Test Raporu

**Proje:** Türkiye'deki İlaç–İlaç ve İlaç–Besin Etkileşimi Karar Destek Web Uygulaması  
**Sorumlu:** Kişi C  
**Test tarihi:** 21 Kasım 2026  
**İlgili dosyalar:**
- `config/yol_d_urun_esleme.csv`
- `src/etkilesim_kontrol.py`
- `data/interim/urun.csv`
- `data/interim/urun_etken.csv`
- `data/interim/etken_madde.csv`
- `data/interim/etkilesim.csv`

## 1. Testin amacı

İP2 otomatik ayrıştırma aşamasında doğru bölünemeyen ilaçların, Kişi C tarafından oluşturulan Yol D manuel eşleme tablosu üzerinden DDI sorgu motoruna doğru aktarılıp aktarılmadığını kontrol etmek.

Testlerde otomatik ayrıştırma algoritması değiştirilmemiştir. Manuel doğrulama kayıtları ayrı bir Yol D tablosunda tutulmuştur.

## 2. Test yöntemi

Python terminalinden `EtkilesimMotoru` sınıfı çalıştırılmış, ürün adıyla sorgulanan ilaçların seçilen barkodları, bileşen listeleri ve DDInter kimlikleri incelenmiştir.

Yol D tablosunda bulunan bileşenlerin otomatik ayrıştırma çıktıları yerine kullanılıp kullanılmadığı kontrol edilmiştir.

## 3. Test sonuçları

| Ürün | Barkod | Beklenen bileşen sayısı | Gözlenen sonuç |
|---|---|---:|---|
| BENORAL 30 tablet | 8699527093859 | 2 | Başarılı |
| BENORAL 50 tablet | 8699527093866 | 2 | Yol D yükleme kontrolü başarılı |
| POLIVIT C 1000 tablet | 8699514094234 | 9 | Başarılı |
| MON.MIBI KIT | 8698923793516 | 1 | Yol D yükleme ve ürün arama kontrolü başarılı |

### 3.1. BENORAL

İlk sorguda motorun BENORAL 30 tabletlik ambalajı seçtiği, ancak Yol D dosyasında yalnızca 50 tabletlik ambalajın kayıtlı olduğu tespit edilmiştir.

Ürün kullanma talimatındaki 250 mg tiamin hidroklorür ve 250 mg piridoksin hidroklorür bilgileri incelenerek 30 tabletlik ambalaj için iki yeni Yol D satırı eklenmiştir.

Tekrar yapılan terminal sorgusunda:

- Tiamin hidroklorür bileşeni bulundu.
- Piridoksin hidroklorür bileşeni bulundu.
- Piridoksin için `DDInter1549` kimliği kullanıldı.
- Tiamin için doğrulanmamış DDInter kimliği atanmadı.

**Sonuç:** BENORAL 30 tablet için Yol D bileşenlerinin ürün sorgusunda kullanıldığı doğrulandı.

### 3.2. POLIVIT C

İlk sorguda motor 1000 tabletlik ambalajı seçmiş ve otomatik ayrıştırmadan gelen beş parçalı çıktıyı göstermiştir.

Yol D dosyasında yalnızca 500 tabletlik ürünün dokuz bileşeni kayıtlı olduğundan, aynı formülasyondaki 30 ve 1000 tabletlik ürünler için toplam 18 yeni kayıt eklenmiştir.

Tekrar yapılan terminal sorgusunda POLIVIT C 1000 tablet için dokuz bileşen listelenmiştir.

DDInter kimliği bulunan dört bileşen:

- B6 vitamini (piridoksin): `DDInter1549`
- C vitamini (askorbik asit): `DDInter124`
- Nikotinamid: `DDInter1289`
- Folik asit: `DDInter771`

Diğer beş bileşenin DDInter kimlikleri doğrulanmadığından boş bırakılmıştır.

**Sonuç:** POLIVIT C 1000 tablet için Yol D bileşenlerinin ürün sorgusunda kullanıldığı doğrulandı.

### 3.3. MON.MIBI KIT

Otomatik ayrıştırmada tek kimyasal kompleksin yanlış biçimde iki parçaya bölündüğü belirlenmiştir.

Yol D tablosunda bu ürün tek bileşen olarak tanımlanmıştır:

**Tetrakis (2-metoksi izobutil izonitril) bakır(I) tetrafloroborat**

Terminal sorgusunda tek bileşen görüntülenmiştir. Uygun DDInter kimliği doğrulanamadığı için sonuç `eslesmedi` olarak gösterilmiştir.

**Sonuç:** Tek bileşenli Yol D kaydı doğru şekilde kullanılmaktadır. Bununla birlikte DDInter etkileşim kapsaması sağlanmış değildir.

## 4. GitHub düzeltmeleri

- **PR #43:** BENORAL 30 tablet için iki Yol D bileşen kaydı eklendi ve `main` dalına birleştirildi.
- **GitHub commit `f106f76`:** POLIVIT C 30 ve 1000 tabletlik ambalajları için toplam 18 bileşen kaydı eklendi.

Son kontrolde `config/yol_d_urun_esleme.csv` dosyasında toplam 56 kayıt bulunmuştur. POLIVIT C'nin üç ambalajı için 27 kayıt mevcuttur.

## 5. Sınırlamalar

- Bu testler bileşen eşleme entegrasyonunu doğrular; bütün ilaç etkileşimlerinin eksiksiz tespit edildiğini göstermez.
- DDInter kimliği bulunmayan maddeler için eşleşme varmış gibi sonuç üretilmemiştir.
- BENORAL 50 tablet ve MON.MIBI KIT için Yol D kaydı yükleme kontrolleri gerçekleştirilmiştir; tüm ürün çiftleriyle uçtan uca etkileşim testi yapılmamıştır.
- POLIVIT C'nin 30 ve 500 tabletlik ambalajları için yeni ürün arama testi bu raporda henüz belgelenmemiştir.
- BEDOXINAL'in belge bekleyen bileşen kayıtlarının sorgu motorunda nasıl ele alınacağı ayrıca değerlendirilmelidir.

## 6. Sonuç

Kişi C tarafından hazırlanan Yol D manuel eşlemelerinin DDI sorgu motoruna aktarılması üzerinde yapılan testlerde BENORAL 30 tablet, POLIVIT C 1000 tablet ve MON.MIBI KIT için beklenen bileşen listeleri elde edilmiştir.

Aynı ilacın farklı barkodlarla kayıtlı ambalajlarında Yol D eşlemelerinin eksik olabildiği tespit edilmiş, BENORAL ve POLIVIT C için gerekli ambalaj kayıtları tamamlanmıştır.

Bu çalışmalar, otomatik ayrıştırma algoritmasının doğruluk oranını değiştirmeden, manuel olarak doğrulanan ilaç bileşenlerinin sorgu motorunda kullanılabildiğini göstermektedir.
