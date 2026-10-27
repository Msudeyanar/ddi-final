# İlaç-İlaç Etkileşimi Tahmini: Literatür Karşılaştırma Tablosu

> **Önemli:** Sonuçlar farklı veri kümeleri, etkileşim türleri, veri bölmeleri ve metriklerle raporlandığından doğrudan karşılaştırılmamalıdır. “—” doğrulanmış sayısal sonuç bulunmadığını gösterir. Grafikten yaklaşık okunan değerler kesin sonuç olarak verilmemiştir. **[KAYNAK KONTROLÜ]** etiketi, özgün makalenin tablo/metot bölümünden bu turda kesinleştirilemeyen ayrıntıları belirtir.

## Karşılaştırma

| Çalışma | Veri kümesi / görev | Bölme ve değerlendirme | Raporlanan sonuçlar | Yöntem ve notlar |
|---|---|---|---|---|
| **DeepDDI** — Ryu et al. (2018) | DrugBank; 86 DDI türü. Ayrıca Drugs.com ve FooDB tabanlı harici değerlendirmeler. | Makale ve ek materyal birden fazla değerlendirme sunar; bu özet için tek bir evrensel train/validation/test oranı doğrulanamadığından oran yazılmamıştır. | Ortalama doğruluk **%92,4**. Makale ayrıca 191.878 ilaç çiftinden gelen 192.284 DDI kaydı ve 86 DDI türü bildirir. | Kimyasal yapı ve ilaç adlarından özellik çıkarımı ile derin sinir ağı kullanır. Bu sonuçları cold-start bölmelerindeki sonuçlarla doğrudan kıyaslamayın. |
| **Decagon** — Zitnik, Agrawal & Leskovec (2018) | TWOSIDES yan etki ilişkileri ve biyomedikal/protein ağı; çok etiketli tahmin. | Makaledeki Tablo 2, 964 yan etki türü üzerinde ortalama performansı raporlar; aynı tablo için tek bir genel train/validation/test oranı bu özette doğrulanmadığından oran verilmemiştir. | Makalenin Tablo 2’sinde 964 yan etki türü üzerindeki ortalama sonuçlar: AUROC **0,872**, AUPRC **0,832**, AP@50 **0,803**. | Grafik evrişimli kodlayıcı ve tensör ayrıştırma tabanlı çözücü kullanır. |
| **MRCGNN** — Xiong et al. (2023) | Deng ve Ryu veri kümeleri; çok ilişkili DDI tahmini. | Bölme oranı ve bağımsız tekrar sayısı bu doğrulama turunda birincil makalenin metninden bağımsız olarak teyit edilemediği için burada kesin split oranı verilmemiştir. | **Deng:** Accuracy **0,8979**, F1 **0,7791**. **Ryu:** Accuracy **0,9567**, F1 **0,8894**. [KAYNAK KONTROLÜ: Karşılaştırmalı tabloda metrik “F1” olarak geçiyor; “Macro-F1” diye genişletilmemelidir.] | Moleküler grafik özelliklerini çok ilişkili DDI grafiğiyle birleştirir; kontrastif öğrenmeyle nadir etkileşim türlerini ele almayı hedefler. |
| **EmerGNN** — Zhang et al. (2023) | DrugBank (çok sınıflı DDI) ve TWOSIDES (çok etiketli yan etki tahmini); biyomedikal ağ bilgisi. | **S0:** mevcut/bilinen ilaçlar. **S1:** yeni + bilinen ilaç. **S2:** iki yeni ilaç. S1/S2 için yeniden bölünmüş veri kümeleri yayımlanmıştır. | Birincil makalenin erişilebilir HTML metninde genel S1/S2 sonuç tablosunun sayısal hücreleri metin olarak görünmediği için genel skor eklenmemiştir. DDI-Ben’in kendi Tablo 4’ü EmerGNN için DrugBank S1’de seçilmiş dokuz DDI türüne ait kesin değerler verir; bunlar tüm görevün genel skoru değildir. | Akış tabanlı GNN; ilaç çiftleri arasındaki biyomedikal ağ yollarını ve ilgili biyomedikal kavramları kullanır. |
| **DDI-Ben** — Shen, Zhou, Zhang & Yao (2025) | DrugBank: 86 etkileşim türü, çok sınıflı görev. TWOSIDES: sıklığı 3.000–6.000 arasında olan **209** etkileşim türü; bir çift birden fazla tür taşıyabilir. | Kimyasal parmak izi benzerliğine dayalı kümeler kullanır. **S1:** bilinen + yeni ilaç; **S2:** yeni + yeni ilaç. Eğitimde iki ilaç da bilinen kümedendir. Dağılım değişimi olan ve olmayan koşullar ayrı değerlendirilir. | Birincil metrikler **DrugBank F1** ve **TWOSIDES ROC-AUC**. Şekil 6’daki tüm model-senaryo genel skorları bu dosya için sayısal olarak doğrulanamadığından tahmini değer yazılmamıştır. Tablo 4’teki seçilmiş DrugBank S1 etkileşim tipi skorları aşağıdaki ayrı tabloda verilmiştir; bunlar genel model skorları değildir. | Dağılım değişimini taklit eden küme tabanlı bölme önerir. Makalenin genel sonucu, dağılım değişiminde çoğu yöntemin performansının düşmesi; TextDDI ve DDI-GPT’nin daha dayanıklı görünmesidir. |

## DDI-Ben Tablo 4: seçilmiş etkileşim tipi skorları

Aşağıdaki değerler DDI-Ben makalesinin Tablo 4’ünde verilen DrugBank S1 sonuçlarından aktarılmıştır. Bunlar **tek bir etkileşim tipine** ait skorlardır; genel F1 veya tüm veri kümesindeki ortalama başarı olarak yorumlanmamalıdır. **[KAYNAK KONTROLÜ — TAMAMLANMADI]** Bu üç satırın metrik başlığı, DDI-Ben’in özgün Tablo 4 başlığından bu dosya hazırlanırken bağımsız biçimde teyit edilemedi. Başlık doğrulanana kadar sayılar yalnızca “raporlanan skor” olarak anılmalı; bunları F1, accuracy veya başka bir metrik diye adlandırmayın.

| Yöntem | DDI tipi | Rastgele ilaç bölmesi | Kümeye dayalı bölme | Mutlak fark (puan) |
|---|---:|---:|---:|---:|
| EmerGNN | #48 | 82,4 | 65,3 | 17,1 |
| EmerGNN | #71 | 96,7 | 24,1 | 72,6 |
| DDI-GPT | #71 | 92,4 | 72,4 | 20,0 |

**Yorum:** Örneğin EmerGNN’in #71 tipindeki skorunda 72,6 puanlık düşüş vardır. Bu yalnızca belirtilen DDI tipi ve değerlendirme ayarı için geçerlidir; modelin genel performansının 72,6 puan düştüğü anlamına gelmez.

## İP9’un üç sorusuna kısa yanıt

| Soru | EmerGNN | DDI-Ben |
|---|---|---|
| Cold-start nasıl tanımlanır? | **S1:** yeni ilaç + bilinen ilaç; **S2:** iki yeni ilaç. **S0**, iki ilacın da eğitimde bilindiği ayardır. | S1/S2 senaryolarını kullanır; ayrıca kimyasal benzerliğe dayalı kümelerle bilinen ve yeni ilaçlar arasındaki dağılım değişimini inceler. |
| İlaçlar nasıl bölünür? | İlaç bazında bölme ve S0/S1/S2 senaryoları kullanılır. Bu dosyada 7:1:2 oranı ve 777/111/222 ilaç sayıları özgün ek materyalden kesin olarak doğrulanmadığı için kesin bilgi olarak verilmemiştir. | Rastgele bölme ile kimyasal benzerlik grafiğinin bağlantılı bileşenlerine dayalı kümeli bölme karşılaştırılır. Kümeli bölme, gerçek onay-zamanı bölmesinin kendisi değil, dağılım değişiminin vekilidir. |
| Rastgele bölmeye göre düşüş nedir? | Genel S0/S1/S2 skorları bu dosyada doğrulanmadığından sayısal düşüş verilmemiştir. S1 ile S2 arasındaki fark, rastgele bölmeye göre düşüşle aynı karşılaştırma değildir. | Tablo 4’teki seçilmiş tipler için farklar yukarıda verilmiştir. Şekil 6’dan genel skorlar yaklaşık okunup kesin değer gibi yazılmamıştır. |

## Bölme ayarları

- **S0 / transductive:** Testteki ilaçların ikisi de eğitimde görülen ilaçlar olabilir.
- **S1 / inductive:** Test çifti bir yeni ve bir bilinen ilaç içerir.
- **S2 / fully inductive:** Test çifti iki yeni ilaç içerir.
- **Dağılım değişimi:** DDI-Ben, bilinen ve yeni ilaç kümeleri arasındaki kimyasal parmak izi dağılım farkını kontrol ederek yeni-ilaç değerlendirmesini gerçekçi hale getirmeyi amaçlar. Bu, S1/S2 tanımından ayrı bir deney boyutudur.

## Kaynaklar

1. Ryu JY, Kim HU, Lee SY (2018). *Deep learning improves prediction of drug–drug and drug–food interactions.* PNAS, 115(18), E4304–E4311. https://doi.org/10.1073/pnas.1803294115. Özetin doğruladığı değerler: 86 DDI türü, 192.284 DDI kaydı, 191.878 ilaç çifti ve ortalama doğruluk %92,4. Kaynak: https://pubmed.ncbi.nlm.nih.gov/29666228/
2. Zitnik M, Agrawal M, Leskovec J (2018). *Modeling polypharmacy side effects with graph convolutional networks.* Bioinformatics. https://doi.org/10.1093/bioinformatics/bty294
3. Xiong Z, Liu S, Huang F, Wang Z, Liu X, Zhang Z, Zhang W (2023). *Multi-Relational Contrastive Learning Graph Neural Network for Drug-Drug Interaction Event Prediction.* Proceedings of the AAAI Conference on Artificial Intelligence, 37(4), 5339–5347. https://doi.org/10.1609/aaai.v37i4.25665
4. Zhang Y, Yao Q, Yue L, et al. (2023). *Emerging drug interaction prediction enabled by a flow-based graph neural network with biomedical network.* Nature Computational Science, 3, 1023–1033. https://doi.org/10.1038/s43588-023-00558-4. Veri: https://doi.org/10.5281/zenodo.10016715. Kod: https://github.com/LARS-research/EmerGNN
5. Shen Z, Zhou M, Zhang Y, Yao Q (2025). *Benchmarking drug–drug interaction prediction methods: a perspective of distribution changes.* Bioinformatics, 41(11), btaf569. https://doi.org/10.1093/bioinformatics/btaf569. Kod/veri: https://github.com/LARS-research/DDI-Bench

## Kaynak kontrol durumu ve açık kalan noktalar

- **Doğrulandı:** DeepDDI için özgün PNAS kaynağının özeti 86 DDI türü, 192.284 DDI kaydı, 191.878 ilaç çifti ve %92,4 ortalama doğruluk bildiriyor. Önceki taslakta yer almış olabilecek “yedi metrikte %84,8–%93,2” aralığı bu kaynaktan doğrulanmadığı için kullanılmamalıdır.
- **Doğrulandı / deney bağlamı korunmalı:** Decagon için AUROC 0,872, AUPRC 0,832 ve AP@50 0,803 değerleri 964 yan etki türü üzerindeki özgün çalışmanın raporladığı ortalama sonuçlar olarak verilmiştir. Bunlar DDI-Ben’in yeni bölme senaryolarındaki skorları değildir.
- **Kısmen doğrulandı:** MRCGNN için Deng ve Ryu veri kümelerindeki Accuracy/F1 değerleri karşılaştırmalı tabloda bulunuyor; fakat F1 değerlerinin “Macro-F1” diye etiketlenmesi desteklenmediğinden yalnızca “F1” yazılmıştır. Özgün metottaki split oranı ve tekrar sayısı kesinleştirilmedi.
- **Açık — teslimden önce kontrol et:** DDI-Ben Tablo 4’te #48 ve #71 için aktarılan değerlerin metrik başlığı özgün tablo üzerinden yeniden kontrol edilmelidir. Bu nedenle ilgili değerler şimdilik “raporlanan skor” diye tanımlanmış ve kesin metrik adı verilmemiştir.
- **Açık — teslimden önce kontrol et:** EmerGNN’in genel S1/S2 sonuçları ve 7:1:2 / 777-111-222 gibi bölme ayrıntıları, ilgili özgün tablo veya ek materyal üzerinden hücre düzeyinde kontrol edilmeden bu dosyaya kesin değer olarak eklenmemiştir.
- **Karşılaştırma kuralı:** Farklı görev türleri, veri bölmeleri veya metrikler aynı tabloda bulunsa bile bunlar tek bir sıralama ya da doğrudan performans karşılaştırması olarak yorumlanmamalıdır.

## Doğrulama notları

- **EmerGNN:** Resmî makale S1/S2 için yeniden bölünmüş DrugBank, TWOSIDES ve HetioNet veri kümelerinin yayımlandığını doğrular. Bu dosyada genel S1/S2 performans değerleri verilmemiştir. DDI-Ben Tablo 4’te EmerGNN’in DrugBank S1 için seçilmiş dokuz etkileşim türüne ait sayılar yer alır; bunlar EmerGNN makalesinin genel sonuçlarının yerine kullanılamaz.
- **Decagon:** Birincil makalenin Tablo 2’si 964 yan etki türü için AUROC 0,872, AUPRC 0,832 ve AP@50 0,803 raporlar. Bu değerler o makalenin kendi deney düzenine aittir; DDI-Ben’deki yeni split sonuçları değildir.
- **MRCGNN:** Karşılaştırmalı tabloda aktarılan değerler Deng için Accuracy 0,8979 / F1 0,7791; Ryu için Accuracy 0,9567 / F1 0,8894 biçimindedir. F1 değerini Macro-F1 diye adlandırmak için yeterli doğrulama yoktur. 7:1:2 bölme oranı ve beş tekrar iddiası özgün makalenin metot bölümünden bu turda ayrıca doğrulanmadığından kesin bilgi olarak kullanılmamalıdır.
- **DDI-Ben:** Ana makale veri kümesi boyutlarını, bölme mantığını ve birincil metrikleri açıklar; genel karşılaştırmayı Şekil 6’da gösterir. Tablo 4’ün seçilmiş DrugBank S1 etkileşim türlerine ait sonuçlarıyla ilgili notlar tutulmuştur. Ancak #48/#71 için kullanılan sayısal karşılaştırmanın tablo başlığı/metrik eşlemesi bu turda özgün tablo görüntüsünden bağımsız olarak teyit edilemedi: bu satırlar teslim öncesinde kontrol edilmelidir. Şekil 6’daki tüm model-senaryo ortalamalarını yaklaşık çubuk yüksekliğinden kesin sonuç olarak çıkarmadım. Ek materyalin tüm tablo hücreleri doğrulanmadı.
- Son raporda tüm sonuçları tek bir sıralama olarak sunmayın: veri bölmesi, görev türü ve metrik aynı olmadıkça karşılaştırma adil değildir.
