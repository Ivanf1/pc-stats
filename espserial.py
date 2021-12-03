import serial
from multiprocessing import Process

from wmifilter import process_wmi_data_for_esp32

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
                processed_data = process_wmi_data_for_esp32(data)
                # print(processed_data)
                self.serial_port.write(processed_data.encode("ascii"))
                self.serial_port.flush()
                
                # try:
                #     incoming = self.serial_port.read_all().decode("utf-8")
                #     # incoming = self.serial_port.readline().decode("utf-8")
                #     print(incoming)
                # except Exception as e:
                #     print(e)
        except Exception as e:
            print(e)
            return