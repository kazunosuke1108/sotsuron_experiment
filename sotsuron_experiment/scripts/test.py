import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# import time
# while True:
csvpath="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/scripts/test.csv"
csvpath="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/ras_csv/03_00_00__2023-10-20-17-09-06_2d.csv"
csvpath="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/ras_csv/12_00_00__2023-10-22-16-41-17_2d.csv"
csvpath="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/ras_csv/03_03_00__2023-10-20-17-24-31_2d.csv"
data=pd.read_csv(csvpath)#,names=["tH","x","y","z","0","tR","xR","yR","thR","panR"])
data=data.to_numpy()
for i in range(data.shape[1]):
    if i%3==0:
        continue
    if i%3==1: #x
        plt.plot(data[:,0],data[:,i],"r")
    if i%3==2: #y
        plt.plot(data[:,0],data[:,i],"b")
plt.show()