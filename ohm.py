import wmi
import json

def init_ohm_wmi():
    """Returns the OpenHardwareMonitor WMI namespace if OpenHardwareMonitor is installed,
        exits otherwise"""
    try:
        ohmwmi = wmi.WMI(namespace="root\OpenHardwareMonitor")
        if not is_ohm_running(ohmwmi):
            raise Exception("OpenHardwareMonitor is not running.\nMake sure OpenHardwareMonitor is started with admin privileges.")
        return ohmwmi
    except wmi.x_wmi:
        raise Exception("OpenHardwareMonitor WMI data not found.\nMake sure OpenHardwareMonitor is installed.")

def is_ohm_running(ohmwmi) -> bool:
    # an empty list of sensors means OpenHardwareMonitor is not running
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

    return _hardware_sensors_to_json(hardwares, sensors)

def _hardware_sensors_to_json(hardwares, sensors):
    """Return a json with info about Hardware and associated sensors.
    \nThe json will have this structure:\n
    [
        {
            "t":"CPU",
            "n":"Intel Core i7-6700HQ",
            "i":"/intelcpu/0",
            "s":[
                {
                    "n":"CPU Core #1",
                    "v":37.0
                },
                {
                    "n":"CPU Core #2",
                    "v":47.0
                },
                {
                    "n":"CPU Core #3",
                    "v":40.0
                },
                {
                    "n":"CPU Core #4",
                    "v":38.0
                }
            ]
        },\n
        ...
    ] 
    """

    hardware_json = []
    current_idx = 0

    for hardware in hardwares:
        if hardware.Parent == "":
            hw_obj = {"t": hardware.HardwareType, "n": hardware.Name, "i": hardware.Identifier, "s": []}
            hardware_json.append(hw_obj)
            current_idx = len(hardware_json)-1
    
        for sensor in sensors:
            if sensor.Parent == hardware.Identifier:
                hardware_json[current_idx]["s"].append({"n": sensor.Name, "v": sensor.Value})

        # if this current hardware has no sensors data
        # remove it from the array
        if not hardware_json[current_idx]["s"]:
            hardware_json.pop(current_idx)
    
    return json.dumps(hardware_json, ensure_ascii=True)