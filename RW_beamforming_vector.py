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
        self.step_z = 600
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



        e = np.arange(0,32)
        ee = np.repeat([e],self.step_z,axis=0)
        eee = np.repeat([ee],self.step_x,axis=0)
        eeeP = eee*self.Pitch

        self.eee = eee
        self.eeeP = eeeP


        k = np.arange(0,self.step_z)
        kk = np.repeat([k],32,axis=0).T
        kkk = np.repeat([kk],self.step_x,axis=0)
        kkkZ = kkk*self.res_mm_z

        self.kkk = kkk
        self.kkkZ = kkkZ

        i = np.arange(0,self.step_x)
        ii = np.repeat([i],self.step_z,axis=0)
        print(ii.shape)
        iii = np.repeat([ii],32,axis=0).T
        print(iii.shape)
        iiiX = iii*self.res_mm_x

        self.iii =iii
        self.iiiX = iiiX

        self.eeeF = eee.flatten()

    def t_to_index(self,t):
        return t*self.sampling_rate
        # return t*self.sampling_rate # Poor method.. need to interpolate later on

    # def delay_t(self,z,x,xi,theta):
    #     d_t = x * math.sin(math.radians(theta)) + z * math.cos(math.radians(theta))
    #     # d_t = z
    #     d_r = ( z**2 + (x-xi)**2  )**0.5
    #     t = (d_t + d_r )/self.C
    #     return t

    def delay_t(self,z,x,xi,theta):
        # z is 1000x1. x is 1x32
        d_t = x * math.sin(math.radians(theta)) + z * math.cos(math.radians(theta))
        # d_t = z
        d_r = ( z**2 + (x-xi)**2  )**0.5
        t = (d_t + d_r )/self.C
        return t

    def interpol(self,x1,x2,mod):
        return (mod * (x2 - x1)) + x1
    
    # def Dyn_R(self,X,theta ):
    #     Xf = interp1d(range(0,X.shape[0]), X.T, kind='linear',fill_value = "extrapolate")
    #     Y =  np.ones((self.step_z,self.step_x))
    #     print(X.shape, Y.shape)
    #     for i in range(0, self.step_x):
    #         # print(i, i*self.res_mm_x)
    #         # print("*********************************************")
    #         for k in range(0, self.step_z):
    #             # print( "\t" + str(k) + " " + str(k*self.res_mm_z))
    #             a = k*self.res_mm_z/(2*self.F_num)
    #             start = max(0,math.floor((i*self.res_mm_x - a)/self.Pitch))
    #             end =  min(31, math.ceil((i*self.res_mm_x + a)/self.Pitch)+1)
    #             ee = np.arange(start, end) 

    #             Dd_t = self.delay_t(k*self.res_mm_z, i*self.res_mm_x , ee*self.Pitch, theta)
    #             Dindex = self.t_to_index(Dd_t)  # Check if index is valid

    #             # Dindex_rounded = np.around(Dindex).astype(int)
    #             Dindex_rounded = Dindex.astype(int)
    #             indexes = (Dindex_rounded,ee)

    #             Y[k,i] +=  np.sum(X[indexes])  # Check if within F_nu
          
    #     return Y

    # def Dyn_R(self,X,theta ):
    #     Y =  np.zeros((self.step_z,self.step_x))
    #     print(X.shape, Y.shape)
    #     k = self.kk*self.res_mm_z
    #     eeP =  self.ee*self.Pitch
    #     for i in range(0, self.step_x):
    #         Dd_t = self.delay_t(k, i*self.res_mm_x ,eeP, theta) 
    #         Dindex = self.t_to_index(Dd_t)  # Check if index is vali

    #         Dindex_rounded = np.int32(Dindex+0.5)
    #         # Dindex_rounded = Dindex.astype(int)
    #         # Dindex_rounded = np.round(Dindex).astype(int)
    #         indexes = (Dindex_rounded,self.ee)  # 1000 depth with 32 delays index

    #         Y[:,i] = np.sum(X[indexes]*self.mask[i],axis=1) 
    #     return Y

    # def Dyn_R(self,X,theta ):
    #     # kkkZ = self.kkkZ
    #     # iiiX = self.iiiX
    #     # eeeP = self.eeeP
    #     # eee = self.eee
    #     Dd_t = self.delay_t(self.kkkZ, self.iiiX ,self.eeeP, theta)  #  must return 63,1000,32!
    #     Dindex = self.t_to_index(Dd_t)  # Check if index is vali
    #     # print(Dindex.shape,Dindex.flatten().shape,eee.flatten().shape)
    #     Dindex_rounded = np.int32(Dindex+0.5)
    #     indexes = (Dindex_rounded,self.eee)  # 1000 depth with 32 delays index
       
    #     Y = np.sum(X[indexes]*self.mask,axis=2).T  
    #     return Y


# ********************************************************************************** INTERPOLE

    # def Dyn_R(self,X,theta ):
    #     Xf = interp1d(range(0,X.shape[0]), X.T, kind='linear',fill_value = "extrapolate")
    #     Y =  np.ones((self.step_z,self.step_x))
    #     print(X.shape, Y.shape)
    #     for i in range(0, self.step_x):
    #         # print(i, i*self.res_mm_x)
    #         # print("*********************************************")
    #         for k in range(0, self.step_z):
    #             # print( "\t" + str(k) + " " + str(k*self.res_mm_z))
    #             a = k*self.res_mm_z/(2*self.F_num)
    #             start = max(0,math.floor((i*self.res_mm_x - a)/self.Pitch))
    #             end =  min(31, math.ceil((i*self.res_mm_x + a)/self.Pitch)+1)
    #             ee = np.arange(start, end) 

    #             Dd_t = self.delay_t(k*self.res_mm_z, i*self.res_mm_x , ee*self.Pitch, theta)
    #             Dindex =self.t_to_index(Dd_t) # Check if index is valid

    #             filter_data = np.diag(Xf(Dindex)[start:end])
        
    #             Y[k,i] +=  np.sum(filter_data)  # Check if within F_nu
    #     return Y

    # def Dyn_R(self,X,theta ):
    #     Xf = interp1d(range(0,X.shape[0]), X.T, kind='linear',fill_value = "extrapolate")
        
    #     Y =  np.zeros((self.step_z,self.step_x))
    #     print(X.shape, Y.shape)
    #     k = self.kk*self.res_mm_z
    #     eeP =  self.ee*self.Pitch

    #     for i in range(0, self.step_x):
    #         Dd_t = self.delay_t(k, i*self.res_mm_x ,eeP, theta) 
    #         Dindex = self.t_to_index(Dd_t)  # Check if index is vali

    #         diag_arr = np.diagonal(Xf(Dindex),  axis1 = 0,  axis2 = 2)
        
   
    #         Y[:,i] = np.sum(diag_arr*self.mask[i],axis=1)        
    #     return Y

    def Dyn_R(self,X,theta ):
        Y =  np.zeros((self.step_z,self.step_x))
        print(X.shape, Y.shape)
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


    # def Dyn_R(self,X,theta ):
      
    #     # print(X.shape, Y.shape)
    

    #     arr = np.zeros((1000,32))

    #     x = np.arange(0, 1024)
    #     y = np.arange(0, 32)
    #     points = (x,y)
    #     values = X

    #     kkkZ = self.kkkZ
    #     iiiX = self.iiiX
    #     eeeP = self.eeeP
    #     eee = self.eee
    #     eeeF = self.eeeF

        
    #     # Fix these three lines!
    #     Dd_t = self.delay_t(kkkZ, iiiX ,eeeP, theta)  #  must return 63,1000,32!
    #     Dindex = self.t_to_index(Dd_t)  # Check if index is vali
    #     # print(Dindex.shape,Dindex.flatten().shape,eee.flatten().shape)
    #     point = (Dindex.flatten(),eeeF)
        
    #     t0 = time.perf_counter()
    #     arr = interpn(points, values, point,method='linear',fill_value=0,bounds_error=False).reshape(63,1000,32)
    #     t1 = time.perf_counter()
    #     print('Inte time: ' + "{:.2f}".format(t1-t0))
            
    #     Y = np.sum(arr*self.mask,axis=2).T   
    #     # print(Y.shape)  
    #     return Y

# ******************************************************************************************************************************************************************
# Engine = PW_BF(sampling_rate = 20 ,Pitch = 0.3, C= 1.54, F_num= 1.75)

# XX = np.load('./UserSessions/test2/RFArrays/B_80,0_10,0.npy')
# XX = XX-np.mean(XX,axis=0)

# YY = Engine.Dyn_R(XX,10)

# XX_en = np.abs(hilbert(XX))
# YY_en = np.abs(hilbert(YY))

# plt.figure()
# plt.subplot(121)
# Image = plt.imshow(XX_en,cmap='gray',interpolation='None',extent=[0,31* 0.3,XX_en.shape[0] *1.540*0.5*(1/20),0], animated=False,  aspect=1)
# plt.subplot(122)
# Image = plt.imshow(YY_en,cmap='gray',interpolation='None',extent=[0,31* 0.3,YY_en.shape[0] * Engine.res_mm_z,0],animated=False, aspect=1)
# plt.figure()
# plt.subplot(121)
# Image = plt.imshow(20*np.log10(XX_en),cmap='gray',interpolation='None',extent=[0,31* 0.3,XX_en.shape[0] *1.540*0.5*(1/20),0], animated=False,  aspect=1)
# # Image.set_clim(vmin=10, vmax=60)
# plt.subplot(122)
# Image = plt.imshow(20*np.log10(YY_en),cmap='gray',interpolation='None',extent=[0,31* 0.3,YY_en.shape[0] * Engine.res_mm_z,0],animated=False, aspect=1)
# # Image.set_clim(vmin=37, vmax=62)
# plt.show()

# ******************************************************************************************************************************************************************


# Z = 20*np.log10(YY_en)
# s= np.std(Z.flatten())
# m = np.mean(Z.flatten())
# r = 2
# r1 = m+ r*s 
# r2 = m- r*s 
# print(m,s, r2 , r1)


# z = 0.1
# Engine = PW_BF(20 ,0.3,1.54,1)
# time_delay = Engine.delay_t(z ,0 ,0, 0)
# index = Engine.t_to_index(time_delay)
# print(index)
# print(Engine.interpol(0,10,0.3))
# # With unfocusing
# index_u = 2*20/1.54 * z
# print(index_u)

# ******************************************************************************************************************************************************************

from os import listdir
from os.path import isfile, join

Path = './UserSessions/tube_short/RFArrays/'
# Path = './RFArrays/'
files = listdir(Path)

Engine = PW_BF(sampling_rate = 20 ,Pitch = 0.3, C= 1.54, F_num= 2)
Y_FULL =  np.zeros((Engine.step_z,Engine.step_x))


# for i in range(0, len(files)):
#     print(i)
t0 = time.perf_counter()

# angles = range(-1,2)

# angles = range(-10,11)
angles = np.arange(-5,6,0.5)

for file in files:
    tt0 = time.perf_counter()
    fileName = str(file).replace(".npy","")
    print()
    if fileName[1] == 'F':
        pass
    else:
        fileNameParts = fileName.replace(",", ".").split("_")
        angle = float(fileNameParts[2])

        

        if angle in angles:
            print("filename: " + fileName, "Angle : " , angle)
            X = np.load(Path +file )
            # print(XX.shape)
            X = X-np.mean(X[0:1000,:],axis=0)

            Y = Engine.Dyn_R(X,angle)

            Y_FULL = Y_FULL + Y
            # print(Y_FULL.shape)

            if angle == 0.0:
                YY = Y
                XX = X[0: round(  Engine.step_z*Engine.res_mm_z/(1.540*0.5*(1/20)) )+1,:]
            tt1 = time.perf_counter()
            print('file time: ' + "{:.2f}".format(tt1-tt0))

t1 = time.perf_counter()
print('total time: ' + "{:.2f}".format(t1-t0))

XX_en = np.abs(hilbert(XX))
YY_en = np.abs(hilbert(YY))
Y_FULL_en = np.abs(hilbert(Y_FULL))

plt.figure()
plt.subplot(131)
Image = plt.imshow(XX_en,cmap='gray',interpolation='None',extent=[0,31* 0.3,XX_en.shape[0] *1.540*0.5*(1/20),0], animated=False,  aspect=1)
plt.subplot(132)
Image = plt.imshow(YY_en,cmap='gray',interpolation='None',extent=[0,31* 0.3,YY_en.shape[0] * Engine.res_mm_z,0],animated=False, aspect=1)
plt.subplot(133)
Image = plt.imshow(Y_FULL_en,cmap='gray',interpolation='None',extent=[0,31* 0.3,YY_en.shape[0] * Engine.res_mm_z,0],animated=False, aspect=1)

plt.figure()
plt.subplot(131)
Image = plt.imshow(20*np.log10(XX_en),cmap='gray',interpolation='None',extent=[0,31* 0.3,XX_en.shape[0] *1.540*0.5*(1/20),0], animated=False,  aspect=1)
# Image.set_clim(vmin=10, vmax=60)
plt.subplot(132)
Image = plt.imshow(20*np.log10(YY_en),cmap='gray',interpolation='None',extent=[0,31* 0.3,YY_en.shape[0] * Engine.res_mm_z,0],animated=False, aspect=1)
# Image.set_clim(vmin=37, vmax=62)
plt.subplot(133)
Image = plt.imshow(20*np.log10(Y_FULL_en),cmap='gray',interpolation='None',extent=[0,31* 0.3,YY_en.shape[0] * Engine.res_mm_z,0],animated=False, aspect=1)
# Image.set_clim(vmin=37, vmax=62)

plt.show()


np.save(Path +'BF_0' ,YY)
np.save(Path +'BF' ,Y_FULL)