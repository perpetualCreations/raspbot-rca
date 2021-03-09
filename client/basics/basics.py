"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
basics module, contains basic application functions such as exiting client software, multithreading, and editing configs.
Made by perpetualCreations

Handles exiting and configuration editing.
"""

from basics import objects

def log_init() -> None:
    """
    Initiates logging.
    :return: None
    """
    print("[INFO]: Output redirected from console to logging.")
    objects.log_file_handle = open("logs/log-" + make_timestamp() + ".txt", "w")
    objects.origin_stdout = objects.sys.stdout
    objects.sys.stdout = objects.log_file_handle

def make_timestamp(log_suppress: bool = False) -> str:
    """
    Generates timestamp from current UTC time.
    :return: str, timestamp formatted as month, day, year, hour, minute, second, in that order.
    """
    if log_suppress is False: print("[INFO]: Generating timestamps...")
    return str((objects.strftime("%b%d%Y%H%M%S"), objects.gmtime())[0])

def window_close_exit() -> None:
    """
    Wrapper for exit, used to be linked to protocol handler for when the GUI window is closed.
    Unused ever since migrating to PySide6.
    :return: None
    """
    if objects.messagebox.askyesno("Raspbot RCA: Quit?", "Are you sure you want to exit?") is True: exit(0)

def exit(status) -> None:
    """
    Stops application.
    :return: None
    """
    print("[INFO]: Stopping application...")
    from comms import disconnect
    disconnect.disconnect()
    objects.sys.stdout = objects.origin_stdout
    objects.log_file_handle.close()
    objects.sys.exit(status)

def set_configuration(file: str, var: str, value: str, section: str, key: str, multi: bool) -> None:
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
    var = str(var)
    value = str(value)
    section = str(section)
    key = str(key)
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

def load_hardware_config() -> list:
    """
    Uses configparser to retrieve hardware configuration, and return as nested component list.
    :return: list
    """
    config_parse_load = objects.configparser.ConfigParser()
    try:
        components = [[None, None, None], [None, None]]
        config_parse_load.read("hardware.cfg")
        components[0][0] = objects.literal_eval(config_parse_load["HARDWARE"]["sensehat"])
        components[0][1] = objects.literal_eval(config_parse_load["HARDWARE"]["distance"])
        components[0][2] = objects.literal_eval(config_parse_load["HARDWARE"]["dust"])
        components[1][0] = objects.literal_eval(config_parse_load["HARDWARE"]["arm"])
        components[1][1] = objects.literal_eval(config_parse_load["HARDWARE"]["arm_cam"])
        return components
    except objects.configparser.Error as ce:
        print("[FAIL]: Failed to load configurations! See below for details.")
        print(ce)
        exit(1)
    except KeyError as ke:
        print("[FAIL]: Failed to load configurations! Configuration file is corrupted or has been edited incorrectly.")
        print(ke)
        exit(1)
    except FileNotFoundError as nf:
        print("[FAIL]: Failed to load configurations! Configuration file is missing.")
        print(nf)
        exit(1)
    pass
