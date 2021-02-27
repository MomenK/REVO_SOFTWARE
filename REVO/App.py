from tkinter import * 
from tkinter import ttk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
import matplotlib.pyplot as plt


import numpy as np

import settings

class App:
    def __init__(self,root):
        root.wm_title("REVO IMAGING TOOL")  
        # root.protocol("WM_DELETE_WINDOW", lambda: _quitAll(bTask,Mtask,root))
        root.maxsize(1200, 900) # width x height
        root.config(bg="white")

        self._setup_widgets(root)

    def _setup_widgets(self,root):
        right_frame = Frame(root, width=600, height=400,bg='white') 
        right_frame.grid(row=0, column=1, padx=10, pady=5, sticky='NW')

        left_frame = Frame(root, width=200, height= 400, bg='whitesmoke')
        left_frame.grid(row=0, column=0, padx=10, pady=5, sticky='NWSE')
        Hist_window = Frame(left_frame, width=200, height=200, bg='whitesmoke')
        Hist_window.grid(row=10, column=0,columnspan=4 , padx=5, pady=5, sticky='NWSE')

        # Create Figure 
        fig = plt.figure(figsize =(8,8), facecolor = 'white' )#   
        # ax = fig.gca()
        img =  np.zeros((1024,32))
        if settings.DebugMode == 1:
            image = plt.imshow(img, cmap='gray', aspect=0.1)
        else:
            image = plt.imshow(img, cmap='gray',interpolation='hanning',animated=False, \
                extent=[0, 31* settings.Pitch, settings.end_y* settings.unit_d, settings.start_y* settings.unit_d ], aspect=1)
            plt.xlabel('Width (mm)')
            plt.ylabel('Depth (mm)')
        
        canvas = FigureCanvasTkAgg(fig, master=right_frame)  # A tk.DrawingArea.
        canvas.draw()
        
        fig1 = plt.figure(figsize =(4,4), facecolor = 'whitesmoke' )# 
        Hist = FigureCanvasTkAgg(fig1, master=Hist_window)  # A tk.DrawingArea.
        Hist.draw()

        # FPS label 
        prompt = 'fps'
        label = Label(master= right_frame,bg='white', text=prompt, width=len(prompt))

    
        # Entry 
        label_folder = Label(master= left_frame, text="Folder name")

        folder = Entry(master =left_frame )    
        # Create scale/ Dynamic range max is 20*np.log10(4095) = 72.25
        var = DoubleVar()
        scale = Scale( left_frame, variable = var, orient=HORIZONTAL,from_=1, to=100, resolution=0.5, length=300, label='Dynamic range (dB)' ) 
        scale.set(70)
        var1 = DoubleVar()
        scale1 = Scale( left_frame, variable = var1, orient=HORIZONTAL,from_=1, to=100, resolution=0.5, length=300, label='Reject (dB)' ) 
        scale1.set(0)

        gain = DoubleVar()
        scale_gain = Scale( left_frame, variable = gain, orient=HORIZONTAL,from_=0, to=319, resolution=1, length=300, label='Gain (12-51 dB)' ) 
        gain.set(80)

        angle = DoubleVar()
        scale_angle = Scale( left_frame, variable = angle, orient=HORIZONTAL,from_=settings.start_a, to=settings.end_a, resolution=settings.step_a, length=300, label='Angles' ) 
        angle.set(0)

    
        #  Buttons
        button_M_stop= Button(master=left_frame,bg='whitesmoke', text="Record M-mode", command=lambda:_Mtoggle(m_q_enabler))
        button_stop = Button(master=left_frame,bg='whitesmoke', text="Stop", command=lambda:_toggle(bEnQ))
        button_Mode = Button(master=left_frame,bg='whitesmoke', text="Mode", command=_mode)

        button_Save = Button(master=left_frame,bg='whitesmoke', text="Save", command=_save)
        button_Program = Button(master=left_frame,bg='whitesmoke', text="Program", command=lambda:_Program(bCntlQ))

        button_BF = Button(master=left_frame,bg='whitesmoke', text="BF: OFF", command=_BF)
        button_TGC = Button(master=left_frame,bg='whitesmoke', text="TGC: OFF", command=_TGC)
        button_SaveNext = Button(master=left_frame,bg='whitesmoke', text="Save&next", command=lambda:_SaveNext(bCntlQ,bFbQ))
        
        #  Grid Place *******************************************************************
        canvas.get_tk_widget().grid(row=1, column=0, padx=5, pady=5, sticky='n')
        label.grid(row=2, column=0, padx=5, pady=5, sticky='w'+'e'+'n'+'s')

    

        button_stop.grid(row=1, column=0, padx=5, pady=5, sticky='w'+'e'+'n'+'s')
        button_Mode.grid(row=1, column=1, padx=5, pady=5, sticky='w'+'e'+'n'+'s')
        button_M_stop.grid(row=1, column=2, padx=5, pady=5, sticky='w'+'e'+'n'+'s')

        ttk.Separator(left_frame,orient=HORIZONTAL).grid(row=2, column=0, columnspan=4,pady=5, sticky='EW')
        scale.grid(row=3, column=0,columnspan=3 , padx=5, pady=5, sticky='n')
        scale1.grid(row=4, column=0,columnspan=3,  padx=5, pady=5, sticky='n')


        ttk.Separator(left_frame,orient=HORIZONTAL).grid(row=5, column=0, columnspan=4,pady=5, sticky='EW')
        label_folder.grid(row=6, column=0,columnspan=2, padx=5, pady=5, sticky='w'+'e'+'n'+'s')
        folder.grid(row=6, column=2,columnspan=2, padx=5, pady=5, sticky='w'+'e'+'n'+'s')

        scale_gain.grid(row=7, column=0,columnspan=4,  padx=5, pady=5, sticky='n')
        scale_angle.grid(row=8, column=0,columnspan=4,  padx=5, pady=5, sticky='n')

        
        button_Program.grid(row=9, column=0, padx=5, pady=5, sticky='w'+'e'+'n'+'s')
        button_Save.grid(row=9, column=1, padx=5, pady=5, sticky='w'+'e'+'n'+'s')
        button_BF.grid(row=10, column=0, padx=5, pady=5, sticky='w'+'e'+'n')
        button_TGC.grid(row=10, column=1, padx=5, pady=5, sticky='w'+'e'+'n')
        button_SaveNext.grid(row=9, column=2, padx=5, pady=5, sticky='w'+'e'+'n'+'s')
