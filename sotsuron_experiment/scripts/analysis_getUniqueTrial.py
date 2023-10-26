from glob import glob
from pprint import pprint
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

color_dict={"00":"r",
           "01":"r",
           "03":"m",
           "06":"b",
           "08":"c",
           }

plt.rcParams["figure.figsize"] = (10,8)
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.family'] = 'Times New Roman'
fig, ax = plt.subplots() 

## 管理dict作成
path_management={}
path_management["json_dir_path"]="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/json"
path_management["png_dir_path"]="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/png"
path_management["debug_csv_path"]="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/csv/debug.csv"
path_management["ras_csv_dir_path"]=sorted(glob("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/ras_csv/*_tf.csv"))

csv_labels={}
csv_labels["detectron2_joint"]=["gravity","nose","l_eye","r_eye","l_ear","r_ear","l_shoulder","r_shoulder","l_elbow","r_elbow","l_hand","r_hand","l_base","r_base","l_knee","r_knee","l_foot","r_foot"]
csv_labels["detectron2_joint_3d"]=["timestamp"]
for joint_name in csv_labels["detectron2_joint"]:
    suffixes=["_x","_y","_z"]
    for suffix in suffixes:
        csv_labels["detectron2_joint_3d"].append(joint_name+suffix)


def get_unique_trials():
    path_management["ras_csv_dir_path_unique"]=[]
    for trial in path_management["ras_csv_dir_path"]:
        if trial not in path_management["ras_csv_dir_path_unique"]:
            same_trial=sorted(glob(os.path.split(trial)[0]+"/"+os.path.split(trial)[1][:6]+"*_tf.csv"))
            if same_trial[-1] not in path_management["ras_csv_dir_path_unique"]:
                path_management["ras_csv_dir_path_unique"].append(same_trial[-1])


def initial_processor(data):
    # read_csvしたデータの初期処理を行う
    # nanが含まれる（=全身が映ってない）フレームを削除
    data=data.dropna(how="any",subset=csv_labels["detectron2_joint_3d"][1:])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s')
    data.set_index('timestamp', inplace=True)
    # 0<x<5を抽出する
    data=data.query("0 < gravity_x < 5")
    # data.to_csv(path_management["debug_csv_path"])
    # 次のフレームと重心のx軌跡が1m以上空いているデータを削除する
    gravity_x_diff=data["gravity_x"].diff()
    print(gravity_x_diff)
    gravity_x_diff.to_csv(path_management["debug_csv_path"])
    data=data[gravity_x_diff<0.3]
    data=data[-0.3<gravity_x_diff]
    # # 次のフレームと10秒以上間が空いているフレームを削除する
    # nblank=100
    # while nblank>=0:
    #     time_diff = data.index.to_series().diff().dt.total_seconds()
    #     print(time_diff)
    #     filtered_df = data[time_diff <= 1000]
    #     data=filtered_df
    #     nblank=len(filtered_df)
    return data

def plot_gravity():
    labellist=[]
    for i, trialpath in enumerate(path_management["ras_csv_dir_path_unique"]):
        data=pd.read_csv(trialpath,names=csv_labels["detectron2_joint_3d"])
        data=initial_processor(data)
        plotdata=data["gravity_x"]
        labellist.append(os.path.basename(trialpath)[:8])
        ax.scatter(np.full_like(plotdata,i),plotdata,c=color_dict[os.path.basename(trialpath)[3:5]],s=1)
        print(trialpath)
    ax.set_xticks(range(len(labellist)),labellist,rotation=90)
    plt.xlabel("trial ID")
    plt.ylabel("position x of the gravity [m]")
    # plt.savefig(path_management["png_dir_path"]+"/gravity_compare.png")
    # plt.ylim([0,10])
    # plt.savefig(path_management["png_dir_path"]+"/gravity_compare_closeup.png")
    plt.savefig(path_management["png_dir_path"]+"/gravity_compare_0to5.png")
    plt.show()

def calc_dt():
    for i, trialpath in enumerate(path_management["ras_csv_dir_path_unique"]):
        data=pd.read_csv(trialpath,names=csv_labels["detectron2_joint_3d"])
        data=initial_processor(data)
        dt = data.index.to_series().diff().dt.total_seconds()
        try:
            print(os.path.basename(trialpath)+f" : {np.max(dt)}")
        except ValueError:
            print(os.path.basename(trialpath)+" : not enough data")

def plt_individual_trial():
    for i, trialpath in enumerate(path_management["ras_csv_dir_path_unique"]):
        data=pd.read_csv(trialpath,names=csv_labels["detectron2_joint_3d"])
        data=initial_processor(data)
        ax.scatter(data.index,data["gravity_x"],c=color_dict[os.path.basename(trialpath)[3:5]],s=1)
        plt.xlabel("timestamp [s]")
        plt.ylabel("position x of the gravity [m]")
    # plt.savefig(path_management["png_dir_path"]+"/gravity_compare.png")
    # plt.ylim([0,10])
    # plt.savefig(path_management["png_dir_path"]+"/gravity_compare_closeup.png")
        plt.savefig(path_management["png_dir_path"]+f"/{os.path.basename(trialpath)}.png")
        plt.pause(0.1)
        plt.cla()

## 保存
json_dict={
    "path_management":path_management,
    "csv_labels":csv_labels,
    }
tf = open(path_management["json_dir_path"]+f"/analysis_database.json", "w")
json.dump(json_dict, tf)
tf.close()


get_unique_trials()
# 横軸trial, 縦軸x座標のプロット
# plot_gravity()

## フレーム間時刻差の計算
# calc_dt()

## 各試行の時系列plot
plt_individual_trial()


# 重心軌跡が取得できたx座標を横軸，試行IDを縦軸？
trialname=[]
