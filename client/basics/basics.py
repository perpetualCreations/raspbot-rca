"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
basics module, contains basic application functions such as exiting client software, multiprocessing, and editing configs.
Made by perpetualCreations

Handles exiting and configuration editing.
"""

from basics import objects

def log_init():
    """
    Initiates logging.
    :return: none.
    """
    print("[INFO]: Output redirected from console to logging.")
    objects.log_file_handle = open("logs/log-" + make_timestamp() + ".txt", "w")
    objects.origin_stdout = objects.sys.stdout
    objects.sys.stdout = objects.log_file_handle
pass

def make_timestamp():
    """
    Generates timestamp from current UTC time.
    :return: none.
    """
    print("[INFO]: Generating timestamps...")
    timestamp = objects.strftime("%b%d%Y%H%M%S"), objects.gmtime()
    return str(timestamp[0])
pass

def window_close_exit():
    """
    Wrapper for exit, linked to protocol handler for when the GUI window is closed.
    :return: 
    """
    if objects.messagebox.askyesno("Raspbot RCA: Quit?", "Are you sure you want to exit?") is True:
        exit(0)
    pass
pass

def exit(status):
    """
    Stops application.
    :return: none.
    """
    print("[INFO]: Stopping application...")
    objects.sys.stdout = objects.origin_stdout
    objects.log_file_handle.close()
    objects.sys.exit(status)
pass

def set_configuration(file, var, value, section, key, multi):
    """
    Edits entry in configuration file and applies new edit to variables.
    :param file: configuration file.
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
            config_parse_edit = objects.configparser.ConfigParser()
            config_parse_edit[section[parameter_key]][key[parameter_key]] = var[parameter_key]
            with open(file, "w") as config_write:
                config_parse_edit.write(config_write)
            pass
            cycles -= 1
        pass
        config_write.close()
    else:
        var = value
        config_parse_edit = objects.configparser.ConfigParser()
        config_parse_edit[section][key] = var
        with open(file, "w") as config_write:
            config_parse_edit.write(config_write)
        pass
        config_write.close()
    pass
pass
