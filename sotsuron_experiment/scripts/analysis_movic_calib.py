import numpy as np
import pandas as pd
from glob import glob
import matplotlib.pyplot as plt

from analysis_management import *
from noise_processor import *

class MovicExporter():
    def __init__(self,results_dir_path="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/20240204_12"):
        self.path_management,self.csv_labels,self.color_dict=management_initial()
        plt.rcParams["figure.figsize"] = (15,10)
        plt.rcParams["figure.autolayout"] = True
        plt.rcParams['font.family'] = 'Times New Roman'

        self.results_dir_path=results_dir_path
        self.base_accurate_imu_csv_path=self.results_dir_path+"/hsrb/base_accurate_imu_1.csv"
        self.base_imu_csv_path=self.results_dir_path+"/hsrb/base_imu_1.csv"
        self.head_imu_csv_path=self.results_dir_path+"/hsrb/imu_1.csv"
        self.head_imu_calib_csv_path=self.head_imu_csv_path[:-5]+"calib_1.csv"
        self.zed_imu_csv_path=self.results_dir_path+"/zed/imu_1.csv"
        self.zed_imu_calib_csv_path=self.zed_imu_csv_path[:-5]+"calib_1.csv"
        self.odom_csv_path=self.results_dir_path+"/hsrb/odom_1.csv"
        self.command_velocity_csv_path=self.results_dir_path+"/hsrb/command_velocity_1.csv"
        self.head_imu_calib_csv_path=self.results_dir_path+"/hsrb/imu_1_calib.csv"
        self.zed_imu_calib_csv_path=self.results_dir_path+"/zed/imu_1_calib.csv"
        self.odom_calib_csv_path=self.results_dir_path+"/hsrb/odom_1_calib.csv"
        self.command_velocity_calib_csv_path=self.results_dir_path+"/hsrb/command_velocity_1_calib.csv"
        self.exp_memo_csv_path="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/memo/20240204_exp_memo.csv"

        self.trial_id=self.results_dir_path[-2:]

        self.load_data()

    def load_data(self):

        try:
            self.base_accurate_imu_data=pd.read_csv(self.base_accurate_imu_csv_path,names=self.csv_labels["imu"])
        except FileNotFoundError:
            pass
        try:
            self.base_imu_data=pd.read_csv(self.base_imu_csv_path,names=self.csv_labels["imu"])
        except FileNotFoundError:
            pass
        try:
            self.head_imu_data=pd.read_csv(self.head_imu_csv_path,names=self.csv_labels["imu"])
        except FileNotFoundError:
            pass
        try:
            self.zed_imu_data=pd.read_csv(self.zed_imu_csv_path,names=self.csv_labels["imu"])
        except FileNotFoundError:
            pass
        try:
            self.zed_imu_data=self.zed_imu_data[self.zed_imu_data["timestamp"]!=self.zed_imu_data["timestamp"].min()] # 362行目にzeroが入ってたので消去
        except FileNotFoundError:
            pass
        try:
            self.head_imu_calib_data=pd.read_csv(self.head_imu_calib_csv_path,names=self.csv_labels["imu"])
        except FileNotFoundError:
            pass
        try:
            self.zed_imu_calib_data=pd.read_csv(self.zed_imu_calib_csv_path,names=self.csv_labels["imu"])
        except FileNotFoundError:
            pass
        try:
            self.zed_imu_data=self.zed_imu_data[self.zed_imu_data["timestamp"]!=self.zed_imu_data["timestamp"].min()] # 362行目にzeroが入ってたので消去
        except FileNotFoundError:
            pass
        try:
            self.odom_data=pd.read_csv(self.odom_csv_path,names=self.csv_labels["odometry"])
        except FileNotFoundError:
            pass
        try:
            self.command_velocity_data=pd.read_csv(self.command_velocity_csv_path,names=self.csv_labels["command_velocity"])
        except FileNotFoundError:
            pass

        self.exp_memo_data=pd.read_csv(self.exp_memo_csv_path,header=0)
        print(self.exp_memo_data)

    def calib_data(self,data,data_name):
        calib_start=self.exp_memo_data[self.exp_memo_data["trial_id"]==float(self.trial_id)]["calib_start"].values[0]
        calib_end=calib_start+self.exp_memo_data[self.exp_memo_data["trial_id"]==float(self.trial_id)]["calib_duration"].values[0]
        print(calib_end)
        calib_data=data[data["timestamp"]>=calib_start]
        calib_data=data[data["timestamp"]<=calib_end]
        stable_acc_x=calib_data["lin_acc_x"].mean()
        stable_acc_y=calib_data["lin_acc_y"].mean()
        stable_acc_z=calib_data["lin_acc_z"].mean()
        if data_name=="head_imu_data":
            g=np.sqrt(stable_acc_x**2+stable_acc_z**2)
            stable_angle=-np.arccos(stable_acc_z/g)
            self.head_imu_data["lin_acc_x_calib"]=self.head_imu_data["lin_acc_x"]*np.cos(stable_angle)-self.head_imu_data["lin_acc_z"]*np.sin(stable_angle)
            self.head_imu_data["lin_acc_y_calib"]=self.head_imu_data["lin_acc_y"]
            self.head_imu_data["lin_acc_z_calib"]=self.head_imu_data["lin_acc_x"]*np.sin(stable_angle)+self.head_imu_data["lin_acc_z"]*np.cos(stable_angle)
            plt.plot(self.head_imu_data["timestamp"],self.head_imu_data["lin_acc_x_calib"],"r")
            plt.plot(self.head_imu_data["timestamp"],self.head_imu_data["lin_acc_y_calib"],"g")
            plt.plot(self.head_imu_data["timestamp"],self.head_imu_data["lin_acc_z_calib"],"b")
            plt.show()
            # print(stable_acc_z)
            # print(stable_angle)
            # print(np.median(np.sqrt(self.head_imu_data["lin_acc_x_calib"].values**2+self.head_imu_data["lin_acc_z_calib"].values**2)))
            self.head_imu_data.to_csv(self.head_imu_calib_csv_path,index=False)
            raise TimeoutError
        if data_name=="zed_imu_data":
            g=np.sqrt(stable_acc_x**2+stable_acc_y**2)
            stable_angle=np.arccos(abs(stable_acc_y)/g)
            self.zed_imu_data["lin_acc_y_calib"]=self.zed_imu_data["lin_acc_y"]*np.cos(stable_angle)-self.zed_imu_data["lin_acc_x"]*np.sin(stable_angle)
            self.zed_imu_data["lin_acc_x_calib"]=self.zed_imu_data["lin_acc_y"]*np.sin(stable_angle)+self.zed_imu_data["lin_acc_x"]*np.cos(stable_angle)
            self.zed_imu_data["lin_acc_z_calib"]=self.zed_imu_data["lin_acc_z"]
            plt.plot(self.zed_imu_data["timestamp"],self.zed_imu_data["lin_acc_x_calib"],"r")
            plt.plot(self.zed_imu_data["timestamp"],self.zed_imu_data["lin_acc_y_calib"],"g")
            plt.plot(self.zed_imu_data["timestamp"],self.zed_imu_data["lin_acc_z_calib"],"b")
            print(g)
            print(stable_angle)
            print(np.median(np.sqrt(self.zed_imu_data["lin_acc_x_calib"].values**2+self.zed_imu_data["lin_acc_y_calib"].values**2)))
            plt.show()
            self.zed_imu_data.to_csv(self.zed_imu_calib_csv_path,index=False)

            raise TimeoutError


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
        plt.savefig(self.results_dir_path+f"/{data_name}.png")
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
        plt.savefig(self.results_dir_path+f"/{data_name}.png")
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
        plt.savefig(self.results_dir_path+f"/{data_name}.png")
        plt.cla()


    def plot_all(self):
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

    def main(self):
        self.calib_data(self.head_imu_data,"head_imu_data")
        self.calib_data(self.zed_imu_data,"zed_imu_data")

results_dirs=sorted(glob("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/20240204_*"))
# print(results_dirs)
cls=MovicExporter(results_dirs[11])
cls.main()
# for results_dir_path in results_dirs:
    # cls=MovicExporter(results_dir_path)
    # cls.main()