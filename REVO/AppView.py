from tkinter import * 
from tkinter import ttk

from scipy.signal import hilbert, chirp

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
import matplotlib.pyplot as plt

import numpy as np
import time


import settings


def plot(BModeInstance, bDateQ, bCntlQ, m_q,m_q_fps,m_q_enabler,MModeInstance):
    global root, canvas, image, label , var, var1, gain, angle, fig, ax, Hist, fig1, button_stop
    
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
            extent=[0, 31* settings.Pitch, settings.end_y* settings.C , settings.start_y* settings.C ], aspect=1)
        plt.xlabel('Width (mm)')
        plt.ylabel('Depth (mm)')
    
    canvas = FigureCanvasTkAgg(fig, master=right_frame)  # A tk.DrawingArea.
    canvas.draw()
    
    fig1 = plt.figure(figsize =(4,4), facecolor = 'whitesmoke' )# 
    Hist = FigureCanvasTkAgg(fig1, master=Hist_window)  # A tk.DrawingArea.
    Hist.draw()
 
    
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
    scale_angle = Scale( left_frame, variable = angle, orient=HORIZONTAL,from_=-20, to=20, resolution=1, length=300, label='Angle (12-51 dB)' ) 
    angle.set(0)
    # FPS label 
    prompt = 'fps'
    label = Label(master= right_frame,bg='white', text=prompt, width=len(prompt))
   
    #  Buttons
    button_M_stop= Button(master=left_frame,bg='whitesmoke', text="Record M-mode", command=lambda:_Mtoggle(m_q_enabler))
    button_stop = Button(master=left_frame,bg='whitesmoke', text="Stop", command=lambda:_toggle(bCntlQ))
    button_Mode = Button(master=left_frame,bg='whitesmoke', text="Mode", command=_mode)
    button_Save = Button(master=left_frame,bg='whitesmoke', text="Save", command=_save)

    button_Program = Button(master=left_frame,bg='whitesmoke', text="Program", command=lambda:_Program(bCntlQ))

    #  Grid Place *******************************************************************
    canvas.get_tk_widget().grid(row=1, column=0, padx=5, pady=5, sticky='n')
    label.grid(row=2, column=0, padx=5, pady=5, sticky='w'+'e'+'n'+'s')

    button_stop.grid(row=0, column=0, padx=5, pady=5, sticky='w'+'e'+'n'+'s')
    button_Mode.grid(row=0, column=1, padx=5, pady=5, sticky='w'+'e'+'n'+'s')
    button_Save.grid(row=0, column=2, padx=5, pady=5, sticky='w'+'e'+'n'+'s')
    button_M_stop.grid(row=0, column=3, padx=5, pady=5, sticky='w'+'e'+'n'+'s')

    ttk.Separator(left_frame,orient=HORIZONTAL).grid(row=1, column=0, columnspan=4,pady=5, sticky='EW')
    scale.grid(row=3, column=0,columnspan=4 , padx=5, pady=5, sticky='n')
    scale1.grid(row=4, column=0,columnspan=4,  padx=5, pady=5, sticky='n')

    ttk.Separator(left_frame,orient=HORIZONTAL).grid(row=5, column=0, columnspan=4,pady=5, sticky='EW')
    scale_gain.grid(row=6, column=0,columnspan=4,  padx=5, pady=5, sticky='n')
    scale_angle.grid(row=7, column=0,columnspan=4,  padx=5, pady=5, sticky='n')
    button_Program.grid(row=8, column=2, padx=5, pady=5, sticky='w'+'e'+'n'+'s')

    # Hist.get_tk_widget().grid(row=1, column=0,columnspan=4, padx=20, pady=5, sticky='W')

    # Start App task
    updateplot(bDateQ,bCntlQ)
    M_updateplot(m_q, m_q_fps)
    root.mainloop()



def updateplot(q,q_enabler):
    global DataToPlot, result_RF
    try:    
        bDataD =  q.get_nowait() 
        result_RF = bDataD[0]
   
        if settings.DebugMode == 1:
            result_full = result_RF
        else:
            result_full = np.abs(hilbert(result_RF-np.mean(result_RF,axis=0)))
            

        result = result_full [settings.start_y:settings.end_y,:]
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
            if not (DataToPlot[20,0]   == 147): 
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
        # p = fig1.gca()
        # p.clear()
        # p.hist(DataToPlot.flatten(), 20, range= [-50, 100])
        # Hist.draw()
        canvas.draw()
        text = bDataD[1]
        label.config(text=text, width=len(text))
        root.after(1,updateplot,q,q_enabler)

        # q_enabler.put([settings.stopper, gain.get()])
    except:
        root.after(1,updateplot,q,q_enabler)



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
        root.after(1,M_updateplot,m_q,m_q_fps)
   
def M_mode_plot(agg,boy,timestampArr):
    print('Plotting M mode')
    result = np.array(agg)
    timeStamp = np.array(timestampArr)
    Mimage =  result
    # print(Mimage.shape)
    Mimage = Mimage.transpose(1,0,2)
    # print(Mimage.shape)
    Mimage = Mimage.reshape((1024,-1))
    print(Mimage.shape)
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
        Image = plt.imshow(Mimage,cmap='gray', extent=[0,timestampArr[-1] - timestampArr[0] , 1024*1.498*0.5*(1/20),0], aspect='auto')
        Image.set_data(Mimage)
        Image.set_clim(vmin=0, vmax=var.get()/100 * 4096)
        plt.xlabel('Time (s)')
        plt.ylabel('Depth (mm)')
    #   # Has to be passed from inside the other process
    file =  'M_' + str(time.ctime()).replace(" ", "_").replace(":", "")
    # saving image really slow stuff
    # plt.axis('off')
    plt.savefig('Images/' + file + '.png' ,bbox_inches='tight', pad_inches = 0,dpi = 500)
    plt.axis('on')
    np.save('Arrays/' + file,Mimage)
    np.save('Arrays/' + 'T'+ file,timeStamp)
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

def _quitAll(process,M_process, top):
    global quitter
    quitter = True
    process.terminate()
    M_process.terminate()
    top.quit()
    top.destroy()

def _mode():
    settings.modeVar = not settings.modeVar

def _save():
    # ax.axis('off')
    file =  'B_' + str(time.ctime()).replace(" ", "_").replace(":", "")
    Current_Array = DataToPlot
    Current_RFArray = result_RF
    fig.savefig('Images/' + file + '.png' ,bbox_inches='tight', pad_inches = 0,dpi = 500)
    # ax.axis('on')
    np.save('Arrays/' + file,Current_Array)
    np.save('RFArrays/' + file,Current_RFArray)
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
    
def _toggle(bCntlQ):
    settings.stopper = not settings.stopper
    bCntlQ.put([settings.stopper, gain.get(), angle.get()])
    button_stop.config(text= 'Stop' if settings.stopper else 'Start')

def _Program(bCntlQ):
    bCntlQ.put([settings.stopper, gain.get(), angle.get()])

def _Mtoggle(m_q_enabler):
    # global settings.Mstopper
    # settings.Mstopper = not settings.Mstopper
    
    m_q_enabler.put(True)
    # button_M_stop.config(text= 'Stop')
    button_M_stop["state"] = "disabled"
    # print(settings.Mstopper)
    # button_M_stop.config(text= 'Stop' if settings.Mstopper else 'Start')
