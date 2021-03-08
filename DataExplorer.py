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

start = 400
end = start+2500

too = 70
fromm = too - 55

# too = 105
# fromm = too - 65

# tooC = 140 
# frommC = tooC - 65

tooC = 90
frommC = tooC - 55


aspect = 1
file_name= 'T_3_B1'
Path = './UserSessions/'+ file_name +'/RFArrays/'
file = 'BF.npy'
# file = 'BF_0.npy'
# file = 'B_80,0_-10,0.npy'

X = np.load(Path +file )


# X = butter_highpass_filter(X.T,5*1e6,20*1e6,order =5).T  # MUST BE ROW ARRAY 32*1000
# X = butter_lowpass_filter(X.T,8*1e6,20*1e6,order =5).T  # MUST BE ROW ARRAY 32*1000

z_axis = np.arange(0,X.shape[0]) * 1.540*0.5*(1/20)
TGC_dB = 0.5*5 * z_axis/10

TGC = 10**(TGC_dB/20)

# X = (X.T * TGC).T



# X = X-np.mean(X,axis=0)
XX= np.abs(hilbert(X))

YY = 20*np.log10(XX+1)



print(XX.shape)
XX =XX[start:end,:]
YY =YY[start:end,:]
print(XX.shape)



def _Update(self):
    print(var.get(), var1.get())
    image_c.set_clim(vmin=varC1.get(), vmax= varC.get())
    image.set_clim(vmin=10**(var1.get()/20), vmax= 10**(var.get()/20))
    canvas.draw()


def _quitAll( top):
    top.quit()
    top.destroy()

def _save():
    print("ll")
    fig.savefig( 'Output.png' ,bbox_inches='tight', pad_inches = 0,dpi = 500)

    extent = fig1.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    # fig.savefig('ax2_figure.png', bbox_inches=extent)
    xOffset = -0.3
    extent.x0 += xOffset
    extent.x1 += xOffset

    fig.savefig('Output1.png', bbox_inches=extent.expanded(1.3, 1.2))

    extent = fig2.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    # fig.savefig('ax2_figure.png', bbox_inches=extent)
    xOffset = -0.3
    extent.x0 += xOffset
    extent.x1 += xOffset

    fig.savefig('Output2.png', bbox_inches=extent.expanded(1.3, 1.2))

    pass


root = Tk()
root.wm_title("Data Explorere")  
root.protocol("WM_DELETE_WINDOW", lambda: _quitAll(root))
root.maxsize(1200, 1000) # width x height
# root.config(bg="white")

fig = plt.figure(figsize =(7,7) )# 


fig1 = plt.subplot(121)
image = plt.imshow(XX, cmap='gray',  aspect=aspect, extent=[0,31* 0.3,XX.shape[0] * 0.01,0])
plt.title('Image')
plt.xlabel('Width (mm)')
plt.ylabel('Depth (mm)')

fig2 = plt.subplot(122)
image_c = plt.imshow(YY, cmap='gray',  aspect=aspect, extent=[0,31* 0.3,YY.shape[0] * 0.01,0])
plt.title('Log-compressed Image')
plt.xlabel('Width (mm)')
plt.ylabel('Depth (mm)')

plt.tight_layout()

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()


var = DoubleVar()
scale = Scale( root, variable = var, orient=HORIZONTAL,from_=1, to=150, resolution=0.5, \
    length=300, label='Dynamic range (dB)', command=_Update ) 
scale.set(too)

var1 = DoubleVar()
scale1 = Scale( root, variable = var1, orient=HORIZONTAL,from_=1, to=100, resolution=0.5, \
    length=300, label='Reject (dB)' , command=_Update) 

scale1.set(fromm)

varC = DoubleVar()
scaleC = Scale( root, variable = varC, orient=HORIZONTAL,from_=1, to=150, resolution=0.5, \
    length=300, label='Dynamic range (dB)', command=_Update ) 
scaleC.set(tooC)

varC1 = DoubleVar()
scaleC1 = Scale( root, variable = varC1, orient=HORIZONTAL,from_=1, to=100, resolution=0.5, \
    length=300, label='Reject (dB)' , command=_Update) 

scaleC1.set(frommC)

button_Save = Button(bg='whitesmoke', text="Save", command=_save)

canvas.get_tk_widget().grid(row=1, column=0,columnspan=4, padx=5, pady=5, sticky='n')
scale.grid(row=2, column=0,columnspan=2 , padx=5, pady=5, sticky='n')
scale1.grid(row=3, column=0,columnspan=2,  padx=5, pady=5, sticky='n')
scaleC.grid(row=2, column=2,columnspan=2 , padx=5, pady=5, sticky='n')
scaleC1.grid(row=3, column=2,columnspan=2,  padx=5, pady=5, sticky='n')

button_Save.grid(row=4, column=0, columnspan=4,padx=5, pady=5, sticky='w'+'e'+'n'+'s')


root.mainloop()





