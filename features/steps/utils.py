import configparser
from pathlib import Path


def abs_path(path):
    return Path.resolve(Path.expanduser(Path(path)))


def read_configuration(filename):
    cfg = {}
    cfg_parser = configparser.ConfigParser()
    cfg_file = abs_path(filename)
    cfg_parser.read(cfg_file)
    for section in cfg_parser.sections():
        cfg[section] = {}
        for key in cfg_parser.options(section):
            cfg[section][key] = cfg_parser.get(section, key)

    return cfg
