#  Channel indexs are from 0 to 31

import serial
import numpy as np
import settings
settings.init()

get_bin = lambda x, n: format(x, 'b').zfill(n)


def data_package (channel, address, data):
    channel_b = get_bin(channel,5)
    address_b = get_bin(address,8)
    data_b = get_bin(data,3)
    full_b_int_bytes = int(channel_b + address_b + data_b, 2).to_bytes(2, 'big')
    print(str(full_b_int_bytes).replace('\\x', "")[1:])
    return bytearray(full_b_int_bytes)



def send_data(port, channel, address, data):
    data = data_package(channel, address, data)
    # print(data)
    port.write(data)
    pass


f = open("pulser_test.mif", "r")
lines = f.readlines()
f.close()

ser = serial.Serial(settings.BModePort, 8*1000000, timeout=2)  # open serial port
ser.flushInput()
ser.flushOutput()
ser.write(bytearray(b'\xff\xff')) # Choose mode/reset
ser.write(bytearray(b'\x00\x02')) # set mode to Pulseforming




for J in range(0,31):
    address_counter = 0
    for l in lines:
        # print(get_bin(address_counter,8),l)
        send_data(ser,J,address_counter,int(l,2))
        address_counter = address_counter +1

f.close()