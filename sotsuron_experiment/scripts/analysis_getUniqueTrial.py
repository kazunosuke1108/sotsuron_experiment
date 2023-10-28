from glob import glob
from pprint import pprint
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

color_dict={"00":"r",
           "01":"r",
           "02":"k",
           "03":"m",
           "04":"k",
           "05":"k",
           "06":"b",
           "07":"k",
           "08":"c",
           "09":"k",
           "10":"k",
           "11":"k",
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
path_management["denoise_csv_dir_path"]="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/csv/denoise"

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
    data.reset_index(inplace=True,drop=True)

    # 外れ値除去
    roi_joint="l_base_x"
    threshold_vel=1.5#[m/s]
    while True:
        droplist=[]
        for i in range(1,len(data)):
            dt=abs(data["timestamp"].iat[i]-data["timestamp"].iat[i-1])
            if abs(data[roi_joint].iat[i]-data[roi_joint].iat[i-1])>threshold_vel*dt:
                droplist.append(i)
        print(len(data))
        data=data.drop(droplist)
        data.reset_index(inplace=True,drop=True)
        print(len(data))
        if len(droplist)<10:
            break

    # data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s')
    # data.set_index('timestamp', inplace=True)
    # 0<x<5を抽出する
    # print(len(data))
    data=data.query("-1 < gravity_x < 6")
    data.to_csv(path_management["debug_csv_path"])
    
    # 時系列で見たときに外れ値になっているデータを除外する
    print(data["timestamp"])
    average = np.mean(data["timestamp"].values)
    std=np.std(data["timestamp"].values)
    num_sgm=3
    outlier_min=average-(std)*num_sgm
    outlier_max=average+(std)*num_sgm
    data=data[data["timestamp"]>outlier_min]
    data=data[data["timestamp"]<outlier_max]

    # 速度が狂ってる外れ値を除外する

    # 初期時刻を0にする
    # start_time=data.head(1)["timestamp"].values
    # print(start_time)
    # data["timestamp"]=data["timestamp"]-start_time

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
    roi_joint="l_base_x"
    path_management["png_dir_path"]=path_management["png_dir_path"]+"/"+roi_joint
    os.makedirs(path_management["png_dir_path"],exist_ok=True)
    for i, trialpath in enumerate(path_management["ras_csv_dir_path_unique"][1:]):
        data=pd.read_csv(trialpath,names=csv_labels["detectron2_joint_3d"])
        print(trialpath)
        # print(len(data))
        data=initial_processor(data)
        # print(len(data["gravity_x"]))
        ax.scatter(data.index,data[roi_joint],c=color_dict[os.path.basename(trialpath)[3:5]],s=1)
        plt.xlabel("timestamp [s]")
        plt.ylabel("position x of the gravity [m]")
        plt.title(os.path.basename(trialpath))
        # plt.savefig(path_management["png_dir_path"]+"/gravity_compare.png")
        # plt.ylim([-1,6])
        # plt.savefig(path_management["png_dir_path"]+"/gravity_compare_closeup.png")
        plt.savefig(path_management["png_dir_path"]+f"/{os.path.basename(trialpath)[:8]+'_'+roi_joint}.png")
        plt.pause(0.01)
        plt.cla()

def plt_individual_trial_2joint():
    roi_joint1="l_base_x"
    roi_joint2="r_base_x"
    path_management["png_dir_path"]=path_management["png_dir_path"]+"/"+roi_joint1+"_AND_"+roi_joint2
    os.makedirs(path_management["png_dir_path"],exist_ok=True)
    for i, trialpath in enumerate(path_management["ras_csv_dir_path_unique"]):
        data=pd.read_csv(trialpath,names=csv_labels["detectron2_joint_3d"])
        print(trialpath)
        # print(len(data))
        data=initial_processor(data)
        # save denoise csv
        data.to_csv(path_management["denoise_csv_dir_path"]+"/"+os.path.basename(trialpath)[:-4]+"_denoise.csv")

        ax.scatter(data.index,data[roi_joint1],c="r",s=1,label=roi_joint1)
        ax.scatter(data.index,data[roi_joint2],c="b",s=1,label=roi_joint2)
        plt.xlabel("timestamp [s]")
        plt.ylabel("position x of the gravity [m]")
        plt.title(os.path.basename(trialpath))
        plt.legend()
        # plt.savefig(path_management["png_dir_path"]+"/gravity_compare.png")
        plt.ylim([-1,6])
        # plt.savefig(path_management["png_dir_path"]+"/gravity_compare_closeup.png")
        plt.savefig(path_management["png_dir_path"]+"/"+os.path.basename(trialpath)[:8]+"_"+roi_joint1+"_AND_"+roi_joint2+".png")
        plt.pause(0.01)
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
# plt_individual_trial()
plt_individual_trial_2joint()


# 重心軌跡が取得できたx座標を横軸，試行IDを縦軸？