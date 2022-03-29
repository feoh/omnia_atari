import time
from pathlib import Path

from internetarchive import search_items, Item
from requests.exceptions import ConnectTimeout
from urllib3.exceptions import ConnectTimeoutError

DESTINATION_FOLDER_PATH = Path.home() / "iadownloads"
DESTINATION_FOLDER_PATH.mkdir(exist_ok=True)


# This is my best guess to get all 8 bit Atari Binaries the Internet Archive has on offer.
def download_for_glob(glob_pattern, search_results: search_items):
    # This is imperfect to say the least but if we fail, pause a minute and check the list for uncompleted downloads
    # Also gross - since glob_pattern only supports a SINGLE glob, if I want to ONLY download the various binary formats
    # I need to do separate downloads for each :(
    item: Item
    for item in search_results.iter_as_items():
        while True:
            try:
                item.download(verbose=True, glob_pattern=glob_pattern, retries=50, destdir=str(DESTINATION_FOLDER_PATH))
            except ConnectTimeoutError:
                print("If at first we don't succeed - START AGAIN! - urllib3 timeout.")
                time.sleep(30)
                continue
            except ConnectTimeout:
                print("If at first we don't succeed - START AGAIN! - requests timeout.")
                time.sleep(30)
                continue
            break


search = search_items('a8b_')
download_for_glob("*.atr", search)
download_for_glob("*.rom", search)
download_for_glob("*.cas", search)
download_for_glob("*.car", search)
