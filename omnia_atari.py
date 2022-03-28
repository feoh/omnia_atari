from internetarchive import search_items,Item
from pathlib import Path
from urllib3.exceptions import ConnectTimeoutError
from requests.exceptions import ConnectTimeout
import time


DESTINATION_FOLDER_PATH = Path.home() / "iadownloads"
DESTINATION_FOLDER_PATH.mkdir(exist_ok=True)

# This is my current best guess to get all 8 bit Atari Binaries the Internet Archive has on offer.
search = search_items('atr_ AND a8b_ AND Atari_8_bit')

# This is imperfect to say the least but if we fail, pause a minute and check the list for uncompleted downloads
while True:
    item: Item
    for item in search.iter_as_items():
        try:
            item.download(verbose=True, retries=50, destdir=str(DESTINATION_FOLDER_PATH))
        except ConnectTimeoutError:
            print("If at first we don't succeed - START AGAIN! - urllib3 timeout.")
            time.sleep(30)
            break
        except ConnectTimeout:
            print("If at first we don't succeed - START AGAIN! - requests timeout.")
            time.sleep(30)
            break


