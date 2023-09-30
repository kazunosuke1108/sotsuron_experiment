import pandas as pd
import matplotlib.pyplot as plt
import os

csvpath="/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/gaits/dev_0930_4m.csv"
data=pd.read_csv(csvpath,header=None, names=["x","y","z","1","time","odom_x","odom_y","odom_theta","odom_pan"])

print(data)
print(data["x"].tolist())
print(data["z"].tolist())
plt.subplot(221)
plt.plot(data["x"].tolist(),data["z"].tolist())
plt.subplot(222)
plt.plot(data["time"].tolist(),data["x"].tolist())
plt.subplot(223)
plt.plot(data["time"].tolist(),data["y"].tolist())
plt.subplot(224)
plt.plot(data["time"].tolist(),data["z"].tolist())
plt.savefig(csvpath[:-4]+".png")
plt.show()