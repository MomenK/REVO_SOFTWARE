import serial
import numpy as np
from scipy.signal import hilbert, chirp
import time



class RSerial(serial.Serial):
    def __init__(self,port, rate_M,buff_size, Channels, Debug):
        super().__init__(port, rate_M,timeout=2)
        self.buff_size = buff_size
        self.Channels = Channels
        self.Debug = Debug
       

        super().write(bytearray(b'\xff\xff')) # Choose mode/reset
        super().write(bytearray(b'\x00\x03')) # set to pulsering
   
    
    def fetch(self):
        super().flushInput()
        super().flushOutput()

        # super().write(bytearray(b'\xff\xff')) # Choose mode/reset
        # super().write(bytearray(b'\x00\x03')) # set to pulsering
        super().write(bytearray(b'\xfa\x0a')) # Trigger
        
        data = super().read(self.buff_size)
 
        # assert len(data) == self.buff_size , 'Connection issue we got '+ str(len(data)) + ' Instead of ' + str(self.buff_size)
        if len(data) != self.buff_size: 
            raise ValueError('Connection issue we got '+ str(len(data)) + ' Instead of ' + str(self.buff_size))

        data1 = np.frombuffer(data, dtype=np.int16, count=-1).reshape(self.Channels,-1)

        if self.Debug == 1:
            # data2 = (data1.T-np.mean(data1,axis=1))
            data2 = (data1.T)
            # data2 = data2.astype('int16') 

        else:
            data2 = np.abs(hilbert(data1.T))
          
            data2 = np.abs(hilbert(data1.T-np.mean(data1,axis=1)))
            #data2 = np.abs(hilbert(data1.T-np.mean(data1[:,1000:-1],axis=1)))
        
        return data2

    def fetch8(self):
        super().flushInput()
        super().flushOutput()
        super().write(bytearray(b'\xfa\x0a')) # Trigger
        
        
        data = super().read(self.buff_size)
        
        assert len(data) == self.buff_size , 'Connection issue we got '+ str(len(data)) + ' Instead of ' + str(self.buff_size)
        data1 = np.frombuffer(data, dtype=np.int8, count=-1).reshape(self.Channels,-1)
        data2 = np.abs(hilbert(data1.T-np.mean(data1,axis=1)))
        return data2


# class RSerial:
#     def __init__(self, port, rate_M, buff_size, Channels):
#         self.ser = serial.Serial(port, rate_M, timeout=1)  # open serial port
#         self.ser.flushInput()
#         self.ser.flushOutput()
#         self.buff_size = buff_size
#         self.Channels = Channels
    
#     def fetch(self):
#         self.ser.flushInput()
#         self.ser.flushOutput()
#         self.ser.write(b'a')
        
#         data = self.ser.read(self.buff_size)
#         assert len(data) == self.buff_size , 'Connection issue we got '+ str(len(data)) + ' Instead of ' + str(self.buff_size)
#         data1 = np.frombuffer(data, dtype=np.int16, count=-1).reshape(self.Channels,-1)
#         data2 = np.abs(hilbert(data1.T-np.mean(data1,axis=1)))
#         return data2