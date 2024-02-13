import os
import sys
import re
import pickle
import numpy as np
import pandas as pd
from glob import glob
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from noise_processor import *
from analysis_management import management_initial
from exp_commons import ExpCommons


class FFTProcessor(ExpCommons):
    def __init__(self,csv_path="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12/_2023-12-19-15-20-40/_2023-12-19-15-20-40_od_raw.csv",data_category="odometry"):
        super().__init__()
        self.path_management,self.csv_labels,self.color_dict=management_initial()
        plt.rcParams["figure.figsize"] = (15,10)
        plt.rcParams["figure.autolayout"] = True
        plt.rcParams["font.size"] = 24
        plt.rcParams['font.family'] = 'Times New Roman'

        # load data
        self.odom_csv_path=csv_path
        self.data_category=data_category
        self.odom_data=pd.read_csv(self.odom_csv_path,names=self.csv_labels[self.data_category])
        self.odom_data.drop_duplicates(subset="timestamp", inplace=True)
        print(self.odom_data)
        self.odom_data=vel_processor(self.odom_data)
        
        # fft
        fft_labels=["v_x","v_y"]
        freq,Amp_list=self.calc_fft(self.odom_data,labels=fft_labels)
        
        # plot
        for label,Amp in zip(fft_labels,Amp_list):
             plt.plot(freq,Amp,label=label)

        plt.legend()
        plt.grid()
        plt.xlabel("Frequency [Hz]")
        plt.ylabel("Amplitude")
        plt.title("FFT"+" "+os.path.basename(self.odom_csv_path))
        plt.savefig(self.odom_csv_path[:-4]+"_FFT.png",dpi=300)
        pass

    def calc_fft(self,data,labels=["v_x","v_y"]):
            ## resample
            data=resampling_processor(data)
            ## definition
            N=len(data)
            dt=0.01
            fs=1/dt # サンプリング周波数（標本点の間隔^-1）
            fn=fs/2 # ナイキスト周波数（再現可能な周波数の上限値）
            freq=np.fft.rfftfreq(N,d=dt)

            # from scipy import signal
            # window = signal.hann(N)  # ハニング窓関数(開始・終了地点にずれが生じてしまう場合の解消法．トレンド除去済みのデータになら適用できるかも)

            F_list=[]
            Amp_list=[]
            for label in labels:
                F=np.fft.rfft(data[label],axis=0)/(N/2)
                Amp=np.abs(F)
                F_list.append(F)
                Amp_list.append(Amp[:N//2])

            return freq[:N//2], Amp_list
    
cls=FFTProcessor()