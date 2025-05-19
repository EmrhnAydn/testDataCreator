#   pip install icrawler pillow

import os
import time
from icrawler.builtin import BingImageCrawler
from PIL import Image

TRAIN_DIR = "path"  # Sınıf adlarını buradan al
TEST_DIR  = "test"                                   
TARGET_PER_CLASS = 6    # you can change
LICENSE_FILTER = None  # "creativecommons"

def list_class_names(train_dir: str) -> list[str]:
    return sorted([
        d for d in os.listdir(train_dir)
        if os.path.isdir(os.path.join(train_dir, d))
    ])
def ensure_class_folders(base_dir: str, class_names: list[str]) -> None:
    for name in class_names:
        path = os.path.join(base_dir, name)
        os.makedirs(path, exist_ok=True)

def count_and_clean(folder: str) -> int:
    """Bozuk görselleri silip geçerli dosya sayısını döndürür."""
    valid = 0
    for f in os.listdir(folder):
        fp = os.path.join(folder, f)
        if not os.path.isfile(fp):
            continue
        try:
            with Image.open(fp) as img:
                img.verify()
            valid += 1
        except Exception:
            os.remove(fp)
    return valid

def download_images(class_name: str, out_dir: str, n: int) -> None:
    """Bing'den n adet yeni görsel indirir ve bozukları temizler."""
    print(f"→ {class_name}: {n} adet yeni görsel indiriliyor…")
    crawler = BingImageCrawler(storage={'root_dir': out_dir})

    filters = {}
    if LICENSE_FILTER:
        filters["license"] = LICENSE_FILTER

    # Mevcut dosya sayısını offset olarak kullanmak tekrarını azaltır
    offset = len(os.listdir(out_dir))
    crawler.crawl(
        keyword=f"{class_name} animal photo",
        max_num=n,
        filters=filters,
        file_idx_offset=offset
    )
    # İndirilenleri doğrula
    _ = count_and_clean(out_dir)

def main() -> None:
    class_names = list_class_names(TRAIN_DIR)
    if not class_names:
        print("TRAIN_DIR içinde sınıf klasörü bulunamadı!")
        return

    ensure_class_folders(TEST_DIR, class_names)

    for cls in class_names:
        cls_dir = os.path.join(TEST_DIR, cls)
        while True:
            valid = count_and_clean(cls_dir)
            if valid >= TARGET_PER_CLASS:
                print(f"✓ {cls}: {valid} görsel hazır")
                break
            needed = TARGET_PER_CLASS - valid
            download_images(cls, cls_dir, needed)
            time.sleep(1.0)

    print("\nTüm sınıflar en az", TARGET_PER_CLASS, "görsele tamamlandı.")

if __name__ == "__main__":
    main()
