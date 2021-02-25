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

def short_pulse(num_cycles):
    list = ['000\n'] *200
    offset = 5
    freq = 5 *1e6  # 5*1e6
    settings.clock #  200*1e6
    clock_per_cycle = settings.clock/freq
    clock_half_cycle = round(clock_per_cycle/2)
    end_add = 0
    print('Cycle_time: ' + str(clock_half_cycle))

    if num_cycles == 0:
        list = ['011\n'] *200
    if num_cycles >= 0.5:
        for i in range(offset+0, offset+clock_half_cycle):
            list[i] = '001\n'
            end_add = i

    if num_cycles >= 1:
        for i in range(offset+clock_half_cycle, offset+2*clock_half_cycle):
            list[i] = '010\n'
            end_add = i

    if num_cycles == 2:
        for i in range(offset+2*clock_half_cycle, offset+3*clock_half_cycle):
            list[i] = '001\n'
            end_add = i

        for i in range(offset+3*clock_half_cycle, offset+4*clock_half_cycle):
            list[i] = '010\n'
            end_add = i

    
    for i in range(end_add+1, len(list)):
        if i > len(list)-10:
            list[i] = '011\n'

    print(end_add)
    # list[90:-1]= '011\n'

    return list

# f = open("pulser_test.mif", "r")
# lines = f.readlines()
# f.close()

lines = short_pulse(2)
# print(lines)

ser = serial.Serial(settings.BModePort, 8*1000000, timeout=2)  # open serial port
ser.flushInput()
ser.flushOutput()
ser.write(bytearray(b'\xff\xff')) # Choose mode/reset
ser.write(bytearray(b'\x00\x02')) # set mode to Pulseforming




for J in range(0,32):
    address_counter = 0
    for l in lines:
        # print(get_bin(address_counter,8),l)
        send_data(ser,J,address_counter,int(l,2))
        address_counter = address_counter +1






# my_list = lines
# with open('your_file.txt', 'w') as f:
#     for item in my_list:
#         f.write(item)

    

