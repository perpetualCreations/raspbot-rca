"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.1
computer_hardware_check module, for checking hardware status.
Sourced from an WIP version of RemotePotentia, an open-source remote server management software
Made by perpetualCreations

Contains objects for module, including any package imports. Interact with these objects through hardware_check.objects.
"""

try:
    from time import sleep, strftime, gmtime
    import psutil as stat
    from platform import system, release, version
    from socket import gethostname, error as socket_error
except ImportError as ImportErrorMessage:
    socket = None
    system = None
    release = None
    version = None
    gethostname = None
    socket_error = None
    print("[FAIL]: Import failed!")
    print(ImportErrorMessage)
except ImportWarning as ImportWarningMessage:
    print("[FAIL]: Imports raised warnings.")
    print(ImportWarningMessage)
pass

# Below are all variables that computer_hardware_check.collect output to
# They can be optimized into a list, but there aren't any significant performance benefits, and frankly its going out of your way one step too far
cpu_percentage = None
cpu_frequency = None
memory = None
disk_part = None
os_platform = None
os_release = None
os_version = None
disk_usage = None
disk_io_statistics = None
net_interface = None
sensor_temperature = None
sensor_fans = None
sensor_power = None
system_users = None
hostname = None
# String form of variables that are from being converted, strung into the return of convert
cpu_percentage_str = None
cpu_frequency_str = None
memory_total_str = None
memory_available_str = None
memory_used_str = None
memory_percentage_str = None
disk_usage_total_str = None
disk_usage_used_str = None
disk_usage_free_str = None
disk_usage_percent_str = None
disk_io_statistics_readCount_str = None
disk_io_statistics_writeCount_str = None
disk_io_statistics_byteReadCount_str = None
disk_io_statistics_byteWriteCount_str = None
