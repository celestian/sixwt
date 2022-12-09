# Copyright (C) 2022 sixwt Contributors, see LICENSE

import csv
import os
import sqlite3

from ..core.utils import short_label


class DBStorage:
    def __init__(self, config):
        self.__db_connection = sqlite3.connect(config.database_file)
        self.__db_connection.row_factory = sqlite3.Row
        self.__cursor = self.__db_connection.cursor()
        self.__catalog_folder = config.catalog_folder

    def __del__(self):
        self.__db_connection.close()

    def create(self):
        self.__cursor.execute("CREATE TABLE metatype(hash, metatype, priority, points)")

        data = []
        file_path = os.path.join(self.__catalog_folder, "priority_table/metatype.csv")
        with open(file_path, encoding="utf-8") as csv_file:
            dialect = csv.Sniffer().sniff(csv_file.read(1024))
            csv_file.seek(0)
            reader = csv.DictReader(csv_file, dialect=dialect)
            for row in reader:
                label = short_label(f'{row["priority"]} {row["metatype"]}')
                data.append((label, row["metatype"], row["priority"], row["points"]))

        self.__cursor.executemany("INSERT INTO metatype VALUES (?, ?, ?, ?)", data)
        self.__db_connection.commit()

    def get_metatypes(self, priority):
        self.__cursor.execute(
            "SELECT hash, metatype from metatype where priority=? order by metatype;",
            (priority,),
        )
        return self.__cursor.fetchall()
