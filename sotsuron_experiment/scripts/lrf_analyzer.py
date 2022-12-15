import os
import numpy as np
import matplotlib.pyplot as plt

csv_path=os.environ['HOME']+"/catkin_ws/src/sotsuron_experiment/scripts/monitor/lrf.csv"

data=np.loadtxt(csv_path,delimiter=",")

plt.plot(np.arange(len(data[:,1])),data[:,1])
plt.show()