#!/usr/bin/env python3
'''
ConfigManager.py

This python module contains a class to trivially persist application data.

v0.1  Alpha 15/05/24 
v0.2  22/12/24 Fixed tuple, set and bytes save/load
'''

import os
import json
from pathlib import Path
import base64

class ConfigManager:
    """
    ConfigManager loads and saves configuration data using json. A CM instance will
    construct attributes with stored values from the data it finds in the 'file_name' file.
    New attributes can be generated in code as required, and all non-callable attributes
    (excluding those with names starting with '_') will be saved by a call to
    save_config(). Attributes can be any data type. If no configuration file is found,
    one will be constructed when save_config() is called.
    """

    def __init__(self, foldr: str, file_name: str, comment: str = "DO NOT HAND EDIT!"):
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

    def _custom_decoder(self, dct):
        """Decode custom types."""
        if "__type__" in dct:
            if dct["__type__"] == "tuple":
                return tuple(self._custom_decoder(item) if isinstance(item, dict) else item for item in dct["items"])
            if dct["__type__"] == "set":
                return set(self._custom_decoder(item) if isinstance(item, dict) else item for item in dct["items"])
            if dct["__type__"] == "bytes":
                return base64.b64decode(dct["data"].encode("utf-8"))
        # Process nested dictionaries
        return {key: self._custom_decoder(value) if isinstance(value, dict) else value for key, value in dct.items()}

    def _preprocess(self, obj):
        """Recursively preprocess the object to handle custom types."""
        if isinstance(obj, tuple):
            return {"__type__": "tuple", "items": [self._preprocess(item) for item in obj]}
        if isinstance(obj, set):
            return {"__type__": "set", "items": [self._preprocess(item) for item in obj]}
        if isinstance(obj, bytes):
            return {"__type__": "bytes", "data": base64.b64encode(obj).decode("utf-8")}
        if isinstance(obj, dict):
            return {key: self._preprocess(value) for key, value in obj.items()}
        if isinstance(obj, list):
            return [self._preprocess(item) for item in obj]
        return obj

    def load_config(self):
        """Load configuration data from the file."""
        try:
            with open(self._file_path, 'r', encoding="utf8") as file:
                config_data = json.load(file, object_hook=self._custom_decoder)
                for key, value in config_data.items():
                    setattr(self, key, value)
        except FileNotFoundError:
            print("Config file not found. Creating a new one.")

    def save_config(self):
        """Save configuration data to the file."""
        config_data = {}
        attr_list = (bool, int, float, complex, list, tuple, dict, set, str, bytes)
        for attr_name in dir(self):
            if not attr_name.startswith("_") or attr_name == '_comment':
                if type(getattr(self, attr_name)) in attr_list:
                    config_data[attr_name] = getattr(self, attr_name)

        # Preprocess the data for serialization
        processed_data = self._preprocess(config_data)

        # Save the preprocessed data
        with open(self._file_path, 'w', encoding="utf8") as file:
            json.dump(processed_data, file, indent=2, sort_keys=False)

    def __getattr__(self, name):
        """Get attribute value or None."""
        try:
            return super().__getattribute__(name)
        except AttributeError:
            setattr(self, name, None)
            return None

    def assign(self, attr_name: str, def_val: any = None):
        """Return value of self.'attr_name' unless it's None
           when we assign it and return def_val."""
        current_val = getattr(self, attr_name)
        if current_val is None:
            setattr(self, attr_name, def_val)
            current_val = def_val
        return current_val
