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

def get_update(ohmwmi):
    """Get new data from WMI"""
    # TODO: let the user chose the query
    hardwares = ohmwmi.Hardware()
    # TODO: let the user chose the query
    sensors = ohmwmi.query("SELECT Parent, Name, SensorType, Value \
                            FROM Sensor \
                            WHERE (SensorType='Temperature' OR SensorType='Load') \
                                AND (Parent LIKE '%cpu%' OR Parent LIKE '%gpu%')")

    return _hardware_sensors_to_json(hardwares, sensors)

def _hardware_sensors_to_json(hardwares, sensors):
    """Return a json with info about Hardware and associated sensors. \
    You can pass a filter function to chose which sensors to add based on the name
    \nThe json will have this structure:\n
    [
        {
            "t":"GpuNvidia",
            "n":"NVIDIA GeForce GTX 950M",
            "i":"/nvidiagpu/0",
            "s":[
                {
                    "n":"GPU Core",
                    "t":"Temperature",
                    "v":41.0
                },
                {
                    "n":"GPU Core",
                    "t":"Load",
                    "v":6.0
                }
            ]
        },
        {
            "t":"CPU",
            "n":"Intel Core i7-6700HQ",
            "i":"/intelcpu/0",
            "s":[
                {
                    "n":"CPU Total",
                    "t":"Load",
                    "v":5.27043342590332
                },
                {
                    "n":"CPU Package",
                    "t":"Temperature",
                    "v":45.0
                }
            ]
        }
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
                hardware_json[current_idx]["s"].append({"n": sensor.Name, "t": sensor.SensorType, "v": sensor.Value})

        # if this current hardware has no sensors data
        # remove it from the array
        if not hardware_json[current_idx]["s"]:
            hardware_json.pop(current_idx)

    return json.dumps(hardware_json, ensure_ascii=True)