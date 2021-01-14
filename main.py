from REVO.Rserial import RSerial
from REVO.AppView import plot, M_mode_plot
import settings

import multiprocessing
import time


def BModeTask(port,q,q_enabler,q_fps):
    ser = RSerial(port,8*1000000,2048*32,32)
    enabler = True
    t1 = time.perf_counter()
    while True:
        if not q_enabler.empty():
            enabler = q_enabler.get_nowait()

        if  enabler== True:
            try:
                t0 = t1
                data2 = ser.fetch()
                q.put(data2)
                t1 = time.perf_counter()
                text = 'fps: ' + "{:.2f}".format(1/(t1-t0)) + ' Hz'
                q_fps.put(text)
            except ValueError as err:
                print('Caught this error: ' + repr(err))
            


def MModeTask(port,m_q,m_q_enabler):
    ser = RSerial(port,8*1000000,2048*2,2)  # 16 bits mode
    # ser = RSerial('COM4',8*1000000,2048*1,2)   # 8 bits mode
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
            try:
                t0 = t1
                data2 = ser.fetch() # 16 bits mode
                # data2 = ser.fetch8()  # 8 bits mode
                agg.append(data2)
                counter=counter+1

                t1 = time.perf_counter()
                fps = 1/(t1-t0)
                fpsArr.append(fps)  
                timestampArr.append(t1)

                if counter == 1:
                    print('started M_mode capture at ' + time.ctime())

                if counter == 1000:
                    print("Processing M_mode Image: "+time.ctime())
                    enabler = False
                    M_mode_plot(agg,fpsArr[1:],timestampArr)
                    counter = 0
                    agg = []
                    fpsArr = []
                    timestampArr = []

            except ValueError as err:
                print('Caught this error: ' + repr(err))
                # print(counter)
            
                  


if __name__ == '__main__':

    settings.init()

    q = multiprocessing.Queue()
    q_enabler = multiprocessing.Queue()
    q_fps = multiprocessing.Queue()

    m_q = multiprocessing.Queue()
    m_q_enabler = multiprocessing.Queue()
   
    BModeInstance=multiprocessing.Process(None,BModeTask,args=(settings.BModePort,q,q_enabler,q_fps))
    MModeInstance=multiprocessing.Process(None,MModeTask,args=(settings.MModePort,m_q,m_q_enabler))

    BModeInstance.start()
    MModeInstance.start()
   
    plot(q,q_fps,q_enabler,m_q_enabler,BModeInstance,MModeInstance)
    
    BModeInstance.join()
    MModeInstance.join()
    print('Window closed')