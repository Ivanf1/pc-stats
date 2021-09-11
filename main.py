import sys
from multiprocessing import Queue

import utils
import polling
import espserial
import re

def filter_wmi_data(sensor_name):
    return True if re.search("^CPU Package$|^CPU Total$|^GPU Core$", sensor_name) else False

if __name__ == "__main__":
    ports = utils.get_serial_ports()

    if not ports:
        print("No COM ports available.\nMake sure the ESP32 is connected.")
        sys.exit(0)

    for port in ports:
        print(port.name, port.description)

    q = Queue()
    poll_proc = polling.OhmPollingProcess(q, 5, filter_wmi_data)
    espserial_proc = espserial.EspSerialProcess(q, "COM3")

    poll_proc.start()
    espserial_proc.start()