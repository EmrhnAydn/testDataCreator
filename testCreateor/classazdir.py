import os

def klasor_isimlerini_yazdir(ana_dizin):
  """
  Belirtilen ana dizin içindeki tüm klasörlerin isimlerini yazdırır.

  Args:
    ana_dizin: Klasörlerin aranacağı ana dizinin dosya yolu.
  """
  try:
    sayi = 0
    for item in os.listdir(ana_dizin):
      alt_dizin_yolu = os.path.join(ana_dizin, item)
      if os.path.isdir(alt_dizin_yolu):
        print(item)
        sayi += 1     
    print(f"Toplam {sayi} klasör bulundu.")   
  except FileNotFoundError:
    print(f"Hata: Belirtilen dizin bulunamadı: {ana_dizin}")
  except Exception as e:
    print(f"Bir hata oluştu: {e}")

# Kullanım örneği:
train_veri_dizini = "train path"  # Kendi train veri dizininizin yolunu buraya yazın
klasor_isimlerini_yazdir(train_veri_dizini)