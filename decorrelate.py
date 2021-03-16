from scipy import signal
import numpy as np

from os import listdir
from os.path import isfile, join

file_name= 'N45_100'
ArrayPath = './UserSessions/'+ file_name +'/M_Arrays/'
ImagPath = './UserSessions/'+ file_name +'M_Images/'
file = 'M_Wed_Mar_10_150834_2021.npy'

def autocorr(x):
    result = np.correlate(x, x, mode='same')
    return result

X = np.load(ArrayPath + file)
T = np.load(ArrayPath + 'T' + file)  

print(X.shape)
print(T.shape)

X
print(autocorr([1, 0, 1,0,0]))
