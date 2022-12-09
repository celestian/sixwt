# Copyright (C) 2022 sixwt Contributors, see LICENSE

from pathlib import Path

from InquirerPy import inquirer

from ..character.parser import CharacterParser


class WizardUI:
    def __init__(self, config):
        self.__config = config
        self.__parser = None

        self.__q_choose_character()

    def __q_choose_character(self):

        choices = ["<new_character>"]
        existing_characters = Path(self.__config.character_folder).glob("*")
        character_files = [x.name for x in existing_characters if x.is_file()]
        choices.extend(character_files)

        choice = inquirer.fuzzy(
            message="Choose character:",
            choices=choices,
            default="",
        ).execute()

        if choice == "<new_character>":
            name = inquirer.text(message="Enter name of the new character:").execute()
            name = " ".join([x for x in (name.strip()).split(" ") if x != ""])
            file_name = name.replace(" ", "_").lower() + ".swt"

            continue_on_existing = True
            if file_name in character_files:
                continue_on_existing = inquirer.confirm(
                    message="That character already exists, do you want to edit it?",
                    default=False,
                ).execute()

            if continue_on_existing:
                new_file = self.__config.character_folder.joinpath(file_name)
                self.__parser = CharacterParser(new_file)
                self.__parser.set_name(name)
                self.__q_continue_on_existing()
            else:
                self.__q_choose_character()
        else:
            existing_file = self.__config.character_folder.joinpath(choice)
            self.__parser = CharacterParser(existing_file)
            self.__q_continue_on_existing()

    def __q_continue_on_existing(self):
        print("Pokračujeme.")
