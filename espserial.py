import multiprocessing
import serial
import queue
from serial.tools import list_ports
from multiprocessing import Process

_QUEUE_TIMEOUT = 10

def get_serial_ports():
    """ Returns a list of all serial ports found """
    return sorted(list_ports.comports())

class EspSerialProcess():
    def __init__(self, wmi_data_queue, port):
        self.wmi_data_queue = wmi_data_queue
        self.serial_proc = Process(target=self.send_serial_msg)

        self.serial_port = serial.Serial()
        self.serial_port.port = port
        self.serial_port.baudrate = 115200

    def send_serial_msg(self):
        try:
            # self.serial_port.open()
            while True:
                data = self.wmi_data_queue.get(timeout=_QUEUE_TIMEOUT)
                print(data)
                # self.serial_port.write(0xff)
        except queue.Empty:
            print(f"Queue has been empty for {_QUEUE_TIMEOUT} seconds.")
        except:
            return

    def run(self):
        self.serial_proc.start()
    
    def close(self):
        # self.serial_port.close()
        # self.serial_proc.join(0)
        self.serial_proc.terminate()

        if self.serial_proc.is_alive():
            self.serial_proc.terminate()
        
        self.serial_proc.close()

        print("closing")