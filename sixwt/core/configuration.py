import configparser
import logging
import sys

from ..core.utils import abs_path, does_file_exist


class Config:
    def __init__(self, args, version):
        self.__cfg = {}
        self.__version = version

        cfg_parser = configparser.ConfigParser()
        cfg_file = abs_path(args["--cfg"])
        if not does_file_exist(cfg_file):
            log_format = "%(levelname)s: %(message)s"
            logging.basicConfig(format=log_format, level=logging.INFO)
            logging.error("Configuration file [%s] doesn't exist.", cfg_file)
            sys.exit()
        cfg_parser.read(cfg_file)

        for section in cfg_parser.sections():
            self.__cfg[section] = {}
            for key in cfg_parser.options(section):
                self.__cfg[section][key] = cfg_parser.get(section, key)

        log_format = "%(levelname)s: %(message)s"
        match self.__cfg["sixwt"]["log_level"]:
            case "debug":
                logging.basicConfig(format=log_format, level=logging.DEBUG)
            case "info":
                logging.basicConfig(format=log_format, level=logging.INFO)
            case "warning":
                logging.basicConfig(format=log_format, level=logging.WARNING)
            case "error":
                logging.basicConfig(format=log_format, level=logging.ERROR)
            case "critical":
                logging.basicConfig(format=log_format, level=logging.CRITICAL)
            case _:
                logging.basicConfig(format=log_format, level=logging.INFO)
                logging.warning(
                    "Missing sixwt/log_level in configuration file [%s]",
                    cfg_file,
                )

        logging.info("Configuration loaded from [%s].", cfg_file)

    @property
    def app_header(self):
        return f"SixWT ({self.__version}): Sixth World Tool"

    @property
    def storage_folder(self):
        return abs_path(self.__cfg["sixwt"]["storage_folder"])

    @property
    def character_folder(self):
        return abs_path(self.storage_folder).joinpath("characters")

    @property
    def catalog_folder(self):
        return abs_path(self.storage_folder).joinpath("catalog")

    @property
    def database_file(self):
        return abs_path(self.storage_folder).joinpath("sixwt.db")

    @property
    def catalog_metatype(self):
        return self.catalog_folder.joinpath("priority_table", "metatype.csv")
