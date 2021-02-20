# TOLERANCE = 0
# p = float(10**TOLERANCE)
# def my_round_5(some_float):
#     return int(some_float  + 0.5)

# print(my_round_5(1.4))

import numpy as np
from scipy.interpolate import interp1d, interp2d

z = np.arange(0,50).reshape(10,5).T

print(z)

x = np.arange(0,5)
y = np.arange(0,10)

print(x)

f = interp2d(x,y,z.T)

y_hat = f([0],[1,2])

print(y_hat)





# import numpy as np

# z = np.arange(0,1000)
# print(z.shape)

# x = np.arange(0,32)
# print(x.shape)


# xi = 5


# # Need to generate delays.. 1000 X 32 delays = z + (xi+x)
# zz = np.repeat([z],32, axis=0).T
# print(zz.shape)


# xx = np.repeat([x],1000, axis=0)
# print(xx.shape)


# import numpy as np
# import os
# print(os.path.abspath("."))
# import matplotlib.pyplot as plt
# from scipy.signal import hilbert, chirp
# import math
# from scipy.interpolate import interp1d, interp2d
# import time

# class PW_BF():
#     def __init__(self, sampling_rate, Pitch, C, F_num):
#         self.sampling_rate = sampling_rate
#         self.Pitch = Pitch
#         self.C = C
#         self.F_num = F_num
#         self.step_x = 63
#         self.step_z = 1000
#         self.res_mm_x = Pitch/2
#         self.res_mm_z = 0.02

#         self.postion = np.arange(0, 32) 
#         self.zeros = np.zeros(32)


#         mask = np.zeros((63,1000,32))
#         for i in range(0,63):
#             kk = np.arange(0, self.step_z)
#             a = kk*self.res_mm_z/(2*self.F_num)
#             start = (np.floor((i*self.res_mm_x - a)/self.Pitch)).astype(int)
#             end =  (np.ceil((i*self.res_mm_x + a)/self.Pitch)+1).astype(int)
#             start[ start< 0] = 0
#             end[ end > 31] = 31
#             for jj in range(0,1000):
#                 mask[i, jj, start[jj]:end[jj] ] = 1
#         self.mask = mask

#     def t_to_index(self,t):
#         return t*self.sampling_rate
#         # return t*self.sampling_rate # Poor method.. need to interpolate later on

#     def delay_t(self,z,x,xi,theta):
#         d_t = x * math.sin(math.radians(theta)) + z * math.cos(math.radians(theta))
#         # d_t = z
#         d_r = ( z**2 + (x-xi)**2  )**0.5
#         t = (d_t + d_r )/self.C
#         return t

#     def interpol(self,x1,x2,mod):
#         return (mod * (x2 - x1)) + x1
    
#     # def Dyn_R(self,X,theta ):
#     #     Xf = interp1d(range(0,X.shape[0]), X.T, kind='linear',fill_value = "extrapolate")
#     #     Y =  np.ones((self.step_z,self.step_x))
#     #     print(X.shape, Y.shape)
#     #     for i in range(0, self.step_x):
#     #         # print(i, i*self.res_mm_x)
#     #         # print("*********************************************")
#     #         for k in range(0, self.step_z):
#     #             # print( "\t" + str(k) + " " + str(k*self.res_mm_z))
#     #             a = k*self.res_mm_z/(2*self.F_num)
#     #             start = max(0,math.floor((i*self.res_mm_x - a)/self.Pitch))
#     #             end =  min(31, math.ceil((i*self.res_mm_x + a)/self.Pitch)+1)
#     #             ee = np.arange(start, end) 

#     #             Dd_t = self.delay_t(k*self.res_mm_z, i*self.res_mm_x , ee*self.Pitch, theta)
#     #             Dindex = self.t_to_index(Dd_t)  # Check if index is valid

#     #             Dindex_rounded = np.around(Dindex).astype(int)
#     #             indexes = (Dindex_rounded,ee)

#     #             Y[k,i] +=  np.sum(X[indexes])  # Check if within F_nu
          
#     #     return Y

#     def Dyn_R(self,X,theta ):
#         Xf = interp1d(range(0,X.shape[0]), X.T, kind='linear',fill_value = "extrapolate")
#         Y =  np.zeros((self.step_z,self.step_x))
#         # print(X.shape, Y.shape)
#         for i in range(0, self.step_x):
#             # print(i, i*self.res_mm_x)
#             # print("*********************************************")
#             # for k in range(0, self.step_z):
#                 # print( "\t" + str(k) + " " + str(k*self.res_mm_z))
#             kk = np.arange(0, self.step_z)
#             k = np.repeat([kk],32, axis=0).T
#             # a = kk*self.res_mm_z/(2*self.F_num)

#             # ee = np.arange(0, 32) 

#             ee =  np.repeat([self.postion], self.step_z, axis=0)
#             # print(ee.shape)
#             #  Should take in 1000x1 and 32x1 and give you 1000x32
#             Dd_t = self.delay_t(k*self.res_mm_z, i*self.res_mm_x ,ee*self.Pitch, theta) 
#             Dindex = self.t_to_index(Dd_t)  # Check if index is valid

#             # U do not need to repeat! There must be a better code!!!!!!!!!!!!!!!!!!!!

#             # print(Dindex.shape)

#             Dindex_rounded = np.around(Dindex).astype(int)
#             # print(Dindex_rounded.shape)

#             # mask = np.zeros((1000,32))
#             # start = (np.floor((i*self.res_mm_x - a)/self.Pitch)).astype(int)
#             # end =  (np.ceil((i*self.res_mm_x + a)/self.Pitch)+1).astype(int)
#             # start[ start< 0] = 0
#             # end[ end > 31] = 31

#             # for jj in range(0,1000):
#             #     mask[jj, start[jj]:end[jj] ] = 1
            
#             # mask[(indexies)] = 1
#             # jj = 0
#             # for (row, row_start, row_end) in zip( mask, start, end):
                
#             #     # row[start[jj]:end[jj]] = 1
#             #     row[row_start:row_end] = 1
#             #     # jj = jj +1

    
#             indexes = (Dindex_rounded,ee)
     
            
#             Y[:,i] = np.sum(X[indexes]*self.mask[i],axis=1)         
#         return Y




#     # def Dyn_R(self,X,theta ):
#     #     Xf = interp1d(range(0,X.shape[0]), X.T, kind='linear',fill_value = "extrapolate")
#     #     Y =  np.ones((self.step_z,self.step_x))
#     #     print(X.shape, Y.shape)
#     #     for i in range(0, self.step_x):
#     #         # print(i, i*self.res_mm_x)
#     #         # print("*********************************************")
#     #         for k in range(0, self.step_z):
#     #             # print( "\t" + str(k) + " " + str(k*self.res_mm_z))
#     #             a = k*self.res_mm_z/(2*self.F_num)
#     #             start = max(0,math.floor((i*self.res_mm_x - a)/self.Pitch))
#     #             end =  min(31, math.ceil((i*self.res_mm_x + a)/self.Pitch)+1)
#     #             ee = np.arange(start, end) 

#     #             Dd_t = self.delay_t(k*self.res_mm_z, i*self.res_mm_x , ee*self.Pitch, theta)
#     #             Dindex =self.t_to_index(Dd_t) # Check if index is valid

#     #             filter_data = np.diag(Xf(Dindex)[start:end])
        
#     #             Y[k,i] +=  np.sum(filter_data)  # Check if within F_nu
#     #     return Y
    
#     # def Dyn_R(self,X,theta ):
#     #     Xf = interp1d(range(0,X.shape[0]), X.T, kind='linear',fill_value = "extrapolate")
#     #     Y =  np.ones((self.step_z,self.step_x))
#     #     print(X.shape, Y.shape)
#     #     for i in range(0, self.step_x):
#     #         # print(i, i*self.res_mm_x)
#     #         # print("*********************************************")
#     #         k = np.arange(0, self.step_z)
            
          
#     #         a = k*self.res_mm_z/(2*self.F_num)
#     #         start = max(0,math.floor((i*self.res_mm_x - a)/self.Pitch))
#     #         end =  min(31, math.ceil((i*self.res_mm_x + a)/self.Pitch)+1)

#     #             ee = np.arange(start, end) 

#     #             Dd_t = self.delay_t(k*self.res_mm_z, i*self.res_mm_x , ee*self.Pitch, theta)
#     #             Dindex =self.t_to_index(Dd_t) # Check if index is valid

#     #             filter_data = np.diag(Xf(Dindex)[start:end])
        
#     #             Y[k,i] +=  np.sum(filter_data)  # Check if within F_nu
#     #     return Y

# # ******************************************************************************************************************************************************************
# # Engine = PW_BF(sampling_rate = 20 ,Pitch = 0.3, C= 1.54, F_num= 1.75)

# # XX = np.load('./UserSessions/test2/RFArrays/B_80,0_10,0.npy')
# # XX = XX-np.mean(XX,axis=0)

# # YY = Engine.Dyn_R(XX,10)

# # XX_en = np.abs(hilbert(XX))
# # YY_en = np.abs(hilbert(YY))

# # plt.figure()
# # plt.subplot(121)
# # Image = plt.imshow(XX_en,cmap='gray',interpolation='None',extent=[0,31* 0.3,XX_en.shape[0] *1.540*0.5*(1/20),0], animated=False,  aspect=1)
# # plt.subplot(122)
# # Image = plt.imshow(YY_en,cmap='gray',interpolation='None',extent=[0,31* 0.3,YY_en.shape[0] * Engine.res_mm_z,0],animated=False, aspect=1)
# # plt.figure()
# # plt.subplot(121)
# # Image = plt.imshow(20*np.log10(XX_en),cmap='gray',interpolation='None',extent=[0,31* 0.3,XX_en.shape[0] *1.540*0.5*(1/20),0], animated=False,  aspect=1)
# # # Image.set_clim(vmin=10, vmax=60)
# # plt.subplot(122)
# # Image = plt.imshow(20*np.log10(YY_en),cmap='gray',interpolation='None',extent=[0,31* 0.3,YY_en.shape[0] * Engine.res_mm_z,0],animated=False, aspect=1)
# # # Image.set_clim(vmin=37, vmax=62)
# # plt.show()

# # ******************************************************************************************************************************************************************


# # Z = 20*np.log10(YY_en)
# # s= np.std(Z.flatten())
# # m = np.mean(Z.flatten())
# # r = 2
# # r1 = m+ r*s 
# # r2 = m- r*s 
# # print(m,s, r2 , r1)


# # z = 0.1
# # Engine = PW_BF(20 ,0.3,1.54,1)
# # time_delay = Engine.delay_t(z ,0 ,0, 0)
# # index = Engine.t_to_index(time_delay)
# # print(index)
# # print(Engine.interpol(0,10,0.3))
# # # With unfocusing
# # index_u = 2*20/1.54 * z
# # print(index_u)

# # ******************************************************************************************************************************************************************

# from os import listdir
# from os.path import isfile, join

# Path = './UserSessions/test2/RFArrays/'
# # Path = './RFArrays/'
# files = listdir(Path)

# Engine = PW_BF(sampling_rate = 20 ,Pitch = 0.3, C= 1.54, F_num= 2)
# Y_FULL =  np.zeros((Engine.step_z,Engine.step_x))


# # for i in range(0, len(files)):
# #     print(i)
# t0 = time.perf_counter()

# # angles = [0]

# angles = range(-10,11)

# for file in files:
#     tt0 = time.perf_counter()
#     fileName = str(file).replace(".npy","")
#     fileNameParts = fileName.replace(",", ".").split("_")
#     angle = float(fileNameParts[2])

    

#     if angle in angles:
#         print("filename: " + fileName, "Angle : " , angle)
#         X = np.load(Path +file )
#         # print(XX.shape)
#         X = X-np.mean(X,axis=0)

#         Y = Engine.Dyn_R(X,angle)

#         Y_FULL = Y_FULL + Y
#         print(Y_FULL.shape)

#         if angle == 0.0:
#             YY = Y
#             XX = X[0: round(  Engine.step_z*Engine.res_mm_z/(1.540*0.5*(1/20)) )+1,:]
#         tt1 = time.perf_counter()
#         print('file time: ' + "{:.2f}".format(tt1-tt0))

# t1 = time.perf_counter()
# print('total time: ' + "{:.2f}".format(t1-t0))

# XX_en = np.abs(hilbert(XX))
# YY_en = np.abs(hilbert(YY))
# Y_FULL_en = np.abs(hilbert(Y_FULL))

# plt.figure()
# plt.subplot(131)
# Image = plt.imshow(XX_en,cmap='gray',interpolation='None',extent=[0,31* 0.3,XX_en.shape[0] *1.540*0.5*(1/20),0], animated=False,  aspect=1)
# plt.subplot(132)
# Image = plt.imshow(YY_en,cmap='gray',interpolation='None',extent=[0,31* 0.3,YY_en.shape[0] * Engine.res_mm_z,0],animated=False, aspect=1)
# plt.subplot(133)
# Image = plt.imshow(Y_FULL_en,cmap='gray',interpolation='None',extent=[0,31* 0.3,YY_en.shape[0] * Engine.res_mm_z,0],animated=False, aspect=1)

# plt.figure()
# plt.subplot(131)
# Image = plt.imshow(20*np.log10(XX_en),cmap='gray',interpolation='None',extent=[0,31* 0.3,XX_en.shape[0] *1.540*0.5*(1/20),0], animated=False,  aspect=1)
# # Image.set_clim(vmin=10, vmax=60)
# plt.subplot(132)
# Image = plt.imshow(20*np.log10(YY_en),cmap='gray',interpolation='None',extent=[0,31* 0.3,YY_en.shape[0] * Engine.res_mm_z,0],animated=False, aspect=1)
# # Image.set_clim(vmin=37, vmax=62)
# plt.subplot(133)
# Image = plt.imshow(20*np.log10(Y_FULL_en),cmap='gray',interpolation='None',extent=[0,31* 0.3,YY_en.shape[0] * Engine.res_mm_z,0],animated=False, aspect=1)
# # Image.set_clim(vmin=37, vmax=62)

# plt.show()