#! /usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from glob import glob
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import pandas as pd
from pprint import pprint
import pickle
from noise_processor import *
from analysis_management import *
from analysis_initial_processor import *
from scipy import signal


class wholeBody():
    def __init__(self):
        path_management,csv_labels,color_dict=management_initial()
        plt.rcParams["figure.figsize"] = (10,8)
        plt.rcParams["figure.autolayout"] = True
        plt.rcParams['font.family'] = 'Times New Roman'

        # tf_data
        try:
            self.tfcsvpath=sys.argv[1]
        except Exception:
            self.tfcsvpath="/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-19-20-10-31/_2023-12-19-20-10-31_tf_raw.csv"
        self.savedirpath=os.path.split(self.tfcsvpath)[0]
        tf_data=initial_processor(self.tfcsvpath,False)
        timestamp_xm5_closest_idx=(tf_data["gravity_x"]-(-5)).abs().idxmin()
        timestamp_xm5_closest=tf_data.iloc[timestamp_xm5_closest_idx]["timestamp"]
        # x_x0_closest=tf_data.iloc[timestamp_x0_closest_idx]["gravity_x"]
        tf_data=tf_data[tf_data["timestamp"]<timestamp_xm5_closest]
        timestamp_x8_closest_idx=(tf_data["gravity_x"]-8).abs().idxmin()
        timestamp_x8_closest=tf_data.iloc[timestamp_x8_closest_idx]["timestamp"]
        # x_x8_closest=tf_data.iloc[timestamp_x8_closest_idx]["gravity_x"]
        tf_data=tf_data[tf_data["timestamp"]>timestamp_x8_closest]
        tf_data=tf_data.reset_index()
        self.tf_data=tf_data

        # oddata
        try:
            self.odomcsvpath=sys.argv[2]
        except Exception:
            self.odomcsvpath="/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-19-20-10-31/_2023-12-19-20-10-31_od_raw.csv"
        # odom_data=pd.read_csv(self.odomcsvpath,header=0,names=csv_labels["odometry"])
        odom_data=initial_processor(self.odomcsvpath,False)
        self.odom_data=odom_data

    def plot_gravity(self):
        gs = GridSpec(2, 2, width_ratios=[1,1])
        plt.subplot(gs[0,:])    
        plt.plot(self.tf_data["gravity_x"],self.tf_data["gravity_y"],"o-",markersize=3,label="gravity")
        plt.plot(self.odom_data["x"],self.odom_data["y"],"^-",markersize=3,label="robot")
        plt.legend()
        plt.xlabel("Hallway direction $/it{x}$ [m]")
        plt.ylabel("Width direction $/it{y}$ [m]")
        plt.gca().set_aspect('equal', adjustable='box')
        plt.subplot(gs[1,0])    
        plt.plot(self.tf_data["timestamp"],self.tf_data["gravity_x"],"o-",markersize=3,label="gravity_x")
        plt.plot(self.odom_data["t"],self.odom_data["x"],"^-",markersize=3,label="robot_x")
        plt.legend()
        plt.xlabel("Time $/it{t}$ [s]")
        plt.ylabel("Hallway direction $/it{x}$ [m]")
        plt.subplot(gs[1,1])    
        plt.plot(self.tf_data["timestamp"],self.tf_data["gravity_y"],"o-",markersize=3,label="gravity_y")
        plt.plot(self.odom_data["t"],self.odom_data["y"],"^-",markersize=3,label="robot_y")
        plt.legend()
        plt.xlabel("Time $\it{t}$ [s]")
        plt.ylabel("Hallway direction $\it{y}$ [m]")
        plt.savefig(self.savedirpath+"/"+os.path.basename(self.tfcsvpath)[:-11]+"_gravity_trim")
        plt.cla()

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

    def get_velocity(self):
        best_err=100
        best_start_x=0
        best_start_t=0
        best_end_x=0
        best_end_t=0
        for idx,row in self.tf_data.iterrows():
            start_x=row["gravity_x"]
            start_t=row["timestamp"]
            end_idx=((start_x-self.tf_data["gravity_x"])-(5)).abs().idxmin()
            end_x=self.tf_data.iloc[end_idx]["gravity_x"]
            end_t=self.tf_data.iloc[end_idx]["timestamp"]
            # print(start_x,end_x)
            if abs(start_x-end_x-5)<best_err:
                best_err=abs(start_x-end_x-5)
                best_start_x=start_x
                best_start_t=start_t
                best_end_x=end_x
                best_end_t=end_t
        self.write_log([os.path.basename(self.tfcsvpath),(best_end_x-best_start_x)/(best_end_t-best_start_t),best_err,best_start_x,best_start_t,best_end_x,best_end_t],path_management["velocity_csv_path"], fmt="%s")
        print(os.path.basename(self.tfcsvpath),(best_end_x-best_start_x)/(best_end_t-best_start_t),best_err,best_start_x,best_start_t,best_end_x,best_end_t)

    def get_stride(self):
        data=self.tf_data
        data["r_foot_vx"]=0
        try:
            data["r_foot_vx"].iloc[:-1]=(data["r_foot_x"].values[1:]-data["r_foot_x"].values[:-1])/(data["timestamp"].values[1:]-data["timestamp"].values[:-1])
        except ValueError:
            data["r_foot_vx"]=(data["r_foot_x"].values[1:]-data["r_foot_x"].values[:-1])/(data["timestamp"].values[1:]-data["timestamp"].values[:-1])

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
        plt.savefig(os.path.split(self.tfcsvpath)[0]+"/"+os.path.basename(self.tfcsvpath)[:-8]+"_stride.png")
        # plt.show()
        print(clusterdata["stride"].iloc[1:].mean())
        print(clusterdata["stride"].iloc[1:].median())
        print(clusterdata["stride"].iloc[1:].std())
        self.write_log([os.path.basename(self.tfcsvpath),clusterdata["stride"].iloc[1:].mean(),clusterdata["stride"].iloc[1:].median(),clusterdata["stride"].iloc[1:].std(),clusterdata["stride"].iloc[1:].min(),clusterdata["stride"].iloc[1:].max()],path_management["stride_csv_path"],fmt="%s")
        clusterdata.to_csv(os.path.split(self.tfcsvpath)[0]+"/"+os.path.basename(self.tfcsvpath)[:-8]+"_stride.csv",index=False)


    def plot_head_angle(self):
        """
        体幹のロール・ピッチ・ヨーを求める
        """

        self.tf_data["ear_head_angle_x"]=0 # 耳で見るロール
        self.tf_data["eye_head_angle_x"]=0 # 目で見るロール
        self.tf_data["r_ear_head_angle_y"]=0 # 右耳と鼻で見るピッチ
        self.tf_data["l_ear_head_angle_y"]=0 # 左耳と鼻で見るピッチ
        self.tf_data["r_eye_head_angle_y"]=0 # 右目と鼻で見るピッチ
        self.tf_data["l_eye_head_angle_y"]=0 # 左目と鼻で見るピッチ
        self.tf_data["ear_head_angle_z"]=0 # 耳で見るヨー
        self.tf_data["eye_head_angle_z"]=0 # 目で見るヨー
        
        self.tf_data["ear_head_angle_x"]=np.rad2deg(np.arctan((self.tf_data["r_ear_z"]-self.tf_data["l_ear_z"])/(self.tf_data["r_ear_y"]-self.tf_data["l_ear_y"])))
        self.tf_data["eye_head_angle_x"]=np.rad2deg(np.arctan((self.tf_data["r_eye_z"]-self.tf_data["l_eye_z"])/(self.tf_data["r_eye_y"]-self.tf_data["l_eye_y"])))
        self.tf_data["r_ear_head_angle_y"]=np.rad2deg(np.arctan((self.tf_data["nose_z"]-self.tf_data["r_ear_z"])/(self.tf_data["nose_x"]-self.tf_data["r_ear_x"])))
        self.tf_data["l_ear_head_angle_y"]=np.rad2deg(np.arctan((self.tf_data["nose_z"]-self.tf_data["l_ear_z"])/(self.tf_data["nose_x"]-self.tf_data["l_ear_x"])))
        self.tf_data["r_eye_head_angle_y"]=np.rad2deg(np.arctan((self.tf_data["nose_z"]-self.tf_data["r_eye_z"])/(self.tf_data["nose_x"]-self.tf_data["r_eye_x"])))
        self.tf_data["l_eye_head_angle_y"]=np.rad2deg(np.arctan((self.tf_data["nose_z"]-self.tf_data["l_eye_z"])/(self.tf_data["nose_x"]-self.tf_data["l_eye_x"])))
        self.tf_data["ear_head_angle_z"]=np.rad2deg(np.arctan((self.tf_data["r_ear_x"]-self.tf_data["l_ear_x"])/(self.tf_data["r_ear_y"]-self.tf_data["l_ear_y"])))
        self.tf_data["eye_head_angle_z"]=np.rad2deg(np.arctan((self.tf_data["r_eye_x"]-self.tf_data["l_eye_x"])/(self.tf_data["r_eye_y"]-self.tf_data["l_eye_y"])))

        gs = GridSpec(3, 1)
        plt.subplot(gs[0])    
        plt.plot(self.tf_data["timestamp"],self.tf_data["ear_head_angle_x"],"o-",markersize=3,label="ear_head_angle_x")
        plt.plot(self.tf_data["timestamp"],self.tf_data["eye_head_angle_x"],"o-",markersize=3,label="eye_head_angle_x")
        plt.xlabel("Time $/it{t}$ [s]")
        plt.ylabel("Roll of the head [deg]")
        plt.legend()
        plt.grid()
        plt.subplot(gs[1])   
        plt.plot(self.tf_data["timestamp"],self.tf_data["r_ear_head_angle_y"],"o-",markersize=3,label="r_ear_head_angle_y")
        plt.plot(self.tf_data["timestamp"],self.tf_data["l_ear_head_angle_y"],"o-",markersize=3,label="l_ear_head_angle_y")
        plt.plot(self.tf_data["timestamp"],self.tf_data["r_eye_head_angle_y"],"o-",markersize=3,label="r_eye_head_angle_y")
        plt.plot(self.tf_data["timestamp"],self.tf_data["l_eye_head_angle_y"],"o-",markersize=3,label="l_eye_head_angle_y")
        plt.xlabel("Time $/it{t}$ [s]")
        plt.ylabel("Pitch of the head [deg]")
        plt.legend()
        plt.grid()
        plt.subplot(gs[2])   
        plt.plot(self.tf_data["timestamp"],self.tf_data["ear_head_angle_z"],"o-",markersize=3,label="ear_head_angle_z")
        plt.plot(self.tf_data["timestamp"],self.tf_data["eye_head_angle_z"],"o-",markersize=3,label="eye_head_angle_z")
        plt.xlabel("Time $/it{t}$ [s]")
        plt.ylabel("Yaw of the head [deg]")
        plt.legend()
        plt.grid()
        plt.savefig(self.savedirpath+"/"+os.path.basename(self.tfcsvpath)[:-11]+"_head_angle")
        plt.cla()
        
        pass

    def plot_trunk_angle(self):
        """
        体幹のロール・ピッチ・ヨーを求める
        """
        self.tf_data["c_shoulder_x"]=0
        self.tf_data["c_shoulder_y"]=0
        self.tf_data["c_shoulder_z"]=0
        self.tf_data["c_base_x"]=0
        self.tf_data["c_base_y"]=0
        self.tf_data["c_base_z"]=0
        self.tf_data["c_shoulder_x"]=(self.tf_data["r_shoulder_x"]+self.tf_data["l_shoulder_x"])/2
        self.tf_data["c_shoulder_y"]=(self.tf_data["r_shoulder_y"]+self.tf_data["l_shoulder_y"])/2
        self.tf_data["c_shoulder_z"]=(self.tf_data["r_shoulder_z"]+self.tf_data["l_shoulder_z"])/2
        self.tf_data["c_base_x"]=(self.tf_data["r_base_x"]+self.tf_data["l_base_x"])/2
        self.tf_data["c_base_y"]=(self.tf_data["r_base_y"]+self.tf_data["l_base_y"])/2
        self.tf_data["c_base_z"]=(self.tf_data["r_base_z"]+self.tf_data["l_base_z"])/2

        self.tf_data["r_trunk_angle_x"]=0 # 右半身で見るロール
        self.tf_data["r_trunk_angle_y"]=0 # 右半身で見るピッチ
        self.tf_data["l_trunk_angle_x"]=0 # 左半身
        self.tf_data["l_trunk_angle_y"]=0
        self.tf_data["c_trunk_angle_x"]=0 # 中央
        self.tf_data["c_trunk_angle_y"]=0
        self.tf_data["trunk_angle_z"]=0 # ヨー
        
        self.tf_data["r_trunk_angle_x"]=np.rad2deg(np.arctan((self.tf_data["r_shoulder_y"]-self.tf_data["r_base_y"])/(self.tf_data["r_shoulder_z"]-self.tf_data["r_base_z"])))
        self.tf_data["r_trunk_angle_y"]=np.rad2deg(np.arctan((self.tf_data["r_shoulder_x"]-self.tf_data["r_base_x"])/(self.tf_data["r_shoulder_z"]-self.tf_data["r_base_z"])))
        self.tf_data["l_trunk_angle_x"]=np.rad2deg(np.arctan((self.tf_data["l_shoulder_y"]-self.tf_data["l_base_y"])/(self.tf_data["l_shoulder_z"]-self.tf_data["l_base_z"])))
        self.tf_data["l_trunk_angle_y"]=np.rad2deg(np.arctan((self.tf_data["l_shoulder_x"]-self.tf_data["l_base_x"])/(self.tf_data["l_shoulder_z"]-self.tf_data["l_base_z"])))
        self.tf_data["c_trunk_angle_x"]=np.rad2deg(np.arctan((self.tf_data["c_shoulder_y"]-self.tf_data["c_base_y"])/(self.tf_data["c_shoulder_z"]-self.tf_data["c_base_z"])))
        self.tf_data["c_trunk_angle_y"]=np.rad2deg(np.arctan((self.tf_data["c_shoulder_x"]-self.tf_data["c_base_x"])/(self.tf_data["c_shoulder_z"]-self.tf_data["c_base_z"])))
        self.tf_data["s_trunk_angle_z"]=np.rad2deg(np.arctan((self.tf_data["r_shoulder_x"]-self.tf_data["l_shoulder_x"])/(self.tf_data["r_shoulder_y"]-self.tf_data["l_shoulder_y"])))
        self.tf_data["b_trunk_angle_z"]=np.rad2deg(np.arctan((self.tf_data["r_base_x"]-self.tf_data["l_base_x"])/(self.tf_data["r_base_y"]-self.tf_data["l_base_y"])))

        gs = GridSpec(3, 1)
        plt.subplot(gs[0])    
        plt.plot(self.tf_data["timestamp"],self.tf_data["r_trunk_angle_x"],"o-",markersize=3,label="r_trunk_angle_x")
        plt.plot(self.tf_data["timestamp"],self.tf_data["l_trunk_angle_x"],"o-",markersize=3,label="l_trunk_angle_x")
        plt.plot(self.tf_data["timestamp"],self.tf_data["c_trunk_angle_x"],"o-",markersize=3,label="c_trunk_angle_x")
        plt.xlabel("Time $/it{t}$ [s]")
        plt.ylabel("Roll of the trunk [deg]")
        plt.legend()
        plt.grid()
        plt.subplot(gs[1])   
        plt.plot(self.tf_data["timestamp"],self.tf_data["r_trunk_angle_y"],"o-",markersize=3,label="r_trunk_angle_y")
        plt.plot(self.tf_data["timestamp"],self.tf_data["l_trunk_angle_y"],"o-",markersize=3,label="l_trunk_angle_y")
        plt.plot(self.tf_data["timestamp"],self.tf_data["c_trunk_angle_y"],"o-",markersize=3,label="c_trunk_angle_y")
        plt.xlabel("Time $/it{t}$ [s]")
        plt.ylabel("Pitch of the trunk [deg]")
        plt.legend()
        plt.grid()
        plt.subplot(gs[2])   
        plt.plot(self.tf_data["timestamp"],self.tf_data["s_trunk_angle_z"],"o-",markersize=3,label="s_trunk_angle_z")
        plt.plot(self.tf_data["timestamp"],self.tf_data["b_trunk_angle_z"],"o-",markersize=3,label="b_trunk_angle_z")
        plt.xlabel("Time $/it{t}$ [s]")
        plt.ylabel("Yaw of the trunk [deg]")
        plt.legend()
        plt.grid()
        plt.savefig(self.savedirpath+"/"+os.path.basename(self.tfcsvpath)[:-11]+"_trunk_angle")
        plt.cla()

        self.write_log([os.path.basename(self.tfcsvpath),self.tf_data["c_trunk_angle_y"].mean(),self.tf_data["c_trunk_angle_y"].median(),self.tf_data["c_trunk_angle_y"].std(),self.tf_data["c_trunk_angle_y"].min(),self.tf_data["c_trunk_angle_y"].max()],path_management["humpback_csv_path"],fmt="%s")
        pass

    def plot_knee_angle(self):
        """
        股関節の前後進展角度を求める
        """
        self.tf_data["r_hip_angle_x"]=0
        self.tf_data["r_hip_angle_y"]=0
        self.tf_data["r_hip_angle_z"]=0
        self.tf_data["l_hip_angle_x"]=0
        self.tf_data["l_hip_angle_y"]=0
        self.tf_data["l_hip_angle_z"]=0
        self.tf_data["r_hip_angle_x"]=np.rad2deg(np.arctan((self.tf_data["r_knee_y"]-self.tf_data["r_base_y"])/(self.tf_data["r_knee_z"]-self.tf_data["r_base_z"])))
        self.tf_data["r_hip_angle_y"]=np.rad2deg(np.arctan((self.tf_data["r_knee_x"]-self.tf_data["r_base_x"])/(self.tf_data["r_knee_z"]-self.tf_data["r_base_z"])))
        self.tf_data["r_hip_angle_z"]=np.rad2deg(np.arctan((self.tf_data["r_knee_y"]-self.tf_data["r_base_y"])/(self.tf_data["r_knee_x"]-self.tf_data["r_base_x"])))
        self.tf_data["l_hip_angle_x"]=np.rad2deg(np.arctan((self.tf_data["l_knee_y"]-self.tf_data["l_base_y"])/(self.tf_data["l_knee_z"]-self.tf_data["l_base_z"])))
        self.tf_data["l_hip_angle_y"]=np.rad2deg(np.arctan((self.tf_data["l_knee_x"]-self.tf_data["l_base_x"])/(self.tf_data["l_knee_z"]-self.tf_data["l_base_z"])))
        self.tf_data["l_hip_angle_z"]=np.rad2deg(np.arctan((self.tf_data["l_knee_y"]-self.tf_data["l_base_y"])/(self.tf_data["l_knee_x"]-self.tf_data["l_base_x"])))

        gs = GridSpec(3, 1)
        plt.subplot(gs[0])    
        plt.plot(self.tf_data["timestamp"],self.tf_data["r_hip_angle_x"],"o-",markersize=3,label="r_hip_angle_x")
        plt.plot(self.tf_data["timestamp"],self.tf_data["l_hip_angle_x"],"o-",markersize=3,label="l_hip_angle_x")
        plt.xlabel("Time $/it{t}$ [s]")
        plt.ylabel("Hip angle in (hallway width direction) th_x [deg]")
        plt.legend()
        plt.grid()
        plt.subplot(gs[1])   
        plt.plot(self.tf_data["timestamp"],self.tf_data["r_hip_angle_y"],"o-",markersize=3,label="r_hip_angle_y")
        plt.plot(self.tf_data["timestamp"],self.tf_data["l_hip_angle_y"],"o-",markersize=3,label="l_hip_angle_y")
        plt.xlabel("Time $/it{t}$ [s]")
        plt.ylabel("Hip angle in (hallway direction) th_y [deg]")
        plt.legend()
        plt.grid()
        plt.subplot(gs[2])   
        plt.plot(self.tf_data["timestamp"],self.tf_data["r_hip_angle_z"],"o-",markersize=3,label="r_hip_angle_z")
        plt.plot(self.tf_data["timestamp"],self.tf_data["l_hip_angle_z"],"o-",markersize=3,label="l_hip_angle_z")
        plt.xlabel("Time $/it{t}$ [s]")
        plt.ylabel("Hip angle in (yaw direction) th_z [deg]")
        plt.legend()
        plt.grid()
        plt.savefig(self.savedirpath+"/"+os.path.basename(self.tfcsvpath)[:-11]+"_knee_angle.png")
        plt.cla()
        pass

    def plot_base_elevation(self):
        plt.plot(self.tf_data["timestamp"],self.tf_data["r_base_z"]-self.tf_data["l_base_z"],"o-",markersize=3,label="base_z(r-l)")
        plt.xlabel("Time $/it{t}$ [s]")
        plt.ylabel("Hip position difference [m]")
        plt.legend()
        plt.grid()
        plt.savefig(self.savedirpath+"/"+os.path.basename(self.tfcsvpath)[:-11]+"_base_elevation")
        plt.cla()



    def main(self):
        self.plot_gravity()
<<<<<<< HEAD
=======
        self.get_velocity()
        self.get_stride()
>>>>>>> 141b0383c7a8309af8d74255ccb153f8e5944fc1
        # self.plot_knee_angle()
        # self.plot_base_elevation()
        self.plot_trunk_angle()
        # self.plot_head_angle()

wb=wholeBody()
wb.main()