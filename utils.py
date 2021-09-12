from serial.tools import list_ports
import json
import re

def get_serial_ports():
    """Return a list of all serial ports found"""
    return sorted(list_ports.comports())

def filter_wmi_data(wmi_data_json):
    data = json.loads(wmi_data_json)
    new_data = []

    idx = 0
    for hardware in data:
        sensor_array = hardware.pop("s")
        hardware["s"] = []
        new_data.append(hardware)

        for sensor in sensor_array:
            if re.search("^CPU Package$|^CPU Total$|^GPU Core$", sensor["n"]):
                new_data[idx]["s"].append(sensor)
        idx += 1
    return json.dumps(new_data)