# ConfigManager
There are numerous method for persisting application configuration data in Python:
  * Windows style 'INI' files
  * Binary blobs
  * XML/YAML/JSON formatted files

ConfigManager (CM) is a Python class to trivialise persisting app data from CLI or GUI applications. Your application merely creates an instance of ConfigManager, creates and assignes values to its attributes and calls 'save_config' (as it closes) to write the data to the configuration file.  Subsequent runs of your appliction will read the configuration file on startup, and re-create the previous attributes with the previous values.

Internally, ConfigManager uses JSON to store it's data. New attributes can be created as normal by simple assignment. If you try to assign a non-existent attribute to a variable with =, it will assign 'None' rather than generate an exception.  You can use CM.assign('attrb', DefaultValue) to simultaneously create and assign an attribute - if it doesn't already exist (current value is None), the default value is used.
