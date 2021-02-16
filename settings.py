from sys import platform

def init():
    global BModePort, MModePort, modeVar, stopper, Mstopper, DebugMode
    modeVar = True
    stopper = True
    Mstopper = False
    DebugMode =     0

    if platform == "win32":
        print("win32")

        BModePort = "COM3"
        MModePort = "COM4"
    else:
        print("linux")

        BModePort = "/dev/COM3"
        MModePort = "/dev/COM4"
    
    global start_y, end_y, C, Pitch
    Pitch = 0.3
    C = 1.54 * 0.5 /20
    start_y = 50
    end_y = 500

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
    
