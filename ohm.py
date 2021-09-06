import wmi
from sys import exit

def init_ohm_wmi():
    """ returns the OpenHardwareMonitor WMI namespace if OpenHardwareMonitor is installed,
        exits otherwise """
    try:
        ohmwmi = wmi.WMI(namespace="root\OpenHardwareMonitor")
        return ohmwmi
    except:
        print("OpenHardwareMonitor WMI data not found.\nMake sure OpenHardwareMonitor is installed.")
        exit(0)

def is_ohm_running(ohmwmi) -> bool:
    sensors = ohmwmi.Sensor()
    if not sensors:
        print("OpenHardwareMonitor is not running.\nMake sure OpenHardwareMonitor is started with admin privileges.")
        return False
    else:
        return True

def get_hardware(ohmwmi):
    # get list of hardwares
    hardwares = ohmwmi.Hardware()
    return hardwares

def get_temperature_sensors(ohmwmi):
    # get list of temperature sensors
    sensors = ohmwmi.Sensor(["Name", "Parent", "Value", "Identifier"], SensorType="Temperature")
    if not sensors:
        print("OpenHardwareMonitor is not running.\nMake sure OpenHardwareMonitor is started with admin privileges.")
        return
    return sensors

def print_sensors_info(sensors):
    for sensor in sensors:
        print(sensor.Parent)
        print(sensor.Name)
        print(sensor.Value)