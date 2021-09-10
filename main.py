import sys
from multiprocessing import Queue

import polling
import espserial

def terminate_processes(processes):
    for process in processes:
        process.close()

if __name__ == "__main__":
    ports = espserial.get_serial_ports()

    if not ports:
        print("No COM ports available.\nMake sure the ESP32 is connected.")
        sys.exit(0)

    for port in ports:
        print(port.name, port.description)

    q = Queue()
    poll_proc = polling.OhmPollingProcess(q, 5)
    espserial_proc = espserial.EspSerialProcess(q, "COM3")

    poll_proc.start()
    espserial_proc.start()

    # import time
    # time.sleep(8)
    # terminate_processes([poll_proc, espserial_proc, q])