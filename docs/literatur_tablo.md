# İlaç-İlaç Etkileşimi Tahmini: Literatür Karşılaştırma Tablosu

> **Önemli:** Sonuçlar farklı veri kümeleri, etkileşim türleri, veri bölmeleri ve metriklerle raporlandığından doğrudan karşılaştırılmamalıdır. **"—"**, doğrulanmış sayısal sonuç bulunmadığını gösterir; bu hücrelere tahmin yazılmamıştır. Grafikten yaklaşık okunan değerler kesin sonuç olarak verilmemiştir.

## Karşılaştırma

| Makale | Veri seti | Bölme yöntemi (S0/S1/S2) | Metrik | Değer | Yöntem ve notlar |
|---|---|---|---|---|---|
| **DeepDDI** — Ryu et al. (2018) | DrugBank; 86 DDI türü (ayrıca Drugs.com ve FooDB tabanlı harici değerlendirmeler) | Birden fazla değerlendirme var; tek bir evrensel train/validation/test oranı doğrulanamadığından oran yazılmamıştır | Ortalama doğruluk | %92,4 | Kimyasal yapı ve ilaç adlarından özellik çıkarımı + derin sinir ağı. Makale 191.878 ilaç çiftinden gelen 192.284 DDI kaydı bildirir; bu sayı TDC DrugBank kopyasındaki 191.808 çiftle aynı değildir (farklı kaynak/sürüm). Cold-start bölmelerindeki sonuçlarla doğrudan kıyaslanmamalıdır. |
| **Decagon** — Zitnik, Agrawal & Leskovec (2018) | TWOSIDES yan etki ilişkileri + biyomedikal/protein ağı; çok etiketli, 964 yan etki türü | Makaledeki Tablo 2'nin ortalama sonuçları; tek bir genel train/validation/test oranı doğrulanamadığından verilmemiştir | AUROC | 0,872 | Grafik evrişimli kodlayıcı ve tensör ayrıştırma tabanlı çözücü. Değerler o makalenin kendi deney düzenine aittir. |
| **Decagon** | aynı | aynı | AUPRC | 0,832 | |
| **Decagon** | aynı | aynı | AP@50 | 0,803 | |
| **MRCGNN** — Xiong et al. (2023) | Deng veri kümesi; çok ilişkili DDI | Bölme oranı ve tekrar sayısı birincil metinden teyit edilemediği için verilmemiştir | ACC | 0,8979 | Moleküler grafik özelliklerini çok ilişkili DDI grafiğiyle birleştirir; kontrastif öğrenmeyle nadir etkileşim türlerini hedefler. |
| **MRCGNN** | Deng | aynı | Macro-F1 | 0,7791 | |
| **MRCGNN** | Ryu veri kümesi | aynı | ACC | 0,9567 | |
| **MRCGNN** | Ryu | aynı | Macro-F1 | 0,8894 | |
| **EmerGNN** — Zhang et al. (2023) | DrugBank (çok sınıflı DDI), TWOSIDES (çok etiketli); biyomedikal ağ bilgisi | **S0:** bilinen ilaçlar. **S1:** yeni + bilinen ilaç. **S2:** iki yeni ilaç. S1/S2 için yeniden bölünmüş veri kümeleri yayımlanmıştır | Genel S1/S2 performansı | — | Genel S1/S2 sayısal hücreleri erişilebilen metinden doğrulanamadı. Akış tabanlı GNN; ilaç çiftleri arasındaki biyomedikal ağ yollarını kullanır. DDI-Ben Tablo 4, EmerGNN için DrugBank S1'de yalnızca seçilmiş dokuz DDI türünün değerlerini verir; bunlar genel skor değildir. |
| **DDI-Ben** — Shen, Zhou, Zhang & Yao (2025) | DrugBank: 86 tür, çok sınıflı | Kimyasal parmak izi benzerliğine dayalı kümeler. **S1:** bilinen + yeni ilaç; **S2:** yeni + yeni ilaç. Dağılım değişimi olan ve olmayan koşullar ayrı değerlendirilir | F1 (birincil) | — | Genel sonuçlar Şekil 6'da grafik olarak verilir; ana metinde kesin ortalama±sapma tablosu yoktur, çubuklardan değer okunmamıştır. Ek materyalde accuracy ve Cohen's kappa açıklanır; ek hücreler doğrulanamadı. |
| **DDI-Ben** | TWOSIDES: sıklığı 3.000–6.000 arasında **209** tür; bir çift birden fazla tür taşıyabilir | aynı | ROC-AUC (birincil) | — | Ek materyalde PR-AUC ve accuracy açıklanır; hücreler doğrulanamadı. Genel sonuç: dağılım değişiminde çoğu yöntemin performansı düşer; TextDDI ve DDI-GPT daha dayanıklı görünür (sayısal düşüş doğrulanamadı). |

## Bölme ayarları

- **S0 / transductive:** Testteki ilaçların ikisi de eğitimde görülen ilaçlar olabilir.
- **S1 / inductive:** Test çifti bir yeni ve bir bilinen ilaç içerir.
- **S2 / fully inductive:** Test çifti iki yeni ilaç içerir.
- **Dağılım değişimi:** DDI-Ben, bilinen ve yeni ilaç kümeleri arasındaki kimyasal parmak izi dağılım farkını kontrol ederek yeni-ilaç değerlendirmesini gerçekçi hale getirmeyi amaçlar. Bu, S1/S2 tanımından ayrı bir deney boyutudur.
- **Adlandırma:** Raporda EmerGNN'nin S1 ve S2 adları, T06'daki "biri yeni" ve "ikisi de yeni" senaryolarıyla aynı anlamda kullanılır. DDI-Ben de S1/S2 adlarını aynı anlamda kullanır.

## Plan soruları (İP9)

| Soru | Cevap |
|---|---|
| Cold-start (yeni ilaç) nasıl tanımlanmış? | EmerGNN ve DDI-Ben: S1 = bir yeni + bir bilinen ilaç, S2 = iki yeni ilaç. |
| İlaçlar nasıl bölünmüş? | EmerGNN: S1/S2 için yeniden bölünmüş veri kümeleri yayımlamıştır. DDI-Ben: kimyasal parmak izi benzerliğine dayalı kümeler; eğitimde iki ilaç da bilinen kümedendir. |
| Rastgele bölmeye göre performans ne kadar düşüyor? | Sayısal fark doğrulanamadı (—). DDI-Ben'in niteliksel sonucu: dağılım değişiminde çoğu yöntemin performansı düşer. Açık soru olarak `docs/acik_sorular.md` dosyasına yazılır. |

## Kaynaklar

1. Ryu JY, Kim HU, Lee SY (2018). *Deep learning improves prediction of drug–drug and drug–food interactions.* PNAS. https://doi.org/10.1073/pnas.1803294115
2. Zitnik M, Agrawal M, Leskovec J (2018). *Modeling polypharmacy side effects with graph convolutional networks.* Bioinformatics. https://doi.org/10.1093/bioinformatics/bty294
3. Xiong et al. (2023). *MRCGNN.* AAAI. https://doi.org/10.1609/aaai.v37i4.25665
4. Zhang Y, Yao Q, Yue L, et al. (2023). *Emerging drug interaction prediction enabled by a flow-based graph neural network with biomedical network.* Nature Computational Science, 3, 1023–1033. https://doi.org/10.1038/s43588-023-00558-4. Veri: https://doi.org/10.5281/zenodo.10016715. Kod: https://github.com/LARS-research/EmerGNN
5. Shen Z, Zhou M, Zhang Y, Yao Q (2025). *Benchmarking drug–drug interaction prediction methods: a perspective of distribution changes.* Bioinformatics, 41(11), btaf569. https://doi.org/10.1093/bioinformatics/btaf569. Kod/veri: https://github.com/LARS-research/DDI-Bench

## Doğrulama notları

- **EmerGNN:** Resmî makale S1/S2 için yeniden bölünmüş DrugBank, TWOSIDES ve HetioNet veri kümelerinin yayımlandığını doğrular. Genel S1/S2 performans değerleri doğrulanamadığı için verilmemiştir. DDI-Ben Tablo 4'teki dokuz DDI türüne ait sayılar EmerGNN makalesinin genel sonuçlarının yerine kullanılamaz.
- **Decagon:** Tablo 2'deki AUROC 0,872, AUPRC 0,832 ve AP@50 0,803 değerleri o makalenin kendi deney düzenine aittir; DDI-Ben'deki yeni split sonuçları değildir.
- **MRCGNN:** ACC ve Macro-F1 değerleri AAAI 2023 makalesinin sonuç tablosuyla kontrol edilmiştir. 7:1:2 bölme oranı ve beş tekrar iddiası ayrıca doğrulanmadığından kesin bilgi olarak kullanılmamalıdır.
- **DDI-Ben:** Ana makale veri kümesi boyutlarını, bölme mantığını ve birincil metrikleri açıklar; genel karşılaştırmayı Şekil 6'da gösterir. Şekil 6'daki model-senaryo ortalamaları çubuk yüksekliğinden kesin sonuç olarak çıkarılmamıştır. Ek materyaldeki tüm hücreler doğrulanmamıştır.
- **Veri seti boyutu farkı:** DeepDDI makalesindeki 191.878 ilaç çifti, TDC DrugBank kopyasındaki 191.808 çiftten farklıdır. Raporda TDC için 191.808 kullanılır.
- Son raporda tüm sonuçları tek bir sıralama olarak sunmayın: veri bölmesi, görev türü ve metrik aynı olmadıkça karşılaştırma adil değildir.
