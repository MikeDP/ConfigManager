# ConfigManager
There are numerous method for persisting application configuration data in Python:
  * Windows style 'INI' files
  * Binary blobs
  * XML/YAML/JSON formatted files

This small project provides two simple classes to persist application data without the user needing to provide anything other than a destination file path and (possibly) a list of items to persist:
  * **ConfigManager**: A class that can be used for CLI and non-GUI apps.
  * **QTConfigManager**: A class that can be used with QT5 app to persist/restore specific active GUI elements.

`ConfigManager` (CM) is a Python class to trivialise persisting app data from CLI or GUI applications. Your application merely creates an instance of ConfigManager, creates and assigns values to its attributes and calls 'save_config' (as it closes) to write the data to the configuration file.  Subsequent runs of your appliction will read the configuration file on startup, and re-create the previous attributes with the previous values.

Internally, ConfigManager uses JSON to store it's data. New attributes can be created as normal by simple assignment. If you try to assign a non-existent attribute to a variable with =, it will assign 'None' rather than generate an exception.  You can use `CM.assign('attrb', DefaultValue)` to simultaneously create and assign an attribute - if it doesn't already exist (current value is None), the default value is used.  Attributes can be any normal Python data type[^1] and all attributes are saved _except_ private ones (attributes starting with '_'), with the exception of `_comment`, which can be used as a _header_ for the saved config.
[^1]: Any type from bool, str, bytes, int, float, complex, list, tuple, dict or set.

## Example Usage
Basic config file
```
import ConfigManager
...
# Creates a configuration file at /home/$USER/.config/MyApp/myapp.config
config = ConfigManager('MyApp', 'myapp')

# Basic assign values
config.user = "Mike"
config.position = {'X': 24.5, 'Y': -16.1}

# and save
config.save_config()
```
Better usage - accepts persisted data on re-start
```
# Create/use configuration file at /home/$USER/.config/MyApp/myapp.config
config = ConfigManager('MyApp', 'myapp')
# Now, after creation, config.user is 'Mike' and config.position is {'X': 24.5 ...

# Assign default value 'Dave' if config.user doesn't already exist
config.user = config.assign("user", "Dave")  # config.user is aready set to 'Mike'

# Assign new default value if config.position doesn't exist
global_position = config.assign(config.position, {'X': 0.00, 'Y': 0.00})
# Both global_position and config.position are unchanged at {'X':24.5...
 
config._counter = 100   # Won't be saved with configuration file

global_uid = config.uid  # config.uid doesn't exist yet so both global_uid and config.uid are set None
global_guid = config.assign('guid', 12345678) # Both global_guid and config.guid set 12345678
# or simply
config.assign('another_guid', 987654321) # Initialises config.another_guid if it doesn't already exist

# and save
config.save_config()
```
