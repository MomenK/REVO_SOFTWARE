import numpy as np
import os
print(os.path.abspath("."))
import matplotlib.pyplot as plt

X = np.load('./Arrays/filee.npy')

print(X.shape)

# RAW MATRIX NO DPI OR SCALING 
Image = plt.imshow(X,cmap='gray',interpolation='None',animated=False, aspect=1)
Image.set_clim(vmin=0, vmax=200)

plt.show()