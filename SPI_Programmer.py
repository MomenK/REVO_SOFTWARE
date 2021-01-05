import serial

import numpy as np

get_bin = lambda x, n: format(x, 'b').zfill(n)


def data_package (channel, delay):
    channel_b = get_bin(channel,5)
    print(channel_b)
    delay_b = get_bin(delay,11)

    full_b = channel_b + delay_b
    print(full_b)
    full_b_int = int(full_b, 2)
    print(full_b_int)

    full_b_int_bytes = full_b_int.to_bytes(2, 'big')
    print(full_b_int_bytes)

    return bytearray(full_b_int_bytes)



def send_data(port, channel, delay):
    data = data_package(channel,delay)
    print(data)
    port.write(data)
    pass


print(data_package(4,0))
# print(bytearray(b'\xf8\x00'))
delayV = 10


ser = serial.Serial('COM3', 8*1000000, timeout=2)  # open serial port
ser.flushInput()
ser.flushOutput()
ser.write(bytearray(b'\xff\xff')) # Choose mode/reset
ser.write(bytearray(b'\x00\x04')) # set mode to beamforming


send_data(ser,i,delayV*i)

time.sleep(0.1)
