import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from analysis_management import *
from matplotlib.gridspec import GridSpec
from noise_processor import *

path_management,csv_labels,color_dict=management_initial()


t=np.arange(0,5,0.01)
n=t//(1/3)
print(n)
x=0.4*t-0.05*n
x_FSMPC=x+0.05*np.exp(-10*(t-n*(1/3)))
flg_odd=n%2==0
x_houraku=((0.4*1/3-0.05)/(1/3))*t+0.05
x_proposed=x_houraku+0.02*np.sin(2*np.pi/(2*(1/3))*t-np.pi)
plt.plot(t,x,"b",label="x")
plt.plot(t,x_FSMPC,"r",label="x_FSMPC")
# plt.plot(t,x_houraku,"k",label="x_houraku")
plt.plot(t,x_proposed,"g",label="x_proposed")
plt.legend()
plt.show()

data=pd.DataFrame(columns=["timestamp","x","x_FSMPC"])
data["timestamp"]=t
data["x"]=x
data["x_FSMPC"]=x_FSMPC
data["x_proposed"]=x_proposed
vel_processor(data,labels=["x","x_FSMPC","x_proposed"])
print(data)

[freq,Amp_list,F]=fft_processor(data,labels=["v_x","v_x_FSMPC","v_x_proposed"])

gs=GridSpec(3,1)
plt.subplot(gs[0])
plt.bar(freq[:len(freq)//2],Amp_list[0][:len(freq)//2],color="b",alpha=1,label="x")
draw_labels_fft()
plt.subplot(gs[1])
plt.bar(freq[:len(freq)//2],Amp_list[1][:len(freq)//2],color="r",alpha=1,label="x_FSMPC")
draw_labels_fft()
plt.subplot(gs[2])
plt.bar(freq[:len(freq)//2],Amp_list[2][:len(freq)//2],color="g",alpha=1,label="x_proposed")
draw_labels_fft()
plt.show()