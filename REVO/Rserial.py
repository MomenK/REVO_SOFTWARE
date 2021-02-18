import serial
import numpy as np
from scipy.signal import hilbert, chirp
import time

get_bin = lambda x, n: format(x, 'b').zfill(n)

class RSerial(serial.Serial):
    def __init__(self,port, rate_M,buff_size, Channels):
        super().__init__(port, rate_M,timeout=2)
        self.buff_size = buff_size
        self.Channels = Channels     
        super().write(bytearray(b'\xff\xff')) # Choose mode/reset
        super().write(bytearray(b'\x00\x03')) # set to pulsering
   
    def fetch(self):
        super().flushInput()
        super().flushOutput()
        super().write(bytearray(b'\xfa\x0a')) # Trigger
        data = super().read(self.buff_size)
        # assert len(data) == self.buff_size , 'Connection issue we got '+ str(len(data)) + ' Instead of ' + str(self.buff_size)
        if len(data) != self.buff_size: 
            raise ValueError('Connection issue we got '+ str(len(data)) + ' Instead of ' + str(self.buff_size))
        data1 = np.frombuffer(data, dtype=np.int16, count=-1).reshape(self.Channels,-1)
        return data1.T
    
    def envelope(self,data1):
        return np.abs(hilbert(data1.T-np.mean(data1,axis=1)))
    
    # def fetch8(self):
    #     super().flushInput()
    #     super().flushOutput()
    #     super().write(bytearray(b'\xfa\x0a')) # Trigger
    #     data = super().read(self.buff_size)
    #     assert len(data) == self.buff_size , 'Connection issue we got '+ str(len(data)) + ' Instead of ' + str(self.buff_size)
    #     data1 = np.frombuffer(data, dtype=np.int8, count=-1).reshape(self.Channels,-1)
    #     data2 = np.abs(hilbert(data1.T-np.mean(data1,axis=1)))
    #     return data2

# SPI *******************************************************
    def write_spi (self,data):
        a =  data[0:2]
        b =  data[2:4]
        c =  '0'+ data[4:5]
        d =  data[5:7]
        X = bytearray.fromhex(a+b)
        Y = bytearray.fromhex(c+d)
        super().write(X)
        super().write(Y) 
        # time.sleep(0.1)
        super().write(bytearray(b'\x00\x00')) 
        # time.sleep(0.1)
        pass

    def write_gain(self,gain):
        super().write(bytearray(b'\xff\xff')) # Choose mode/reset
        super().write(bytearray(b'\x00\x04')) # set mode to SPI

        self.write_spi( '2000000')
        self.write_spi( '2000010')
        self.write_spi( '1000010')

        gain_hex = ['00' + hex(gain).split('x')[-1]][-1][-3:]
        self.write_spi( '1B50' + gain_hex)
        self.write_spi( '2B50' + gain_hex)

        self.write_spi( '1B68000')
        self.write_spi( '2B68000')

        super().write(bytearray(b'\xff\xff')) # Choose mode/reset
        super().write(bytearray(b'\x00\x03')) # set to pulsering
        return gain_hex

# Beamforiming *******************************************************
    def data_package (self,channel, delay):
        channel_b = get_bin(channel,5)
        # print(channel_b)
        delay_b = get_bin(delay,11)
        full_b = channel_b + delay_b
        # print(full_b)
        full_b_int = int(full_b, 2)
        # print(full_b_int)
        full_b_int_bytes = full_b_int.to_bytes(2, 'big')
        # print(full_b_int_bytes)

        return bytearray(full_b_int_bytes)

    def send_data(self, channel, delay):
        data = self.data_package(channel,delay)
        # print(data)
        super().write(data)
    pass

    def write_angle(self, n):
        super().write(bytearray(b'\xff\xff')) # Choose mode/reset
        super().write(bytearray(b'\x00\x01')) # set mode to beamforming
        
        if n > 0:
            for i in range(0,32):
                self.send_data(i, round(n* i) )
        else:   
            for i in range(0,32):
                self.send_data(i, round(n*(i - 31)) )

        # for i in range(0,32):
        #     self.send_data(i,delayV)

        super().write(bytearray(b'\xff\xff')) # Choose mode/reset
        super().write(bytearray(b'\x00\x03')) # set to pulsering

