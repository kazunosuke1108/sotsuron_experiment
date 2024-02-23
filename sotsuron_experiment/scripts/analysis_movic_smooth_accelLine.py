import os
import sys
import shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from exp_commons import ExpCommons
from analysis_management import *
from noise_processor import *

class AccelLine(ExpCommons):
    def __init__(self):
        super(ExpCommons).__init__()
        self.path_management,self.csv_labels,self.color_dict=management_initial()        


        # self.odom_csv_path="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/20240204_12/hsrb/odom_1.csv"
        self.odom_csv_path="/home/hayashide/ytlab_ros_ws/ytlab_nlpmp2/ytlab_nlpmp2_modules/results/20240223_03/odom_1.csv"
        self.odom_data=pd.read_csv(self.odom_csv_path,names=self.csv_labels["odometry"])

        self.command_velocity_csv_path="/home/hayashide/ytlab_ros_ws/ytlab_nlpmp2/ytlab_nlpmp2_modules/results/20240223_03/command_velocity_1.csv"
        self.command_velocity_data=pd.read_csv(self.command_velocity_csv_path,names=self.csv_labels["command_velocity"])

        self.hsrzr8_csv_path="/home/hayashide/ytlab_ros_ws/ytlab_nlpmp2/ytlab_nlpmp2_modules/results/20240223_03/HsrZr8_1.csv"
        self.HsrZr8_data=pd.read_csv(self.hsrzr8_csv_path,names=self.csv_labels["hsrzr8"])

        self.result_individual_dir_path=self.odom_csv_path[:-4]
        os.makedirs(self.result_individual_dir_path,exist_ok=True)
        shutil.rmtree(self.result_individual_dir_path)
        os.makedirs(self.result_individual_dir_path,exist_ok=True)
        self.common_memo=f"{os.path.basename(self.odom_csv_path)} {os.path.basename(sys.argv[0])}"
        # resampling
        self.odom_data.sort_values("timestamp",inplace=True)
        self.odom_data=resampling_processor(self.odom_data,resample_dt_str="0.01S")
        
        self.odom_data=vel_processor(self.odom_data)
        self.plot_timeseries(self.odom_data["timestamp"],self.odom_data["v_x"],label="$\it{v_x}$",memo="Before_LPF_v_x")
        self.plot_timeseries(self.odom_data["timestamp"],self.odom_data["v_y"],label="$\it{v_y}$",memo="Before_LPF_v_y")


        
    def denoise(self):
        ## FFT
        [self.freq,self.Amp_list,self.F_list]=fft_processor(data=self.odom_data,labels=["v_x","v_y"])
        
        # LPF
        thredshold_hz=1
        ## LPF for v_x
        label="$\it{v_x}$"
        self.F_x=self.F_list[0]
        self.Amp_x=self.Amp_list[0]
        self.plot_fft(self.freq,self.Amp_x,label=label,memo=f"Before_LPF_thre_{thredshold_hz}_v_x")
        self.odom_data["v_x_LPF"]=self.LPF_processor(self.freq,self.F_x,thredshold_hz=thredshold_hz,label=label,memo="v_x")
        self.plot_timeseries(self.odom_data["timestamp"],self.odom_data["v_x_LPF"],label="$\it{v_x}$ (LPF)",memo="after_LPF_v_x")


        ## LPF for v_y
        label="$\it{v_y}$"
        self.F_y=self.F_list[1]
        self.Amp_y=self.Amp_list[1]
        self.plot_fft(self.freq,self.Amp_y,label=label,memo=f"Before_LPF_thre_{thredshold_hz}_v_y")
        self.odom_data["v_y_LPF"]=self.LPF_processor(self.freq,self.F_y,thredshold_hz=thredshold_hz,label=label,memo="v_y")
        self.plot_timeseries(self.odom_data["timestamp"],self.odom_data["v_y_LPF"],label="$\it{v_y}$ (LPF)",memo="after_LPF_v_y")

        ## save LPF data
        self.odom_data.to_csv(self.odom_csv_path[:-4]+"_LPF.csv",index=0)

    def compare_with_reference(self):
        plt.plot(self.odom_data["timestamp"],self.odom_data["v_x"],"r",label="Odometry")
        plt.plot(self.command_velocity_data["timestamp"],self.command_velocity_data["v_x"],"b",label="ref_after_mpc")
        plt.plot(self.HsrZr8_data["timestamp"],self.HsrZr8_data["v_x"],"g",label="ref_before_mpc")
        draw_labels_timeseries_velocity()
        plt.savefig(self.result_individual_dir_path+"odom_twist_compare.png")
        pass

    def LPF_processor(self,freq,F,thredshold_hz=3,label="",memo=""):
        cut_idx=np.where(abs(freq)>thredshold_hz)[0]
        F[cut_idx]=0
        Amp=np.abs(F)
        self.plot_fft(freq,Amp,memo=f"After_LPF_cut_{thredshold_hz}Hz_{memo}",label=label)
        f=np.fft.ifft(F).real
        processed_timeseries=f
        return processed_timeseries

    def plot_timeseries(self,timestamp,value,label="",memo=""):
        plt.plot(timestamp,value,label=label)
        plt.title(f"{memo} {self.common_memo}")
        plt.xlabel("Time $\it{t}$ [s]")
        plt.ylabel("Velocity $\it{v}$ [m/s]")
        plt.legend()
        plt.savefig(self.result_individual_dir_path+"/"+"timeseries_"+memo+".png")
        plt.close()

    def plot_fft(self,freq,Amp,label="",memo=""):
        plt.bar(freq[:len(freq)//2],Amp[:len(Amp)//2],label=label)
        plt.title(f"FFT: {memo} {self.common_memo}")
        plt.xlabel("Frequency [Hz]")
        plt.ylabel("Amplitude")
        plt.legend()
        plt.savefig(self.result_individual_dir_path+"/"+"fft_"+memo+".png")
        plt.close()


cls=AccelLine()
cls.denoise()
cls.compare_with_reference()