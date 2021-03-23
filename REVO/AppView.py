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


from datetime import datetime

from REVO.Beamformer import PW_BF

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

import settings




def plot(BModeInstance, bDateQ, bCntlQ, bEnQ, bFbQ, m_q,m_q_fps,m_q_enabler,MModeInstance):
    global root, canvas, image, label , var, var1, gain, angle, fig, ax, Hist, fig1, folder, Engine, Focus_depth
    global button_stop, button_M_stop, button_TGC, button_BF, button_SaveNext, SaveNext

    SaveNext = False
    Engine = PW_BF(sampling_rate = 20 ,Pitch = 0.3, C= 1.54, F_num= 1.75)
    # Create root object
    root = Tk()
    root.wm_title("REVO IMAGING TOOL")  
    root.protocol("WM_DELETE_WINDOW", lambda: _quitAll(BModeInstance,MModeInstance,root))
    root.maxsize(1200, 900) # width x height
    root.config(bg="white")

    # Create left and right frame
    right_frame = Frame(root, width=600, height=400,bg='white') 
    right_frame.grid(row=0, column=1, padx=10, pady=5, sticky='NW')

    left_frame = Frame(root, width=200, height= 400, bg='whitesmoke')
    left_frame.grid(row=0, column=0, padx=10, pady=5, sticky='NWSE')
    # Hist_window = Frame(left_frame, width=200, height=200, bg='whitesmoke')
    # Hist_window.grid(row=10, column=0,columnspan=4 , padx=5, pady=5, sticky='NWSE')

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

        print(settings.end_y* settings.unit_d, settings.start_y* settings.unit_d)
    
    canvas = FigureCanvasTkAgg(fig, master=right_frame)  # A tk.DrawingArea.
    canvas.draw()
    
    # fig1 = plt.figure(figsize =(4,4), facecolor = 'whitesmoke' )# 
    # Hist = FigureCanvasTkAgg(fig1, master=Hist_window)  # A tk.DrawingArea.
    # Hist.draw()

    # FPS label 
    prompt = 'fps'
    label = Label(master= right_frame,bg='white', text=prompt, width=len(prompt))

 
    # Entry 
    label_folder = Label(master= left_frame, text="Folder name")
    Focus_depth_label = Label(master= left_frame, text="Focus Depth")

    folder = Entry(master =left_frame )  
    Focus_depth = Entry(master =left_frame ) 

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

    Focus_depth_label.grid(row=9, column=0,columnspan=2,  padx=5, pady=5, sticky='n')
    Focus_depth.grid(row=9, column=2,columnspan=2,  padx=5, pady=5, sticky='n')

    
    button_Program.grid(row=10, column=0, padx=5, pady=5, sticky='w'+'e'+'n')
    button_Save.grid(row=10, column=1, padx=5, pady=5, sticky='w'+'e'+'n')
    button_SaveNext.grid(row=10, column=2, padx=5, pady=5, sticky='w'+'e'+'n')

    button_BF.grid(row=11, column=0, padx=5, pady=5, sticky='w'+'e'+'n')
    button_TGC.grid(row=11, column=1, padx=5, pady=5, sticky='w'+'e'+'n')
    


    # Hist.get_tk_widget().grid(row=1, column=0,columnspan=4, padx=20, pady=5, sticky='W')

    # Start App task
    updateplot(bDateQ,bCntlQ,bEnQ, bFbQ,)
    M_updateplot(m_q, m_q_fps)
    root.mainloop()


def updateplot(bDateQ,bCntlQ,bEnQ, bFbQ,):
    global DataToPlot, result_RF, SaveNext
    try:    
        bDataD =  bDateQ.get_nowait()
    except:
        root.after(1,updateplot,bDateQ,bCntlQ,bEnQ, bFbQ)
    else: 

        result_RF = bDataD[0]

        if settings.DebugMode == 1:
            result_full = result_RF
        else:  

            result_RF_noMean = butter_highpass_filter(result_RF.T,1*1e6,20*1e6,order =5).T  # MUS
            result_RF_noMean = result_RF_noMean[settings.start_y+settings.offset_correction:-1,:]

            if settings.TGC == True:
                z_axis = np.arange(0,result_RF_noMean.shape[0]) * 1.540*0.5*(1/20)
                TGC_dB = 0.5*5 * z_axis/10
                TGC = 10**(TGC_dB/20)
                result_RF_noMean = (result_RF_noMean.T * TGC).T

            if settings.BF == True:
                result_RF_noMean = Engine.Dyn_R(result_RF_noMean,0)
 

            result_full = np.abs(hilbert(result_RF_noMean.T)).T
      
        result = result_full[0:settings.end_y,:]

        if settings.DebugMode == 1:
            DataToPlot = result
            image.set_data(DataToPlot)
            image.set_clim(vmin=-1000, vmax=1000)
            failed = []
            for i in range(0,31-2):
                if np.all(DataToPlot[3:,i] == DataToPlot[3:,i+2]) :
                    pass
                else:
                    print(i)
                    x = DataToPlot[3:,i] == DataToPlot[3:,i+2]
                    # print(x)
                    print(np.where( x == False))
                    failed.append(i)
            if (DataToPlot[20,0] % 2) == 0:
                print("Even!")
            # else:
            #     print("Odd!")
            if not (DataToPlot[20,0]   == 47): 
                print("Sample of interest is :" + str(DataToPlot[20,:]))
                assert True, "DOGSHITE"

            if len(failed) > 0:
                print(failed)
                print(len(failed))
        else:
            if settings.modeVar:
                DataToPlot = 20*np.log10(result)
                image.set_clim(vmin=var1.get(), vmax= var.get())

            else:
                DataToPlot =  result
                image.set_clim(vmin=10**(var1.get()/20), vmax= 10**(var.get()/20))

            image.set_data(DataToPlot)
            # print(DataToPlot.max(), np.mean(DataToPlot))

        canvas.draw()
        canvas.flush_events()
        text = bDataD[1]
        label.config(text=text, width=len(text))

        if SaveNext == False:
            button_SaveNext.update()
            button_SaveNext["state"] = NORMAL
        
        # If the mode is SaveNext .. You need to Save, Update, block until feed back, Enable button, 
        if SaveNext == True:

            button_SaveNext["state"] = DISABLED
            button_SaveNext.update()

            SaveNext = False
            _save()
            current = angle.get()
            if current == settings.end_a:
                new = settings.start_a
            else:
                new =  current + settings.step_a

            angle.set(new)
            _Program(bCntlQ)

            bFbD = bFbQ.get()

        root.after(1,updateplot,bDateQ,bCntlQ,bEnQ, bFbQ)

        # q_enabler.put([settings.stopper, gain.get()])

        


def _save():
    # ax.axis('off')
    fold = str(folder.get())
    if fold != "":
        fold = 'UserSessions/' + fold + '/'
        print(fold)
        # os.mkdir("./"+str(fold))
        Path("./"+str(fold)).mkdir(parents=True, exist_ok=True)
        Path("./"+str(fold)+'Images/').mkdir(parents=True, exist_ok=True)
        Path("./"+str(fold)+'Arrays/').mkdir(parents=True, exist_ok=True)
        Path("./"+str(fold)+'RFArrays/').mkdir(parents=True, exist_ok=True)
    else:
        print("Saving at top level")


    now = datetime.now()
    current_time = now.strftime("%H_%M_%S")
    # print("Current Time =", current_time)
    
    # file =  fold + 'B_' + str(time.ctime()).replace(" ", "_").replace(":", "")
    # file =  'B_' + current_time +"_" +str(angle.get()).replace(".", "_")
    file =  'B_' + str(gain.get()).replace(".", ",") + "_" +str(angle.get()).replace(".", ",")
    print(file)
    Current_Array = DataToPlot
    Current_RFArray = result_RF
    fig.savefig(fold +'Images/' + file + '.png' ,bbox_inches='tight', pad_inches = 0,dpi = 500)
    # ax.axis('on')
    np.save(fold +'Arrays/' + file,Current_Array)
    np.save(fold +'RFArrays/' + file,Current_RFArray)
    if settings.DebugMode == 1:
        print(Current_Array.shape)
        np.savetxt("bar.csv", Current_Array, delimiter=",",fmt='%5.1f')
        failed = []
        for i in range(0,31-2):
            if np.all(Current_Array[1:,i] == Current_Array[1:,i+2]) :
                pass
            else:
                print(i)
                x = Current_Array[1:,i] == Current_Array[1:,i+2]
                # print(x)
                print(np.where( x == False))
                failed.append(i)
        print("Sample of interest is!" + str(Current_Array[20,0]))
        if (Current_Array[20,0] % 2) == 0:
            print("Even!")
        else:
            print("Odd!")


        print(failed)
        print(len(failed))
    


def _Program(bCntlQ):
    depth = Focus_depth.get()
    if len(depth) > 0:
        depth = float(depth)*1e-3
        x_axis = (np.arange(0,32)-16) * settings.Pitch*1e-3
        delays = depth/(settings.C*1e-3) * (1 - np.sqrt( 1+ (x_axis/depth)**2  ) )
        print(delays)
        n = np.round(delays * 200*1e6).astype("int")
        print(n)

    else:
        d = settings.Pitch * round(math.sin(math.radians(angle.get())), 10)
        # print("distance (mm):")
        # print(d)
        
        n = d * settings.clock / settings.C 
        print("number of cycles:")
        print(n)

    # bCntlQ.put([settings.stopper, gain.get(), n])
    bCntlQ.put([ gain.get(), n])


def _SaveNext(bCntlQ,bFbQ):
    global SaveNext
    if  SaveNext == False:
        SaveNext = True

def _toggle(bEnQ):
    settings.stopper = not settings.stopper
    bEnQ.put(settings.stopper)
    button_stop.config(text= 'Stop' if settings.stopper else 'Start')

def _BF():
    settings.BF = not settings.BF
    button_BF.config(text= 'BF: ON' if settings.BF else 'BF: OFF')

def _TGC():
    settings.TGC = not settings.TGC
    button_TGC.config(text= 'TCG: ON ' if settings.TGC else 'TGC: OFF')

def _quitAll(process,M_process, top):
    global quitter
    quitter = True
    process.terminate()
    M_process.terminate()
    top.quit()
    top.destroy()

def _mode():
    settings.modeVar = not settings.modeVar

# ************************************************ M-Mode ******************************************

# ************************************************ M-Mode ******************************************

# ************************************************ M-Mode ******************************************
def _Mtoggle(m_q_enabler):
    m_q_enabler.put(True)
    button_M_stop["state"] = "disabled"


def M_updateplot(m_q,m_q_fps):
    try:
        Q = m_q.get_nowait()
        M_Image = Q[0]
        M_timestamp =  Q[1]
        # time.sleep(1)
        # M_timestamp = m_q_fps.get_nowait()
        root.after(1,M_mode_plot,M_Image,M_timestamp,M_timestamp)
        # M_mode_plot(M_Image,M_timestamp,M_timestamp)
        root.after(10,M_updateplot,m_q,m_q_fps)
    except:
        root.after(10,M_updateplot,m_q,m_q_fps)
   
def M_mode_plot(agg,boy,timestampArr):
    print('Plotting M mode')



    timeStamp = np.array(timestampArr)
    Mimage =  np.array(agg)
    # print(Mimage.shape)
    Mimage = Mimage.transpose(1,0,2)
    # print(Mimage.shape)
    Mimage = Mimage.reshape((1024,-1))
    print(Mimage.shape)

    result_RF = Mimage
    result_RF_noMean = butter_highpass_filter(result_RF.T,1*1e6,20*1e6,order =5).T  # MUS
    result = np.abs(hilbert(result_RF_noMean.T)).T



    # print(len(boy))
    plt.close()
    plt.figure()
    # THIS IS BAD AND INTRODUCES BLACK LINES FOR SOME REASON
    # Image = plt.imshow(Mimage,cmap='gray',interpolation='None', extent=[0,timestampArr[-1] - timestampArr[0] , 1024*1.498*0.5*(1/20),0], aspect='auto',animated=False)
    # Image = plt.imshow(Mimage,cmap='gray',aspect= 4)
    # This is the fix for some reason! interpolation=None works. interpolation='None' does not!
    Img =  np.zeros((1024,2000))
    if settings.DebugMode == 1:
        Image = plt.imshow(Img, cmap='gray', aspect=1)
        Image.set_data(Mimage)
        Image.set_clim(vmin=-1000, vmax=1000)
        np.savetxt("foo.csv", Mimage, delimiter=",",fmt='%5.1f')
        failed = []
        for i in range(0,2000-1):
            if np.all(Mimage[10:,i] == Mimage[10:,i+1]) :
                pass
            else:
                print(i)
                x = Mimage[10:,i] == Mimage[10:,i+1]
                print(np.where( x == False))
                failed.append(i)
        print(failed)
        print(len(failed))
    else:
        if settings.modeVar:
            M_Data = 20*np.log10(result)
            Image = plt.imshow(M_Data,cmap='gray', extent=[0,timestampArr[-1] - timestampArr[0] , 1024*1.498*0.5*(1/20),0], aspect='auto')
            Image.set_clim(vmin=var1.get(), vmax= var.get())

        else:
            M_Data =  result
            Image = plt.imshow(M_Data,cmap='gray', extent=[0,timestampArr[-1] - timestampArr[0] , 1024*1.498*0.5*(1/20),0], aspect='auto')
            Image.set_clim(vmin=10**(var1.get()/20), vmax= 10**(var.get()/20))

        
        # Image.set_data(Mimage)
        # Image.set_clim(vmin=10**(var1.get()/20), vmax= 10**(var.get()/20))
        plt.xlabel('Time (s)')
        plt.ylabel('Depth (mm)')
    #   # Has to be passed from inside the other process
    # plt.show()
    # SAVING
    file =  'M_' + str(time.ctime()).replace(" ", "_").replace(":", "")
    
    fold = str(folder.get())
    if fold != "":
        fold = 'UserSessions/' + fold + '/'
        print(fold)
        # os.mkdir("./"+str(fold))
        Path("./"+str(fold)).mkdir(parents=True, exist_ok=True)
        Path("./"+str(fold)+'M_Images/').mkdir(parents=True, exist_ok=True)
        Path("./"+str(fold)+'M_Arrays/').mkdir(parents=True, exist_ok=True)
        Path("./"+str(fold)+'M_RFArrays/').mkdir(parents=True, exist_ok=True)
    else:
        print("Saving at top level")

    
    # saving image really slow stuff
    # plt.axis('off')
    plt.savefig( fold +'M_Images/'  + file + '.png' ,bbox_inches='tight', pad_inches = 0,dpi = 500)
    plt.axis('on')
    np.save( fold +'M_Arrays/' + file,result)
    np.save(fold +'M_RFArrays/' + file,result_RF)
    np.save(fold +'M_Arrays/' + 'T'+ file,timeStamp)
   

    # fold = str(folder.get())
    # if fold != "":
    #     fold = 'UserSessions/' + fold + '/'
    #     print(fold)
    #     # os.mkdir("./"+str(fold))
    #     Path("./"+str(fold)).mkdir(parents=True, exist_ok=True)
    #     Path("./"+str(fold)+'M_Images/').mkdir(parents=True, exist_ok=True)
    #     Path("./"+str(fold)+'M_Arrays/').mkdir(parents=True, exist_ok=True)
    #     Path("./"+str(fold)+'M_RFArrays/').mkdir(parents=True, exist_ok=True)
    # else:
    #     print("Saving at top level")

    # file =  'M_' + str(gain.get()).replace(".", ",") + "_" +str(angle.get()).replace(".", ",")
    # print(file)

    # # Current_Array = DataToPlot
    # # Current_RFArray = result_RF
    # fig.savefig(fold +'M_Images/' + file + '.png' ,bbox_inches='tight', pad_inches = 0,dpi = 500)
    # # # ax.axis('on')
    # np.save(fold +'M_Arrays/' + file,result)
    # np.save(fold +'M_RFArrays/' + file,result_RF)


    fps = []
    for i in range(0,1000-1):
        fps.append(1/(timeStamp[i+1] - timeStamp [i]))
    print('average fps: ' + str(sum(fps)/len(fps)))
    print("Done")
    figf, axsf = plt.subplots(3)
    figf.suptitle('Vertically stacked subplots')
    axsf[0].plot(boy)
    axsf[1].plot(timeStamp)
    axsf[2].plot(fps)
    button_M_stop["state"] = "normal"
    plt.show()
    return