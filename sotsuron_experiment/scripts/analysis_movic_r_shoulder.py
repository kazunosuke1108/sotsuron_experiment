import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from analysis_management import *

path_management,csv_labels,color_dict=management_initial()
plt.rcParams["figure.figsize"] = (15,10)
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.family'] = 'Times New Roman'

# 3d
three_d_csv_path="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/velocity_error/_2023-12-21-10-22-39_tf_raw.csv"
zH=pd.read_csv(three_d_csv_path,names=csv_labels["detectron2_joint_3d"])
zH_trunk_x=zH[["r_shoulder_x","l_shoulder_x","r_base_x","l_base_x"]]

# odom
odom_to_zed_csv_path="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-21-10-22-39/_2023-12-21-10-22-39_od_raw.csv"

zR=pd.read_csv(odom_to_zed_csv_path,names=["t","x","y","theta","phi"])

# 2d
two_d_10x_csv_path="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/velocity_error/_2023-12-21-10-22-39_2d_raw.csv"
two_d_01x_csv_path="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/velocity_error/_2023-12-21-10-22-39_2d_raw_01x.csv"
two_d_10x_csv=pd.read_csv(two_d_10x_csv_path,names=csv_labels["detectron2_joint_2d"])
two_d_01x_csv=pd.read_csv(two_d_01x_csv_path,names=csv_labels["detectron2_joint_2d"])

fig,ax1=plt.subplots()
ax1.plot(zH["timestamp"],zH["r_shoulder_x"],"k",markersize=1,label="r_shoulder_x (3d)")
ax1.set_xlabel("Time $\it{t}$ [s]")
ax1.set_ylabel("Position of the human $\it{x}$ [s]")
ax1.legend(loc="upper left")
ax2=ax1.twinx()

ax2.plot(zR["t"],zR["x"],label="xR")
ax2.plot(zR["t"],zR["y"],label="yR")
ax2.plot(zR["t"],zR["theta"],label="theta")
ax2.plot(zR["t"],zR["phi"],label="phi")
plt.ylabel("Position of the robot$\it{x_R}$ [m]")
# ax2.plot(two_d_10x_csv["timestamp"],two_d_10x_csv["r_shoulder_x"],label="r_shoulder_x (2d)")
# ax2.plot(two_d_10x_csv["timestamp"],two_d_10x_csv["r_shoulder_y"],label="r_shoulder_y (2d)")
# plt.ylabel("Position in image $\it{x}$ [pixel]")
ax2.legend(loc="upper right")
ax1.grid()
plt.title(f"relationship between odom & estimation result ({os.path.basename(sys.argv[0])} _2023-12-21-10-22-39)")
plt.savefig("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/velocity_error/_2023-12-21-10-22-39_odom_and_position.png")
print(zR)
plt.show()