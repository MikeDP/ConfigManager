#!/usr/bin/env python3
"""
test_configmanager.py
pytest module for ConfigManger functional testing

v1.0  12/05/24
v0.2  22/12/24 for v0.2
"""

import os
import json
import pytest
from ConfigManager import ConfigManager

@pytest.fixture
def config_manager():
    """
    Fixture to create a ConfigManager instance for testing.

    Args:
        tmp_path: Pytest fixture for creating a temporary directory.

    Returns:
        ConfigManager: An instance of ConfigManager for testing.
    """

    folder ="TESTING"
    # Initialize ConfigManager with temporary directory and file name
    manager = ConfigManager(folder, "test_config")

    # Yield the ConfigManager instance for testing
    yield manager

    # Tidy up
    del manager

    # Cleanup after testing (delete temporary directory and files)
    folder = os.path.expanduser('~/.config/' + folder)
    for file in os.listdir(folder):
        os.remove(os.path.join(folder, file))
    os.rmdir(folder)

def test_initialization(config_manager: ConfigManager):
    """
    Test initialization of ConfigManager.

    Args:
        config_manager: Pytest fixture for ConfigManager instance.
    """
    assert isinstance(config_manager, ConfigManager)

def test_load_config(config_manager: ConfigManager):
    """
    Test some configuration data.

    Args:
        config_manager: Pytest fixture for ConfigManager instance.
    """
    # Modify some attributes and save the configuration
    config_manager.USER = "TestUser"
    config_manager.save_config()

    # Modify some attributes
    config_manager.USER = "TestUser"
    config_manager.NUMBER = 42

    # Save the configuration
    config_manager.save_config()

    # Read the saved configuration file and assert its contents
    with open(config_manager._file_path, 'r', encoding='utf8') as file:
        saved_config = json.load(file)
        assert saved_config == {"_comment": 'DO NOT HAND EDIT!', "USER": "TestUser", "NUMBER": 42}

def test_get_attribute(config_manager: ConfigManager):
    """
    Test accessing attributes that don't exist.

    Args:
        config_manager: Pytest fixture for ConfigManager instance.
    """
    # Access an attribute that doesn't exist
    assert config_manager.test_attribute is None

def test_assign(config_manager: ConfigManager):
    """
    Test assigning values to attributes.

    Args:
        config_manager: Pytest fixture for ConfigManager instance.
    """
    # Assign a value to a non-existent attribute
    test_var = config_manager.assign("test_attribute", "test_value")
    assert test_var == "test_value"
    # Check if the assigned value persists
    assert config_manager.test_attribute == "test_value"
    config_manager.assign("test2", "Test2 value")
    assert "Test2 value" == config_manager.test2

def test_save_attr(config_manager: ConfigManager):
    """
    Test _attr not persisted
    """
    # Modify some attributes
    config_manager.USER = "TestUser"
    config_manager.NUMBER = 42
    config_manager._notsaved = "This attribute is not saved"
    config_manager._comment = "This is the title and should be saved"

    # Save the configuration
    config_manager.save_config()

    # Read the saved configuration file and assert its contents
    with open(config_manager._file_path, 'r', encoding='utf8') as file:
        saved_config = json.load(file)
        assert '_notsaved' not in saved_config.keys()
        assert config_manager._comment in saved_config.values()

def test_add_class(config_manager: ConfigManager):
    """
    Add class attribute to check it doesn't save
    """
     # Modify some attributes
    config_manager.USER = "TestUser"
    config_manager.NUMBER = 42
    config_manager._notsaved = "This attribute is not saved"
    config_manager._comment = "This is the title and should be saved"
    # Add a class object
    from MDPLibrary.ClassesLib import PersistUI
    config_manager.class_item = PersistUI(None)

    config_manager.save_config()

    # Read the saved configuration file and assert its contents
    with open(config_manager._file_path, 'r', encoding='utf8') as file:
        saved_config = json.load(file)
        assert 'class_item' not in saved_config.keys()
        
def test_set_handling(config_manager: ConfigManager):
    """Test saving and loading sets."""
    config_manager.test_set = {1, 2, 3}
    config_manager.save_config()
    config_manager.load_config()
    assert config_manager.test_set == {1, 2, 3}

def test_tuple_handling(config_manager: ConfigManager):
    """Test saving and loading tuples."""
    config_manager.test_tuple = (4, 5, 6)
    config_manager.save_config()
    config_manager.load_config()
    assert config_manager.test_tuple == (4, 5, 6)

def test_integer_handling(config_manager: ConfigManager):
    """Test saving and loading tuples."""
    config_manager.test_tuple = 666
    config_manager.save_config()
    config_manager.load_config()
    assert config_manager.test_tuple == 666

def test_string_handling(config_manager: ConfigManager):
    """Test saving and loading tuples."""
    config_manager.test_tuple = "qwerty uiop\n"
    config_manager.save_config()
    config_manager.load_config()
    assert config_manager.test_tuple == "qwerty uiop\n"


def test_float_handling(config_manager: ConfigManager):
    """Test saving and loading tuples."""
    config_manager.test_tuple = 3.14159
    config_manager.save_config()
    config_manager.load_config()
    assert config_manager.test_tuple == 3.14159

def test_bool_handling(config_manager: ConfigManager):
    """Test saving and loading tuples."""
    config_manager.test_tuple = True
    config_manager.save_config()
    config_manager.load_config()
    assert config_manager.test_tuple 
    
def test_dict_handling(config_manager: ConfigManager):
    """Test saving and loading tuples."""
    config_manager.test_tuple = {"A": 12, "B": "string item"}
    config_manager.save_config()
    config_manager.load_config()
    assert config_manager.test_tuple == {"A": 12, "B": "string item"}

def test_byte_handling(config_manager: ConfigManager):
    """Test saving and loading tuples."""
    byt = "a byte sting".encode()
    config_manager.test_tuple = byt
    config_manager.save_config()
    config_manager.load_config()
    assert config_manager.test_tuple == byt

def test_nested_structures(config_manager: ConfigManager):
    """Test saving and loading nested structures."""
    config_manager.nested = [set([1, 2]), (3, 4), {"key": set([5, 6])}]
    config_manager.save_config()
    config_manager.load_config()
    assert config_manager.nested == [set([1, 2]), (3, 4), {"key": set([5, 6])}] 
