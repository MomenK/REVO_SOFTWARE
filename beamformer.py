import serial
import numpy as np
import settings
settings.init()

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

delayV = 0


ser = serial.Serial(settings.BModePort, 8*1000000, timeout=2)  # open serial port
ser.flushInput()
ser.flushOutput()
ser.write(bytearray(b'\xff\xff')) # Choose mode/reset
ser.write(bytearray(b'\x00\x01')) # set mode to beamforming

for i in range(0,32):
    send_data(ser,i,delayV*i)



# send_data(ser,0,delayV)
# send_data(ser,1,delayV)
# send_data(ser,2,delayV)
# send_data(ser,3,delayV)
# send_data(ser,4,delayV)
# send_data(ser,5,delayV)
# send_data(ser,6,delayV)
# send_data(ser,7,delayV)

# send_data(ser,8,delayV)
# send_data(ser,9,delayV)
# send_data(ser,10,delayV)
# send_data(ser,11,delayV)
# send_data(ser,12,delayV)
# send_data(ser,13,delayV)
# send_data(ser,14,delayV)
# send_data(ser,15,delayV)

# send_data(ser,16,delayV)
# send_data(ser,17,delayV)
# send_data(ser,18,delayV)
# send_data(ser,19,delayV)
# send_data(ser,20,delayV)
# send_data(ser,21,delayV)
# send_data(ser,22,delayV)
# send_data(ser,23,delayV)

# send_data(ser,24,delayV)
# send_data(ser,25,delayV)
# send_data(ser,26,delayV)
# send_data(ser,27,delayV)
# send_data(ser,28,delayV)
# send_data(ser,29,delayV)
# send_data(ser,30,delayV)
# send_data(ser,31,delayV)



# # # while True:
# # #     ser.flushInput()
# # #     ser.flushOutput()
# # #     ser.reset_input_buffer()
# # #     ser.reset_output_buffer()
# # #     # # ser.write(b'a')
# # #     # ser.write(b'\xfa') 
# # #     # ser.write(b'\x0a')
# # #     ser.write(bytearray(b'\xf8\x00'))
# # #     ser.write(bytearray(b'\xf0\x00'))
# # #     ser.write(bytearray(b'\xe8\x00'))
# # #     ser.write(bytearray(b'\xe0\x00'))
# # #     ser.write(bytearray(b'\xd8\x00'))
# # #     ser.write(bytearray(b'\xd0\x00'))
# # #     ser.write(bytearray(b'\xc8\x00'))
# # #     ser.write(bytearray(b'\xc0\x00'))
# # #     ser.write(bytearray(b'\xb8\x00'))
# # #     ser.write(bytearray(b'\xb0\x00'))
# # #     ser.write(bytearray(b'\xa8\x00'))
# # #     ser.write(bytearray(b'\xa0\x00'))
# # #     ser.write(bytearray(b'\x98\x00'))
# # #     ser.write(bytearray(b'\x90\x00'))
# # #     ser.write(bytearray(b'\x88\x00'))
# # #     ser.write(bytearray(b'\x80\x00'))


# # #     ser.write(bytearray(b'\x78\x00'))
# # #     ser.write(bytearray(b'\x70\x00'))
# # #     ser.write(bytearray(b'\x68\x00'))
# # #     ser.write(bytearray(b'\x60\x00'))
# # #     ser.write(bytearray(b'\x58\x00'))
# # #     ser.write(bytearray(b'\x50\x00'))
# # #     ser.write(bytearray(b'\x48\x00'))
# # #     ser.write(bytearray(b'\x40\x00'))
# # #     ser.write(bytearray(b'\x38\x00'))
# # #     ser.write(bytearray(b'\x30\x00'))
# # #     ser.write(bytearray(b'\x28\x00'))
# # #     ser.write(bytearray(b'\x20\x00'))
# # #     ser.write(bytearray(b'\x18\x00'))
# # #     ser.write(bytearray(b'\x10\x00'))
# # #     ser.write(bytearray(b'\x08\x00'))
# # #     ser.write(bytearray(b'\x00\x00'))
# # #     data = ser.read(1000000)
# # #     print(len(data))
# # #     break



# #     data1 = np.frombuffer(data, dtype=np.int16, count=-1).reshape(-1,1024)


# #     print(data1.shape)
    
    

