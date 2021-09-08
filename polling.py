from multiprocessing import Process
from time import sleep

import ohm

class OhmPollingProcess():
    def __init__(self, wmi_data_queue):
        self.wmi_data_queue = wmi_data_queue
        self.polling_proc = Process(target=self.poll)

    def poll(self):
        try:
            ohm_thread_wmi = ohm.init_ohm_wmi()
            while True:
                wmi_data = ohm.get_update(ohm_thread_wmi)
                self.wmi_data_queue.put_nowait(wmi_data)
                sleep(3)
        except Exception as e:
            print(e.args[0])
            return

    def run(self):
        self.polling_proc.start()
    
    def close(self):
        # self.polling_proc.join(0)
        self.polling_proc.terminate()

        if self.polling_proc.is_alive():
            self.polling_proc.terminate()
        
        self.polling_proc.close()
