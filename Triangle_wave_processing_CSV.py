# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 10:47:42 2021

@author: LAB_632
"""


## triangle_wave_process
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

t = np.linspace(0, 40, 1000)
v = 1* signal.sawtooth(2 * np.pi * 0.025 * t,0.5)
plt.plot(t,v) 
plt.xlabel("Time[s]")
plt.ylabel("Amplitude[V]")
plt.title("Singal for sampling")

plt.show()
print(v)




## write_processed_signal_to_CSV
import pandas as pd
import os
filename = ['detail.csv']

father_path = os.getcwd()
path_csv = father_path+r'\detail.csv'

df = filename

data = np.empty(shape=[0,2])
for i in range(len(v)):
    temp = np.array([t[i],v[i]])
    temp = np.expand_dims(temp,axis=0)
    data = np.append(data,temp,axis=0)
df = pd.DataFrame(data,columns=["t","v"])
df.to_csv(path_csv)
