# Ayrıştırma kontrolünün doğrulanması

`ayristirma_kontrol.md`, hocanın işaret ettiği tarihsel 50 ürünü sabit barkodlarla inceler. Teknik karar tablosu `ayristirma_kontrol_50.csv` içindedir. CSV'deki `kisi_c_onayi` alanları boş bırakılmıştır; teknik inceleme, Kişi C'nin nihai insan onayı olarak sunulmaz.

Teknik sonuç 40 uygun ve 10 uygun olmayan bileşen listesidir (%80). GYNOFERON kaynak verisiyle ilgili ek bulgu ayrı belirtilmiştir; bu toplam saf regex/ayırıcı doğruluğu değildir. Aynı örneklemde düzeltilmiş kodun doğruluğu henüz ölçülmemiştir.

## Komutlar

Python, pandas ve numpy gerekir. Depo kökünden:

```console
python audit/verify_audit.py --self-check
python audit/verify_audit.py --urun data/interim/urun.csv --urun-etken data/interim/urun_etken.csv
```

İlk komut rapor, karar tablosu, manifest ve kayıtlı notebook örnekleminin tutarlılığını sınar. İkinci komut verilen girdilerle tarihsel kodu yeniden çalıştırır ve örneklemi karşılaştırır. Girdi sürümü değiştiyse doğrulamanın başarısız olması beklenebilir; eski örneklem yeni örneklemle değiştirilmemelidir.

`audit/sample50_manifest.json` sıra/barkodları, kaynak satırlarını ve kararları içerir. Girdiler, bu incelemede 23.801 ürün ve 32.076 bileşen kaydından oluşur. Son doğrulama sonucu `audit/verification_result.json` içindedir. Ham dosya baytlarının hash eşitliği denetlenmiş gibi sunulmaz.

`reference` klasörü d4afc8df9de1381097fb9934488f705339820757 commitindeki notebook, normalleştirme kodu ve tuz listesinin tarihsel kopyasıdır. Doğrulama bu kopyayı kullanır; çalışan pipeline'ın yerine kopyalanmamalıdır. Özellikle eski notebook'un otomatik 50/50 çıktısı burada geçmiş kanıt olarak korunur, elle kontrol sonucu olarak kullanılmaz.

Bu commit çalışma notebook'unu veya ayrıştırma motorunu düzeltmez. Hata düzeltmelerinden sonra aynı 50 barkod üzerinde yeni çıktı ayrıca değerlendirilmelidir. BEDOXINAL ve OSMEGA için raporda belirtilen ürün belgesi tamamlama işleri de sürmektedir.
