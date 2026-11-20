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

1. **Öncelikli Faz (MVP) — Birincil Kullanıcı: Hasta / Hasta Yakını**
   - Projenin ilk aşamasında doğrudan **Hasta / Hasta Yakını** hedef kitle olarak referans alınmalıdır.
   - **Gerekçe:** 
     - Küresel etkileşim kontrol araçlarının (Drugs.com, WebMD vb.) Türkiye'ye özgü ticari ilaç adlarını (*"Arveles"*, *"Klacid"*, *"Coumadin"* vb.) tanımaması, hastaların reçeteli veya reçetesiz ilaçlarını kendi başlarına güvenle denetleyebilecekleri yerelleştirilmiş bir platforma olan acil ihtiyacı göstermektedir.
     - TİTCK ve SKRS veri omurgası sayesinde, hastadan tıbbi etken madde veya ATC kodu bilgisi beklenmeksizin doğrudan kutu üzerindeki ticari marka adı veya barkod ile tek adımda sorgulama yapabilmesi sağlanacaktır.
   - **Arayüz ve Tasarım İlkeleri:**
     - **Arayüz Dili:** Tıbbi jargondan (CYP inhibisyonu, farmakokinetik/farmakodinamik mekanizmalar vb.) tamamen arındırılmış; sade, anlaşılır, yönlendirici ve hastada panik yaratmayan bir Türkçe anlatım.
     - **Şiddet Gösterimi:** 3 kademeli net renk kodlaması:
       - 🔴 **Kırmızı (Ciddi Etkileşim / Birlikte Kullanmayınız):** *"Hemen hekiminize veya eczacınıza danışınız."*
       - 🟡 **Sarı (Orta Risk / Takip Gerektirir):** *"İlaçların kullanım saatleri arasında en az 2 saat bırakınız veya eczacınıza danışınız."*
       - 🟢 **Yeşil (Düşük / Bilinen Ciddi Etkileşim Yok):** Standart kullanım bilgilendirmesi.
     - **Uyarı Metni Gereksinimi:** Hastanın ilacını hekime danışmadan kendi kendine kesmesini engellemek amacıyla her sonuç ekranında zorunlu yasal feragatname: *"Bu sistem yalnızca bilgilendirme amaçlıdır ve tıbbi teşhis/tedavi yerine geçmez. Hekiminize veya eczacınıza danışmadan ilaç kullanımınızı değiştirmeyiniz."*
     - **Öne Çıkan Kullanıcı Hikâyesi:** *"Bir hasta yakını olarak, anneme yeni yazılan antibiyotik ile her gün kullandığı tansiyon ilacının kutu isimlerini yazıp aralarında bir etkileşim olup olmadığını ve ne yapmam gerektiğini sade bir dille görmek istiyorum."*

2. **İkinci Faz (Genişleme) — Eczacı / Sağlık Profesyoneli Modu:**
   - Sistem ve yerel veri tabanı olgunlaştığında arayüze "Profesyonel / Eczacı Modu" geçişi eklenerek; 86 etkileşim tipinin farmakolojik mekanizmaları, CYP enzim inhibisyonu/indüksiyonu detayları, alternatif etken madde önerileri ve çoklu reçete etkileşim matrisi sağlık çalışanlarının kullanımına açılacaktır.