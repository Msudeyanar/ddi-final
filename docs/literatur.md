# Literatür İncelemesi

## EmerGNN

S0 iki mevcut ilacın, S1 bir yeni ve bir mevcut ilacın, S2 iki yeni ilacın etkileşim tahminini ölçer. DrugBank için aşağıdaki skorlar makalede yüzde ölçeğinde raporlanan test ortalamalarıdır.

| Model | Veri seti | Bölme | Metrik | Sonuç | Kaynak |
|---|---|---|---|---:|---|
| EmerGNN | DrugBank | S0 | Macro-F1 | 94,4 | [Ek Tablo 3](https://arxiv.org/html/2311.09261#A3.T3) |
| EmerGNN | DrugBank | S1 | Macro-F1 | 62,0 | [Tablo 1](https://arxiv.org/html/2311.09261#S6.T1) |
| EmerGNN | DrugBank | S2 | Macro-F1 | 25,0 | [Tablo 1](https://arxiv.org/html/2311.09261#S6.T1) |

S0’a göre düşüş S1’de **32,4 yüzde puanı** (94,4 − 62,0), S2’de **69,4 yüzde puanı** (94,4 − 25,0). [Makale ve ek tablolar](https://arxiv.org/html/2311.09261)

DDI-Ben ve önceki hafta incelenen çalışmalar için [literatür kaynak tablosuna](literatur_tablo.md) bakın. Kaynak tablo veya bölümle doğrulanabilen sayısal değerler raporlanır.
