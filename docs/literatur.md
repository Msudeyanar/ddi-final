# Literatür İncelemesi: Cold-Start DDI Tahmini ve Bölme Protokolleri

Bu doküman, ilaç-ilaç etkileşimi (DDI) tahmininde cold-start (yeni ilaç) senaryolarını ele alan EmerGNN ve DDI-Ben makalelerinin özetlerini ve 1. hafta çalışmalarıyla birleştirilmiş sonuç tablosunu içerir.

---

## 1. EmerGNN (Nature Computational Science / arXiv)

- **Cold-Start (Yeni İlaç) Tanımı:** 
  Makalede cold-start senaryoları iki seviyede tanımlanmıştır:
  - **S1 (Biri Yeni):** Etkileşim çiftindeki ilaçlardan biri eğitim kümesinde bulunurken, diğeri yalnızca test kümesinde yer alan "yeni" bir ilaçtır.
  - **S2 (İkisi de Yeni):** Etkileşim çiftindeki her iki ilaç da eğitim kümesinde hiç görülmemiş, tamamen test kümesine ayrılmış ilaçlardır. (T06 grafiğindeki S1 ve S2 tanımları bu adlandırmaya dayanmaktadır).
- **İlaçların Bölünmesi:** 
  İlaç kümesi rastgele bölünerek eğitim ve test ilaçları ayrılmıştır.
- **Performans Düşüşü:** 
  Standart rastgele çift bölmesine (S0) kıyasla, S1 senaryosunda AUC ve F1 skorlarında %8-15 arası düşüş görülürken; S2 (çift kör / ikisi yeni) senaryosunda yapısal bilgi aktarımı zorlaştığı için performans düşüşü %25-40 seviyelerine kadar çıkmaktadır.

---

## 2. DDI-Ben (Bioinformatics, 2025)

- **Cold-Start (Yeni İlaç) Tanımı:** 
  Dağılım değişimi (distribution shift) altında genelleştirme yeteneği olarak tanımlanır. Yeni onaylanan moleküllerin kimyasal iskelet (scaffold) ve özellik uzayındaki farklılıklarının modele etkisi değerlendirilir.
- **İlaçların Bölünmesi:** 
  Yalnızca rastgele ilaç bölmesi değil; Murcko scaffold (kimyasal çekirdek) bazlı bölme yapılarak yapısal olarak eğitimden tamamen farklı ilaçların testte kalması sağlanmıştır.
- **Performans Düşüşü:** 
  Scaffold bazlı cold-start testlerinde modellerin çoğunda rastgele bölmeye kıyasla belirgin performans kaybı (F1 ve AUPR'de %20'nin üzerinde düşüş) raporlanmıştır.

---

## 3. Literatür Sonuç Tablosu

| Makale | Veri Seti | Bölme Yöntemi | Metrik | Değer |
| :--- | :--- | :--- | :--- | :--- |
| **EmerGNN** | DrugBank DDI | S0 (Rastgele çift) | Macro-F1 | 0.884 |
| **EmerGNN** | DrugBank DDI | S1 (Biri yeni) | Macro-F1 | 0.762 |
| **EmerGNN** | DrugBank DDI | S2 (İkisi de yeni) | Macro-F1 | 0.615 |
| **DDI-Ben** | DrugBank DDI | Scaffold Split | ROC-AUC | 0.741 |
| **MRCGNN** | DrugBank DDI (Ryu) | S0 (Rastgele çift) | Accuracy | 0.923 |
| **CASTER** | DrugBank DDI | S0 (Rastgele çift) | ROC-AUC | 0.861 |
| **DeepDDI** | DrugBank DDI (Ryu) | S0 (Rastgele çift) | Accuracy | 0.892 |