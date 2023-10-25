import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# import time
# while True:
csvpath="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/scripts/test.csv"
csvpath="/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/ras_csv/03_00_00__2023-10-20-17-09-06_tf.csv"
data=pd.read_csv(csvpath)#,names=["tH","x","y","z","0","tR","xR","yR","thR","panR"])
data=data.to_numpy()
sort_idx=np.argsort(data,axis=0)[:,0]
print(np.argsort(data,axis=0)[:,0])

data=data[sort_idx,:]
# data=np.sort(data,axis=0)
# data.sort(axis=0)
# data=data[::-1]
# print(data["tH"])

# plt.plot(data[:,0],data[:,1],label="x",lw=0.25)#,s=3)
# plt.plot(data[:,0],data[:,2],label="y",lw=0.25)#,s=3)
plt.plot(data[:,1],data[:,2])
# plt.ylim([0,2])
# plt.scatter(data[:,0],data[:,3],label="z",s=3)
plt.legend()
plt.grid()
plt.savefig(csvpath[:-4]+".png")
plt.show()
# plt.cla()
# time.sleep(1)
