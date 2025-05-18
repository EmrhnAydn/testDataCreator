# download_test_images.py
#
# Gereken ek paket:
#   pip install icrawler pillow
#
# Kullanım:
#   python download_test_images.py
#
# NOT: İlk çalıştırmada Bing'in günlük kota sınırını zorlamamak için
#      max_num değerini küçük tutun (ör: 15-20). Gerektikçe artırabilirsiniz.

import os
import shutil
from icrawler.builtin import BingImageCrawler
from PIL import Image  # yalnızca görseli doğrulamak için

# -------------------------------------------------
# Ortak yardımcılar
# -------------------------------------------------
def create_class_folders(base_dir: str, classes: list[str]) -> None:
    """Her sınıf için (varsa temizleyip) klasör oluşturur."""
    for cls in classes:
        folder_path = os.path.join(base_dir, cls)
        if os.path.exists(folder_path):
            # İçindeki eski görselleri sil
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                if os.path.isfile(item_path):
                    os.remove(item_path)
                else:
                    shutil.rmtree(item_path)
        else:
            os.makedirs(folder_path)
        print(f"[✓] Hazır klasör: {folder_path}")

def download_images(class_name: str,
                    output_dir: str,
                    num_images: int = 20) -> None:
    """
    Bing üzerinden belirtilen hayvan sınıfı için gerçek görseller indirir.
    İndirilen her görsel Pillow ile açılarak doğrulanır; bozuksa silinir.
    """
    print(f"→ {class_name} sınıfı için {num_images} görsel indiriliyor...")
    crawler = BingImageCrawler(storage={'root_dir': output_dir})

    crawler.crawl(
    keyword=f"{class_name} animal photo",
    max_num=num_images,
    filters={
        # Örnek: yalnızca Creative Commons
        "license": "creativecommons",
        # veya kamu malı istersen:
        "license": "publicdomain",
        #
        # Boyut filtresi de eklemek istersen:
         "size": "large",
    },
    file_idx_offset=0
)


    # Bozuk veya Pillow'un açamadığı görselleri temizle
    for fname in os.listdir(output_dir):
        fpath = os.path.join(output_dir, fname)
        try:
            with Image.open(fpath) as img:
                img.verify()  # yalnızca doğrulama, belleğe almıyor
        except Exception:
            print(f"  ⚠️  Silindi (bozuk): {fpath}")
            os.remove(fpath)

# -------------------------------------------------
# Ana akış
# -------------------------------------------------
def main() -> None:
    classes = [
        "antelope", "badger", "bat", "bear", "chimpanzee", "cockroach",
        "cow", "coyote", "crab", "crow", "deer", "dog", "dolphin", "donkey",
        "dragonfly", "duck", "eagle", "elephant", "flamingo", "fly", "fox",
        "goat", "goldfish", "goose", "gorilla", "grasshopper", "hamster",
        "hare", "hedgehog", "hippopotamus", "hornbill", "horse", "hummingbird",
        "hyena", "jellyfish", "kangaroo", "koala", "ladybugs", "leopard",
        "lion", "lizard", "lobster", "mosquito", "moth", "mouse", "octopus",
        "okapi", "orangutan", "otter", "owl", "ox", "oyster", "panda",
        "parrot", "pelecaniformes", "penguin", "pig", "pigeon", "porcupine",
        "possum", "raccoon", "rat", "reindeer", "rhinoceros", "sandpiper",
        "seahorse", "seal", "shark", "sheep", "snake", "sparrow", "squid",
        "squirrel", "starfish", "swan", "tiger", "turkey", "turtle", "whale",
        "wolf", "wombat", "woodpecker", "zebra"
    ]

    test_dir = "test"
    create_class_folders(test_dir, classes)

    for cls in classes:
        out_path = os.path.join(test_dir, cls)
        download_images(cls, out_path, num_images=20)

    print("\n✔️  Tüm sınıflar için indirme tamamlandı.")

if __name__ == "__main__":
    main()
