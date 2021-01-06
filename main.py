from REVO.Rserial import RSerial
from REVO.AppView import plot, M_mode_plot

import multiprocessing
import time


def BModeTask(q,q_enabler,q_fps):
    ser = RSerial('COM5',8*1000000,2048*32,32)
    enabler = True
    t1 = time.perf_counter()
    while True:
        if not q_enabler.empty():
            enabler = q_enabler.get_nowait()

        if  enabler== True:
            t0 = t1
            data2 = ser.fetch()
            q.put(data2)
            t1 = time.perf_counter()
            text = 'fps: ' + "{:.2f}".format(1/(t1-t0)) + ' Hz'
            q_fps.put(text)
 


def MModeTask(m_q,m_q_enabler):
    # ser = RSerial('COM4',8*1000000,2048*2,2)  # 16 bits mode
    ser = RSerial('COM6',8*1000000,2048*1,2)   # 8 bits mode
    enabler = False
    counter = 0
    agg = []
    fpsArr = []
    timestampArr = []
    t1 = time.perf_counter()
    while True:
        if not m_q_enabler.empty():
            enabler = m_q_enabler.get_nowait()

        if  enabler== True:
            t0 = t1
            # data2 = ser.fetch() # 16 bits mode
            data2 = ser.fetch8()  # 8 bits mode
            agg.append(data2)
            counter=counter+1
            t1 = time.perf_counter()
            fps = 1/(t1-t0)
            fpsArr.append(fps)  
            timestampArr.append(t1)
            if counter == 1000:
                print("Processing M_mode Image: "+time.ctime())
                enabler = False
                M_mode_plot(agg,fpsArr[1:],timestampArr)
                counter = 0
                agg = []
                fpsArr = []
                timestampArr = []
            if counter == 1:
                print('started M_mode capture at ' + time.ctime())
                  


if __name__ == '__main__':


    
    q = multiprocessing.Queue()
    q_enabler = multiprocessing.Queue()
    q_fps = multiprocessing.Queue()

    m_q = multiprocessing.Queue()
    m_q_enabler = multiprocessing.Queue()
   
    BModeInstance=multiprocessing.Process(None,BModeTask,args=(q,q_enabler,q_fps))
    MModeInstance=multiprocessing.Process(None,MModeTask,args=(m_q,m_q_enabler))

    BModeInstance.start()
    MModeInstance.start()
   
    plot(q,q_fps,q_enabler,m_q_enabler,BModeInstance,MModeInstance)
    
    BModeInstance.join()
    MModeInstance.join()
    print('Window closed')