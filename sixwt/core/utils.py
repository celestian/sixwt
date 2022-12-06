import hashlib
import os
from pathlib import Path

LINE_LENGTH = 79


def short_label(string, length=6):

    if length > 128:
        raise ValueError(f"length {length} exceeds 128")
    hash_object = hashlib.sha512(string.encode())
    hash_hex = hash_object.hexdigest()
    return hash_hex[0:length]


def clear_screen():
    _ = os.system("clear" if os.name == "posix" else "cls")


def print_centered(string, before=1, after=0):
    count = int((LINE_LENGTH - len(string) - 4) / 2)
    extra = "=" * count
    output = f"{extra}> {string} <{extra}"
    while 1:
        if len(output) == LINE_LENGTH:
            break
        output = output + "="
    before_str = "\n" * before
    after_str = "\n" * after
    print(before_str + output + after_str)


def print_hr():
    extra = "=" * LINE_LENGTH
    print(extra)


def abs_path(path):
    return Path.resolve(Path.expanduser(Path(path)))


def does_file_exist(path_to_file):
    path = Path(path_to_file)
    return path.is_file()


def does_dir_exist(path_to_dir):
    path = Path(path_to_dir)
    return path.is_dir()


def is_file_empty(path_to_file):
    path = Path(path_to_file)
    return path.stat().st_size == 0
