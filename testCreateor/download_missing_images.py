# download_missing_images.py
#
# Gereken ek paketler:
#   pip install icrawler pillow
#
# Çalıştırma:
#   python download_missing_images.py
#
# Bu script, "test/" altındaki sınıf klasörlerini tarar.
# İçinde hiç **doğrulanmış** görsel bulunmayan klasörleri tespit eder
# ve her biri için Bing üzerinden yeni görseller indirir.

import os
from icrawler.builtin import BingImageCrawler
from PIL import Image

# -------------------------------------------------
# Ayarlar – gerekirse değiştir
# -------------------------------------------------
BASE_DIR = "test"          # Sınıf klasörlerinin olduğu ana dizin
NUM_IMAGES = 20            # Her eksik sınıf için indirilecek görsel sayısı
LICENSE_FILTER = "creativecommons"   # (None ⇒ lisans filtresi yok)
# Geçerli değerler: creativecommons, publicdomain, noncommercial,
#                  commercial, noncommercial,modify, commercial,modify

# -------------------------------------------------
# Yardımcılar
# -------------------------------------------------
def count_valid_images(folder: str) -> int:
    """Klasördeki bozuk dosyaları temizler ve geçerli görsel sayısını döndürür."""
    valid = 0
    for fname in os.listdir(folder):
        fpath = os.path.join(folder, fname)
        if not os.path.isfile(fpath):
            continue
        try:
            with Image.open(fpath) as img:
                img.verify()
            valid += 1
        except Exception:
            # Bozuk dosyayı sil
            os.remove(fpath)
    return valid


def find_empty_classes(base_dir: str) -> list[str]:
    """Hiç geçerli görseli olmayan alt klasörleri döndürür."""
    empty = []
    for cls in sorted(os.listdir(base_dir)):
        cls_path = os.path.join(base_dir, cls)
        if not os.path.isdir(cls_path):
            continue
        if count_valid_images(cls_path) == 0:
            empty.append(cls)
    return empty


def download_images(class_name: str,
                    output_dir: str,
                    num_images: int = 20) -> None:
    """Belirtilen sınıf için Bing'den görseller indirir ve bozukları ayıklar."""
    print(f"→ {class_name} için {num_images} görsel indiriliyor…")
    crawler = BingImageCrawler(storage={'root_dir': output_dir})

    filters = {}
    if LICENSE_FILTER:
        filters["license"] = LICENSE_FILTER

    crawler.crawl(
        keyword=f"{class_name} animal photo",
        max_num=num_images,
        filters=filters,
        file_idx_offset=0
    )

    # İndirilen dosyaları doğrula
    _ = count_valid_images(output_dir)


def main() -> None:
    empty_classes = find_empty_classes(BASE_DIR)
    if not empty_classes:
        print("✔️  Boş sınıf klasörü bulunmadı – işlem yapılmadı.")
        return

    print(f"⚠️  Görseli olmayan sınıflar: {', '.join(empty_classes)}")
    for cls in empty_classes:
        cls_dir = os.path.join(BASE_DIR, cls)
        download_images(cls, cls_dir, NUM_IMAGES)

    print("\n✔️  Eksik sınıflar için indirme tamamlandı.")


if __name__ == "__main__":
    main()
