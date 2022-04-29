#!/usr/bin/env python
import pathlib
import time
import argparse
from pathlib import Path
from slugify import slugify

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

    current_item: Item
    for current_item in search.iter_as_items():
        item_files = get_item_files(current_item)
        atari_files: list = find_atari_files(item_files)
        if not atari_files:
            continue

        atari_files_flat = " ".join(atari_files)
        print(f"atari_files: {atari_files_flat}")

        print(f"Downloading {current_item.identifier} to {destination_items_path}")
        current_item.download(verbose=True, files=atari_files_flat, destdir=str(destination_items_path), retries=3)
        collection_ids = [
            collection.metadata['identifier']
            for collection in current_item.collection
        ]
        print(f"collection_ids: {collection_ids}")
        current_item_path: pathlib.Path = destination_items_path / current_item.identifier
        for collection_name in collection_ids:
            collection_folder_path: pathlib.Path = destination_collections_path / collection_name
            collection_folder_path.mkdir(exist_ok=True)
            slugified_title = slugify(current_item.metadata['title'])
            collection_symlink_path: pathlib.Path = collection_folder_path / slugified_title
            collection_symlink_path.mkdir(exist_ok=True)
            print(f"Creating symbolic link from {current_item_path} to {collection_symlink_path}")
            if not collection_symlink_path.exists():
                current_item_path.symlink_to(collection_symlink_path