import numpy as np
import os
print(os.path.abspath("."))
import matplotlib.pyplot as plt
from scipy.signal import hilbert, chirp
import math
from scipy.interpolate import interp1d, interp2d, interpn
import time

class PW_BF():
    def __init__(self, sampling_rate, Pitch, C, F_num):
        self.sampling_rate = sampling_rate
        self.Pitch = Pitch
        self.C = C
        self.F_num = F_num
        self.step_x = 63
        self.step_z = 760
        self.res_mm_x = Pitch/2
        self.res_mm_z = 0.05

        self.postion = np.arange(0, 32) 
        self.zeros = np.zeros(32)


        mask = np.zeros((self.step_x,self.step_z,32))
        for i in range(0,self.step_x):
            kk = np.arange(0, self.step_z)
            a = kk*self.res_mm_z/(2*self.F_num)
            start = (np.floor((i*self.res_mm_x - a)/self.Pitch)).astype(int)
            end =  (np.ceil((i*self.res_mm_x + a)/self.Pitch)+1).astype(int)
            start[ start< 0] = 0
            end[ end > 31] = 31
            for jj in range(0,self.step_z):
                mask[i, jj, start[jj]:end[jj] ] = 1
        self.mask = mask

        self.kk = np.repeat([kk],32, axis=0).T
        self.ee  = np.repeat([self.postion], self.step_z, axis=0)


    def t_to_index(self,t):
        return t*self.sampling_rate
        # return t*self.sampling_rate # Poor method.. need to interpolate later on


    def delay_t(self,z,x,xi,theta):
        # z is 1000x1. x is 1x32
        d_t = x * math.sin(math.radians(theta)) + z * math.cos(math.radians(theta))
        # d_t = z
        d_r = ( z**2 + (x-xi)**2  )**0.5
        t = (d_t + d_r )/self.C
        return t

    def interpol(self,x1,x2,mod):
        return (mod * (x2 - x1)) + x1
    

    def Dyn_R(self,X,theta ):
        Y =  np.zeros((self.step_z,self.step_x))
        # print(X.shape, Y.shape)
        k = self.kk*self.res_mm_z
        eeP =  self.ee*self.Pitch
        for i in range(0, self.step_x):
            Dd_t = self.delay_t(k, i*self.res_mm_x ,eeP, theta) 
            Dindex = self.t_to_index(Dd_t)  # Check if index is vali

            Dindex_rounded = np.intc(Dindex+0.5)
            # Dindex_rounded = Dindex.astype(int)
            # Dindex_rounded = np.round(Dindex).astype(int)
            indexes = (Dindex_rounded,self.ee)  # 1000 depth with 32 delays index

            Y[:,i] = np.sum(X[indexes]*self.mask[i],axis=1) 
        return Y

    def Dyn_R_int(self,X,theta ):
        Y =  np.zeros((self.step_z,self.step_x))
    
        k = self.kk*self.res_mm_z
        eeP =  self.ee*self.Pitch

  
        x = np.arange(0, 1024)
        y = np.arange(0, 32)
        points = (x,y)
        values = X
        EE = self.ee.flatten()

        for i in range(0, self.step_x):
            Dd_t = self.delay_t(k, i*self.res_mm_x ,eeP, theta) 
            Dindex = self.t_to_index(Dd_t)  # Check if index is vali

            point = (Dindex.flatten(),EE)
          
            arr = interpn(points, values, point,method='linear',fill_value=0,bounds_error=False).reshape(self.step_z,32)
            
            Y[:,i] = np.sum(arr*self.mask[i],axis=1)        
        return Y

# Engine = PW_BF(sampling_rate = 20 ,Pitch = 0.3, C= 1.54, F_num= 1.75)

# Y = Engine.Dyn_R(X,angle)