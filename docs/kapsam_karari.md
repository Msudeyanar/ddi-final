# İP11: Kapsam ve Hedef Kitle Kararı Hazırlığı (Kişi C)

Bu doküman, DDI karar destek sisteminin hedef kitlesini netleştirmek amacıyla hazırlanan 1 sayfalık karşılaştırma ve kapsam önerisini içerir.

---

## 1. Hedef Kitle Karşılaştırma Tablosu

| Değerlendirme Kriteri | Hasta / Hasta Yakını | Eczacı / Sağlık Profesyoneli |
| :--- | :--- | :--- |
| **Girdi Beklentisi** | Kutu üzerindeki ticari ad, barkod okutma veya reçete fotoğrafı (OCR). Etken madde bilgisine sahip değildir. | Doğrudan etken madde, ticari marka, ATC kodu veya dozaj/form bilgisiyle hızlı sorgulama. |
| **Dil ve Anlatım Tonu** | Sade, tıbbi jargondan arındırılmış, panik yaratmayan, "Doktorunuza danışınız" rehberliğinde yönlendirici dil. | Farmakokinetik/farmakodinamik mekanizmayı (CYP inhibisyonu, QT uzaması vb.), kanıt düzeyini ve klinik eylem önerisini içeren teknik dil. |
| **Hukuki ve Klinik Risk** | Yanlış alarmda hastanın ilacını kendi kendine bırakması veya alarm verilmediğinde oluşabilecek komplikasyonlarda yüksek malpraktis/sorumluluk riski. | Karar destek niteliğinde kullanım; nihai klinik inisiyatif ve sorumluluk sağlık profesyonelindedir. |
| **Arayüz Karmaşıklığı** | Minimal, büyük butonlar, net renk kodlaması (Kırmızı/Sarı/Yeşil) ve net aksiyon önerileri. | Detaylı filtreleme, reçetedeki çoklu ilaç listesi analizi, alternatif etken madde önerileri ve etkileşim matrisi. |

---

## 2. Kapsam ve Fazlandırma Önerisi

1. **Öncelikli Faz (MVP):** 
   - Projenin ilk aşamasında **Eczacı / Sağlık Profesyoneli** hedef kitlesi referans alınmalıdır.
   - Gerekçe: Sistemin ürettiği 86 farklı etkileşim tipinin farmakolojik açıklamalarının ve şiddet seviyelerinin tıbbi değerlendirmesini en doğru şekilde eczacılar yapabilir; bu durum projenin klinik geçerlilik testlerini kolaylaştırır.

2. **İkinci Faz (Genişleme):**
   - İlaç köprüsü ve OCR modülleri olgunlaştığında arayüze "Basitleştirilmiş Hasta Modu" eklenerek teknik çıktılar sadeleştirilmiş uyarı kartlarına dönüştürülebilir.