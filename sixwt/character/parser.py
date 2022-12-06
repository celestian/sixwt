import json

from ..core.utils import does_file_exist
from .character import Character


class CharacterParser:
    def __init__(self, filename):
        self.__filename = filename
        self.__steps = []

        self.__load_steps()

    def __save_steps(self):
        with open(self.__filename, "w", encoding="utf-8") as out:
            json.dump(self.__steps, out, sort_keys=True, ensure_ascii=False, indent=2)

    def __load_steps(self):
        if not does_file_exist(self.__filename):
            self.__save_steps()

        with open(self.__filename, "r", encoding="utf-8") as source:
            self.__steps = json.load(source)

        print(self.__steps)

    def set_name(self, name):
        self.__steps.extend(
            [{"id": len(self.__steps) + 1, "step": "set_name", "value": name}]
        )
        print(self.__steps)
        self.__save_steps()
