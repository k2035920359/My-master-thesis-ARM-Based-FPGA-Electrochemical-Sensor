
# coding: utf-8

# In[1]:


#設定時間
get_ipython().system('sudo date -s "20230324 09:40:00"')
import matplotlib.pyplot as plt
plt.show()


# In[5]:


import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
from time import sleep,time,process_time,strftime,localtime
from pynq.lib import Pmod_ADC, Pmod_DAC
from pynq.overlays.base import BaseOverlay
import threading
import os
import csv
from datetime import datetime
from numpy import char
from scipy.interpolate import BSpline
from IPython.display import HTML as html_print
from IPython.display import display
from matplotlib.pyplot import MultipleLocator

def cstr(s, color='black'):
    return "<text style=color:{}>{}</text>".format(color, s)

def print_color(t):
    display(html_print(' '.join([cstr(ti, color=ci) for ti,ci in t])))



now = datetime.now() # current date and time

year = now.strftime("%Y")
print("year:", year)

date = now.strftime("%m%d")
print("date:", date)

local_time = now.strftime("%H-%M-%S")
print("time:", local_time)

date_time = now.strftime("%m/%d/%Y, %H-%M-%S")
print("date and time:",date_time)	

path = "./output" + "/" + str(year) + "/" + str(date) + "/" + str(local_time)
#print(time.localtime())




ol = BaseOverlay("base.bit")

dac = Pmod_DAC(ol.PMODB)
adc = Pmod_ADC(ol.PMODA)
adc.reset()

time_fuc = np.linspace(0,40,2000) # 時間

x = 1*(1-abs(signal.sawtooth( 2 * np.pi * 0.025 * time_fuc ))) # 產生三角波
V_value  = []
V_out_samples = []

sleep_time = 0.02

tic = time()


# 主執行緒繼續執行自己的工作
for value in x:
    dac.write(value)
    sample = adc.read()
    V_out_samples.append(sample[0])
    sleep(sleep_time)
# 等待 t 這個子執行緒結束

toc = time()
print(toc-tic,'s')

V_value = x
I_value = [10*i for i in V_out_samples]
V = np.array(V_value)
I = np.array(I_value)

arr = np.vstack((V,I))
arr = np.transpose(arr)


if not os.path.isdir(path):
    os.makedirs(path)  # 多層次建立目錄
    np.savetxt(path + '/' + str(year + date + local_time) + '_raw.csv', arr, delimiter=', ')

else:
    np.savetxt(path + '/' + str(year + date + local_time) + '_raw.csv', arr, delimiter=', ')

#y = -0.0028*x + 1.304


mean_len_half = 10
for i in range(mean_len_half):
    I_value.insert(i,0)
    I_value.append(0)
    
I_ = np.array(I_value)
I_mean = []

for i in range(mean_len_half,mean_len_half+len(I)):
    I_mean = np.append(I_mean,[[np.mean(I_[(i-mean_len_half):(i+mean_len_half)])]])  

np.savetxt(path + '/' + str(year + date + local_time) + '_mean.csv', np.array(I_mean), delimiter=', ')

y = max(I_mean[400:900])
y_ = round(y,2)
print('max I: ' + str(y_) + ' μA')

x = ((abs(y-1.0)/1.0)+0.0408)/0.0028
x = round(x,2)
x_ = '濃度: ' + str(x)+' μg/ml'

print_color(((x_, 'red'),))
x_ = np.array(x_)
np.savetxt(path + '/' +'濃度.csv',x_.reshape(-1,1),fmt='%s')

y_major_locator = MultipleLocator(0.05)
    
plt.figure()
plt.plot(time_fuc,V,color='blue',label='V')
plt.xlabel( 't (s)' )
plt.ylabel( 'Voltage (V)' )
plt.legend(loc='upper left', frameon=False)
plt.title('V')
plt.savefig(path + '/' + str(year + date + local_time) + '_V.png')

plt.figure()
plt.plot(time_fuc,I_mean,color='blue',label='I')
plt.xlabel( 't (s)' )
plt.ylabel( 'Current (μA)' )
plt.legend(loc='upper left', frameon=False)
plt.title('I')
plt.savefig(path + '/' + str(year + date + local_time) + '_I.png')

plt.figure()
plt.plot(time_fuc,I,color='blue',label='I')
plt.xlabel( 't (s)' )
plt.ylabel( 'Current (μA)' )
plt.legend(loc='upper left', frameon=False)
plt.title('I')
#plt.savefig(path + '/' + str(year + date + local_time) + '_I.png')


plt.figure()
plt.plot(V,I_mean,color='red',label='IV plot')
ax = plt.gca()
ax.yaxis.set_major_locator(y_major_locator)
#plt.ylim(0,1)
plt.xlabel( ' Voltage (V)' )
plt.ylabel( 'current (μA)' )
plt.legend(loc='upper left', frameon=False)
plt.title('IV plot')
plt.savefig(path + '/' + str(year + date + local_time) + '_IV_plot.png')

plt.show()


# In[22]:


import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
from time import sleep,time,process_time,strftime,localtime
from pynq.lib import Pmod_ADC, Pmod_DAC
from pynq.overlays.base import BaseOverlay
import threading
import os
import csv
from datetime import datetime
from numpy import char
from scipy.interpolate import BSpline
from IPython.display import HTML as html_print
from IPython.display import display
from matplotlib.pyplot import MultipleLocator




