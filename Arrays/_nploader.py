import numpy as np
import os
print(os.path.abspath("."))
import matplotlib.pyplot as plt

X = np.load('./Arrays/B_Tue_Feb__9_183900_2021.npy')

print(X.shape)

# RAW MATRIX NO DPI OR SCALING 
Image = plt.imshow(X,cmap='gray',interpolation='None',animated=False, aspect=0.1)
# Image.set_clim(vmin=0, vmax=200)

plt.show()



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