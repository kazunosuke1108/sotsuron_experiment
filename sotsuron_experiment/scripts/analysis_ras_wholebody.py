#! /usr/bin/python3
# -*- coding: utf-8 -*-

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
        self.tfcsvpath="/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-11-11-55-46/_2023-12-11-11-55-46_tf_raw.csv"
        self.savedirpath=os.path.split(self.tfcsvpath)[0]
        tf_data=initial_processor(self.tfcsvpath,True)
        timestamp_x5_closest_idx=(tf_data["gravity_x"]-5).abs().idxmin()
        timestamp_x5_closest=tf_data.iloc[timestamp_x5_closest_idx]["timestamp"]
        x_x5_closest=tf_data.iloc[timestamp_x5_closest_idx]["gravity_x"]
        timestamp_x0_closest_idx=(tf_data[tf_data["timestamp"]>timestamp_x5_closest]["gravity_x"]-0).abs().idxmin()
        timestamp_x0_closest=tf_data.iloc[timestamp_x0_closest_idx]["timestamp"]
        x_x0_closest=tf_data.iloc[timestamp_x0_closest_idx]["gravity_x"]
        tf_data=tf_data[tf_data["timestamp"]>timestamp_x5_closest]
        tf_data=tf_data[tf_data["timestamp"]<timestamp_x0_closest]
        self.tf_data=tf_data

        # oddata
        self.odomcsvpath="/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-11-11-55-46/_2023-12-11-11-55-46_od_raw.csv"
        odom_data=pd.read_csv(self.odomcsvpath,header=0,names=csv_labels["odometry"])
        self.odom_data=odom_data

    def plot_gravity(self):
        gs = GridSpec(2, 2, width_ratios=[1,1])
        plt.subplot(gs[0,:])    
        plt.plot(self.tf_data["gravity_x"],self.tf_data["gravity_y"],"o-",markersize=3,label="gravity")
        plt.plot(self.odom_data["x"],self.odom_data["y"],"^-",markersize=3,label="robot")
        plt.legend()
        plt.xlabel("Hallway direction $\it{x}$ [m]")
        plt.ylabel("Width direction $\it{y}$ [m]")
        plt.gca().set_aspect('equal', adjustable='box')
        plt.subplot(gs[1,0])    
        plt.plot(self.tf_data["timestamp"],self.tf_data["gravity_x"],"o-",markersize=3,label="gravity_x")
        plt.plot(self.odom_data["t"],self.odom_data["x"],"^-",markersize=3,label="robot_x")
        plt.legend()
        plt.xlabel("Time $\it{t}$ [s]")
        plt.ylabel("Hallway direction $\it{x}$ [m]")
        plt.subplot(gs[1,1])    
        plt.plot(self.tf_data["timestamp"],self.tf_data["gravity_y"],"o-",markersize=3,label="gravity_y")
        plt.plot(self.odom_data["t"],self.odom_data["y"],"^-",markersize=3,label="robot_y")
        plt.legend()
        plt.xlabel("Time $\it{t}$ [s]")
        plt.ylabel("Hallway direction $\it{y}$ [m]")
        plt.savefig(self.savedirpath+"/"+os.path.basename(self.tfcsvpath)[:-11]+"_gravity")
        plt.cla()
    
    def plot_hip(self):
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
        plt.xlabel("Time $\it{t}$ [s]")
        plt.ylabel("Hip angle in (hallway width direction) th_x [deg]")
        plt.legend()
        plt.grid()
        plt.subplot(gs[1])   
        plt.plot(self.tf_data["timestamp"],self.tf_data["r_hip_angle_y"],"o-",markersize=3,label="r_hip_angle_y")
        plt.plot(self.tf_data["timestamp"],self.tf_data["l_hip_angle_y"],"o-",markersize=3,label="l_hip_angle_y")
        plt.xlabel("Time $\it{t}$ [s]")
        plt.ylabel("Hip angle in (hallway direction) th_y [deg]")
        plt.legend()
        plt.grid()
        plt.subplot(gs[2])   
        plt.plot(self.tf_data["timestamp"],self.tf_data["r_hip_angle_z"],"o-",markersize=3,label="r_hip_angle_z")
        plt.plot(self.tf_data["timestamp"],self.tf_data["l_hip_angle_z"],"o-",markersize=3,label="l_hip_angle_z")
        plt.xlabel("Time $\it{t}$ [s]")
        plt.ylabel("Hip angle in (yaw direction) th_z [deg]")
        plt.legend()
        plt.grid()
        plt.savefig(self.savedirpath+"/"+os.path.basename(self.tfcsvpath)[:-11]+"_hip")
        plt.cla()
        pass


    def main(self):
        # self.plot_gravity()
        self.plot_hip()

wb=wholeBody()
wb.main()