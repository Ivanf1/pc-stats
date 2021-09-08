import wmi
import sys

def init_ohm_wmi():
    """ returns the OpenHardwareMonitor WMI namespace if OpenHardwareMonitor is installed,
        exits otherwise """
    try:
        ohmwmi = wmi.WMI(namespace="root\OpenHardwareMonitor")
        if not is_ohm_running(ohmwmi):
            # print("OpenHardwareMonitor is not running.\nMake sure OpenHardwareMonitor is started with admin privileges.")
            raise Exception("OpenHardwareMonitor is not running.\nMake sure OpenHardwareMonitor is started with admin privileges.")
            # sys.exit(0)
        return ohmwmi
    except wmi.x_wmi:
        raise Exception("OpenHardwareMonitor WMI data not found.\nMake sure OpenHardwareMonitor is installed.")
        # print("OpenHardwareMonitor WMI data not found.\nMake sure OpenHardwareMonitor is installed.")
        # sys.exit(0)

def is_ohm_running(ohmwmi) -> bool:
    sensors = ohmwmi.Sensor()
    return False if not sensors else True

def get_hardware(ohmwmi):
    # get list of hardwares
    hardwares = ohmwmi.Hardware()
    return hardwares

def get_temperature_sensors(ohmwmi):
    # get list of temperature sensors
    sensors = ohmwmi.Sensor(["Name", "Parent", "Value", "Identifier"], SensorType="Temperature")
    if not sensors:
        print("OpenHardwareMonitor is not running.\nMake sure OpenHardwareMonitor is started with admin privileges.")
        return []
    return sensors

def get_update(ohmwmi):
    """ get new data from WMI """
    hardwares = ohmwmi.Hardware()
    sensors = ohmwmi.Sensor(["Name", "Parent", "Value", "Identifier"], SensorType="Temperature")

    return _hardware_sensors_to_dict(hardwares, sensors)

def _hardware_sensors_to_dict(hardwares, sensors):
    """ make a dictionary from Hardware and Sensor data """
    hardware_dict = {}

    for hardware in hardwares:
        if hardware.Parent == "":
            hardware_dict[hardware.HardwareType] = {"name": hardware.Name, "id": hardware.Identifier, "sensors": []}
        
        for sensor in sensors:
            if sensor.Parent == hardware.Identifier:
                hardware_dict[hardware.HardwareType]["sensors"].append({"name": sensor.Name, "value": sensor.Value})

    return hardware_dict

def _print_sensors_info(sensors):
    for sensor in sensors:
        print(sensor.Parent)
        print(sensor.Name)
        print(sensor.Value)