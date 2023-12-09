#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
from glob import glob
import numpy as np
import matplotlib.pyplot as plt

csv_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/results/0214/csv/20230214_d_090_10_20230214_y075_v000_09_EtoE.csv"

data=np.loadtxt(csv_path,delimiter=",")
t=data[:,0]-data[0,0]
plt.plot(t,data[:,1])
# plt.plot(t,data[:,3])

plt.legend()
plt.show()