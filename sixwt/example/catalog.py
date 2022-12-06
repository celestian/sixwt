import csv
import os

from ..core.utils import does_dir_exist, does_file_exist


def generate_examples(config):
    priority_table_folder = config.catalog_folder.joinpath("priority_table")
    if not does_dir_exist(priority_table_folder):
        os.makedirs(priority_table_folder)
    metatype_file = priority_table_folder.joinpath("metatype.csv")
    if not does_file_exist(metatype_file):
        with open(metatype_file, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["priority", "metatype", "points"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect="unix")
            writer.writeheader()
            writer.writerow({"priority": "a", "metatype": "human", "points": 10})
            writer.writerow({"priority": "a", "metatype": "hobit", "points": 10})
            writer.writerow({"priority": "b", "metatype": "human", "points": 8})
            writer.writerow({"priority": "b", "metatype": "hobit", "points": 8})
