from tkinter import * 
from tkinter import ttk

from scipy.signal import hilbert, chirp

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
import matplotlib.pyplot as plt

import numpy as np
import time
import math

import os
from pathlib import Path



Path = './UserSessions/noise/RFArrays/'
file = 'noise3.npy'

X = np.load(Path +file )

offset = np.mean(X[0:1000,:],axis=0)

print(np.around(offset,2))

offseter = np.array([-66.02,  91.58, -30.42,   2.46, -10.13, -42.97 ,-54.68, -78.3,  -33.97, -77.83,
  57.07, -12.34, -21.24,  -3.77, -35.7,    7.62,   2.9,  146.3,  67.74 ,141.88,
  96.44 , 20.47 , 58.54, -29.55, 111.67,  50.69, 106.68,  66.95, 166.36, -29.3,
 -44.9,   66.47])

print(offset-offseter)
