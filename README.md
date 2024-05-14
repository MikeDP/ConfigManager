# ConfigManager
There are numerous method for persisting application configuration data in Python:
  * Windows style 'INI' files
  * Binary blobs
  * XML/YAML/JSON formatted files

`ConfigManager` (CM) is a Python class to trivialise persisting app data from CLI or GUI applications. Your application merely creates an instance of ConfigManager, creates and assigns values to its attributes and calls 'save_config' (as it closes) to write the data to the configuration file.  Subsequent runs of your appliction will read the configuration file on startup, and re-create the previous attributes with the previous values.

Internally, ConfigManager uses JSON to store it's data. New attributes can be created as normal by simple assignment. If you try to assign a non-existent attribute to a variable with =, it will assign 'None' rather than generate an exception.  You can use CM.assign('attrb', DefaultValue) to simultaneously create and assign an attribute - if it doesn't already exist (current value is None), the default value is used.  Attributes can be any normal Python data type[^1] and all attributes are saved _except_ those that are 'private' (start with '_').
[^1]: Any type from str, int, complex, list, float, tuple, dict, set or bytes.

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
Better usage - doesn't overwrite persisted data
```
# Create/use configuration file at /home/$USER/.config/MyApp/myapp.config
config = ConfigManager('MyApp', 'myapp')

# Assign default value 'Dave' if config.user doesn't already exist
config.user = config.assign("user", "Dave")  # config.user is aready set to 'Mike'

# Assign new default value if config.position doesn't exist
global_position = config.assign(config.position, {'X': 0.00, 'Y': 0.00})
# Both global_position and config.position are unchanged at {'X':24.5...
 
config._counter = 100   # Won't be saved with configuration file

global_uid = config.uid  # config.uid doesn't exist so both global_uid and config.uid set None
global_guid = config.assign('guid', 12345678) # Both global_guid and config.guid set 12345678

# and save
config.save_config()
```
