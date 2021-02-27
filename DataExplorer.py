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

from scipy import signal


def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y


aspect = 0.1
Path = './UserSessions/SaveNext/RFArrays/'
# file = 'BF.npy'
file = 'B_80,0_-10,0.npy'

X = np.load(Path +file )


X = butter_highpass_filter(X.T,1*1e6,20*1e6,order =5).T  # MUST BE ROW ARRAY 32*1000
# X = butter_lowpass_filter(X.T,10*1e6,20*1e6,order =5).T  # MUST BE ROW ARRAY 32*1000

z_axis = np.arange(0,X.shape[0]) * 1.540*0.5*(1/20)
TGC_dB = 0.5*5 * z_axis/10

TGC = 10**(TGC_dB/20)

X = (X.T * TGC).T



# X = X-np.mean(X,axis=0)
XX= np.abs(hilbert(X))

YY = 20*np.log10(XX+1)








def _Update(self):
    print(var.get(), var1.get())
    image_c.set_clim(vmin=var1.get(), vmax= var.get())
    image.set_clim(vmin=10**(var1.get()/20), vmax= 10**(var.get()/20))
    canvas.draw()


def _quitAll( top):
    top.quit()
    top.destroy()


root = Tk()
root.wm_title("Data Explorere")  
root.protocol("WM_DELETE_WINDOW", lambda: _quitAll(root))
root.maxsize(1200, 1000) # width x height
# root.config(bg="white")

fig = plt.figure(figsize =(8,8) )# 

plt.subplot(121)
image = plt.imshow(XX, cmap='gray',  aspect=aspect)
plt.title('Image')
plt.xlabel('Width (mm)')
plt.ylabel('Depth (mm)')

plt.subplot(122)
image_c = plt.imshow(YY, cmap='gray',  aspect=aspect)
plt.title('Compressed Image')
plt.xlabel('Width (mm)')
plt.ylabel('Depth (mm)')

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()


var = DoubleVar()
scale = Scale( root, variable = var, orient=HORIZONTAL,from_=1, to=150, resolution=0.5, \
    length=300, label='Dynamic range (dB)', command=_Update ) 
scale.set(70)

var1 = DoubleVar()
scale1 = Scale( root, variable = var1, orient=HORIZONTAL,from_=1, to=100, resolution=0.5, \
    length=300, label='Reject (dB)' , command=_Update) 

scale1.set(0)

canvas.get_tk_widget().grid(row=1, column=0, padx=5, pady=5, sticky='n')
scale.grid(row=2, column=0,columnspan=3 , padx=5, pady=5, sticky='n')
scale1.grid(row=3, column=0,columnspan=3,  padx=5, pady=5, sticky='n')


root.mainloop()