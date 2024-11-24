"""
find files that are missing in the destination
"""

import os
import argparse

parser = argparse.ArgumentParser(
    prog="python3 filediff.py",
    description="files that are not present on the destination"
)
parser.add_argument("-s", "--source")
parser.add_argument("-d", "--destination")
args = parser.parse_args()
src_location = args.source
dst_location = args.destination

if not src_location or not dst_location:
    parser.print_help()
    exit(1)

print(f"src_location: {src_location}")
print(f"dst_location: {dst_location}")


path_exists = os.path.exists


def get_file_set_from_location(location: str) -> set[str]:
    """
    get all files from location (root)

    Args:
        location (str): filesystem path

    Returns:
        set[str]: returns only the sub-path/filename 

        example:
            SRC_LOCATION=/Users/admin/work-sync

            found:
            /Users/admin/work-sync/abc/a.txt

            here root: /Users/admin/work-sync
            will return /abc/a.txt

    """
    file_set = set()
    for root, dirs, files in os.walk(location):
        sub_dir = ""
        if root.startswith(location):
            start_idx = len(location)
            sub_dir = root[start_idx:]
        for file in files:
            f = os.path.join(sub_dir, file)
            file_set.add(f)

    return file_set


def print_file_set(title: str, file_set: set[str]):
    """
    print file set

    Args:
        title (str): use to describe whats being printed
        file_set (set[str]): file locations
    """
    print()
    print(f"{title}")
    print()
    for f in file_set:
        print(f)
    
    print()
    print(f"total files: {len(file_set)}")
    print()


if not path_exists(src_location):
    print("source path does not exist")
    exit(1)

if not path_exists(dst_location):
    print("destination path does not exist")
    exit(1)

src_file_set = get_file_set_from_location(src_location)
dst_file_set = get_file_set_from_location(dst_location)

files_not_found_set = src_file_set - dst_file_set
print_file_set("files not present in the destination", files_not_found_set)
