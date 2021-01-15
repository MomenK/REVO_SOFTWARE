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

    def fetch(self):

       super().write(bytearray([240]))
       
       # time.sleep(0.001)

       data = bytearray(super().read(self.buff_size))

       if len(data) != self.buff_size: 
            raise ValueError('Connection issue we got '+ str(len(data)) + ' Instead of ' + str(self.buff_size))
        
       data1 = np.frombuffer(data, dtype=np.int16, count=-1).reshape(self.Channels,-1)
       data2 = np.abs(hilbert(data1.T-np.mean(data1,axis=1)))

       super().flush()

       return data2


# USE CASE:
# dev = RUSBfifo(2048*2,2)
# dev.fetch()