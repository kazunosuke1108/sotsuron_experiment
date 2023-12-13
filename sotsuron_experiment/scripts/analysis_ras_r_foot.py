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

# リアルタイム処理
pass
# 後解析処理
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

data["r_foot_vx"]=0
data["r_foot_vx"].iloc[:-1]=(data["r_foot_x"].values[1:]-data["r_foot_x"].values[:-1])/(data["timestamp"].values[1:]-data["timestamp"].values[:-1])
maybe_truth_vel_x=(data["gravity_x"].values[-1]-data["gravity_x"].values[0])/(data["timestamp"].values[-1]-data["timestamp"].values[0])
velocity_threshold=abs(maybe_truth_vel_x)
print(maybe_truth_vel_x)
binary_movestop=(data["r_foot_vx"]<velocity_threshold) & (data["r_foot_vx"]>-velocity_threshold)
data["r_foot_stop"]=False
data["r_foot_stop"]=binary_movestop
# print(len(data))
# print(np.sum(binary_movestop))
# raise TimeoutError

# クラスタリング
data=data.reset_index()
clusterdata=pd.DataFrame({"start_timestamp":[],
                            "end_timestamp":[],
                            "mean_timestamp":[],
                            "cluster_size":[],
                            "mean_x":[],
                            "mean_y":[]})
cluster_idx=0
temp_x=[]
temp_y=[]
for idx,row in data.iterrows():
    print(f"{idx} / {len(data)}")
    if idx==0:
        if (data["r_foot_stop"].iat[idx]) & (data["r_foot_stop"].iat[idx+1]):
            print("クラスターの最初")
            clusterdata.loc[cluster_idx]=0
            clusterdata["start_timestamp"].iat[cluster_idx]=row["timestamp"]
            clusterdata["cluster_size"].iat[cluster_idx]+=1
            temp_x.append(row["r_foot_x"])
            temp_y.append(row["r_foot_y"])
        else:
            continue
    elif idx==len(data)-1:
        if (data["r_foot_stop"].iat[idx-1]) & (data["r_foot_stop"].iat[idx]):
            print("クラスターの最後")
            clusterdata["end_timestamp"].iat[cluster_idx]=row["timestamp"]
            clusterdata["mean_timestamp"]=(clusterdata["start_timestamp"]+clusterdata["end_timestamp"])/2
            clusterdata["cluster_size"].iat[cluster_idx]+=1
            temp_x.append(row["r_foot_x"])
            temp_y.append(row["r_foot_y"])
            clusterdata["mean_x"].iat[cluster_idx]=np.mean(np.array(temp_x))
            clusterdata["mean_y"].iat[cluster_idx]=np.mean(np.array(temp_y))
            cluster_idx+=1
            temp_x=[]
            temp_y=[]
            continue
        else:
            continue
    if (not(data["r_foot_stop"].iat[idx-1])) & (data["r_foot_stop"].iat[idx]) & (data["r_foot_stop"].iat[idx+1]):
        print("クラスターの最初")
        clusterdata.loc[cluster_idx]=0
        clusterdata["start_timestamp"].iat[cluster_idx]=row["timestamp"]
        clusterdata["cluster_size"].iat[cluster_idx]+=1
        temp_x.append(row["r_foot_x"])
        temp_y.append(row["r_foot_y"])
    elif (data["r_foot_stop"].iat[idx-1]) & (data["r_foot_stop"].iat[idx]) & (data["r_foot_stop"].iat[idx+1]):
        print("クラスターの中心")
        clusterdata["cluster_size"].iat[cluster_idx]+=1
        temp_x.append(row["r_foot_x"])
        temp_y.append(row["r_foot_y"])
    elif (data["r_foot_stop"].iat[idx-1]) & (data["r_foot_stop"].iat[idx]) & (not(data["r_foot_stop"].iat[idx+1])):
        print("クラスターの最後")
        clusterdata["end_timestamp"].iat[cluster_idx]=row["timestamp"]
        clusterdata["mean_timestamp"]=(clusterdata["start_timestamp"]+clusterdata["end_timestamp"])/2
        clusterdata["cluster_size"].iat[cluster_idx]+=1
        temp_x.append(row["r_foot_x"])
        temp_y.append(row["r_foot_y"])
        clusterdata["mean_x"].iat[cluster_idx]=np.mean(np.array(temp_x))
        clusterdata["mean_y"].iat[cluster_idx]=np.mean(np.array(temp_y))
        cluster_idx+=1
        temp_x=[]
        temp_y=[]
        pass


# クラスターの絞り込み
clusterdata=clusterdata[clusterdata["cluster_size"]>10]
clusterdata["adjacent_vel_x"]=0
clusterdata["adjacent_vel_x"].iloc[1:]=(clusterdata["mean_x"].values[1:]-clusterdata["mean_x"].values[:-1])/(clusterdata["start_timestamp"].values[1:]-clusterdata["end_timestamp"].values[:-1])
clusterdata=clusterdata[(clusterdata["adjacent_vel_x"]>1.5*abs(maybe_truth_vel_x)) | (clusterdata["adjacent_vel_x"]<-1.5*abs(maybe_truth_vel_x))]
# raise TimeoutError

# 歩幅の算出
clusterdata["stride"]=0
clusterdata["stride"].iloc[1:]=abs(clusterdata["mean_x"].values[1:]-clusterdata["mean_x"].values[:-1])
print(clusterdata)


plt.subplot(211)
plt.plot(data["timestamp"],data["r_foot_x"],"m",label="left foot $\it{x}$")
plt.scatter(data["timestamp"][data["r_foot_stop"]],data["r_foot_x"][data["r_foot_stop"]],color="m",marker="x",alpha=0.25,label="stop moment")
plt.scatter(clusterdata["mean_timestamp"],clusterdata["mean_x"],color="k",marker="o",label="mean stoppoint")
plt.xlabel("Time $\it{t}$ [s]")
plt.ylabel("Position of the left ancle in $\it{x}$-direction $\it{x}$ [m]")
plt.grid()
plt.legend()
plt.subplot(212)
plt.plot(data["timestamp"],data["r_foot_vx"],"m",label="left foot $\it{v_x}$")
plt.scatter(data["timestamp"][data["r_foot_stop"]],data["r_foot_vx"][data["r_foot_stop"]],color="m",marker="x",alpha=0.25,label="stop moment")
plt.xlabel("Time $\it{t}$ [s]")
plt.ylabel("Velocity of the left ancle in $\it{x}$-direction $\it{v_x}$ [m/s]")
plt.grid()
plt.legend()
plt.savefig(os.path.split(csvpath)[0]+"/"+os.path.basename(csvpath)[:-8]+"_stride.png")
# plt.show()

clusterdata.to_csv(os.path.split(csvpath)[0]+"/"+os.path.basename(csvpath)[:-8]+"_stride.csv",index=False)