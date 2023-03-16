#!/usr/bin/env python
""" 
Author: KylesDev
"""

# Import standard modules
import tomli

# Import Libraries

# Import Application Modules

CONFIG_FILE_PATH = "resources/config.toml"


def load_config():
    """This method loads the TOML configuration file in resources/config.toml
    and returns a dictionary with the configuration values"""

    with open(CONFIG_FILE_PATH, mode="rb") as config_file:
        config = tomli.load(config_file)
        return config


CONFIG = load_config()
