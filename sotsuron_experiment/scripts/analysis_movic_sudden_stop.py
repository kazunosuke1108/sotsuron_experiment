import numpy as np
import pandas as pd
from glob import glob
import matplotlib.pyplot as plt

from analysis_management import *
from noise_processor import *

class AnalyzeSuddenStop():
    def __init__(self,results_dir_path="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/20240204_04"):
        self.path_management,self.csv_labels,self.color_dict=management_initial()
        plt.rcParams["figure.figsize"] = (15,10)
        plt.rcParams["figure.autolayout"] = True
        plt.rcParams['font.family'] = 'Times New Roman'
        self.png_prefix="ROI"

        self.results_dir_path=results_dir_path
        self.base_accurate_imu_csv_path=self.results_dir_path+"/hsrb/base_accurate_imu_1.csv"
        self.base_imu_csv_path=self.results_dir_path+"/hsrb/base_imu_1.csv"
        self.head_imu_csv_path=self.results_dir_path+"/hsrb/imu_1.csv"
        self.zed_imu_csv_path=self.results_dir_path+"/zed/imu_1.csv"
        self.odom_csv_path=self.results_dir_path+"/hsrb/odom_1.csv"
        self.command_velocity_csv_path=self.results_dir_path+"/hsrb/command_velocity_1.csv"

    def load_data(self):
        try:
            self.command_velocity_data=pd.read_csv(self.command_velocity_csv_path,names=self.csv_labels["command_velocity"])
        except FileNotFoundError:
            pass
        start_timestamp=self.command_velocity_data["timestamp"].min()-0.5
        end_timestamp=self.command_velocity_data["timestamp"].max()+2
        try:
            self.base_accurate_imu_data=pd.read_csv(self.base_accurate_imu_csv_path,names=self.csv_labels["imu"])
            self.base_accurate_imu_data=self.base_accurate_imu_data[self.base_accurate_imu_data["timestamp"]>=start_timestamp]
            self.base_accurate_imu_data=self.base_accurate_imu_data[self.base_accurate_imu_data["timestamp"]<=end_timestamp]
        except FileNotFoundError:
            pass
        try:
            self.base_imu_data=pd.read_csv(self.base_imu_csv_path,names=self.csv_labels["imu"])
            self.base_imu_data=self.base_imu_data[self.base_imu_data["timestamp"]>=start_timestamp]
            self.base_imu_data=self.base_imu_data[self.base_imu_data["timestamp"]<=end_timestamp]
        except FileNotFoundError:
            pass
        try:
            self.head_imu_data=pd.read_csv(self.head_imu_csv_path,names=self.csv_labels["imu"])
            self.head_imu_data=self.head_imu_data[self.head_imu_data["timestamp"]>=start_timestamp]
            self.head_imu_data=self.head_imu_data[self.head_imu_data["timestamp"]<=end_timestamp]
        except FileNotFoundError:
            pass
        try:
            self.zed_imu_data=pd.read_csv(self.zed_imu_csv_path,names=self.csv_labels["imu"])
            self.zed_imu_data=self.zed_imu_data[self.zed_imu_data["timestamp"]>=start_timestamp]
            self.zed_imu_data=self.zed_imu_data[self.zed_imu_data["timestamp"]<=end_timestamp]
        except FileNotFoundError:
            pass
        try:
            self.zed_imu_data=self.zed_imu_data[self.zed_imu_data["timestamp"]!=self.zed_imu_data["timestamp"].min()] # 362行目にzeroが入ってたので消去
        except FileNotFoundError:
            pass
        try:
            self.odom_data=pd.read_csv(self.odom_csv_path,names=self.csv_labels["odometry"])
            self.odom_data=self.odom_data[self.odom_data["timestamp"]>=start_timestamp]
            self.odom_data=self.odom_data[self.odom_data["timestamp"]<=end_timestamp]
        except FileNotFoundError:
            pass


        

    def plot_imu(self,data,data_name):
        plt.plot(data["timestamp"],data["lin_acc_x"],"r",label="lin_acc_x(accurate)")
        # plt.plot(base_imu_data["timestamp"],base_imu_data["lin_acc_x"],"",label="lin_acc_x")
        plt.plot(data["timestamp"],data["lin_acc_y"],"g",label="lin_acc_y(accurate)")
        plt.plot(data["timestamp"],data["lin_acc_z"],"b",label="lin_acc_z(accurate)")
        plt.legend()
        plt.grid()
        plt.xlabel("Time $\it{t}$ [s]")
        plt.ylabel("Acceleration $\it{a}$ [m/s$^{2}$]")
        plt.title(data_name+" "+os.path.basename(self.results_dir_path))
        plt.savefig(self.results_dir_path+f"/{data_name}_{self.png_prefix}.png")
        plt.cla()

    def plot_odom(self,data,data_name):
        # print(np.mean(data["timestamp"].values[1:]-data["timestamp"].values[:-1]))
        # print(np.std(data["timestamp"].values[1:]-data["timestamp"].values[:-1]))
        # print(np.min(data["timestamp"].values[1:]-data["timestamp"].values[:-1]))
        # print(np.max(data["timestamp"].values[1:]-data["timestamp"].values[:-1]))
        # plt.hist(data["timestamp"].values[1:]-data["timestamp"].values[:-1])
        plt.cla()
        # raise TimeoutError
        # data=resampling_processor(data)
        data=vel_processor(data)
        fig,ax1=plt.subplots()
        ax1.plot(data["timestamp"],data["x"],"r",label="$\it{x}$")
        ax1.plot(data["timestamp"],data["y"],"g",label="$\it{y}$")
        ax1.plot(data["timestamp"],data["theta"],"b",label=r"$\theta$")
        ax1.plot(data["timestamp"],data["pan"],"c",label="$\phi$")
        ax1.legend(loc="upper left")
        ax1.grid()
        ax1.set_xlabel("Time $\it{t}$ [s]")
        ax1.set_ylabel("Position [m]")
        ax2=ax1.twinx()
        ax2.plot(data["timestamp"],data["v_x"],"r--",label="$\it{v_x}$ [m/s]")
        ax2.plot(data["timestamp"],data["v_y"],"g--",label="$\it{v_y}$ [m/s]")
        ax2.plot(data["timestamp"],data["v_theta"],"b--",label=r"$v_{\theta}$ [rad/s]")
        ax2.plot(data["timestamp"],data["v_pan"],"c--",label="$v_{\phi}$ [rad/s]")
        ax2.legend(loc="upper right")
        ax2.set_ylabel("Velocity [m/s]")

        plt.title(data_name+" "+os.path.basename(self.results_dir_path))
        plt.savefig(self.results_dir_path+f"/{data_name}_{self.png_prefix}.png")
        plt.cla()

    def plot_command_velocity(self,data,data_name):
        plt.plot(data["timestamp"],data["v_x"],"r",label="$\it{v_x}$ [m/s]")
        plt.plot(data["timestamp"],data["v_y"],"g",label="$\it{v_y}$ [m/s]")
        plt.plot(data["timestamp"],data["omg_z"],"b",label=r"$v_{\theta}$+v_{\phi} [rad/s]")
        plt.legend()
        plt.grid()
        plt.xlabel("Time $\it{t}$ [s]")
        plt.ylabel("Velocity")
        plt.title(data_name+" "+os.path.basename(self.results_dir_path))
        plt.savefig(self.results_dir_path+f"/{data_name}_{self.png_prefix}.png")
        plt.cla()

    def plot_all(self):
        self.load_data()
        ## IMU
        try:
            self.plot_imu(self.base_accurate_imu_data,"base_accurate_imu_data")
        except AttributeError:
            pass
        try:
            self.plot_imu(self.base_imu_data,"base_imu_data")
        except AttributeError:
            pass
        try:
            self.plot_imu(self.head_imu_data,"head_imu_data")
        except AttributeError:
            pass
        try:
            self.plot_imu(self.zed_imu_data,"zed_imu_data")
        except AttributeError:
            pass

        ## Odometry
        try:
            self.plot_odom(self.odom_data,"odom_data")
        except AttributeError:
            pass

        ## Command velocity
        try:
            self.plot_command_velocity(self.command_velocity_data,"command_velocity_data")
        except AttributeError:
            pass

cls=AnalyzeSuddenStop()
cls.plot_all()