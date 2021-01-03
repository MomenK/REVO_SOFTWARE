import serial

import numpy as np


ser = serial.Serial('COM3', 8*1000000, timeout=2)  # open serial port


while True:
    ser.flushInput()
    ser.flushOutput()
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    # # ser.write(b'a')
    # ser.write(b'\xfa') 
    # ser.write(b'\x0a')
    ser.write(bytearray(b'\x00\xff'))
    ser.write(bytearray(b'\x08\xff'))
    ser.write(bytearray(b'\x10\xff'))
    ser.write(bytearray(b'\x18\xff'))
    data = ser.read(1000000)
    print(len(data))
    break



    data1 = np.frombuffer(data, dtype=np.int16, count=-1).reshape(-1,1024)


    print(data1.shape)
    
    

