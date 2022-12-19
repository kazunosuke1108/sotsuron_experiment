import os
import numpy as np
import matplotlib.pyplot as plt

csv_path=os.environ['HOME']+"/catkin_ws/src/sotsuron_experiment/scripts/sources/ranges.csv"

data=np.loadtxt(csv_path,delimiter=",")

plt.plot(np.arange(len(data)),data)
plt.ylim([0,10])
plt.show()