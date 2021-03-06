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
        super().write(bytearray(b'\x30\x03')) # set to pulsering
   
    def fetch(self):
        super().flushInput()
        super().flushOutput()
        super().write(bytearray(b'\xff\xff')) # Choose mode/reset
        super().write(bytearray(b'\x30\x03')) # set to pulsering
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

    def set_HPF(self):
        super().write(bytearray(b'\xff\xff')) # Choose mode/reset
        super().write(bytearray(b'\x40\x04')) # set mode to SPI
        
        self.write_spi( '2000000') # swith to VGA
        self.write_spi( '1000000') # swith to VGA

#  Power mode seems to work fine.
        self.write_spi( '2E50000') # set 
        self.write_spi( '1E50000') # set

        # self.write_spi( '2E50001') # set 
        # self.write_spi( '1E50001') # set

#  The HPF seems to be working fine.. need to disable TR_external pins
        self.write_spi( '2E60000') # set 
        self.write_spi( '1E60000') # set

        # self.write_spi( '2E6001F') # set 
        # self.write_spi( '1E6001F') # set

        # self.write_spi( '2C70000') # set 
        # self.write_spi( '1C70000') # set

        # self.write_spi( '2C70400') # set 
        # self.write_spi( '1C70400') # set


#  The LPF seems to be working fine
        self.write_spi( '2C70000') # set 
        self.write_spi( '1C70000') # set

        # self.write_spi( '2C70100') # set 
        # self.write_spi( '1C70100') # set

        # self.write_spi( '2C70080') # set 
        # self.write_spi( '1C70080') # set

        # self.write_spi( '2C70180') # set 
        # self.write_spi( '1C70180') # set

        super().write(bytearray(b'\xff\xff')) # Choose mode/reset
        super().write(bytearray(b'\x30\x03')) # set to pulsering
        pass


    def write_gain(self,gain):
        super().write(bytearray(b'\xff\xff')) # Choose mode/reset
        super().write(bytearray(b'\x40\x04')) # set mode to SPI

        
        self.write_spi( '2000010')  # swith to DTGC
        self.write_spi( '1000010')  # swith to DTGC

        gain_hex = ['00' + hex(gain).split('x')[-1]][-1][-3:]
        self.write_spi( '1B50' + gain_hex)
        self.write_spi( '2B50' + gain_hex)

        self.write_spi( '1B68000')
        self.write_spi( '2B68000')

        self.write_spi( '2000000') # swith to VGA
        self.write_spi( '1000000') # swith to VGA

        # 
        super().write(bytearray(b'\xff\xff')) # Choose mode/reset
        super().write(bytearray(b'\x30\x03')) # set to pulsering
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
        super().write(bytearray(b'\x10\x01')) # set mode to beamforming
        
        # if n > 0:
        #     for i in range(0,32):
        #         self.send_data(i, round(n* i) )
        # else:   
        #     for i in range(0,32):
        #         self.send_data(i, round(n*(i - 31)) )
        
        for i in range(0,32):
                self.send_data(i, round(n* i) + 500)

        super().write(bytearray(b'\xff\xff')) # Choose mode/reset
        super().write(bytearray(b'\x30\x03')) # set to pulsering



    def write_focus_depth(self, n):
        super().write(bytearray(b'\xff\xff')) # Choose mode/reset
        super().write(bytearray(b'\x10\x01')) # set mode to beamforming
        # n[16] = 1000
        for i in range(0,32):
                self.send_data(i, n[i] + 500)

        super().write(bytearray(b'\xff\xff')) # Choose mode/reset
        super().write(bytearray(b'\x30\x03')) # set to pulsering


