#! /usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from glob import glob
import matplotlib.pyplot as plt
import pandas as pd
from pprint import pprint
import pickle
from noise_processor import *
from analysis_management import *
from analysis_initial_processor import *

path_management,csv_labels,color_dict=management_initial()
plt.rcParams["figure.figsize"] = (7,7)
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.family'] = 'Times New Roman'

try:
    csvpath=sys.argv[1]
except Exception:
    csvpath="/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-11-11-55-46/_2023-12-11-11-55-46_tf_raw.csv"

data=initial_processor(csvpath,True)
# data=mean_processor(data)

# try:
timestamp_x5_closest_idx=(data["gravity_x"]-5).abs().idxmin()
timestamp_x5_closest=data.iloc[timestamp_x5_closest_idx]["timestamp"]
x_x5_closest=data.iloc[timestamp_x5_closest_idx]["gravity_x"]
timestamp_x0_closest_idx=(data[data["timestamp"]>timestamp_x5_closest]["gravity_x"]-0).abs().idxmin()
timestamp_x0_closest=data.iloc[timestamp_x0_closest_idx]["timestamp"]
x_x0_closest=data.iloc[timestamp_x0_closest_idx]["gravity_x"]
# except (TypeError,ValueError):
#     continue
# x=5,0を通過するtimestampを取得
data=data[data["timestamp"]>timestamp_x5_closest]
data=data[data["timestamp"]<timestamp_x0_closest]

print(data.columns)
# raise TimeoutError
data["r_humpback_roll"]=0
data["r_humpback_roll"]=np.rad2deg(np.arctan2(data["r_shoulder_y"]-data["r_base_y"],data["r_shoulder_z"]-data["r_base_z"]))
data["r_humpback_pitch"]=0
data["r_humpback_pitch"]=np.rad2deg(np.arctan2(data["r_shoulder_x"]-data["r_base_x"],data["r_shoulder_z"]-data["r_base_z"]))
# data["r_humpback_yaw"]=0
# data["r_humpback_yaw"]=np.arctan2(data["r_shoulder_x"]-data["r_base_x"],data["r_shoulder_z"]-data["r_base_z"])


# クラスタdata)

plt.subplot(211)
plt.plot(data["timestamp"],data["r_foot_x"],"m",label="right foot $\it{x}$")
plt.xlabel("Time $\it{t}$ [s]")
plt.ylabel("Position of the left ancle in $\it{x}$-direction $\it{x}$ [m]")
plt.grid()
plt.legend()
plt.subplot(212)
plt.plot(data["timestamp"],data["r_humpback_roll"],"r",label="roll")
plt.plot(data["timestamp"],data["r_humpback_pitch"],"b",label="pitch")
plt.ylim([-50,50])
plt.xlabel("Time $\it{t}$ [s]")
plt.ylabel("Angle of the humpback [deg]")
plt.grid()
plt.legend()
# plt.xlabel("Time $\it{t}$ [s]")
# plt.ylabel("Velocity of the left ancle in $\it{x}$-direction $\it{v_x}$ [m/s]")
# plt.grid()
# plt.legend()
plt.savefig(os.path.split(csvpath)[0]+"/"+os.path.basename(csvpath)[:-8]+"_humpback.png")
# plt.show()
