import numpy as np
def focus_delay(centre_elment,depth):
    c = 1540
    pitch = 0.3*1e-3
    elements = np.arange(0,32)

    x_axis = (elements-centre_elment) * pitch

    delays = depth/c * (1 - np.sqrt( 1+ (x_axis/depth)**2  ) )

    clock_cycles = np.round(delays * 200*1e6).astype("int")


    return clock_cycles

print(focus_delay(15,10e-3))