# İP8: Etkileşim Kontrol Araçları Testi

Sorumlu: Kişi C. Senaryo: **Arveles (deksketoprofen), Coumadin (varfarin), Klacid (klaritromisin)** birlikte kullanılır mı?
Bu belge test kayıtlarını plandaki biçimde sunar: ticari ad tanındı mı, etkin madde ile giriş gerekti mi, bulunan çiftler,
araca özgü şiddet etiketi, açıklama özeti ve ekran görüntüsü dosyası.

> **Kapsam notu:** Bölüm 2'deki ilk testler sitelerin **yapay zekâ sohbet araçlarıyla** yapılmıştır (Ask Drugs.com AI, Medscape AI, WebMD site araması).
> Planın İP8 maddesinin istediği, sitelerin **etkileşim kontrol araçlarıyla** (Drug Interaction Checker) yapılan tekrar Bölüm 3'te kayıtlıdır.

## 1. Test koşulları

| Madde | Bilgi |
|---|---|
| Girilen sorgu | "Arveles (Deksketoprofen), Coumadin (Varfarin), Klacid (Klaritromisin) birlikte kullanılır mı?" |
| Sorgu biçimi | Serbest metin; **ticari ad ve etkin madde birlikte yazılmıştır** |
| Kullanılan araçlar | Drugs.com: Ask Drugs.com AI. Medscape: Medscape AI. WebMD: site arama kutusu |
| Test tarihi | 7 Ekim 2026 (WebMD ekran görüntüsündeki sistem saatine göre) |

Sorguda etkin madde de yazıldığı için **"ticari ad tanındı mı" bu testte ölçülemedi.** Bunun için yalnızca "Arveles", "Coumadin", "Klacid" yazılarak test tekrarlanmalıdır.

## 2. Sonuçlar (yapay zekâ sohbet araçları)

| Araç | Ticari ad tanındı mı | Etkin madde ile giriş gerekti mi | Bulunan çiftler | Şiddet etiketi (araca özgü) | Açıklama özeti | Ekran görüntüsü |
|---|---|---|---|---|---|---|
| **Drugs.com** (Ask Drugs.com AI) | Ölçülemedi | Ölçülemedi | Üç ilaç birlikte ele alınmış. Arveles (NSAİİ) ve Klacid'in (antibiyotik) Coumadin'in kan sulandırıcı etkisini artırdığı, ciddi kanama riski olduğu belirtilmiş. Arveles'in mide tahrişi yoluyla kanama riskini artırabileceği de yazılmış | Etiket yok (Major/Moderate/Minor kullanılmamış). İfade: üçü çok dikkatli tıbbi gözetim olmadan genelde birlikte kullanılmamalı | Kısa, hasta diliyle özet; doktora veya eczacıya danışma önerisi. Yanıt İngilizce | `figs/arac_drugscom_ai.png` |
| **Medscape** (Medscape AI) | Ölçülemedi | Ölçülemedi | 1) Klaritromisin–varfarin: INR yükselmesi ve kanama riski. 2) NSAİİ (deksketoprofen benzeri)–varfarin: kanama riski anlamlı artar. 3) Klaritromisin ile diğer antikoagülanlar (örn. rivaroksaban): CYP3A4/P-gp üzerinden kanama riski | Etiket yok. İfade: üçlü kombinasyondan "mümkünse kaçınılmalı"; majör kanama ve aşırı INR yükselmesi riski | Profesyonel dil, mekanizma (CYP3A4, P-gp) ve numaralı kaynak atıfları. Öneriler: alternatif antibiyotik, NSAİİ yerine başka analjezik, gerekirse sık INR kontrolü. Yanıt Türkçe | `figs/arac_medscape_ai_1.png`, `figs/arac_medscape_ai_2.png` |
| **WebMD** (site arama) | Ölçülemedi | Ölçülemedi | **Sonuç alınamadı:** arama yükleme ekranında kalmış | Yok | Yok | `figs/arac_webmd_arama.png` |
| **BNF** | Denenmedi | Denenmedi | Denenmedi | Denenmedi | Sistem ücretli olduğundan denenmedi. BNF sütunları danışman için boş bırakılmıştır | Yok |
| **RxMediaPharma** | Denenmedi | Denenmedi | Denenmedi | Denenmedi | Sistem ücretli olduğundan denenmedi (bkz. Bölüm 4) | Yok |

Notlar:
- Drugs.com ve Medscape yanıtları yapay zekâ metnidir; sitelerin etkileşim kontrol aracının çıktısı yerine kullanılamaz.
- Medscape yanıtı "deksketoprofen benzeri" ifadesini kullandığından, deksketoprofenin kendisine özgü bir kayıt bulunduğu söylenemez.
- Deksketoprofen–klaritromisin çifti iki yanıtta da ayrı bir çift olarak belirtilmemiştir.

## 3. Etkileşim kontrol araçlarıyla tekrar

Aynı senaryo üç sitenin etkileşim kontrol araçlarıyla tekrarlandı. 1. turda yalnızca ticari adlar, tanınmayan ilaç için 2. turda etkin madde girildi.
Test tarihi ve saati: 16 Ekim 2026, 23:01 (TSİ). Girilen ilaçlar: Arveles (dexketoprofen), Coumadin (warfarin), Klacid (clarithromycin).

| Araç ve adres | Ticari ad tanındı mı | Etkin madde ile giriş gerekti mi | Bulunan çiftler ve şiddet etiketi | Açıklama özeti | Ekran görüntüsü |
|---|---|---|---|---|---|
| **Drugs.com Interaction Checker** — drugs.com/drug_interactions.html | Arveles: hayır. Coumadin: evet. Klacid: evet | Evet, Arveles için (dexketoprofen girildi) | 1) Deksketoprofen–varfarin: **Major**. 2) Klaritromisin–varfarin: **Major**. 3) Deksketoprofen–klaritromisin: **Bulunamadı** (etkileşim kaydı çıkmadı) | Deksketoprofen ile varfarinin birlikte kullanımı gastrointestinal kanama riskini ciddi oranda artırır. Klaritromisin varfarin metabolizmasını engelleyerek INR düzeyini yükseltebilir ve majör kanama riski oluşturur. Deksketoprofen–klaritromisin çifti için sistemde kayıtlı etkileşim bulunamadı | `figs/arac_drugscom_checker.png`, `figs/arac_drugscom_checker_1.png` |
| **Medscape Drug Interaction Checker** — reference.medscape.com/drug-interactionchecker | Arveles: hayır. Coumadin: evet. Klacid: evet | Evet, Arveles için (dexketoprofen girildi) | 1) Deksketoprofen–varfarin: **Serious – Use Alternative**. 2) Klaritromisin–varfarin: **Serious – Use Alternative**. 3) Deksketoprofen–klaritromisin: **Monitor Closely** | Deksketoprofen ve varfarin kombinasyonu ciddi kanama riski nedeniyle alternatif tedavi gerektirir. Klaritromisin varfarin etkisini artırdığı için yakın takip önerilir. Deksketoprofen–klaritromisin için hastanın yakından izlenmesini gerektiren "Monitor Closely" düzeyinde etkileşim belirtilmiştir | `figs/arac_medscape_checker.png`, `figs/arac_medscape_checker_1.png` |
| **WebMD Interaction Checker** — webmd.com/interaction-checker/default.htm | Arveles: hayır. Coumadin: evet. Klacid: evet | Evet, Arveles için (dexketoprofen girildi) | 1) Deksketoprofen–varfarin: **Major**. 2) Klaritromisin–varfarin: **Major**. 3) Deksketoprofen–klaritromisin: **Minor** | Ağrı kesici (deksketoprofen) ve kan sulandırıcı (varfarin) birlikte kullanımı yüksek kanama potansiyeli taşır. Klaritromisin–varfarin etkileşiminde INR takibi ve doz ayarlaması kritiktir. Deksketoprofen–klaritromisin çifti minör (hafif) düzeyde etiketlenmiştir | `figs/arac_webmd_checker.png`, `figs/arac_webmd_checker_1.png` |

**Araç bazında gözlemler**
- **Drugs.com:** Arveles Türkiye/Avrupa menşeli bir ticari ad olduğu için tanınmadı; 2. turda etkin madde eklendi. Üç ilaçla ücretli duvar (paywall) çıkmadı.
- **Medscape:** Ücretsiz hesapla oturum açmak gerekti. Arveles ticari adıyla sonuç alınamadı; etkin madde veri tabanından seçildi. "Serious – Use Alternative" ve "Monitor Closely" etiketleri rapora aynen yansıdı.
- **WebMD:** Hesap gerekmedi. Arayüz sade bir liste sunuyor; uzun sonuç ekranı kaydırılarak iki parçada kaydedildi.

**Doğrulanan noktalar**
- **Girilen madde:** Üç araca da ikame madde (ketoprofen/ibuprofen) değil, doğrudan dexketoprofen girilmiştir. 1. ve 3. çift sonuçları dexketoprofen için geçerlidir.
- **WebMD etiketleri:** Ekran görüntülerindeki tekil etiketler yazılmıştır: Major, Major, Minor. "Monitor Closely" Medscape'e özgü etikettir.
- **Drugs.com 3. çift:** Deksketoprofen–klaritromisin için etkileşim kaydı çıkmamıştır ("Bulunamadı").
- **Ekran görüntüleri:** Altı dosya (`arac_*_checker.png` ve `_1.png`) depoya eklenmelidir.

**Karşılaştırma:** Üç araç da iki varfarin çiftini en yüksek düzey olarak işaretlemiştir. Deksketoprofen–klaritromisin çiftinde araçlar ayrışmıştır: Drugs.com kayıt bulamamış, Medscape "Monitor Closely", WebMD "Minor" vermiştir. Etiket adları araçlar arasında doğrudan eşdeğer değildir.

## 4. Diğer notlar

- **BNF sütunları:** Danışman için boş bırakılmıştır.
- **RxMediaPharma lisansı:** Fakültenin veya üniversite hastanesi eczanesinin lisansı olup olmadığı henüz sorulmamıştır. Sonuç sorulduktan sonra bu satıra yazılacaktır.
- **`docs/acik_sorular.md`:** "İP8: Arveles üç checker'da da tanınmadı, etkin madde girildi. Deksketoprofen–klaritromisin çiftinde araçlar ayrıştı (Drugs.com: bulunamadı, Medscape: Monitor Closely, WebMD: Minor). WebMD sohbet/arama testinde sonuç alınamadı."

## 5. Türkiye'deki mevcut mobil uygulama: Prospektüs Pro

Barkod okutularak denenmiştir (örnek ürün: Buscopan 10 mg kaplı tablet, 20 tablet). Ekran görüntüsü: `figs/arac_prospektus_pro.png`.

**Gözlenenler**
- Ürün için şu başlıklar sunuluyor: ne için kullanılır, aç mı tok mu kullanılır, alkol ile etkileşimi, hamilelikte, emzirme döneminde ve çocuklarda kullanımı.
- "Kısa Ürün Bilgisi" ve "Kullanım Talimatı" düğmeleri var. Kullanım talimatından prospektüsün dijital sürümüne ulaşılıyor.
- Ürünün muadillerini de gösteriyor; güncelliği kesin değil.
- Ekranda uyarı var: yapay zekâ tarafından üretilen bilgiler yalnızca genel bilgilendirme amaçlıdır ve tıbbi tavsiye değildir.

**Eksikler**
- İlaçlar veya etkin maddeler arası karşılaştırma yok; yalnızca tek ilaçla ilerleniyor.
- Aynı anda birçok ilaç girilemiyor. Her ilaç sırayla okutulup prospektüsü açılarak elle karşılaştırılması gerekiyor (yaşlı kullanıcı için uygun değil).
- Yalnızca App Store'da bulunuyor.
- Kullanıcının yaşı, böbrek/karaciğer işlevi, alerjileri ve kronik hastalıkları hesaba katılmıyor.

**Ayrıca belirtilen, ancak bu testte doğrulanmayanlar:** barkod/karekod okumaya bağımlılık (kutusu atılmış ilaçlar için OCR zayıflığı), kameranın ışık ve netleme hassasiyeti, gıda takviyelerinin ve bitkisel ürünlerin kapsam dışı kalması.

## 6. Araçların özellik karşılaştırması (1. hafta incelemesi)

| Ölçüt | Drugs.com | Medscape | WebMD | BNF | RxMediaPharma |
|---|---|---|---|---|---|
| Türkçe desteği | Yok (İngilizce/İspanyolca) | Yok (arayüz İngilizce, Almanca, İspanyolca, Fransızca, Portekizce) | Yok | Yok | Var (arayüz ve içerik Türkçe) |
| Ticari isimle arama | Evet (jenerik veya marka, otomatik tamamlama) | ABD merkezli; ABD'de kayıtlı olmayan ilaçlar bulunamayabilir | ABD pazarının marka adları; Türkiye'ye özgü adlar yok | İngiltere/NHS odaklı; Türkiye'ye özgü adlar yok | Evet (TİTCK ruhsatlı ürünler, barkod dahil) |
| Çoklu ilaç girişi | Evet | Evet | Evet | Evet | Evet |
| Şiddet sınıflandırması | Major / Moderate / Minor | "Serious – Use Alternative", "Monitor Closely" (resmî sayfada görülenler) | Severe / Serious, Significant / Moderate, Minor | Severity (Severe, Moderate, Mild, Unknown) ve Evidence | Kontrendike, Önemli, Minör (renk kodlu) |
| Açıklama düzeyi | Hasta dili + profesyonel metin | Profesyonel, mekanizma açıklamalı | Hasta odaklı, sade | Klinik, kanıta dayalı | Klinik, ayrıntılı |
| Ücret | Ücretsiz | Ücretsiz, kayıt gerekli | Ücretsiz | Karma; Birleşik Krallık dışında ücretli abonelik | Ücretli (lisans/abonelik) |
| Platform | Web + uygulama | Web + mobil | Web + mobil | Web + mobil | Masaüstü + web + mobil |

Bu tablo 1. haftadaki inceleme notlarından aktarılmıştır; özellikler bu turda yeniden doğrulanmamıştır.

## 7. Bulgular: Türkiye'de eksik olan

- Hastaya yönelik, ücretsiz, sade Türkçe bir etkileşim kontrol aracı yok. Güçlü Türkçe kaynak lisanslı ve profesyonellere dönük.
- Yabancı araçlar Türkiye'deki ticari isimleri tanımıyor; hasta etkin maddeyi değil kutudaki marka adını bilir.
- Ücret ve lisans modeli bireysel kullanıcıyı dışarıda bırakıyor.
- "Major" gibi şiddet etiketi hastaya ne yapması gerektiğini söylemiyor.
- Gıda, bitkisel ürün ve reçetesiz ilaç kapsamı Türkçe ve kolay erişilir değil.
- Mevcut Türkçe mobil uygulama (Prospektüs Pro) ilaç bilgisi veriyor ama ilaç–ilaç etkileşimi kontrolü ve çoklu ilaç girişi sunmuyor.
- e-Nabız ve reçete sistemleriyle bağlantılı bir kontrol sunulmuyor (araştırılarak doğrulanmalı).
