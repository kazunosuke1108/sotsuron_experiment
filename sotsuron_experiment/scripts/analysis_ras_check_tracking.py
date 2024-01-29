import pandas as pd
import numpy as np
from noise_processor import *
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import pickle
import sys
from analysis_management import *
path_management,csv_labels,color_dict=management_initial()

try:
    tfcsvpath=sys.argv[1]
except Exception:
    tfcsvpath="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-16-17-47-38/_2023-12-16-17-47-38_tf_raw.csv"
try:
    odomcsvpath=sys.argv[2]
except Exception:
    odomcsvpath="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-16-17-47-38/_2023-12-16-17-47-38_od_raw.csv"
try:
    picklepath=sys.argv[3]
except Exception:
    picklepath="C:/Users/hayashide/ytlab_ros_ws/ytlab_nlpmp/ytlab_nlpmp_modules/results/20231216/20231216_180747_20231214_01_00_hayashide/20231216_180812_0001/20231216_180812_0001.pickle"

plt.rcParams["figure.figsize"] = (10,6)
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.family'] = 'Times New Roman'
print(picklepath)
with open(picklepath, 'rb') as f:
    pickledata = pickle.load(f)
print(pickledata["sns"])

tf_data=pd.read_csv(tfcsvpath,names=["timestamp","trunk_x","trunk_y","trunk_z"],usecols=[0,1,2,3])
odom_data=pd.read_csv(odomcsvpath,names=["timestamp","x","y","theta","pan"])
tf_data=resampling_processor(tf_data,"0.1S")
odom_data=resampling_processor(odom_data,"0.1S")

merged_data=pd.merge(tf_data,odom_data,on="timestamp_datetime_round",how="outer")

merged_data["r"]=np.sqrt((merged_data["trunk_x"]-merged_data["x"])**2+(merged_data["trunk_y"]-merged_data["y"])**2)
merged_data["theta_h"]=np.rad2deg(np.arctan((merged_data["trunk_y"]-merged_data["y"])/(merged_data["trunk_x"]-merged_data["x"])))
merged_data["theta_rh"]=merged_data["theta_h"]-np.rad2deg(merged_data["theta"]+merged_data["pan"])
merged_data["theta_rh2"]=merged_data["theta_h"]-180-np.rad2deg(merged_data["theta"]+merged_data["pan"])
# for idx,row in merged_data.iterrows():
#     if row["theta_rh"]>np.pi/2:
#         print("replace")
#         print(idx)
#         merged_data["theta_rh"].iat[idx]=row["theta_rh"]-np.pi/2
# plt.plot(merged_data["timestamp_datetime_round"],merged_data["theta_h"],marker="o",color="b")
# plt.plot(merged_data["timestamp_datetime_round"],merged_data["theta_h"]-np.pi,marker="o",color="b")
# plt.plot(merged_data["timestamp_datetime_round"],merged_data["theta"]+merged_data["pan"])
# plt.plot(merged_data["timestamp_datetime_round"],merged_data["theta"]+merged_data["pan"])


gs = GridSpec(2, 2, width_ratios=[1,1])
plt.subplot(gs[0,0])
plt.plot(merged_data["timestamp_datetime_round"],merged_data["r"],marker="o",color="b")
plt.fill_between([merged_data["timestamp_datetime_round"].min(),merged_data["timestamp_datetime_round"].max()],pickledata["sns"]["r1"],pickledata["sns"]["r2"],color='red', alpha=0.5)
plt.xlabel("Time [s]")
plt.ylabel("Distance [m]")
plt.subplot(gs[0,1])
plt.plot(merged_data["trunk_x"],merged_data["r"],marker="o",color="b")
plt.fill_between([merged_data["trunk_x"].min(),merged_data["trunk_x"].max()],pickledata["sns"]["r1"],pickledata["sns"]["r2"],color='red', alpha=0.5)
plt.xlabel("Human position in hallway direction $/it{x}$ [m]")
plt.ylabel("Distance [m]")
plt.subplot(gs[1,0])
plt.plot(merged_data["timestamp_datetime_round"],merged_data["theta_rh"],marker="o",color="b")
plt.plot(merged_data["timestamp_datetime_round"],merged_data["theta_rh2"],marker="^",color="c")
plt.fill_between([merged_data["timestamp_datetime_round"].min(),merged_data["timestamp_datetime_round"].max()],-np.rad2deg(pickledata["sns"]["phi"]),np.rad2deg(pickledata["sns"]["phi"]),color='red', alpha=0.5)
plt.xlabel("Time [s]")
plt.ylabel("Angle seen from the robot [deg]")
plt.subplot(gs[1,1])
plt.plot(merged_data["trunk_x"],merged_data["theta_rh"],marker="o",color="b")
plt.plot(merged_data["trunk_x"],merged_data["theta_rh2"],marker="^",color="c")
plt.fill_between([merged_data["trunk_x"].min(),merged_data["trunk_x"].max()],-np.rad2deg(pickledata["sns"]["phi"]),np.rad2deg(pickledata["sns"]["phi"]),color='red', alpha=0.5)
plt.xlabel("Human position in hallway direction $/it{x}$ [m]")
plt.ylabel("Angle seen from the robot [deg]")
plt.savefig(os.path.split(tfcsvpath)[0]+"/check_tracking.png")