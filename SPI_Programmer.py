import serial
import numpy as np
import time
import settings
settings.init()

def write_gain(port,gain):
    gain_hex = ['00' + hex(gain).split('x')[-1]][-1][-3:]
    write_spi(ser, '2000000')
    write_spi(ser, '2000010')
    write_spi(ser, '1000010')

    write_spi(ser, '1B50' + gain_hex)
    write_spi(ser, '2B50' + gain_hex)


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



ser = serial.Serial(settings.BModePort, 8*1000000, timeout=2)  # open serial port
ser.flushInput()
ser.flushOutput()
ser.write(bytearray(b'\xff\xff')) # Choose mode/reset
ser.write(bytearray(b'\x00\x04')) # set mode to SPI
# ser.write(bytearray(b'\x00\x00')) # This is needed some


# Write Mode 
write_spi(ser, '2000000')
write_spi(ser, '1000000')

# Write data
if settings.DebugMode == 1:
    print('DEBUG')
    write_spi(ser, '2020380') #  2020380 for SYNC
else:
    write_spi(ser, '2020000') #  2020380 for SYNC

# Read Mode 
write_spi(ser, '2000002')

# read data
write_spi(ser, '2020000')


# Try changing gain values 
# write_spi(ser, '2000000')

# write_spi(ser, '2000010')
# write_spi(ser, '1000010')

# # 20dB
# write_spi(ser, '1B50050')

# write_spi(ser, '2B50050')

# 906 ... 607
# write_spi(ser, '1B5013F')

# write_spi(ser, '2B5013F')


# 490 -- 325
# write_spi(ser, '1B50100')

# write_spi(ser, '2B50100')

# 267 -- 193
# write_spi(ser, '1B500C0')

# write_spi(ser, '2B500C0')

# 123
# write_spi(ser, '1B5003F')

# write_spi(ser, '2B5003F')

# 108
# write_spi(ser, '1B50000')

# write_spi(ser, '2B50000')



# write_spi(ser, '1B68000')

# write_spi(ser, '2B68000')


# write_gain(ser, 0)

# write_gain(ser, 319)