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

Path = './UserSessions/tube/RFArrays/'
file = 'BF.npy'

X = np.load(Path +file )
# X = X-np.mean(X,axis=0)
XX= np.abs(hilbert(X))

YY = 20*np.log10(XX)




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
image = plt.imshow(XX, cmap='gray',extent=[0,31* 0.3,XX.shape[0] *1.540*0.5*(1/20),0],  aspect=0.7)
plt.title('Image')
plt.xlabel('Width (mm)')
plt.ylabel('Depth (mm)')

plt.subplot(122)
image_c = plt.imshow(YY, cmap='gray',extent=[0,31* 0.3,XX.shape[0] *1.540*0.5*(1/20),0],  aspect=0.7)
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