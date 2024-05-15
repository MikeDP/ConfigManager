#!/usr/bin/env python3
'''
ConfigManager.py

This python module contains a class to trivially persist application data.

V0.1  Alpha 15/05/24 
'''
import json
import os
from pathlib import Path

# ############################### CONSTANTS #############################
__VER__ = '0.1'

# ############################### CLASSES ###############################

class ConfigManager:
    """
    ConfigManager loads and saves configuration data using json.  A CM instance will
    construct attibutes with stored values from the data it finds in the 'file_name' file.
    New attributes can be generated in code as required and all non-private attributes
    (but including 'CM._comment') will be saved by a call to save_config().  Attributes 
    can be any data type.  If no configuration file is found,  one will be constructed 
    when save_config() is called.
    """
    def __init__(self, foldr: str, file_name: str, comment: str="DO NOT HAND EDIT!"):
        """
        Initialize the ConfigManager.
        Args:
            foldr (str): Name of a folder in ~/.config in which to place
                         the config file - created if not present.
            file_name (str): The name of the configuration file, no extension!
            comment (str): User definable comment saved with config.
        """
        # Ensure config file and folder can exist
        HOME = os.path.expanduser("~")
        self._file_path = f"{HOME}/.config/{foldr}"
        Path(self._file_path).mkdir(parents=True, exist_ok=True)
        self._file_path += f"/{file_name}.conf"
        self._comment = comment
        self.load_config()

    def load_config(self):
        """ Load configuration data from the file."""
        try:
            with open(self._file_path, 'r', encoding="utf8") as file:
                config_data = json.load(file)
                for key, value in config_data.items():
                    setattr(self, key, value)
        except FileNotFoundError:
            print("Config file not found. Creating a new one.")

    def save_config(self):
        """Save configuration data to the file. """
        config_data = {}
        for attr_name in dir(self):
            if not attr_name.startswith("_") or attr_name == '_comment':
                if type(getattr(self, attr_name)) in (bool, str, int, complex, list, float, tuple, dict, set, bytes):
                    config_data[attr_name] = getattr(self, attr_name)

        # Sort it
        sorted_attributes = sorted(config_data.items(), key=lambda x: (not x[0].startswith('_'), x[0]))
        sorted_dict = {key: value for key, value in sorted_attributes}
        # Now sort and save it
        with open(self._file_path, 'w', encoding="utf8") as file:
            json.dump(sorted_dict, file, indent=2, sort_keys=False)


    def __getattr__(self, name):
        """
        Get attribute of 'name'
        Returns value if 'name' exists or creates it as/return None
        """
        try:
            return super().__getattribute__(name)
        except AttributeError:
            setattr(self, name, None)
            return None

    def assign(self, attr_name: str, def_val: any = None):
        """Return value of self.'attr_name' unless it's None
           when we assign it and return def_val"""
        current_val = getattr(self, attr_name)
        if current_val is None:
            setattr(self, attr_name, def_val)
            current_val = def_val
        return current_val
