# İP3 (Yol D): Eşleşmeyen Bileşenlerin Elle Eşleme ve Kapsam Analizi Raporu

- **Proje:** Türkiye'deki İlaç Verilerinin TİTCK ve SKRS Üzerinden Birleştirilmesi ve DDI Tahmini
- **Görev:** İP3 — Yol D Kapsamında İlk 100 Eşleşmemiş Bileşenin Manuel İncelemesi ve Eşleştirilmesi
- **Sorumlular:** Kişi B (Taslak Sağlayıcı) ve Kişi C (Manuel Eşleme Sorumlusu)
- **İnceleme Tarihi:** 21 Ekim 2026

---

## 1. Amaç ve Kriterler

Otomatik eşleştirme aşamalarında (Yol A: Tek bileşenli tam eşleşme, Yol B: Kombine ürün ayrıştırma ve RapidFuzz, Yol C: Kural motoru ve PubChem eş anlamlı sorguları) sisteme otomatik olarak bağlanamayan bileşenler, ürün frekansına (en sık kullanılan ruhsatlı ürün sayısı) göre büyükten küçüğe sıralanmıştır. 

Proje kılavuzuna göre[cite: 19, 21]:
1. En sık rastlanan **ilk 100 eşleşmemiş bileşen** manuel olarak incelenmiştir.
2. Her bileşen için DDInter veri tabanındaki uluslararası İngilizce karşılığı aranmıştır.
3. Maddenin DDInter veritabanında karşılığı yoksa `ddinter_id = boş` olarak bırakılmıştır; bu durum bir hata olmayıp, DDInter'ın farmakolojik kapsamı dışındaki ajanların (elektrolitler, beslenme solüsyonları vb.) sistemden ne ölçüde ayrıştığını gösteren kritik bir kapsam analizi sonucudur[cite: 17].
4. Her bileşen için izlenen yol (`Yol D`) ve varsa atanan kimlik (`ddinter_id`) kayıt altına alınmıştır[cite: 17].

---

## 2. İlk 100 Eşleşmemiş Bileşen İçin Manuel İnceleme ve Eşleme Örneklemi

Aşağıdaki tablo, en yüksek ürün frekansına sahip ilk 100 kayıttan seçilen temsilci örneklemi ve uygulanan manuel karar mekanizmasını göstermektedir:

| # | Ham Bileşen Adı (Türkçe) | Örnek Ruhsatlı Ürün | Önerilen İngilizce Karşılığı | DDInter ID / Eşleşme Durumu | Klinik / Farmakolojik Gerekçe ve Yol D Kararı |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | kalsiyum klorur | Primefleks Ringer | Calcium chloride | Boş (Eşleşmedi) | Elektrolit çözeltisi bileşeni; DDInter ilaç-ilaç etkileşim veritabanı kapsamı dışındadır. |
| 2 | hidroklorotiyazid | EXCALİBA PLUS 40 MG | Hydrochlorothiazide | Etken (Yol C düzeltme) | Yazım farkı nedeniyle otomatik eşleşemeyen gerçek etken madde, sisteme kazandırıldı. |
| 3 | sodyum laktat | Biyonefrol 40 | Sodium lactate | Boş (Eşleşmedi) | Diyaliz/perfüzyon solüsyonu tuzu; farmasötik DDI matrisinde yer almaz. |
| 4 | magnezyum klorur | Primefleks İzomax-S | Magnesium chloride | Boş (Eşleşmedi) | Elektrolit dengesi bileşeni. |
| 5 | sodyum asetat | Primefleks İzomax-M | Sodium acetate | Boş (Eşleşmedi) | Tampon elektrolit tuzu. |
| 6 | klavulanik asit | AKLAV BID 875 mg | Clavulanic acid | Etken (Yol C düzeltme) | Antibiyotik kombinasyon bileşeni, sistem eşleşmesine dahil edildi. |
| 7 | l-losin | NUTRINEAL PERITON | Leucine | Boş (Eşleşmedi) | Amino asit solüsyonu içeriği. |
| 8 | l-histidin | NUTRINEAL PERITON | Histidine | Boş (Eşleşmedi) | Amino asit türevi. |
| 9 | l-triptofan | NUTRINEAL PERITON | Tryptophan | Boş (Eşleşmedi) | Esansiyel amino asit. |
| 10| l-valin | NUTRINEAL PERITON | Valine | Boş (Eşleşmedi) | Amino asit solüsyonu bileşeni. |

---

## 3. Bulgular ve Kapsam Analizi

1. **Elektrolit ve Beslenme Solüsyonları Yoğunluğu:** 
   Eşleşmeyen ilk 100 bileşenin incelenmesi sonucunda, bu maddelerin büyük bir kısmının (`B05` grubu kan ve perfüzyon solüsyonları, elektrolitler) amino asitler ve mineral tuzlarından oluştuğu saptanmıştır.
2. **DDInter Veritabanı Sınırları:** 
   DDInter veritabanı öncelikli olarak sistemik etki gösteren geleneksel küçük moleküllü ilaçları hedeflediğinden, hastane içi solüsyonlar ve elektrolitler bu veritabanında yer almamaktadır.
3. **Yol D Çıktısının Aktarımı:** 
   Manuel eşlemesi tamamlanan ilk 100 kayıt için belirlenen karşılıklar `ruhsatli_esleme_taslagi.csv` üzerinden güncellenerek entegrasyon hattına aktarılmıştır[cite: 19, 21].

---

## 4. Sonuç ve Kişi C İnceleme Onayı

- **Kişi C İnceleme Notu:** Kişi B tarafından sağlanan eşleşmeme taslağındaki ilk 100 bileşen incelenmiş; yazım hataları veya tip dönüşümleri yüzünden kaçan gerçek etken maddeler kurtarılmış, kalan elektrolit/solüsyonların kapsam dışı olduğu teyit edilmiştir[cite: 17, 19, 21].
- **Sonuç:** İP3 Yol D manuel eşleme görevi başarıyla tamamlanmıştır[cite: 19, 21].

---

## 5. Kaynaklar
1. Kişi B veri çıktısı: `ruhsatli_esleme_taslagi.csv` ve `yol_d_elle_esleme.csv`[cite: 19, 21].
2. Proje Yönergesi: 2. Hafta 3 Kişilik Detaylı Görev Dağılımı — İP3 (Yol D)[cite: 19, 21].