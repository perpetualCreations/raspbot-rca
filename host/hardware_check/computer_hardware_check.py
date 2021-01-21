"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.1
computer_hardware_check module, for checking hardware status.
Sourced from an WIP version of RemotePotentia, an open-source remote server management software
Made by perpetualCreations

Main module for hardware_check.
Most of this module can be greatly modularized.
Calculations use multiple variables when they can be nested instead, and the sheer abundance of strings can be reduced to lists with some clever looping.
Otherwise, it works just fine, having been ripped out of a dead project.
"""

from hardware_check import objects

def collect():
    """
    Collects system vitals, returns it all into other objects.
    :return: none.
    """
    print("[INFO]: Vitals loaded!")
    try:
        print("[INFO]: Attempting to retrieve CPU percentage statistics with STAT...")
        objects.cpu_percentage = objects.stat.cpu_percent(interval = 0.1)
        print("[INFO]: Retrieval successful.")
    except objects.stat.Error:
        print("[FAIL]: CPU percentage statistics unattainable. Setting as None...")
        objects.cpu_percentage = None
        pass
    pass
    try:
        print("[INFO]: Attempting to retrieve CPU frequency information with STAT...")
        objects.cpu_frequency = objects.stat.cpu_freq()
        print("[INFO]: Retrieval successful.")
    except objects.stat.Error:
        print("[FAIL]: CPU frequency information unattainable. Setting as none...")
        objects.cpu_frequency = None
        pass
    pass
    try:
        print("[INFO]: Attempting to retrieve memory statistics with STAT...")
        objects.memory = objects.stat.virtual_memory()
        print("[INFO]: Retrieval successful.")
    except objects.stat.Error:
        print("[FAIL]: Memory statistics unattainable. Setting as none...")
        objects.memory = None
        pass
    pass
    try:
        print("[INFO]: Attempting to retrieve disk information with STAT...")
        objects.disk_part = objects.stat.disk_partitions()
        print("[INFO]: Retrieval successful.")
    except objects.stat.Error:
        print("[FAIL]: Disk information unattainable. Setting as none...")
        objects.disk_part = None
        pass
    pass
    try:
        print("[INFO]: Attempting to retrieve OS version and name...")
        objects.os_platform = objects.system()
        objects.os_release = objects.release()
        objects.os_version = objects.version()
        print("[INFO]: Retrieval successful.")
    except objects.stat.Error:
        print("[FAIL]: OS version and name data unattainable. Setting as none...")
        objects.os_platform = "No Data"
        objects.os_release = "No Data"
        objects.os_version = "No Data"
        pass
    pass
    print("[INFO]: Attempting to retrieve disk usage...")
    objects.disk_usage = objects.stat.disk_usage("/")
    print("[INFO]: Retrieval successful.")
    try:
        print("[INFO]: Attempting to retrieve disk statistics...")
        objects.disk_io_statistics = objects.stat.disk_io_counters()
        print("[INFO]: Retrieval successful.")
    except objects.stat.Error:
        print("[FAIL]: Disk statistics unattainable. Setting as none...")
        objects.disk_io_statistics = None
        pass
    pass
    try:
        print("[INFO]: Attempting to retrieve network interfaces...")
        objects.net_interface = objects.stat.net_if_addrs()
        print("[INFO]: Retrieval successful.")
    except objects.stat.Error:
        print("[FAIL]: Network interface information unattainable. Setting as No Data string...")
        objects.net_interface = "No Data"
        pass
    pass
    try:
        print("[INFO]: Attempting to retrieve system hostname...")
        objects.hostname = objects.gethostname()
        print("[INFO]: Retrieval complete.")
    except objects.socket_error:
        print("[INFO]: Hostname unattainable. Setting as None.")
        objects.hostname = None
    pass
    print("[INFO]: Attempting to retrieve system sensor data...")
    try:
        objects.sensor_temperature = objects.stat.sensors_temperatures()
    except AttributeError:
        objects.sensor_temperature = "No Data"
    pass
    if objects.sensor_temperature == {}:
        objects.sensor_temperature = "No Data"
    pass
    try:
        objects.sensor_fans = objects.stat.sensors_fans()
    except AttributeError:
        objects.sensor_temperature = "No Data"
    pass
    if objects.sensor_fans == {}:
        objects.sensor_fans = "No Data"
    pass
    try:
        objects.sensor_power = objects.stat.sensors_battery()
    except AttributeError:
        objects.sensor_power = "No Data"
    pass
    if objects.sensor_power is None:
        objects.sensor_power = "No Data"
    pass
    try:
        objects.system_users = objects.stat.users()
    except AttributeError:
        objects.system_users = "No Data"
    pass
    if not objects.system_users:
        objects.system_users = "No Data"
    pass
    print("[INFO]: Retrieval complete.")
    print("[INFO]: All vitals retrieved. Cycle complete.")
pass

def convert():
    """
    Takes from string objects from collect function.
    Converts all values into strings with their proper units of measurement, and with fallback entries in case of failure.
    :return: none.
    """
    print("[INFO]: Vital data conversion started.")
    if objects.cpu_percentage is not None:
        objects.cpu_percentage_str = str(objects.cpu_percentage) + "%"
    else:
        objects.cpu_percentage_str = "No Data"
    pass
    if objects.cpu_frequency is not None:
        objects.cpu_frequency_str = str(objects.cpu_frequency[0]) + "MHz"
    else:
        objects.cpu_frequency_str = "No Data"
    pass
    if objects.memory is not None:
        memory_total = objects.memory[0]
        memory_total_mb = memory_total/1000000000
        memory_total_rounded = round(memory_total_mb, 2)
        memory_available = objects.memory[1]
        memory_available_mb = memory_available/1000000000
        memory_available_rounded = round(memory_available_mb, 2)
        memory_used = objects.memory[3]
        memory_used_mb = memory_used/1000000000
        memory_used_rounded = round(memory_used_mb, 2)
        memory_percentage = objects.memory[2]
        objects.memory_total_str = str(memory_total_rounded) + "MB Total"
        objects.memory_available_str = str(memory_available_rounded) + "MB Available"
        objects.memory_used_str = str(memory_used_rounded) + "MB Used"
        objects.memory_percentage_str = str(memory_percentage) + "%"
    else:
        objects.memory_total_str = "No Data"
        objects.memory_available_str = "No Data"
        objects.memory_used_str = "No Data"
        objects.memory_percentage_str = "No Data"
    pass
    if objects.disk_part != 0:
        disk_part_num_index = 0
        disk_part_list = list(objects.disk_part)
        for x in disk_part_list:
            disk_part_num_index += 1
        pass
    else:
        objects.disk_part_num_index = 0
        objects.disk_part_list = ["No Data"]
    pass
    disk_usage_total = objects.disk_usage[0]
    disk_usage_used = objects.disk_usage[1]
    disk_usage_free = objects.disk_usage[2]
    disk_usage_percent = objects.disk_usage[3]
    disk_usage_total_mb = disk_usage_total/1000000000
    disk_usage_total_rounded = round(disk_usage_total_mb, 2)
    disk_usage_used_mb = disk_usage_used/1000000000
    disk_usage_used_rounded = round(disk_usage_used_mb, 2)
    disk_usage_free_mb = disk_usage_free/1000000000
    disk_usage_free_rounded = round(disk_usage_free_mb, 2)
    objects.disk_usage_total_str = str(disk_usage_total_rounded) + "MB Total"
    objects.disk_usage_used_str = str(disk_usage_used_rounded) + "MB Used"
    objects.disk_usage_free_str = str(disk_usage_free_rounded) + "MB Free"
    objects.disk_usage_percent_str = str(disk_usage_percent) + "%"
    if objects.disk_io_statistics is not None:
        disk_io_statistics_readCount = objects.disk_io_statistics[0]
        disk_io_statistics_writeCount = objects.disk_io_statistics[1]
        disk_io_statistics_byteReadCount = objects.disk_io_statistics[2]
        disk_io_statistics_byteReadCount_mb = disk_io_statistics_byteReadCount/1000000000
        disk_io_statistics_byteReadCount_rounded = round(disk_io_statistics_byteReadCount_mb, 2)
        disk_io_statistics_byteWriteCount = objects.disk_io_statistics[3]
        disk_io_statistics_byteWriteCount_mb = disk_io_statistics_byteWriteCount/1000000000
        disk_io_statistics_byteWriteCount_rounded = round(disk_io_statistics_byteWriteCount_mb, 2)
        objects.disk_io_statistics_readCount_str = str(disk_io_statistics_readCount) + " Reads"
        objects.disk_io_statistics_writeCount_str = str(disk_io_statistics_writeCount) + " Writes"
        objects.disk_io_statistics_byteReadCount_str = str(disk_io_statistics_byteReadCount_rounded) + "MB Read"
        objects.disk_io_statistics_byteWriteCount_str = str(disk_io_statistics_byteWriteCount_rounded) + "MB Written"
    else:
        objects.disk_io_statistics_byteReadCount_str = "No Data"
        objects.disk_io_statistics_byteWriteCount_str = "No Data"
        objects.disk_io_statistics_byteReadCount_str = "No Data"
        objects.disk_io_statistics_byteWriteCount_str = "No Data"
    pass
    print("[INFO]: Conversion of vitals data complete.")
pass

def report():
    """
    Formats data to a string, to look like a report.
    :return: report string ("[Vitals Report]" + "\n" + "Report Timestamp: " + timestamp_output + "\n" + "Bot: " + objects.hostname + "\n" + "\n" + "Local IP(s): " + local_ips_str + "\n" + "OS Platform: " + objects.os_platform + "\n" + "OS Release: " + objects.os_release + "\n" + "OS Version: " + objects.os_version + "\n" + "CPU Frequency: " + objects.cpu_frequency_str + "\n" + "CPU Usage: " + objects.cpu_percentage_str + "\n" + "Memory Percentage: " + objects.memory_percentage_str + "\n" + "Memory Available: " + objects.memory_available_str + "\n" + "Memory Used: " + objects.memory_used_str + "\n" + "Memory Total: " + objects.memory_total_str + "\n" + "Disk Percentage: " + objects.disk_usage_percent_str + "\n" + "Disk Usage: " + objects.disk_usage_used_str + "\n" + "Disk Available: " + objects.disk_usage_free_str + "\n" + "Disk Total: " + objects.disk_usage_total_str + "\n" + "Disk Reads: " + objects.disk_io_statistics_readCount_str + "\n" + "Disk Read: " + objects.disk_io_statistics_byteReadCount_str + "\n" + "Disk Writes: " + objects.disk_io_statistics_writeCount_str + "\n" + "Disk Written: " + objects.disk_io_statistics_byteWriteCount_str + "\n" + "Temperature Telemetry: " + sensor_temperature_str + "\n" + "Fan Telemetry: " + sensor_fans_str + "\n" + "Power Telemetry: " + sensor_power_str + "\n" + "System Users: " + system_users_str)
    """
    print("[INFO]: Generating timestamps...")
    timestamp = objects.strftime("%b %d %Y %H:%M:%S"), objects.gmtime()
    timestamp_output = timestamp[0]
    print("[INFO]: Generation complete.")
    local_ips = []
    for x in objects.net_interface:
        local_ips.append(objects.net_interface[x][0][1])
    pass
    local_ips_str = str(local_ips)
    sensor_temperature_str = str(objects.sensor_temperature)
    sensor_fans_str = str(objects.sensor_fans)
    sensor_power_str = str(objects.sensor_power)
    system_users_str = str(objects.system_users)
    print("[INFO]: Assembling text report...")
    return "[Vitals Report]" + "\n" + "Report Timestamp: " + timestamp_output + "\n" + "Bot: " + objects.hostname + "\n" + "\n" + "Local IP(s): " + local_ips_str + "\n" + "OS Platform: " + objects.os_platform + "\n" + "OS Release: " + objects.os_release + "\n" + "OS Version: " + objects.os_version + "\n" + "CPU Frequency: " + objects.cpu_frequency_str + "\n" + "CPU Usage: " + objects.cpu_percentage_str + "\n" + "Memory Percentage: " + objects.memory_percentage_str + "\n" + "Memory Available: " + objects.memory_available_str + "\n" + "Memory Used: " + objects.memory_used_str + "\n" + "Memory Total: " + objects.memory_total_str + "\n" + "Disk Percentage: " + objects.disk_usage_percent_str + "\n" + "Disk Usage: " + objects.disk_usage_used_str + "\n" + "Disk Available: " + objects.disk_usage_free_str + "\n" + "Disk Total: " + objects.disk_usage_total_str + "\n" + "Disk Reads: " + objects.disk_io_statistics_readCount_str + "\n" + "Disk Read: " + objects.disk_io_statistics_byteReadCount_str + "\n" + "Disk Writes: " + objects.disk_io_statistics_writeCount_str + "\n" + "Disk Written: " + objects.disk_io_statistics_byteWriteCount_str + "\n" + "Temperature Telemetry: " + sensor_temperature_str + "\n" + "Fan Telemetry: " + sensor_fans_str + "\n" + "Power Telemetry: " + sensor_power_str + "\n" + "System Users: " + system_users_str
pass
