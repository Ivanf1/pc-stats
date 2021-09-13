import enum
from serial.tools import list_ports
import json
import re
from enum import Enum

def get_serial_ports():
    """Return a list of all serial ports found"""
    return sorted(list_ports.comports())

class DrawingType(Enum):
    ARC = 0
    LINE = 1

def process_wmi_data_for_esp32(wmi_data_json):
    data = json.loads(wmi_data_json)
    new_data = []

    idx = 0
    for hardware in data:
        sensor_array = hardware.pop("s")

        if re.search("cpu|gpu", hardware["i"]):
            hardware["t"] = DrawingType.ARC.value
        if re.search("ram", hardware["i"]):
            hardware["n"] = hardware["t"]
            hardware["t"] = DrawingType.LINE.value
        
        hardware.pop("i")
        hardware["s"] = []
        new_data.append(hardware)

        for sensor in sensor_array:
            if re.search("^CPU Package$|^CPU Total$|^GPU Core$|^Memory$", sensor["n"]):
                sensor["v"] = round(sensor["v"], 1)
                new_data[idx]["s"].append(sensor)

        # sort sensors by type
        new_data[idx]["s"] = sorted(new_data[idx]["s"], key=lambda k: k["t"])

        idx += 1

    return json.dumps(sorted(new_data, key=lambda k: (k['t'], k['n'])))