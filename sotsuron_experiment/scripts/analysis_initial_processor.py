import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from noise_processor import *

from analysis_management import *

path_management,csv_labels,color_dict=management_initial()

def initial_processor(csvpath,denoise=True):
    # read_csvしたデータの初期処理を行う
    # nanが含まれる（=全身が映ってない）フレームを削除
    if "_2d" in csvpath:
        data=pd.read_csv(csvpath,names=csv_labels["detectron2_joint_2d"])
        data=data.dropna(how="any",subset=csv_labels["detectron2_joint_2d"][1:])
    elif "_tf" in csvpath:
        data=pd.read_csv(csvpath,names=csv_labels["detectron2_joint_3d"])
        data=data.dropna(how="any",subset=csv_labels["detectron2_joint_3d"][1:])
    else:
        data=pd.read_csv(csvpath,names=csv_labels["detectron2_joint_3d_4"])
        data=data.dropna(how="any",subset=csv_labels["detectron2_joint_3d_4"][1:])
    data=data.sort_values("timestamp")
    data.reset_index(inplace=True,drop=True)
    # plt.plot(data["timestamp"],data["gravity_x"])
    # plt.show()

    if denoise:
        # 外れ値除去
        roi_joint="gravity_x"
        if "_2d" in csvpath:
            threshold_vel=500#[pixel/s]
        elif "_tf" in csvpath:
            threshold_vel=1.2#[m/s]
        else:
            threshold_vel=1.2
        while True:
            droplist=[]
            for i in range(1,len(data)):
                dt=abs(data["timestamp"].iat[i]-data["timestamp"].iat[i-1])
                if abs(data[roi_joint].iat[i]-data[roi_joint].iat[i-1])>threshold_vel*dt:
                    droplist.append(i)
            # print(len(data))
            data=data.drop(droplist)
            data.reset_index(inplace=True,drop=True)
            # print(len(data))
            if len(droplist)<1:
                break
    average = np.mean(data["timestamp"].values)
    std=np.std(data["timestamp"].values)
    num_sgm=3
    outlier_min=average-(std)*num_sgm
    outlier_max=average+(std)*num_sgm
    data=data[data["timestamp"]>outlier_min]
    data=data[data["timestamp"]<outlier_max]
    data=mean_processor(data,span=10)
    return data