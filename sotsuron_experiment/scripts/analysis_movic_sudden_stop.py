import numpy as np
import pandas as pd
from glob import glob
import matplotlib.pyplot as plt

from analysis_management import *
from noise_processor import *
from matplotlib.gridspec import GridSpec

class AnalyzeSuddenStop():
    def __init__(self,results_dir_path="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/20240204_04"):
        self.path_management,self.csv_labels,self.color_dict=management_initial()
        plt.rcParams["figure.figsize"] = (15,10)
        plt.rcParams["figure.autolayout"] = True
        plt.rcParams["font.size"] = 24
        plt.rcParams['font.family'] = 'Times New Roman'
        self.png_prefix="ROI"

        self.results_dir_path=results_dir_path
        self.base_accurate_imu_csv_path=self.results_dir_path+"/hsrb/base_accurate_imu_1.csv"
        self.base_imu_csv_path=self.results_dir_path+"/hsrb/base_imu_1.csv"
        self.head_imu_csv_path=self.results_dir_path+"/hsrb/imu_1_calib.csv"
        self.zed_imu_csv_path=self.results_dir_path+"/zed/imu_1_calib.csv"
        self.odom_csv_path=self.results_dir_path+"/hsrb/odom_1.csv"
        self.command_velocity_csv_path=self.results_dir_path+"/hsrb/command_velocity_1.csv"

        self.load_data()

    def load_data(self):
        try:
            self.command_velocity_data=pd.read_csv(self.command_velocity_csv_path,names=self.csv_labels["command_velocity"])
        except FileNotFoundError:
            pass
        start_timestamp=self.command_velocity_data["timestamp"].min()-5
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
            self.head_imu_data=pd.read_csv(self.head_imu_csv_path,header=0)
            print(self.head_imu_data["timestamp"])
            self.head_imu_data=self.head_imu_data[self.head_imu_data["timestamp"]>=start_timestamp]
            self.head_imu_data=self.head_imu_data[self.head_imu_data["timestamp"]<=end_timestamp]
        except FileNotFoundError:
            pass
        try:
            self.zed_imu_data=pd.read_csv(self.zed_imu_csv_path,header=0)
            self.zed_imu_data=self.zed_imu_data[self.zed_imu_data["timestamp"]>=start_timestamp]
            self.zed_imu_data=self.zed_imu_data[self.zed_imu_data["timestamp"]<=end_timestamp]
            self.zed_imu_data=self.zed_imu_data[self.zed_imu_data["timestamp"]!=self.zed_imu_data["timestamp"].min()] # 362行目にzeroが入ってたので消去
        except FileNotFoundError:
            pass
        try:
            self.odom_data=pd.read_csv(self.odom_csv_path,names=self.csv_labels["odometry"])
            self.odom_data=vel_processor(self.odom_data)
            self.odom_data=self.odom_data[self.odom_data["timestamp"]>=start_timestamp]
            self.odom_data=self.odom_data[self.odom_data["timestamp"]<=end_timestamp]
        except FileNotFoundError:
            pass

    def plot_all_imu(self):
        # fig,ax1=plt.subplots()
        gs = GridSpec(2, 1)
        plt.subplot(gs[0])
        plt.plot(self.base_accurate_imu_data["timestamp"],self.base_accurate_imu_data["lin_acc_x"],label=r"base $\it{\alpha_x}$")
        plt.plot(self.head_imu_data["timestamp"],-self.head_imu_data["lin_acc_x_calib"],label=r"head $\it{\alpha_x}$")
        plt.plot(self.zed_imu_data["timestamp"],self.zed_imu_data["lin_acc_x_calib"],label=r"zed $\it{\alpha_x}$")
        plt.legend()
        plt.grid()
        plt.xlabel("Time $\it{t}$ [s]")
        plt.ylabel("Acceleration $\it{a}$ [m/s$^{2}$]")
        plt.subplot(gs[1])
        plt.plot(self.odom_data["timestamp"],self.odom_data["v_x"],label="odometry")
        plt.plot(self.command_velocity_data["timestamp"],self.command_velocity_data["v_x"],label="command")
        plt.grid()
        plt.legend()
        plt.xlabel("Time $\it{t}$ [s]")
        plt.ylabel("Velocity $\it{v_x}$ [m/s]")
        plt.title("all IMU and velocity"+" "+os.path.basename(self.results_dir_path))
        plt.savefig(self.results_dir_path+"/all_IMU_and_vel.png")
        plt.clf()

    def plot_fft(self,fft_start_timestamp=None,fft_end_timestamp=None,png_suffix="accelOff_and_2s"):
        if fft_start_timestamp==None:
            fft_start_timestamp=self.command_velocity_data["timestamp"].max()
        if fft_end_timestamp==None:
            fft_end_timestamp=self.command_velocity_data["timestamp"].max()+2

        brake_odom_data=self.odom_data[self.odom_data["timestamp"]>=fft_start_timestamp]
        brake_odom_data=brake_odom_data[self.odom_data["timestamp"]<=fft_end_timestamp]
        brake_base_accurate_imu_data=self.base_accurate_imu_data[self.base_accurate_imu_data["timestamp"]>=fft_start_timestamp]
        brake_base_accurate_imu_data=brake_base_accurate_imu_data[self.base_accurate_imu_data["timestamp"]<=fft_end_timestamp]
        brake_head_imu_data=self.head_imu_data[self.head_imu_data["timestamp"]>=fft_start_timestamp]
        brake_head_imu_data=brake_head_imu_data[self.head_imu_data["timestamp"]<=fft_end_timestamp]
        brake_zed_imu_data=self.zed_imu_data[self.zed_imu_data["timestamp"]>=fft_start_timestamp]
        brake_zed_imu_data=brake_zed_imu_data[self.zed_imu_data["timestamp"]<=fft_end_timestamp]

        def plot_before_fft():
            gs = GridSpec(2, 1)
            plt.subplot(gs[0])
            plt.plot(brake_base_accurate_imu_data["timestamp"],brake_base_accurate_imu_data["lin_acc_x"],label=r"base $\it{\alpha_x}$")
            plt.plot(brake_head_imu_data["timestamp"],-brake_head_imu_data["lin_acc_x_calib"],label=r"head $\it{\alpha_x}$")
            plt.plot(brake_zed_imu_data["timestamp"],brake_zed_imu_data["lin_acc_x_calib"],label=r"zed $\it{\alpha_x}$")
            plt.legend()
            plt.grid()
            plt.xlabel("Time $\it{t}$ [s]")
            plt.ylabel("Acceleration $\it{a}$ [m/s$^{2}$]")
            plt.subplot(gs[1])
            # plt.plot(self.command_velocity_data["timestamp"],self.command_velocity_data["v_x"],label="command")
            plt.plot(brake_odom_data["timestamp"],brake_odom_data["v_x"],label="odometry")
            plt.grid()
            plt.legend()
            plt.xlabel("Time $\it{t}$ [s]")
            plt.ylabel("Velocity $\it{v_x}$ [m/s]")
            plt.title("all IMU and velocity"+" "+os.path.basename(self.results_dir_path))
            plt.savefig(self.results_dir_path+f"/all_IMU_and_vel_before_fft_{png_suffix}.png")
            plt.clf()

        plot_before_fft()

        def calc_fft(data):
            ## resample
            data=resampling_processor(data)
            ## definition
            print(data)
            N=len(data)
            dt=0.01
            fs=1/dt # サンプリング周波数（標本点の間隔^-1）
            fn=fs/2 # ナイキスト周波数（再現可能な周波数の上限値）
            freq=np.fft.rfftfreq(N,d=dt)

            # from scipy import signal
            # window = signal.hann(N)  # ハニング窓関数(開始・終了地点にずれが生じてしまう場合の解消法．トレンド除去済みのデータになら適用できるかも)
            try:
                F_vx=np.fft.rfft(data["lin_acc_x_calib"],axis=0)
                F_vy=np.fft.rfft(data["lin_acc_y_calib"],axis=0)
                F_vz=np.fft.rfft(data["lin_acc_z_calib"],axis=0)
            except KeyError:
                F_vx=np.fft.rfft(data["lin_acc_x"],axis=0)
                F_vy=np.fft.rfft(data["lin_acc_y"],axis=0)
                F_vz=np.fft.rfft(data["lin_acc_z"],axis=0)

            F_vx=F_vx/(N/2)
            F_vy=F_vy/(N/2)
            F_vz=F_vz/(N/2)

            Amp_x=np.abs(F_vx)
            Amp_y=np.abs(F_vy)
            Amp_z=np.abs(F_vy)

            return freq[:N//2], Amp_x[:N//2]
        
        [freq_base_accurate_imu_data,amp_base_accurate_imu_data]=calc_fft(brake_base_accurate_imu_data)
        [freq_head_imu_data,amp_head_imu_data]=calc_fft(brake_head_imu_data)
        [freq_zed_imu_data,amp_zed_imu_data]=calc_fft(brake_zed_imu_data)
        # gs = GridSpec(3, 1)
        # plt.subplot(gs[0])
        plt.clf()
        plt.plot(freq_base_accurate_imu_data,amp_base_accurate_imu_data,label="base")
        plt.plot(freq_head_imu_data,amp_head_imu_data,label="head")
        plt.plot(freq_zed_imu_data,amp_zed_imu_data,label="zed")
        plt.legend()
        plt.grid()
        plt.xlabel("Frequency [Hz]")
        plt.ylabel("Amplitude")
        plt.title("FFT of the main IMUs when stop"+" "+os.path.basename(self.results_dir_path))
        plt.savefig(self.results_dir_path+f"/all_IMU_fft_{png_suffix}.png")
        # plt.show()
        pass
        

    def plot_imu(self,data,data_name):
        try:
            if "head" in data_name:
                plt.plot(data["timestamp"],-data["lin_acc_x_calib"],"r",label="lin_acc_x (calib)")
            else:
                plt.plot(data["timestamp"],data["lin_acc_x_calib"],"r",label="lin_acc_x (calib)")
            if "head" in data_name:
                plt.plot(data["timestamp"],-data["lin_acc_y_calib"],"g",label="lin_acc_y (calib)")
            else:
                plt.plot(data["timestamp"],data["lin_acc_y_calib"],"g",label="lin_acc_y (calib)")
            plt.plot(data["timestamp"],data["lin_acc_z_calib"],"b",label="lin_acc_z (calib)")
        except KeyError:
            plt.plot(data["timestamp"],data["lin_acc_x"],"r",label="lin_acc_x")
            plt.plot(data["timestamp"],data["lin_acc_y"],"g",label="lin_acc_y")
            plt.plot(data["timestamp"],data["lin_acc_z"],"b",label="lin_acc_z")
        plt.legend()
        plt.grid()
        plt.xlabel("Time $\it{t}$ [s]")
        plt.ylabel("Acceleration $\it{a}$ [m/s$^{2}$]")
        plt.title(data_name+" "+os.path.basename(self.results_dir_path))
        plt.savefig(self.results_dir_path+f"/{data_name}_{self.png_prefix}.png")
        plt.clf()

    def plot_odom(self,data,data_name):
        # print(np.mean(data["timestamp"].values[1:]-data["timestamp"].values[:-1]))
        # print(np.std(data["timestamp"].values[1:]-data["timestamp"].values[:-1]))
        # print(np.min(data["timestamp"].values[1:]-data["timestamp"].values[:-1]))
        # print(np.max(data["timestamp"].values[1:]-data["timestamp"].values[:-1]))
        # plt.hist(data["timestamp"].values[1:]-data["timestamp"].values[:-1])
        plt.clf()
        # raise TimeoutError
        # data=resampling_processor(data)
        data=vel_processor(data)
        fig,ax1=plt.subplots()
        ax1.plot(data["timestamp"],data["x"],"r",label="$\it{x}$")
        # ax1.plot(data["timestamp"],data["y"],"g",label="$\it{y}$")
        # ax1.plot(data["timestamp"],data["theta"],"b",label=r"$\theta$")
        # ax1.plot(data["timestamp"],data["pan"],"c",label="$\phi$")
        ax1.legend()
        ax1.grid()
        ax1.set_xlabel("Time $\it{t}$ [s]")
        ax1.set_ylabel("Position [m]")
        ax2=ax1.twinx()
        ax2.plot(data["timestamp"],data["v_x"],"r--",label="Odometry $\it{v_x}$ [m/s]")
        plt.plot(self.command_velocity_data["timestamp"],self.command_velocity_data["v_x"],"k",label="Control input $\it{v_x}$ [m/s]")
        # ax2.plot(data["timestamp"],data["v_y"],"g--",label="$\it{v_y}$ [m/s]")
        # ax2.plot(data["timestamp"],data["v_theta"],"b--",label=r"$v_{\theta}$ [rad/s]")
        # ax2.plot(data["timestamp"],data["v_pan"],"c--",label="$v_{\phi}$ [rad/s]")
        ax2.legend()
        ax2.set_ylabel("Velocity [m/s]")

        plt.title(data_name+" "+os.path.basename(self.results_dir_path))
        plt.savefig(self.results_dir_path+f"/{data_name}_{self.png_prefix}.png")
        plt.clf()

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
        plt.clf()

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
# cls.plot_all_imu()
cls.plot_all()
# cls.plot_fft()
# start_timestamp=cls.command_velocity_data["timestamp"].min()-3
# end_timestamp=start_timestamp+1
# idx=0
# while end_timestamp<=cls.command_velocity_data["timestamp"].max()+2:
#     cls.plot_fft(start_timestamp,end_timestamp,str(start_timestamp))
#     start_timestamp=start_timestamp+0.5
#     end_timestamp=start_timestamp+1
#     print(start_timestamp)
#     break