import serial

import numpy as np

import time



ser = serial.Serial('COM5', 8*1000000, timeout=2)  # open serial port
ser.flushInput()
ser.flushOutput()
ser.write(bytearray(b'\xff\xff')) # Choose mode/reset
ser.write(bytearray(b'\x00\x04')) # set mode to beamforming
# ser.write(bytearray(b'\x00\x00')) # This is needed some


# time.sleep(1)

# Write Mode 
ser.write(bytearray(b'\x20\x00')) 
ser.write(bytearray(b'\x00\x00')) 

time.sleep(0.1)

ser.write(bytearray(b'\x00\x00')) 
# ser.write(bytearray(b'\x00\x00')) 

time.sleep(0.1)

# Write data
ser.write(bytearray(b'\x20\x20')) 
ser.write(bytearray(b'\x00\x00')) 

time.sleep(0.1)

ser.write(bytearray(b'\x00\x00')) 
# ser.write(bytearray(b'\x00\x00')) 
time.sleep(0.1)

# Read Mode 
ser.write(bytearray(b'\x20\x00')) 
ser.write(bytearray(b'\x00\x02')) 

time.sleep(0.1)

ser.write(bytearray(b'\x00\x00')) 
# ser.write(bytearray(b'\x00\x00')) 

time.sleep(0.1)
# read data
ser.write(bytearray(b'\x20\x20')) 
ser.write(bytearray(b'\x01\x00')) 

time.sleep(0.1)

ser.write(bytearray(b'\x00\x00')) 
time.sleep(0.1)
# ser.write(bytearray(b'\x00\x00')) 
