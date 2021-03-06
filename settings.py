from sys import platform

def init():
    global BModePort, MModePort, modeVar, stopper, Mstopper, DebugMode, TGC, BF
    modeVar = True
    stopper = True
    Mstopper = False
    DebugMode =     0
    TGC= False
    BF = False

    if platform == "win32":
        print("win32")

        BModePort = "COM3"
        MModePort = "COM4"
    else:
        print("linux")

        BModePort = "/dev/COM3"
        MModePort = "/dev/COM4"
    
    global start_y, end_y, C, Pitch, unit_d, sampF, clock, offset_correction
    # offset in Pyserial and offset  in the begin of programmed pulser file
    offset_correction = 1*(50 + 2)

    Pitch = 0.3 # mm
    C = 1540 *1e3    # mm/s
    sampF = 20*1e6  # MHz
    unit_d = C* (1/sampF) * 0.5

    start_y = 0  
    end_y = 900

    clock = 200*1e6

    global start_a, end_a, step_a
    start_a = -5
    end_a = 5
    step_a = 0.5

# init()
    
# from sys import platform

# class Rsetting:
#     def __init__(self):
#         if platform == "win32":
#             print("win32")

#             self.BModePort = "COM3"
#             self.MModePort = "COM4"
#         else:
#             print("linux")

#             self.BModePort = "/dev/COM3"
#             self.MModePort = "/dev/COM4"

    
# R = Rsetting()
# print(R.BModePort)
    
