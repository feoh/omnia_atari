from internetarchive import search_items,Item
from pathlib import Path


DESTINATION_FOLDER_PATH = Path.home() / "iadownloads"
DESTINATION_FOLDER_PATH.mkdir(exist_ok=True)

# This is my current best guess to get all 8 bit Atari Binaries the Internet Archive has on offer.
search = search_items('atr_ AND a8b_ AND Atari_8_bit')

item: Item
for item in search.iter_as_items():
    print(f"Downloading {item}")
    item.download(verbose=True, destdir=str(DESTINATION_FOLDER_PATH))

