import numpy as np
import os
print(os.path.abspath("."))
import matplotlib.pyplot as plt
from scipy.signal import hilbert, chirp
import math, time
from scipy.interpolate import interp1d, interp2d

class PW_BF():
    def __init__(self, sampling_rate, Pitch, C, F_num):
        self.sampling_rate = sampling_rate
        self.Pitch = Pitch
        self.C = C
        self.F_num = F_num
        self.step_x = 63
        self.step_z = 1000
        self.res_mm_x = Pitch/2
        self.res_mm_z = 0.01

    def t_to_index(self,t):
        index = t*self.sampling_rate
        # if index < 0:
        #     print(index)
        #     print(round(index, 2))
        return index
        # return t*self.sampling_rate # Poor method.. need to interpolate later on

    def delay_t(self,z,x,xi,theta):
        d_t = x * math.sin(math.radians(theta)) + z * math.cos(math.radians(theta))
        # d_t = z
        d_r = ( z**2 + (x-xi)**2  )**0.5
        t = (d_t + d_r )/self.C
        return t

    def interpol(self,x1,x2,mod):
        return (mod * (x2 - x1)) + x1
    
    def Dyn_R(self,X,theta ):
        # XF = interp2d(range(0,X.shape[0]), range(0,X.shape[1]), X.T, kind='linear')
        Y =  np.ones((self.step_z,self.step_x))
        print(X.shape, Y.shape)
        for i in range(0, self.step_x):
            # print(i, i*self.res_mm_x)
            # print("*********************************************")
            for k in range(0, self.step_z):
                # print( "\t" + str(k) + " " + str(k*self.res_mm_z))
                a = k*self.res_mm_z/(2*self.F_num)

                for e in range(0, 32):
                    # print( "\t\t" + str(e) + " " + str(e*self.Pitch))
                    Dd_t = self.delay_t(k*self.res_mm_z, i*self.res_mm_x , e*self.Pitch, theta)
                    Dindex = self.t_to_index(Dd_t)  # Check if index is valid
                    # print("Index: "+ str(Dindex))
                    
                    if e*self.Pitch > i*self.res_mm_x - a and e*self.Pitch < i*self.res_mm_x + a :
                    # if Dindex < X.shape[0] and e*self.Pitch > i*self.res_mm_x - a and e*self.Pitch < i*self.res_mm_x + a :

                        Y[k,i] = Y[k,i] + X[round(Dindex),e]  # Check if within F_nu

                        # Y[k,i] = Y[k,i] + self.interpol( X[math.floor(Dindex),e] , X[math.ceil(Dindex),e] , Dindex - math.floor(Dindex)  )  # Check if within F_num

                        # f = interp1d(range(0,X.shape[0]), X[:,e], kind='linear')
                        # Y[k,i] = Y[k,i] + f(Dindex)  # Check if within F_num

                        # Y[k,i] = Y[k,i] + XF(round(Dindex, 2),e)  # Check if within F_num            
        return Y

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

Path = './UserSessions/test2/RFArrays/'
files = listdir(Path)

Engine = PW_BF(sampling_rate = 20 ,Pitch = 0.3, C= 1.54, F_num= 1.75)
Y_FULL =  np.zeros((Engine.step_z,Engine.step_x))


# for i in range(0, len(files)):
#     print(i)
t0 = time.perf_counter()

for file in files:
    tt0 = time.perf_counter()
    fileName = str(file).replace(".npy","")
    if fileName[1] == 'F':
        pass
    else:
        fileNameParts = fileName.replace(",", ".").split("_")
        angle = float(fileNameParts[2])

        print("filename: " + fileName, "Angle : " , angle)

        X = np.load(Path +file )
        # print(XX.shape)
        X = X-np.mean(X,axis=0)

        Y = Engine.Dyn_R(X,angle)

        Y_FULL = Y_FULL + Y
        print(Y_FULL.shape)

        if angle == 0.0:
            YY = Y
            XX = X[0: round(  Engine.step_z*Engine.res_mm_z/(1.540*0.5*(1/20)) ),:]
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