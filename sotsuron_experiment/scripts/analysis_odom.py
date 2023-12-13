#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from noise_processor import *
from scipy import signal

plt.rcParams["figure.figsize"] = (10,8)
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.family'] = 'Times New Roman'

csvpath="/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-11-11-55-46/_2023-12-11-11-55-46_od_raw.csv"

data=pd.read_csv(csvpath,names=["t","x","y","theta","pan"])
data["z"]=data["theta"]+data["pan"]

# リサンプリング
resample_dt_str="0.01S"
resample_dt_float=float(resample_dt_str[:-1])
data["timestamp_datetime"]=pd.to_datetime(data["t"], unit='s',utc=True).dt.tz_convert('Asia/Tokyo')
data["timestamp_datetime"]=data["timestamp_datetime"].dt.round(resample_dt_str)
data=data.set_index("timestamp_datetime")

data=mean_processor(data)
data=vel_processor(data)

data = data.replace([np.inf, -np.inf], np.nan)
data=data.dropna(how="any")
print(data)
# FFTに向けてdetrend
data["vx_trend"]=0
data["vy_trend"]=0
data["vx_detrend"]=0
data["vy_detrend"]=0

data["vx_detrend"]=signal.detrend(data["vx"])
data["vx_trend"]=data["vx"]-data["vx_detrend"]
data["vy_detrend"]=signal.detrend(data["vy"])
data["vy_trend"]=data["vy"]-data["vy_detrend"]


# FFT for velocity
N=len(data)
dt=resample_dt_float
fs=1/dt # サンプリング周波数（標本点の間隔^-1）
fn=fs/2 # ナイキスト周波数（再現可能な周波数の上限値）
freq=np.fft.rfftfreq(N,d=dt)
print(N)
print(dt)
print(len(freq))

# raise TimeoutError

# from scipy import signal
# window = signal.hann(N)  # ハニング窓関数(開始・終了地点にずれが生じてしまう場合の解消法．トレンド除去済みのデータになら適用できるかも)
F_vx=np.fft.rfft(data["vx_detrend"],axis=0)
F_vy=np.fft.rfft(data["vy_detrend"],axis=0)

F_vx=F_vx/(N/2)
F_vy=F_vy/(N/2)

Amp_x=np.abs(F_vx)
Amp_y=np.abs(F_vy)

fig, ax = plt.subplots()
ax.plot(freq[:N//2], Amp_x[:N//2],"r",label="odom $\it{v_x}$")
ax.plot(freq[:N//2], Amp_y[:N//2],"b",label="odom $\it{v_y}$")
ax.set_xlabel("Frequency [Hz]")
ax.set_ylabel("Amplitude")
ax.set_title(os.path.basename(csvpath)[:-8])
ax.legend()
ax.grid()
plt.savefig(os.path.split(csvpath)[0]+"/"+os.path.basename(csvpath)[:-8]+"_vel_beforeFFT.png",dpi=300)
plt.cla()
# raise TimeoutError

partial_data=data
# partial_data=mean_processor(partial_data)
partial_data=vel_processor(partial_data)
# partial_data=mean_processor(partial_data)

plt.rcParams["figure.figsize"] = (10,8)
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.family'] = 'Times New Roman'
fig, ax1 = plt.subplots()
ax1.plot(partial_data["t"],partial_data["x"],label="x")
ax1.plot(partial_data["t"],partial_data["y"],label="y")
ax1.plot(partial_data["t"],partial_data["theta"],label="theta")
ax1.plot(partial_data["t"],partial_data["pan"],label="pan")
ax1.legend()
ax1.set_xlabel("Time [s]")
ax1.set_ylabel("Position [m]")
ax2 = ax1.twinx()
ax2.plot(partial_data["t"],partial_data["vx"],label="vx")
ax2.plot(partial_data["t"],partial_data["vy"],label="vy")
ax2.legend()
ax2.set_ylabel("Velocity [m/s]")
plt.savefig(os.path.split(csvpath)[0]+"/"+os.path.basename(csvpath)[:-4]+".png")

# for i in range(5,len(data)):
#     partial_data=data.iloc[:i]
#     partial_data=mean_processor(partial_data)
#     partial_data=vel_processor(partial_data)
#     partial_data=mean_processor(partial_data)

#     # fig, ax1 = plt.subplots()
#     # plt.plot(partial_data["t"],partial_data["x"],label="x")
#     # plt.plot(partial_data["t"],partial_data["y"],label="y")
#     # plt.plot(partial_data["t"],partial_data["theta"],label="theta")
#     # plt.plot(partial_data["t"],partial_data["pan"],label="pan")
#     # ax2 = ax1.twinx()
#     plt.plot(partial_data["t"],partial_data["vx"],label="vx")
#     plt.plot(partial_data["t"],partial_data["vy"],label="vy")
#     plt.legend()
#     # ax2.legend()
#     plt.pause(0.01)
#     plt.cla()