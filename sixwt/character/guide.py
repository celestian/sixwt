from tabulate import tabulate

from ..core.utils import print_centered
from .character import Priority, States


class CharacterGuide:  # pylint: disable=too-few-public-methods
    def __init__(self, character, storage):
        self.__character = character
        self.__storage = storage

    def advise(self):
        may_add_metatype = self.__character.may_add_metatype()

        if self.__character.state == States.PRIORITY and not may_add_metatype:
            print("  Jak vybrat priority")

        if self.__character.state == States.PRIORITY and may_add_metatype:
            priorities = self.__character.get_data()["priorities"]
            priority = list(priorities.keys())[
                list(priorities.values()).index(str(Priority.METATYPE))
            ]
            table = self.__storage.get_metatypes(priority)

            print_centered("Next Step")
            print("Select a metatype from given table:")
            print(
                tabulate(table, headers=["hash", "metatype"], tablefmt="simple_outline")
            )
            print("Use commmand:\n  metatype <metatype_hash>")
