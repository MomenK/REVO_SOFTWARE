import serial
import numpy as np
import time
import settings
settings.init()


def write_spi (port,data):
    a =  data[0:2]
    b =  data[2:4]
    c =  '0'+ data[4:5]
    d =  data[5:7]
    X = bytearray.fromhex(a+b)
    Y = bytearray.fromhex(c+d)

    port.write(X)
    port.write(Y) 
    time.sleep(0.01)
    port.write(bytearray(b'\x00\x00')) 
    time.sleep(0.01)
    pass


ser = serial.Serial(settings.BModePort, 8*1000000, timeout=2)  # open serial port
ser.flushInput()
ser.flushOutput()
ser.write(bytearray(b'\xff\xff')) # Choose mode/reset
ser.write(bytearray(b'\x00\x04')) # set mode to beamforming

f = open("full12x14.mif", "r")
lines = f.readlines()
f.close()

for line in lines:
    command = line.strip('\n')
    print(command)

    write_spi(ser, command)
    if command == '2000002':
        time.sleep(1)


