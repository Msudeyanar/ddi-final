# Lisanslar ve Kullanım Koşulları

Bu belge, projede kullanılan dış veri kaynaklarının lisans durumunu ve projenin bu kaynakları nasıl kullandığını özetler.
Sorumlu: Kişi C (İP5). Son güncelleme: 2026-10-26.

## 1. TDC DrugBank DDI veri seti

- **Kaynak:** Therapeutics Data Commons (TDC), `DDI(name='DrugBank')`. Erişim tarihi: 2026-10-26.
- **Açıklama:** FDA/Health Canada ilaç etiketlerinden ve birincil literatürden elle derlenmiş ilaç–ilaç etkileşimi
  veri seti. 86 etkileşim türü, 1.706 ilaç, 191.808 etkileşim çifti. Görev: iki ilacın SMILES dizesinden
  etkileşim türünü tahmin etme (çok sınıflı sınıflandırma). TDC'nin önerdiği bölme yöntemi rastgele bölmedir.
- **Yerel kopya:** `data/raw/tdc_drugbank_ddi.csv` (bir kez indirildi, `.gitignore` içinde, depoya eklenmez).
- **Tip açıklamaları:** `data/interim/drugbank_tip_aciklama.csv` (`get_label_map(name='DrugBank', task='DDI')` ile üretildi).
- **Referanslar:**
  1. Wishart DS ve diğerleri (2017). DrugBank 5.0: a major update to the DrugBank database for 2018. *Nucleic Acids Research* 46:D1074–D1082.
  2. Ryu JY, Kim HU, Lee SY (2018). Deep learning improves prediction of drug–drug and drug–food interactions. *PNAS* 115(18):E4304–E4311.
- **Veri seti lisansı (TDC sayfasındaki ifadeye göre):** DrugBank Online halka ücretsiz erişimli bir kaynak olarak
  sunulmaktadır. DrugBank Online içeriğinin veya DrugBank Verilerinin tamamının ya da bir kısmının herhangi bir
  amaçla kullanımı ve yeniden dağıtımı lisans gerektirir. Akademik kullanıcılar belirli kullanım durumları için
  ücretsiz lisans başvurusunda bulunabilir; diğer tüm kullanıcılar ücretli lisansa ihtiyaç duyar.
- **TDC yazılım lisansı:** PyTDC Python paketi MIT lisanslıdır. Bu, veri seti lisansından ayrıdır; veri
  setlerinin lisansı TDC'de her veri setinin kendi sayfasında belirtilir.

## 2. DrugBank

- DrugBank, akademik veri indirmelerini durdurmuştur. Bu nedenle ham DrugBank dosyası projede doğrudan
  kullanılmaz; DrugBank kaynaklı veri yalnızca TDC üzerinden alınmış tek bir kopya olarak elimizdedir.
- Yukarıdaki lisans ifadesine göre bu verinin kullanımı lisans gerektirir. Ücretsiz lisans yalnızca akademik
  kullanıcılara ve belirli kullanım durumlarına açıktır. Bu nedenle proje kullanımı aşağıdaki sınırla yürütülür.

## 3. Projedeki kullanım kapsamı

- TDC DrugBank verisi **yalnızca akademik deney** (EDA ve makine öğrenmesi denemeleri) için kullanılır.
- Uygulamada kullanıcıya gösterilen sonuçların kaynağı DDInter ve Türk ilaç verisidir (TİTCK, SKRS).
  TDC DrugBank verisi ürüne veya kullanıcıya dönük çıktıya dahil edilmez.
- Ticari kullanım ve verinin yeniden dağıtımı proje kapsamı dışındadır. Depoda yalnızca türetilmiş özetler
  (tip açıklamaları, sayılar, grafikler) bulunur; ham veri `data/` altında tutulur ve depodan hariç tutulur.
- Raporlarda ve sunumlarda TDC ve DrugBank kaynak olarak anılır.

## 4. Diğer kaynaklar

| Kaynak | Projedeki kullanım | Kullanım ilkesi |
|---|---|---|
| DDInter | Etkileşim verisi (8 CSV, `ddinter_code_A…V`) | Akademik amaçla kullanılır; kaynak raporlarda anılır; 10 çiftlik web kontrolü elle yapılır, toplu veri çekilmez |
| TİTCK ruhsatlı ilaç listesi | Ürün, barkod, etkin madde, ATC | Kamuya açık liste; ham dosya değiştirilmez, temizlik bayrak sütunuyla yapılır |
| SKRS | Barkod, ATC adı, aktif/pasif durum | Ham dosya değiştirilmez; yalnızca eşleme ve tamamlama için kullanılır |
| PubChem | Eş anlamlı ad ve SMILES sorguları | Saniyede en fazla 5 istek; yanıtlar `data/cache/pubchem/` altında saklanır, aynı istek tekrarlanmaz |

## 5. Uyarı

Bu proje bir akademik çalışmadır; tıbbi tavsiye vermez. Etkileşim sonuçları kaynak veri setlerinin
kapsamıyla sınırlıdır ve klinik karar için kullanılmamalıdır.

## 6. Lisans durumu ve açık sorular

- **Mevcut durum:** Ekibin ve danışmanın DrugBank için onaylı bir lisansı yoktur. DrugBank akademik lisansı
  için başvuru yapılmıştır; son kontrolde (2026-10-26) DrugBank'tan yanıt gelmemiştir.
- **Kural:** Bölüm 1'deki ifadeye göre DrugBank verisinin kullanımı lisans gerektirdiğinden, onay gelene kadar
  TDC DrugBank verisi yalnızca yerelde tutulur; depoya eklenmez, paylaşılmaz ve yeniden dağıtılmaz.
- **Etki alanı:** Lisansa bağlı kısımlar İP5 (07 notebook), T grafikleri ve makine öğrenmesi denemeleridir.
  Ana hat (TİTCK, SKRS, DDInter, eşleme, uçtan uca test) bundan etkilenmez ve beklemeden ilerler.
- **Açık sorular (`docs/acik_sorular.md` ve toplantı gündemi):**
  1. DrugBank'a başvuru ne zaman ve kimin adıyla yapıldı; yanıt için ne kadar beklenecek?
  2. Belirlenen tarihe kadar yanıt gelmezse TDC DrugBank verisi projeden çıkarılacak mı, yoksa
     yalnızca yerel ve yayımlanmayan deney olarak mı sınırlanacak? (Karar danışmanla verilir.)
