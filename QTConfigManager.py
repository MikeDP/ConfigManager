#!/usr/bin/env python3
'''
QTConfigManager.py

This python module contains a class to trivially persist application data,
including QT GUI interface items.

V0.1  Alpha 17/05/24 
v0.2  18/05/24 Extended to multiple forms handling
'''
import json
import os
from pathlib import Path
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import (QCheckBox, QComboBox, QDateEdit, QDoubleSpinBox,
                             QLabel, QLineEdit, QRadioButton, QSpinBox, QWidget)

# ############################# CONSTANTS ##############################
__VER__ = '0.2'

# ############################## CLASSES ###############################

class QTConfigManager:
    """
    QTConfigManager loads and saves configuration data using json.  A QM instance will
    construct attibutes with stored values from the data it finds in the 'file_name' file.
    New attributes can be generated in code as required and all non-private attributes
    (but including 'QM._comment') will be saved by a call to save_config().  Attributes 
    can be any data type.  If no configuration file is found,  one will be constructed 
    when save_config() is called.
    Two special attributes QM.ui_list and QM.ui control persisting data from QT5 ui
    elements on a single form. QM.ui_list is a list of ui element names to be persisted 
    and QM.ui is a dict of name:value pairs which is automatically generated from QM.ui_list 
    """
    def __init__(self, form, foldr: str, file_name: str, comment: str="DO NOT HAND EDIT!"):
        """
        Initialize the ConfigManager.
        Args:
            form (obj): Ref to object that owns GUI objects (MainForm)
            foldr (str): Name of a folder in ~/.config in which to place
                         the config file - created if not present.
            file_name (str): The name of the configuration file, no extension!
            comment (str): User definable comment saved with config.
        """
        # This is the form that has the GUI elements
        self._mainform = form
        # Ensure config file and folder can exist
        user_home = os.path.expanduser("~")
        self._file_path = f"{user_home}/.config/{foldr}"
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
            # Now load UI data if present
            if "ui" in dir(self):
                self.restore_qt(self.ui)

        except FileNotFoundError:
            print("Config file not found. Creating a new one.")

    def save_state(self, items: list) -> dict:
        """
        Returns the current state of 'items' GUI objects as a dict
        """

    def save_config(self):
        """Save configuration data to the file. """
        config_data = {}
        # Generate UI elements dict
        if "ui_list" in dir(self):
            self.ui = self.save_qt(self.ui_list)
        # Now get all the attributes to save
        for attr_name in dir(self):
            if not attr_name.startswith("_") or attr_name == '_comment':
                if type(getattr(self, attr_name)) in (bool, str, int, complex, list, float, tuple, dict, set, bytes):
                    config_data[attr_name] = getattr(self, attr_name)

        # Sort it
        sorted_attributes = sorted(config_data.items(), key=lambda x: (not x[0].startswith('_'), x[0]))
        sorted_dict = dict(sorted_attributes)
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

    def save_qt(self, uilist: list, form=None) -> dict:
        """Generic persist UI values as a dictionary.
            LST: list of UIelements to save values for.
            Returns: dictionairy of UIelement name:value pairs
        """
        dic = {}
        if form is None:
            form = self._mainform
        try:
            for wdgt_name in uilist:
                # Get GUI Object
                gui_obj = getattr(form, wdgt_name)
                # now get the data from the GUI object
                if isinstance(gui_obj, (QLineEdit, QLabel)):
                    val = gui_obj.text()
                elif isinstance(gui_obj, QComboBox):
                    val = gui_obj.currentIndex()
                elif isinstance(gui_obj, QDateEdit):
                    val = gui_obj.date().toString("dd.MM.yyyy")
                elif isinstance(gui_obj, (QRadioButton, QCheckBox)):
                    val = gui_obj.isChecked()
                elif isinstance(gui_obj, (QDoubleSpinBox, QSpinBox)):
                    val = gui_obj.value()
                else:
                    print("WIDGET NOT FOUND!")
                    val = None
                dic.update({gui_obj.objectName(): val})
            return dic
        except Exception as xcpt:
            print(f'Bad call to Persist: ({uilist})')
            print(f'Exception: {xcpt}')
            return {}

    def restore_qt(self, uidict: dict, form=None):
        """Generic load values into UIelements from dictionairy uidict"""
        if form is None:
            form = self._mainform
        try:
            # Restore each value to GUI element
            for key in uidict.keys():
                wdgt = form.findChild(QWidget, key)
                if isinstance(wdgt, (QLineEdit, QLabel)):
                    wdgt.setText(uidict[key])
                elif isinstance(wdgt, QComboBox):
                    wdgt.setCurrentIndex(uidict[key])
                elif isinstance(wdgt, QDateEdit):
                    wdgt.setDate(QDate.fromString(uidict[key], "dd.MM.yyyy"))
                elif isinstance(wdgt, (QCheckBox, QRadioButton)):
                    wdgt.setChecked(uidict[key])
                elif isinstance(wdgt, (QDoubleSpinBox, QSpinBox)):
                    wdgt.setValue(uidict[key])
                else:
                    print("WIDGET TYPE UNKNON!")
        except:
            print(f'Invalid dictionairy:\n{uidict}')
