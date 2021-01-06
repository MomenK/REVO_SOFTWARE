import serial

import numpy as np

import time

def write_spi (port,data):
    a =  data[0:2]
    b =  data[2:4]
    c =  '0'+ data[4:5]
    d =  data[5:7]
    X = bytearray.fromhex(a+b)
    Y = bytearray.fromhex(c+d)

    port.write(X)
    port.write(Y) 
    time.sleep(0.1)
    port.write(bytearray(b'\x00\x00')) 
    time.sleep(0.1)
    pass




ser = serial.Serial('COM3', 8*1000000, timeout=2)  # open serial port
ser.flushInput()
ser.flushOutput()
ser.write(bytearray(b'\xff\xff')) # Choose mode/reset
ser.write(bytearray(b'\x00\x04')) # set mode to beamforming
# ser.write(bytearray(b'\x00\x00')) # This is needed some


# Write Mode 
write_spi(ser, '2000000')

# Write data
write_spi(ser, '2020000')

# Read Mode 
write_spi(ser, '2000002')

# read data
write_spi(ser, '2020000')

