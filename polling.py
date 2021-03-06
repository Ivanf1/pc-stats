from multiprocessing import Process
from time import sleep

import ohm

class OhmPollingProcess(Process):
    def __init__(self, wmi_data_queue, polling_interval_secs):
        self.polling_interval_secs = polling_interval_secs
        self.wmi_data_queue = wmi_data_queue
        Process.__init__(self)

    def run(self):
        try:
            ohm_thread_wmi = ohm.init_ohm_wmi()
            while True:
                wmi_data = ohm.get_update(ohm_thread_wmi)
                self.wmi_data_queue.put_nowait(wmi_data)
                sleep(self.polling_interval_secs)
        except Exception as e:
            print(e.args[0])
            return