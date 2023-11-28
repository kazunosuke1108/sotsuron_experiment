import sys
from glob import glob
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import pandas as pd
from pprint import pprint
import pickle

from analysis_management import *
from analysis_initial_processor import *
from noise_processor import *

plt.rcParams["figure.figsize"] = (8,8)
# plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.family'] = 'Times New Roman'
# gs = GridSpec(2, 3, width_ratios=[1,1,1])
path_management,csv_labels,color_dict=management_initial()

roi_joint1="l_foot_x"
roi_joint2="r_foot_x"
path_management["png_dir_path"]=path_management["png_dir_path"]+"/new_"+roi_joint1+"_AND_"+roi_joint2
os.makedirs(path_management["png_dir_path"],exist_ok=True)
for i, trialpath in enumerate(path_management["ras_tf_csv_dir_path_unique"]):
    if "12_00_00" not in trialpath:
        continue
    # data=pd.read_csv(trialpath,names=csv_labels["detectron2_joint_3d"])
    # print(trialpath)
    # print(len(data))
    data=initial_processor(trialpath,denoise=True)
    data=data[data["l_base_x"]<6]
    data=data[data["l_base_x"]>-1]
    data=data.iloc[20:]
    data.reset_index(inplace=True,drop=True)
    # save denoise csv
    # data.to_csv(path_management["denoise_csv_dir_path"]+"/"+os.path.basename(trialpath)[:-4]+"_denoise.csv")

    plt.scatter(data["timestamp"],data[roi_joint1],c="r",s=1,label=roi_joint1)
    # plt.scatter(data["timestamp"],data[roi_joint2],c="b",s=1,label=roi_joint2)
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