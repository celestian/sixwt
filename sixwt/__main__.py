# Copyright (C) 2022 sixwt Contributors, see LICENSE

"""SixWT: Sixth World Tool

Usage:
  sixwt [--cfg=<cfg_file>] init [--with-examples]
  sixwt [--cfg=<cfg_file>] db update
  sixwt [--cfg=<cfg_file>] wizard
  sixwt [--cfg=<cfg_file>] build <character.swt>
  sixwt (-h | --help)
  sixwt --version

Options:
  --cfg=<cfg_file>  Configuration file [default: ./sixwt.conf].
  -h --help         Show this screen.
  --version         Show version.
"""

import logging
import os
import sys

from docopt import docopt

from ._version import __version__
from .core.configuration import Config
from .core.utils import does_dir_exist, does_file_exist
from .example.catalog import generate_examples
from .storage.database import DBStorage
from .ui.wizard import WizardUI


def check_storage(config):
    correct = True
    if not does_dir_exist(config.storage_folder):
        logging.warning("Directory [%s] is not created.", config.storage_folder)
        correct = False
    if not does_dir_exist(config.character_folder):
        logging.warning("Directory [%s] is not created.", config.character_folder)
        correct = False
    if not does_dir_exist(config.catalog_folder):
        logging.warning("Directory [%s] is not created.", config.catalog_folder)
        correct = False
    if not correct:
        print("You should run `sixwt init`.")
    return correct


def prepare_storage(config):
    if not does_dir_exist(config.storage_folder):
        os.makedirs(config.storage_folder)
        logging.info("Directory [%s] created.", config.storage_folder)
    if not does_dir_exist(config.character_folder):
        os.makedirs(config.character_folder)
        logging.info("Directory [%s] created.", config.character_folder)
    if not does_dir_exist(config.catalog_folder):
        os.makedirs(config.catalog_folder)
        logging.info("Directory [%s] created.", config.catalog_folder)


def main():

    args = docopt(__doc__, version=__version__)
    config = Config(args, __version__)
    print(config.app_header)

    if args["init"]:
        prepare_storage(config)
        if args["--with-examples"]:
            generate_examples(config)
        sys.exit()

    if not check_storage(config):
        sys.exit()

    if args["update"] and args["db"]:
        if not does_file_exist(config.catalog_metatype):
            logging.error(
                "Catalog file [%s] is missing.",
                config.catalog_metatype,
            )
            print(
                "For a better understanding of the catalog format,",
                "you can run `sixwt init --with-examples`.",
            )

        storage = DBStorage(config)
        storage.create()
        sys.exit()

    if not does_file_exist(config.database_file):
        logging.error("Database file [%s] is missing.", config.database_file)
        print("You should run `sixwt db update`.")
        sys.exit()

    if args["wizard"]:
        WizardUI(config)
        sys.exit()


if __name__ == "__main__":
    main()
