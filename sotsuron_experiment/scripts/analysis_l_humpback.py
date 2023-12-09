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

csvs=path_management["ras_tf_csv_dir_path"]

for csvpath in csvs:
    if "12_07_00" not in csvpath:
        continue
    print(csvpath)
    # data=pd.read_csv(csvpath,names=csv_labels["detectron2_joint_3d"],skiprows=1)
    data=initial_processor(csvpath,True)
    # data=mean_processor(data)

    # リアルタイム処理
    pass
    # 後解析処理
    try:
        timestamp_x5_closest_idx=(data["gravity_x"]-5).abs().idxmin()
        timestamp_x5_closest=data.iloc[timestamp_x5_closest_idx]["timestamp"]
        x_x5_closest=data.iloc[timestamp_x5_closest_idx]["gravity_x"]
        timestamp_x0_closest_idx=(data[data["timestamp"]>timestamp_x5_closest]["gravity_x"]-0).abs().idxmin()
        timestamp_x0_closest=data.iloc[timestamp_x0_closest_idx]["timestamp"]
        x_x0_closest=data.iloc[timestamp_x0_closest_idx]["gravity_x"]
    except (TypeError,ValueError):
        continue
    # x=5,0を通過するtimestampを取得
    data=data[data["timestamp"]>timestamp_x5_closest]
    data=data[data["timestamp"]<timestamp_x0_closest]

    print(data.columns)
    # raise TimeoutError
    data["l_humpback_roll"]=0
    data["l_humpback_roll"]=np.rad2deg(np.arctan2(data["l_shoulder_y"]-data["l_base_y"],data["l_shoulder_z"]-data["l_base_z"]))
    data["l_humpback_pitch"]=0
    data["l_humpback_pitch"]=np.rad2deg(np.arctan2(data["l_shoulder_x"]-data["l_base_x"],data["l_shoulder_z"]-data["l_base_z"]))
    # data["l_humpback_yaw"]=0
    # data["l_humpback_yaw"]=np.arctan2(data["l_shoulder_x"]-data["l_base_x"],data["l_shoulder_z"]-data["l_base_z"])
    

    # クラスタdata)
    
    
    plt.subplot(211)
    plt.plot(data["timestamp"],data["l_foot_x"],"m",label="left foot $\it{x}$")
    plt.xlabel("Time $\it{t}$ [s]")
    plt.ylabel("Position of the left ancle in $\it{x}$-direction $\it{x}$ [m]")
    plt.grid()
    plt.legend()
    plt.subplot(212)
    plt.plot(data["timestamp"],data["l_humpback_roll"],"r",label="roll")
    plt.plot(data["timestamp"],data["l_humpback_pitch"],"b",label="pitch")
    plt.ylim([-50,50])
    plt.xlabel("Time $\it{t}$ [s]")
    plt.ylabel("Angle of the humpback [deg]")
    plt.grid()
    plt.legend()
    # plt.xlabel("Time $\it{t}$ [s]")
    # plt.ylabel("Velocity of the left ancle in $\it{x}$-direction $\it{v_x}$ [m/s]")
    # plt.grid()
    # plt.legend()
    plt.savefig(path_management["png_dir_path"]+"/12_07_00_humpback.png")
    # plt.show()
