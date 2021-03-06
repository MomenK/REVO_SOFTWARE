from REVO.Rserial import RSerial
from REVO.Rusbfifo import RUSBfifo
from REVO.AppView import plot
import settings
import multiprocessing
import time
import numpy as np

def BModeTask(port,bDateQ,bCntlQ,bEnQ,bFbQ):
    ser = RSerial(port,8*1000000,2048*32,32)
    enabler = True  
    # local_gain = 0
    # local_angle = 0
    t1 = time.perf_counter()
    ser.set_HPF()
    
    ser.write_angle(0)
   
    while True:
        # print("Writing FOCUS")
        if not bCntlQ.empty():
            bCntlD = bCntlQ.get_nowait()
            # enabler = bCntlD[0]
            gain = bCntlD[0]
            num_cycle = bCntlD[1]
            # if gain != local_gain: #write the gain value
            # local_gain = gain
            gain_hex = ser.write_gain(int(gain))
            print(gain, gain_hex)
            
            
            # if angle != local_angle:
            # local_angle = angle
            
            if isinstance(num_cycle,  (list, tuple, np.ndarray)):
                print("Writing FOCUS")
                print(num_cycle + 500)
                ser.write_focus_depth(num_cycle)
            else:
                print("Writing ANGLE")
                ser.write_angle(num_cycle)


            bFbQ.put([gain,num_cycle])

        if not bEnQ.empty():
            enabler = bEnQ.get_nowait()

        if  enabler:
            try:
                t0 = t1
                data2 = ser.fetch()
                t1 = time.perf_counter()
                text = 'fps: ' + "{:.2f}".format(1/(t1-t0)) + ' Hz'
                bDateQ.put([data2, text])
            except ValueError as err:
                print('Caught this error: ' + repr(err))
                

def MModeTask(port,m_q,m_q_enabler,m_q_fps):
    # ser = RSerial(port,8*1000000,2048*2,2)  # 16 bits mode
    # ser = RSerial('COM4',8*1000000,2048*1,2)   # 8 bits mode
    ser = RUSBfifo(2048*2,2)  # 16 bits mode
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

                if counter == 6000:
                    print("Processing M_mode Image: "+time.ctime())
                    Q = [ agg, timestampArr ]
          
                    m_q.put(Q)
                    # time.sleep(1)
                    # m_q_fps.put(timestampArr)
                    enabler = False
                    # M_mode_plot(agg,fpsArr[1:],timestampArr)
                    counter = 0
                    agg = []
                    fpsArr = []
                    timestampArr = []

            except ValueError as err:
                print('Caught this error: ' + repr(err))
                # print(counter)
            
                  


if __name__ == '__main__':

    settings.init()

    bDateQ = multiprocessing.Queue() # Data from serial port client
    bCntlQ = multiprocessing.Queue() # Ctrl SPI from root client
    bEnQ = multiprocessing.Queue()   # Enable from root client
    bFbQ = multiprocessing.Queue()   # Feedback from serial port client

    m_q = multiprocessing.Queue()
    m_q_enabler = multiprocessing.Queue()
    m_q_fps = multiprocessing.Queue()
   
    BModeInstance=multiprocessing.Process(None,BModeTask,args=(settings.BModePort,bDateQ,bCntlQ,bEnQ,bFbQ))
    MModeInstance=multiprocessing.Process(None,MModeTask,args=(settings.MModePort,m_q,m_q_enabler,m_q_fps))

    BModeInstance.start()
    MModeInstance.start()
   
    plot(BModeInstance, bDateQ, bCntlQ , bEnQ, bFbQ ,m_q,m_q_fps,m_q_enabler,MModeInstance)
    
    BModeInstance.join()
    MModeInstance.join()
    print('Window closed')