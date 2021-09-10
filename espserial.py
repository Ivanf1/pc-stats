import serial
from serial.tools import list_ports
from multiprocessing import Process

def get_serial_ports():
    """Return a list of all serial ports found"""
    return sorted(list_ports.comports())

class EspSerialProcess(Process):
    def __init__(self, wmi_data_queue, port):
        self.wmi_data_queue = wmi_data_queue
        self.serial_port = serial.Serial()
        self.serial_port.port = port
        self.serial_port.baudrate = 115200 # must match ESP's
        Process.__init__(self)

    def run(self):
        try:
            self.serial_port.open()
            while self.serial_port.isOpen():
                data = self.wmi_data_queue.get()
                print(data)
                self.serial_port.write(data.encode("ascii"))
                self.serial_port.flush()
                
                try:
                    incoming = self.serial_port.readline().decode("utf-8")
                    print(incoming)
                except Exception as e:
                    print(e)
                    pass
        except:
            return