"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
basics module, contains basic application functions such as exiting client software, multiprocessing, and editing configs.
Made by Taian Chen

Handles exiting and configuration editing.
"""

try:
    from sys import exit as app_end
    import configparser
except ImportError as ImportErrorMessage:
    app_end = None
    configparser = None
    print("[NAV][FAIL]: Import failed!")
    print(ImportErrorMessage)
except ImportWarning as ImportWarningMessage:
    print("[NAV][FAIL]: Imports raised warnings.")
    print(ImportWarningMessage)
pass

def exit(status):
    """
    Stops application.
    :return: none.
    """
    print("[INFO]: Stopping application...")
    app_end(status)
pass

def set_configuration(var, value, section, key, multi):
    """
    Edits entry in configuration file and applies new edit to variables.
    :param var: variable being updated.
    :param value: value to be assigned to variable and entered into configuration file.
    :param section: section in the configuration file to be edited.
    :param key: key to variable in section in the configuration file to be edited.
    :param multi: boolean for whether to run a for range when reading params, useful when making multiple configuration settings.
    :return: None
    """
    print("[INFO]: Editing configurations...")
    str(var)
    str(value)
    str(section)
    str(key)
    if multi is True:
        cycles = len(var)
        while cycles != 0:
            parameter_key = cycles - 1
            var[parameter_key] = value[parameter_key]
            config_parse_edit = configparser.ConfigParser()
            config_parse_edit[section[parameter_key]][key[parameter_key]] = var[parameter_key]
            with open("main.cfg", "w") as config_write:
                config_parse_edit.write(config_write)
            pass
            cycles -= 1
        pass
        config_write.close()
    else:
        var = value
        config_parse_edit = configparser.ConfigParser()
        print(section)
        print(key)
        config_parse_edit[section][key] = var
        with open("main.cfg", "w") as config_write:
            config_parse_edit.write(config_write)
        pass
        config_write.close()
    pass
pass
