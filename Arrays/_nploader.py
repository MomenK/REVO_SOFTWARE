import numpy as np
import os
print(os.path.abspath("."))
import matplotlib.pyplot as plt

# X = np.load('./Arrays/B_Wed_Feb_10_105708_2021.npy')

# print(X.shape)


# # RAW MATRIX NO DPI OR SCALING 
# Image = plt.imshow(X,cmap='gray',interpolation='None',animated=False, aspect=0.1)
# # Image.set_clim(vmin=0, vmax=200)

# plt.show()


# odd=X[:,::2]    #odd cols  index 0 is odd
# even=X[:,1::2]   #even cols index 1 is even

# print(odd.shape,even.shape)
# Y = np.zeros((1024,32))

# for i in range(0,16):
#     print(i)
#     Y[:,2*i]    =  even[:,i]
#     Y[:,2*i +1] = odd[:,i]

# print(Y.shape)

# # RAW MATRIX NO DPI OR SCALING 
# Image = plt.imshow(Y,cmap='gray',interpolation='None',animated=False, aspect=0.1)
# # Image.set_clim(vmin=0, vmax=200)

# plt.show()


from os import listdir
from os.path import isfile, join

files = listdir('./Arrays')

for i in range(5, len(files)-1):
    print(i)

    file = files[i]
    X = np.load('./Arrays/'+file)
    print(file)

    X = X[70:600,:]

    DEPTH = X.shape[0] 

    plt.subplot(221)
    Image = plt.imshow(X,cmap='gray',interpolation='None',animated=False, extent=[0,31* 0.3,DEPTH*1.540*0.5*(1/20),0], aspect=0.8)
    # Image.set_clim(vmin=0, vmax=200)

    plt.subplot(222)
    plt.hist(X.flatten(), bins=200)


    plt.subplot(223)
    shif = 0
    r = 3
    Z= 20*np.log10(X)
    s= np.std(Z.flatten())
    m = np.mean(Z.flatten())
    r1 = m+ r*s + shif
    r2 = m- r*s + shif
    print(m,s, r2 , r1)

    Image = plt.imshow(X,cmap='gray',interpolation='hanning',animated=False,extent=[0,31* 0.3,DEPTH*1.540*0.5*(1/20),0], aspect=0.8)
    Image.set_clim(vmin=r2, vmax=r1)


    plt.subplot(224)
    plt.hist(Z.flatten(), bins=200)
    # 

    # plt.show()









    plt.show()

