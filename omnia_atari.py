from operator import itemgetter
import time
import argparse
from pathlib import Path

from internetarchive import search_items, Item
from requests.exceptions import ConnectTimeout
from urllib3.exceptions import ConnectTimeoutError

parser = argparse.ArgumentParser()

parser.add_argument("root", help="Root folder for downloads")
args = parser.parse_args()

DESTINATION_FOLDER_ROOT = Path(args.root)
DESTINATION_ITEMS_PATH = DESTINATION_FOLDER_ROOT / "items"
DESTINATION_ITEMS_PATH.mkdir(exist_ok=True)
DESTINATION_COLLECTIONS_PATH = DESTINATION_FOLDER_ROOT / "collections"
DESTINATION_COLLECTIONS_PATH.mkdir(exist_ok=True)


# This is my best guess to get all 8 bit Atari Binaries the Internet Archive has on offer.
def download_for_glob(glob_pattern, search_results):
    # This is imperfect to say the least but if we fail, pause a minute and check the list for uncompleted downloads
    # Also gross - since glob_pattern only supports a SINGLE glob, if I want to ONLY download the various binary formats
    # I need to do separate downloads for each :(
    item: Item
    for item in search_results.iter_as_items():
        while True:
            try:
                item.download(verbose=True, glob_pattern=glob_pattern, retries=50, destdir=str(DESTINATION_ITEMS_PATH))
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

# Now that we've downloaded the giant bag of items,
# Create symlinks for the collections each title is in
# in the collections folder. Name the links by the
# item's title.
