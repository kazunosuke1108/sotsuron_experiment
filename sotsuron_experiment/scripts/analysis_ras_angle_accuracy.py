import os
import sys
import numpy as np
import pandas as pd
from glob import glob
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from analysis_management import *
from analysis_initial_processor import *
from sklearn.metrics import mean_absolute_error

path_management,csv_labels,color_dict=management_initial()
plt.rcParams["figure.figsize"] = (10,8)
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.family'] = 'Times New Roman'

class analysisAngleAccuracy():
    def __init__(self,merged_data_path="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-20-19-45-25/_2023-12-20-19-45-25_merged.csv"):
        self.merged_data_path=merged_data_path
        self.merged_data=pd.read_csv(merged_data_path,header=0)
        print(self.merged_data)
        self.merged_data["relative_distance"]=np.sqrt((self.merged_data["trunk_x"]-self.merged_data["x"])**2+(self.merged_data["trunk_y"]-self.merged_data["y"])**2)

        
    
    def extract_ROI(self,data,rel_dist_thre):
        ROI_data=data[data["relative_distance"]<rel_dist_thre]
        ROI_data.reset_index(inplace=True)
        ROI_data["time_diff"]=0
        print(ROI_data["time_diff"])
        print(ROI_data["timestamp_x"].iloc[1:]-ROI_data["timestamp_x"].iloc[:-1])
        ROI_data["time_diff"][:-1]=(ROI_data["timestamp_x"].values[1:]-ROI_data["timestamp_x"].values[:-1])
        print(ROI_data["time_diff"].max())
        try:
            cut_timestamp_x=ROI_data["timestamp_x"][ROI_data["time_diff"]>10].values[0]
            ROI_data=ROI_data[ROI_data["timestamp_x"]<cut_timestamp_x]
        except IndexError:
            pass
        print(ROI_data)
        return ROI_data
    
    def write_log(self,output_data,csvpath,fmt="%s"):
        try:
            with open(csvpath, 'a') as f_handle:
                np.savetxt(f_handle,[output_data],delimiter=",")
        except TypeError:
            with open(csvpath, 'a') as f_handle:
                np.savetxt(f_handle,[output_data],delimiter=",",fmt=fmt)    
        except FileNotFoundError:
            np.savetxt(csvpath,[output_data],delimiter=",")
        pass  
    
    def analyze_humpback_accuracy(self,rel_dist_thre=(5+0.6301867843887389)/2):
        # ROI_merged_data=self.merged_data[self.merged_data["relative_distance"]<rel_dist_thre]
        ROI_merged_data=self.extract_ROI(self.merged_data,rel_dist_thre=rel_dist_thre)
        print(ROI_merged_data)

        ROI_merged_data["c_shoulder_x"]=0
        ROI_merged_data["c_shoulder_y"]=0
        ROI_merged_data["c_shoulder_z"]=0
        ROI_merged_data["c_base_x"]=0
        ROI_merged_data["c_base_y"]=0
        ROI_merged_data["c_base_z"]=0
        ROI_merged_data["c_shoulder_x"]=(ROI_merged_data["r_shoulder_x"]+ROI_merged_data["l_shoulder_x"])/2
        ROI_merged_data["c_shoulder_y"]=(ROI_merged_data["r_shoulder_y"]+ROI_merged_data["l_shoulder_y"])/2
        ROI_merged_data["c_shoulder_z"]=(ROI_merged_data["r_shoulder_z"]+ROI_merged_data["l_shoulder_z"])/2
        ROI_merged_data["c_base_x"]=(ROI_merged_data["r_base_x"]+ROI_merged_data["l_base_x"])/2
        ROI_merged_data["c_base_y"]=(ROI_merged_data["r_base_y"]+ROI_merged_data["l_base_y"])/2
        ROI_merged_data["c_base_z"]=(ROI_merged_data["r_base_z"]+ROI_merged_data["l_base_z"])/2

        ROI_merged_data["r_trunk_angle_x"]=0 # 右半身で見るロール
        ROI_merged_data["r_trunk_angle_y"]=0 # 右半身で見るピッチ
        ROI_merged_data["l_trunk_angle_x"]=0 # 左半身
        ROI_merged_data["l_trunk_angle_y"]=0
        ROI_merged_data["c_trunk_angle_x"]=0 # 中央
        ROI_merged_data["c_trunk_angle_y"]=0
        ROI_merged_data["trunk_angle_z"]=0 # ヨー
        
        ROI_merged_data["r_trunk_angle_x"]=np.rad2deg(np.arctan((ROI_merged_data["r_shoulder_y"]-ROI_merged_data["r_base_y"])/(ROI_merged_data["r_shoulder_z"]-ROI_merged_data["r_base_z"])))
        ROI_merged_data["r_trunk_angle_y"]=np.rad2deg(np.arctan((ROI_merged_data["r_shoulder_x"]-ROI_merged_data["r_base_x"])/(ROI_merged_data["r_shoulder_z"]-ROI_merged_data["r_base_z"])))
        ROI_merged_data["l_trunk_angle_x"]=np.rad2deg(np.arctan((ROI_merged_data["l_shoulder_y"]-ROI_merged_data["l_base_y"])/(ROI_merged_data["l_shoulder_z"]-ROI_merged_data["l_base_z"])))
        ROI_merged_data["l_trunk_angle_y"]=np.rad2deg(np.arctan((ROI_merged_data["l_shoulder_x"]-ROI_merged_data["l_base_x"])/(ROI_merged_data["l_shoulder_z"]-ROI_merged_data["l_base_z"])))
        ROI_merged_data["c_trunk_angle_x"]=np.rad2deg(np.arctan((ROI_merged_data["c_shoulder_y"]-ROI_merged_data["c_base_y"])/(ROI_merged_data["c_shoulder_z"]-ROI_merged_data["c_base_z"])))
        ROI_merged_data["c_trunk_angle_y"]=np.rad2deg(np.arctan((ROI_merged_data["c_shoulder_x"]-ROI_merged_data["c_base_x"])/(ROI_merged_data["c_shoulder_z"]-ROI_merged_data["c_base_z"])))
        ROI_merged_data["s_trunk_angle_z"]=np.rad2deg(np.arctan((ROI_merged_data["r_shoulder_x"]-ROI_merged_data["l_shoulder_x"])/(ROI_merged_data["r_shoulder_y"]-ROI_merged_data["l_shoulder_y"])))
        ROI_merged_data["b_trunk_angle_z"]=np.rad2deg(np.arctan((ROI_merged_data["r_base_x"]-ROI_merged_data["l_base_x"])/(ROI_merged_data["r_base_y"]-ROI_merged_data["l_base_y"])))

        ROI_merged_data.dropna(subset=["hayashide_LThoraxAngles_Y","r_trunk_angle_y"],how="any",inplace=True)

        gs = GridSpec(3, 1)
        # plt.subplot(gs[0])    
        # plt.plot(ROI_merged_data["timestamp_x"],ROI_merged_data["hayashide_LThoraxAngles_X"],"o-",markersize=3,label="hayashide_LThoraxAngles_X")
        # plt.plot(ROI_merged_data["timestamp_x"],ROI_merged_data["r_trunk_angle_x"],"o-",markersize=3,label="r_trunk_angle_x")
        # # plt.plot(ROI_merged_data["timestamp_x"],ROI_merged_data["l_trunk_angle_x"],"o-",markersize=3,label="l_trunk_angle_x")
        # # plt.plot(ROI_merged_data["timestamp_x"],ROI_merged_data["c_trunk_angle_x"],"o-",markersize=3,label="c_trunk_angle_x")
        # plt.xlabel("Time $/it{t}$ [s]")
        # plt.ylabel("Roll of the trunk [deg]")
        # plt.legend()
        # plt.grid()
        plt.subplot(gs[1])   
        plt.plot(ROI_merged_data["timestamp_x"],ROI_merged_data["hayashide_LThoraxAngles_Y"],"o-",markersize=3,label="hayashide_LThoraxAngles_Y")
        plt.plot(ROI_merged_data["timestamp_x"],ROI_merged_data["r_trunk_angle_y"],"o-",markersize=3,label="r_trunk_angle_y")
        # plt.plot(ROI_merged_data["timestamp_x"],ROI_merged_data["l_trunk_angle_y"],"o-",markersize=3,label="l_trunk_angle_y")
        # plt.plot(ROI_merged_data["timestamp_x"],ROI_merged_data["c_trunk_angle_y"],"o-",markersize=3,label="c_trunk_angle_y")
        plt.xlabel("Time $/it{t}$ [s]")
        plt.ylabel("Pitch of the trunk [deg]")
        plt.legend()
        plt.grid()
        # plt.subplot(gs[2])   
        # plt.plot(ROI_merged_data["timestamp_x"],ROI_merged_data["hayashide_LThoraxAngles_Z"],"o-",markersize=3,label="hayashide_LThoraxAngles_Z")
        # plt.plot(ROI_merged_data["timestamp_x"],ROI_merged_data["s_trunk_angle_z"],"o-",markersize=3,label="s_trunk_angle_z")
        # # plt.plot(ROI_merged_data["timestamp_x"],ROI_merged_data["b_trunk_angle_z"],"o-",markersize=3,label="b_trunk_angle_z")
        # plt.xlabel("Time $/it{t}$ [s]")
        # plt.ylabel("Yaw of the trunk [deg]")
        # plt.legend()
        # plt.grid()
        plt.savefig(os.path.split(self.merged_data_path)[0]+"/"+os.path.basename(self.merged_data_path)[:-10]+"_trunk_ROI.png")
        plt.pause(1)
        plt.cla()
        # ファイル名，データ数，最大誤差，MAE，相関係数
        print(ROI_merged_data[["hayashide_LThoraxAngles_Y","r_trunk_angle_y"]].corr())
        output_data=[os.path.basename(self.merged_data_path),rel_dist_thre,len(ROI_merged_data),abs(ROI_merged_data["hayashide_LThoraxAngles_Y"]-ROI_merged_data["r_trunk_angle_y"]).max(),mean_absolute_error(ROI_merged_data["hayashide_LThoraxAngles_Y"],ROI_merged_data["r_trunk_angle_y"]),ROI_merged_data[["hayashide_LThoraxAngles_Y","r_trunk_angle_y"]].corr().values[0,1]]
        self.write_log(output_data=output_data,csvpath=path_management["vicon_humpback_table_path"])
    
    def analyze_hip_accuracy(self,rel_dist_thre=(5+0.6301867843887389)/2):
        # ROI_merged_data=self.merged_data[self.merged_data["relative_distance"]<rel_dist_thre]
        ROI_merged_data=self.extract_ROI(self.merged_data,rel_dist_thre=rel_dist_thre)
        print(ROI_merged_data)

        ROI_merged_data["r_hip_angle_x"]=0
        ROI_merged_data["r_hip_angle_y"]=0
        ROI_merged_data["r_hip_angle_z"]=0
        ROI_merged_data["l_hip_angle_x"]=0
        ROI_merged_data["l_hip_angle_y"]=0
        ROI_merged_data["l_hip_angle_z"]=0
        ROI_merged_data["r_hip_angle_x"]=np.rad2deg(np.arctan((ROI_merged_data["r_knee_y"]-ROI_merged_data["r_base_y"])/(ROI_merged_data["r_knee_z"]-ROI_merged_data["r_base_z"])))
        ROI_merged_data["r_hip_angle_y"]=np.rad2deg(np.arctan((ROI_merged_data["r_knee_x"]-ROI_merged_data["r_base_x"])/(ROI_merged_data["r_knee_z"]-ROI_merged_data["r_base_z"])))
        ROI_merged_data["r_hip_angle_z"]=np.rad2deg(np.arctan((ROI_merged_data["r_knee_y"]-ROI_merged_data["r_base_y"])/(ROI_merged_data["r_knee_x"]-ROI_merged_data["r_base_x"])))
        ROI_merged_data["l_hip_angle_x"]=np.rad2deg(np.arctan((ROI_merged_data["l_knee_y"]-ROI_merged_data["l_base_y"])/(ROI_merged_data["l_knee_z"]-ROI_merged_data["l_base_z"])))
        ROI_merged_data["l_hip_angle_y"]=np.rad2deg(np.arctan((ROI_merged_data["l_knee_x"]-ROI_merged_data["l_base_x"])/(ROI_merged_data["l_knee_z"]-ROI_merged_data["l_base_z"])))
        ROI_merged_data["l_hip_angle_z"]=np.rad2deg(np.arctan((ROI_merged_data["l_knee_y"]-ROI_merged_data["l_base_y"])/(ROI_merged_data["l_knee_x"]-ROI_merged_data["l_base_x"])))

        # トレンド除去
        # self.tf_data["r_hip_angle_y_trend"]=0
        # self.tf_data["r_hip_angle_y_detrend"]=0

        # self.tf_data["r_hip_angle_y_detrend"]=signal.detrend(self.tf_data["r_hip_angle_y"])
        # self.tf_data["r_hip_angle_y_trend"]=self.tf_data["r_hip_angle_y"]-self.tf_data["r_hip_angle_y_detrend"]

        gs = GridSpec(3, 1)
        plt.subplot(gs[0])    
        plt.plot(ROI_merged_data["timestamp_x"],ROI_merged_data["hayashide_RHipAngles_X"],"o-",markersize=3,label="hayashide_RHipAngles_X")
        plt.plot(ROI_merged_data["timestamp_x"],ROI_merged_data["r_hip_angle_y"],"o-",markersize=3,label="r_hip_angle_y")
        # plt.plot(ROI_merged_data["timestamp_x"],ROI_merged_data["r_hip_angle_x"],"o-",markersize=3,label="r_hip_angle_x")
        # plt.plot(ROI_merged_data["timestamp_x"],ROI_merged_data["l_hip_angle_x"],"o-",markersize=3,label="l_hip_angle_x")
        plt.xlabel("Time $/it{t}$ [s]")
        plt.ylabel("Hip angle in (hallway width direction) th_x [deg]")
        plt.legend()
        # plt.grid()
        # plt.subplot(gs[1])   
        # plt.plot(ROI_merged_data["timestamp_x"],ROI_merged_data["hayashide_RHipAngles_Y"],"o-",markersize=3,label="hayashide_RHipAngles_Y")
        # plt.plot(ROI_merged_data["timestamp_x"],ROI_merged_data["r_hip_angle_y_detrend"],"o-",markersize=3,label="r_hip_angle_y_detrend")
        # plt.plot(ROI_merged_data["timestamp_x"],ROI_merged_data["l_hip_angle_y"],"o-",markersize=3,label="l_hip_angle_y")
        # plt.xlabel("Time $/it{t}$ [s]")
        # plt.ylabel("Hip angle in (hallway direction) th_y [deg]")
        # plt.legend()
        # plt.grid()
        # plt.subplot(gs[2])   
        # plt.plot(ROI_merged_data["timestamp_x"],ROI_merged_data["hayashide_RHipAngles_Z"],"o-",markersize=3,label="hayashide_RHipAnglesZ")
        # plt.plot(ROI_merged_data["timestamp_x"],ROI_merged_data["r_hip_angle_z"],"o-",markersize=3,label="r_hip_angle_z")
        # plt.plot(ROI_merged_data["timestamp_x"],ROI_merged_data["l_hip_angle_z"],"o-",markersize=3,label="l_hip_angle_z")
        # plt.xlabel("Time $/it{t}$ [s]")
        # plt.ylabel("Hip angle in (yaw direction) th_z [deg]")
        # plt.legend()
        # plt.grid()
        # plt.savefig(self.savedirpath+"/"+os.path.basename(self.arctan((ROI_merged_data["r_base_x"]-ROI_merged_data["l_base_x"])/(ROI_merged_data["r_base_y"]-ROI_merged_data["l_base_y"]))))

        ROI_merged_data.dropna(subset=["hayashide_RHipAngles_X","r_hip_angle_y"],how="any",inplace=True)
        plt.savefig(os.path.split(self.merged_data_path)[0]+"/"+os.path.basename(self.merged_data_path)[:-10]+"_hip_ROI.png")
        plt.pause(1)
        plt.cla()
        try:
            output_data=[os.path.basename(self.merged_data_path),rel_dist_thre,len(ROI_merged_data),abs(ROI_merged_data["hayashide_RHipAngles_X"]-ROI_merged_data["r_hip_angle_y"]).max(),mean_absolute_error(ROI_merged_data["hayashide_RHipAngles_X"],ROI_merged_data["r_hip_angle_y"]),ROI_merged_data[["hayashide_RHipAngles_X","r_hip_angle_y"]].corr().values[0,1]]
            self.write_log(output_data=output_data,csvpath=path_management["vicon_hip_table_path"])
        except ValueError:
            pass

    def main(self):
        self.analyze_hip_accuracy()
        self.analyze_humpback_accuracy()

tfodomdirpaths=sorted(glob("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-20*"))
for tfodomidirpath in tfodomdirpaths:
    print(tfodomidirpath)
    print(sorted(glob(tfodomidirpath+"/*_merged.csv")))
    try:
        merged_data_path=sorted(glob(tfodomidirpath+"/*_merged.csv"))[0]
    except IndexError:
        continue
    aaa=analysisAngleAccuracy(merged_data_path=merged_data_path)
    aaa.main()