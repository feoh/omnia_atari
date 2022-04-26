import time
import argparse
from pathlib import Path

from internetarchive import search_items, Item


def handle_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", help="Root folder for downloads")
    return parser.parse_args()


def find_atari_files(files: list) -> list:
    atari_extensions = ['.atr', '.rom', '.cas', '.car', '.xex']
    found_files = [
        atari_file
        for atari_file in files
        for extension in atari_extensions
        if atari_file.endswith(extension)
    ]
    return found_files


def get_item_files(item: Item) -> list:
    item_files = [
        item_file['name']
        for item_file in item.files
    ]
    return item_files


if __name__ == '__main__':
    args = handle_args()
    destination_folder_root = Path(args.root)
    destination_items_path = destination_folder_root / "items"
    destination_items_path.mkdir(exist_ok=True)
    destination_collections_path = destination_folder_root / "collections"
    destination_collections_path.mkdir(exist_ok=True)

    search = search_items('a8b_')

    # perform_download(search)

    current_item: Item
    for current_item in search.iter_as_items():
        item_files = get_item_files(current_item)
        atari_files = find_atari_files(item_files)
        current_item.download(verbose=True, files=atari_files, destdir=str(destination_items_path), retries=3)
        # TODO symlink a nicely named (by title) dir for this item into the collections folder.
