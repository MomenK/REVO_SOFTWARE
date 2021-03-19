from pylibftdi import Driver, Device

import numpy as np
from scipy.signal import hilbert, chirp
import time

class RUSBfifo(Device):
    def __init__(self,buff_size,Channels):
        super().__init__(device_id="REVO", mode='b', interface_select=2)
        self.buff_size = buff_size
        self.Channels = Channels
        super().open()
        super().flush()

        # data = bytearray(super().read(self.buff_size))
        # while(len(data) != self.buff_size):
        # # while True:
        #     super().write(bytearray([240]))
        #     time.sleep(0.001)
        #     data = bytearray(super().read(self.buff_size))
        # print(  super().ftdi_fn.ftdi_get_latency_timer())
        # New line
        # super().ftdi_fn.ftdi_read_data_set_chunksize(0x10000)
        # super().ftdi_fn.ftdi_write_data_set_chunksize(0x10000)
        # # super().ftdi_fn.ftdi_set_latency_timer(16)
        # # *****************
        # super().write(bytearray([240]))
        # time.sleep(0.001)
        # data = bytearray(super().read(self.buff_size))

    def fetch(self):
       
        # time.sleep(0.001)
        super().write(bytearray([240]))
        # time.sleep(0.0003)
        # super().write(bytearray([0]))
       
        # time.sleep(0.001)
        # print(  super().ftdi_fn.ftdi_get_latency_timer())
 
        data = bytearray(super().read(self.buff_size))
        # super().flush() 

        if len(data) != self.buff_size:
                # time.sleep(0.01)
                raise ValueError('Connection issue we got '+ str(len(data)) + ' Instead of ' + str(self.buff_size))
                
            
        data1 = np.frombuffer(data, dtype=np.int16, count=-1).reshape(self.Channels,-1)
        # data2 = np.abs(hilbert(data1.T-np.mean(data1,axis=1)))

        
        
        return data1.T


# USE CASE:
# dev = RUSBfifo(2048*2,2)
# dev.fetch()