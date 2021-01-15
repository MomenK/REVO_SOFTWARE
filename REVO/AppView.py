import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
import matplotlib.pyplot as plt

import numpy as np
import time



class settings:
    def __init__(self):
        self.modeVar = True
        self.stopper = True
        self.Mstopper = False

settings = settings()

def plot(q,q_fps,m_q,m_q_fps,q_enabler,m_q_enabler,BModeInstance,MModeInstance):
    global canvas, toolbar, image, button_stop, label, root, var, fig, image, ax
    
    root = tkinter.Tk()
    root.wm_title("REVO IMAGING TOOL")  
    root.protocol("WM_DELETE_WINDOW", lambda: _quitAll(BModeInstance,MModeInstance,root))

    var = tkinter.DoubleVar()
    scale = tkinter.Scale( root, variable = var, orient=tkinter.HORIZONTAL,from_=1, to=100, resolution=0.5, length=300, label='Dynamic range' )
    scale.pack(anchor=tkinter.CENTER)

    fig = plt.figure(figsize=(2,4), dpi=180)
    ax = fig.gca()
    img =  np.zeros((1024,32))
    image = plt.imshow(img, cmap='gray',interpolation='hanning',animated=False,extent=[0,31* 0.3,1024*1.498*0.5*(1/20),0], aspect=1)

    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    # canvas.mpl_connect("key_press_event", on_key_press)


    prompt = 'fps'
    label = tkinter.Label(master= root, text=prompt, width=len(prompt))
    label.pack(side=tkinter.TOP)

    button_M_stop =tkinter.Button(master=root, text="Record M-mode", command=lambda:_Mtoggle(m_q_enabler))
    button_quit = tkinter.Button(master=root, text="Quit", command=lambda: _quitAll(BModeInstance,MModeInstance,root))
    button_stop =tkinter.Button(master=root, text="Stop", command=lambda:_toggle(q_enabler))
    button_Mode = tkinter.Button(master=root, text="Mode", command=_mode)
    button_Save = tkinter.Button(master=root, text="Save", command=_save)

    button_quit.pack(side=tkinter.LEFT)
    button_stop.pack(side=tkinter.LEFT)
    button_Mode.pack(side=tkinter.LEFT)
    button_Save.pack(side=tkinter.LEFT)
    button_M_stop.pack(side=tkinter.RIGHT)

  

    updateplot(q,   q_fps)
    M_updateplot(m_q, m_q_fps)
    root.mainloop()

# def on_key_press(event):
#     print("you pressed {}".format(event.key))
#     key_press_handler(event, canvas, toolbar)


def _quitAll(process,M_process, top):
    global quitter
    quitter = True
    process.terminate()
    M_process.terminate()
    top.quit()
    top.destroy()

def _mode():
    settings.modeVar = not settings.modeVar
    # plt.close()

    # plt.figure(1)
    # Image = plt.imshow(DataToPlot,cmap='gray',interpolation='nearest', aspect='auto',animated=False)
    
    # Image.set_clim(vmin=0, vmax=200)
    # # plt.show(block=False)

    # # plt.close()
    # plt.figure(2)
    # Image = plt.imshow(DataToPlot,cmap='gray',interpolation='nearest', aspect='auto',animated=False)
    
    # Image.set_clim(vmin=0, vmax=1)
    # # plt.show(block=False)

    # plt.show()



def _save():
    
    # ax.axis('off')
    file =  'B_' + str(time.ctime()).replace(" ", "_").replace(":", "")
    Current_Array = DataToPlot
    fig.savefig('Images/' + file + '.png' ,bbox_inches='tight', pad_inches = 0,dpi = 500)
    ax.axis('on')

    np.save('Arrays/' + file,Current_Array)
    
    

def _toggle(q_enabler):

    settings.stopper = not settings.stopper
    q_enabler.put(settings.stopper)
    button_stop.config(text= 'Stop' if settings.stopper else 'Start')



def _Mtoggle(m_q_enabler):
    # global settings.Mstopper
    # settings.Mstopper = not settings.Mstopper
    
    m_q_enabler.put(True)
    # print(settings.Mstopper)
    # button_M_stop.config(text= 'Stop' if settings.Mstopper else 'Start')


def updateplot(q,q_fps):
    global DataToPlot, maxScale

    try:       
        
        result=q.get_nowait()
    
        result_log = np.log10(result)  # Chaning log is add a sacling factor!
        DataToPlot =  result if settings.modeVar else result_log
        # DataToPlot =  result 
        # maxScale =  var.get()/100 * 4096 if settings.modeVar else var.get()/100 * DataToPlot.max()
        maxScale =  var.get()/100 * DataToPlot.max()
        
        image.set_data(DataToPlot)
        # print(maxScale)
        image.set_clim(vmin=0, vmax=maxScale)
        # DataToPlot.min()

        canvas.draw()
        text = q_fps.get_nowait()
        label.config(text=text, width=len(text))
        root.after(1,updateplot,q,q_fps)
    
    except:
     
        root.after(1,updateplot,q,q_fps)

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
    # print(Mimage.shape)
    # print(len(boy))

   
    plt.close()
    plt.figure()
    
    Image = plt.imshow(Mimage,cmap='gray',interpolation='nearest', extent=[0,timestampArr[-1] - timestampArr[0] , 1024*1.498*0.5*(1/20),0], aspect='auto',animated=False)
    
    Image.set_clim(vmin=0, vmax=maxScale)  # Has to be passed from inside the other process

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
    
  

    plt.show()

    return

  
