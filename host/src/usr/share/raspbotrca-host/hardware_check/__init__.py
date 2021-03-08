"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.1
computer_hardware_check module, for checking hardware status.
Sourced from an WIP version of RemotePotentia, an open-source remote server management software
Made by perpetualCreations

Host-only module.
Ripped out of a dead project.
"""

print("[INFO]: Initiating hardware_check module...")

try:
    import psutil as stat
    from platform import system, release, version
    from socket import gethostname, error as socket_error
    from basics import basics
except ImportError as ImportErrorMessage:
    print("[FAIL]: Import failed!")
    print(ImportErrorMessage)
    basics.exit(1)
except ImportWarning as ImportWarningMessage:
    print("[FAIL]: Imports raised warnings.")
    print(ImportWarningMessage)
    basics.exit(1)
pass

print("[INFO]: Initiation of hardware_check complete!")

class hardwareCheck:
    """
    Main class for hardware_check module.
    """
    def __init__(self) -> None:
        self.cpu_stats = ["No Data", "No Data"]
        self.memory = None
        self.memory_stats = ["No Data", "No Data", "No Data", "No Data"]
        self.disk_usage = None
        self.disk_usage_stats = ["No Data", "No Data", "No Data", "No Data"]
        self.disk_io = None
        self.disk_io_stats = ["No Data", "No Data", "No Data", "No Data"]
        self.sensor = ["No Data", "No Data", "No Data"]

    def collect(self) -> str:
        """
        Collects hardware data, converts and formats into multi-line string.
        :return: str, multi-line report
        """
        print("[INFO]: Starting hardware check...")
        try: self.cpu_stats[0] = str(stat.cpu_percent(interval = 0.1)) + "%"
        except stat.Error: self.cpu_stats[0] = "No Data"
        try: self.cpu_stats[1] = str(stat.cpu_freq()[0]) + " MHz"
        except stat.Error: self.cpu_stats[1] = "No Data"
        try:
            self.memory = stat.virtual_memory()
            self.memory_stats = [str(round(self.memory[0]/1000000000, 2)) + " GB Total", str(round(self.memory[1]/1000000000, 2)) + " GB Available", str(round(self.memory[3]/1000000000, 2)) + " GB Used", str(self.memory[2]) + "%"]
        except stat.Error: self.memory_stats = ["No Data", "No Data", "No Data", "No Data"]
        self.disk_usage = stat.disk_usage("/")
        if self.disk_usage is not None: self.disk_usage_stats = [str(round(self.disk_usage[0]/1000000000, 2)) + " GB Total", str(round(self.disk_usage[1]/1000000000, 2)) + " GB Used", str(round(self.disk_usage[2]/1000000000, 2)) + " GB Free", str(self.disk_usage[3]) + "%"]
        else: self.disk_usage_stats = ["No Data", "No Data", "No Data", "No Data"]
        try: self.disk_io = stat.disk_io_counters()
        except stat.Error: self.disk_io = None
        if self.disk_io is not None: self.disk_io_stats = [str(self.disk_io[0]) + " Reads", str(self.disk_io[1]) + " Writes", str(round(self.disk_io[2]/1000000000, 2)) + " GH Read", str(round(self.disk_io[3]/1000000000, 2)) + " GB Written"]
        else: self.disk_io_stats = ["No Data", "No Data", "No Data", "No Data"]
        try: self.sensor[0] = str(stat.sensors_temperatures())
        except AttributeError: self.sensor[0] = "No Data"
        if stat.sensors_temperatures() == {}: self.sensor[0] = "No Data"
        try: self.sensor[1] = str(stat.sensors_fans())
        except AttributeError: self.sensor[1] = "No Data"
        if stat.sensors_fans() == {}: self.sensor[1] = "No Data"
        try: self.sensor[2] = str(stat.sensors_battery())
        except AttributeError: self.sensor[2] = "No Data"
        if stat.sensors_battery() is None: self.sensor[2] = "No Data"
        try: system_users = str(stat.users())
        except AttributeError: system_users = "No Data"
        if not system_users: system_users = "No Data"
        try: net_interface = stat.net_if_addrs()
        except stat.Error: net_interface = [[[None, "No Data"]]]
        local_ips = []
        for x in net_interface: local_ips.append(net_interface[x][0][1])
        print("[INFO]: Retrieval complete.")
        print("[INFO]: Assembling text report...")
        return "Report Timestamp: " + basics.make_timestamp() + "\n" + \
               "Bot: " + gethostname() + "\n" + "\n" + "Local IP(s): " + str(local_ips) + "\n" + "OS Platform: " + \
               system() + "\n" + "OS Release: " + release() + "\n" + "OS Version: " + version() + "\n" + \
               "CPU Frequency: " + self.cpu_stats[1] + "\n" + "CPU Usage: " + self.cpu_stats[0] + "\n" + \
               "Memory Percentage: " + self.memory_stats[3] + "\n" + "Memory Available: " + self.memory_stats[1] + \
               "\n" + "Memory Used: " + self.memory_stats[2] + "\n" + "Memory Total: " + self.memory_stats[0] + "\n" + \
               "Disk Percentage: " + self.disk_usage_stats[3] + "\n" + "Disk Usage: " + self.disk_usage_stats[2] + "\n" + \
               "Disk Available: " + self.disk_usage_stats[1] + "\n" + "Disk Total: " + self.disk_usage_stats[0] + "\n" + \
               "Disk Reads: " + self.disk_io_stats[0] + "\n" + "Disk Read: " + self.disk_io_stats[2] + \
               "\n" + "Disk Writes: " + self.disk_io_stats[1] + "\n" + "Disk Written: " + self.disk_io_stats[3] + \
               "\n" + "Temperature Telemetry: " + self.sensor[0] + "\n" + "Fan Telemetry: " + self.sensor[1] + \
               "\n" + "Power Telemetry: " + self.sensor[2] + "\n" + "System Users: " + system_users
    pass
