import pandas as pd
import matplotlib.pyplot as plt
import os
from kalman import kalman_filter
import numpy as np

t=0
# while t<50:
i=1
print(10**i)
csvpath="/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/gaits/dev_1001.csv"
data=pd.read_csv(csvpath,header=None, names=["x","y","z","1","time","odom_x","odom_y","odom_theta","odom_pan"])
x=data["x"].tolist()
y=data["y"].tolist()
z=data["z"].tolist()
x_kalman=kalman_filter(np.nan_to_num(x,0),1,1,10)
y_kalman=kalman_filter(np.nan_to_num(y,0),1,1,10)
z_kalman=kalman_filter(np.nan_to_num(z,0),1,1,10)
print(x_kalman)
print(data["x"].tolist())
print(data["z"].tolist())

plt.figure(figsize=(10,10))
plt.subplot(321)
plt.plot(data["z"].tolist(),data["x"].tolist())
plt.subplot(321).set_aspect('equal')
plt.subplot(322)
plt.plot(data["time"].tolist(),x_kalman[:,1],"k")
plt.plot(data["time"].tolist(),y_kalman[:,1],"r")
plt.plot(data["time"].tolist(),z_kalman[:,1],"g")
plt.ylim([-1,1])
plt.subplot(323)
plt.plot(data["time"].tolist(),data["x"].tolist())
# plt.plot(data["time"].tolist(),x_kalman[:,0],"k")
plt.subplot(324)
plt.plot(data["time"].tolist(),data["y"].tolist())
# plt.plot(data["time"].tolist(),y_kalman[:,0],"r")
plt.subplot(325)
plt.plot(data["time"].tolist(),data["z"].tolist())
# plt.plot(data["time"].tolist(),z_kalman[:,0],"g")
# plt.pause(1)
# plt.clf()
t+=1
plt.savefig(csvpath[:-4]+".png")
plt.show()