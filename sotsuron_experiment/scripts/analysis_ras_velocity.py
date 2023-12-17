#! /usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from glob import glob
import matplotlib.pyplot as plt
import pandas as pd
from pprint import pprint
import pickle
from noise_processor import *
from analysis_management import *
from analysis_initial_processor import *
from scipy import signal

path_management,csv_labels,color_dict=management_initial()
plt.rcParams["figure.figsize"] = (10,8)
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.family'] = 'Times New Roman'

try:
    csvpath=sys.argv[1]
except Exception:
    csvpath="/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-11-11-55-46/_2023-12-11-11-55-46_tf_raw.csv"

data=initial_processor(csvpath,True)
# data=mean_processor(data)

# リアルタイム処理
pass
# 後解析処理
# try:
timestamp_x5_closest_idx=(data["gravity_x"]-5).abs().idxmin()
timestamp_x5_closest=data.iloc[timestamp_x5_closest_idx]["timestamp"]
x_x5_closest=data.iloc[timestamp_x5_closest_idx]["gravity_x"]
timestamp_x0_closest_idx=(data[data["timestamp"]>timestamp_x5_closest]["gravity_x"]-0).abs().idxmin()
timestamp_x0_closest=data.iloc[timestamp_x0_closest_idx]["timestamp"]
x_x0_closest=data.iloc[timestamp_x0_closest_idx]["gravity_x"]
# except (TypeError,ValueError):
#     continue
# x=5,0を通過するtimestampを取得
data=data[data["timestamp"]>timestamp_x5_closest]
data=data[data["timestamp"]<timestamp_x0_closest]

# リサンプリング
resample_dt_str="0.01S"
resample_dt_float=float(resample_dt_str[:-1])
data["timestamp_datetime"]=pd.to_datetime(data["timestamp"], unit='s',utc=True).dt.tz_convert('Asia/Tokyo')
data["timestamp_datetime"]=data["timestamp_datetime"].dt.round(resample_dt_str)
data=data.set_index("timestamp_datetime")

data["gravity_vx"]=0
data["gravity_vy"]=0
try:
    data["gravity_vx"].iloc[:-1]=(data["gravity_x"].values[1:]-data["gravity_x"].values[:-1])/(data["timestamp"].values[1:]-data["timestamp"].values[:-1])
    data["gravity_vy"].iloc[:-1]=(data["gravity_y"].values[1:]-data["gravity_y"].values[:-1])/(data["timestamp"].values[1:]-data["timestamp"].values[:-1])
except ValueError:
    data["gravity_vx"]=(data["gravity_x"].values[1:]-data["gravity_x"].values[:-1])/(data["timestamp"].values[1:]-data["timestamp"].values[:-1])
    data["gravity_vy"]=(data["gravity_y"].values[1:]-data["gravity_y"].values[:-1])/(data["timestamp"].values[1:]-data["timestamp"].values[:-1])

# fig,ax=plt.subplots()
# for label in ["gravity"]:
#     ax.plot(data["timestamp"],data[label+"_x"],"o-",markersize=2,color="k",label=label)
#     ax2=ax.twinx()
#     ax2.plot(data["timestamp"],data[label+"_vx"],"o-",markersize=2,color="r",label=label)
#     # ax.plot(data[label+"_x"],data[label+"_y"],"o-",label=label)
# ax.legend()
# # ax.set_aspect("equal")
# plt.grid()
# plt.savefig(os.path.split(csvpath)[0]+"/"+os.path.basename(csvpath)[:-8]+"_vel_raw.png",dpi=300)
# plt.cla()

# raise TimeoutError

# FFTに向けてdetrend
data["gravity_vx_trend"]=0
data["gravity_vy_trend"]=0
data["gravity_vx_detrend"]=0
data["gravity_vy_detrend"]=0

print(data["gravity_x"])

data["gravity_vx_detrend"]=signal.detrend(data["gravity_vx"])
data["gravity_vx_trend"]=data["gravity_vx"]-data["gravity_vx_detrend"]
data["gravity_vy_detrend"]=signal.detrend(data["gravity_vy"])
data["gravity_vy_trend"]=data["gravity_vy"]-data["gravity_vy_detrend"]

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
F_vx=np.fft.rfft(data["gravity_vx_detrend"],axis=0)
F_vy=np.fft.rfft(data["gravity_vy_detrend"],axis=0)

F_vx=F_vx/(N/2)
F_vy=F_vy/(N/2)

Amp_x=np.abs(F_vx)
Amp_y=np.abs(F_vy)

fig, ax = plt.subplots()
ax.plot(freq[:N//2], Amp_x[:N//2],"r",label="gravity $\it{v_x}$")
ax.plot(freq[:N//2], Amp_y[:N//2],"b",label="gravity $\it{v_y}$")
ax.set_xlabel("Frequency [Hz]")
ax.set_ylabel("Amplitude")
ax.set_title(os.path.basename(csvpath)[:-8]+f" fcutoff={5} Hz")
ax.legend()
ax.grid()
plt.savefig(os.path.split(csvpath)[0]+"/"+os.path.basename(csvpath)[:-8]+"_vel_beforeFFT.png",dpi=300)


# denoise using FFT
f_cutoff=5
print(fn)
F_vx[(freq>fn)]=0
F_vy[(freq>fn)]=0
F_vx[(freq>f_cutoff)]=0
F_vy[(freq>f_cutoff)]=0

data["gravity_vx_filtered"]=0
data["gravity_vy_filtered"]=0
data["gravity_vx_filtered"]=np.real(np.fft.irfft(F_vx))*N
data["gravity_vy_filtered"]=np.real(np.fft.irfft(F_vy))*N
data=data.iloc[:-1]


# raise TimeoutError

# detrendの復元
data["gravity_vx_filtered"]=data["gravity_vx_filtered"]+data["gravity_vx_trend"]
data["gravity_vy_filtered"]=data["gravity_vy_filtered"]+data["gravity_vy_trend"]
# plot
fig, ax1 = plt.subplots()
print(data)
ax1.plot(data["timestamp"],data["gravity_x"],"r-",label="gravity_x")
ax1.plot(data["timestamp"],data["gravity_y"],"b-",label="gravity_y")
ax1.set_xlabel("Time $\it{t}$ [s]")
ax1.set_ylabel("Position $\it{x}$ $\it{y}$ [m]")
ax1.set_title(f"{os.path.basename(csvpath)[:8]} (resample_dt: {resample_dt_float}[s] f_cutoff: {f_cutoff}[Hz])")
ax1.legend(loc='upper left', borderaxespad=0)
ax1.grid()

ax2 = ax1.twinx()
ax2.plot(data["timestamp"],data["gravity_vx"],"m--",linewidth=0.2,label="raw velocity $\it{v_x}$")
ax2.plot(data["timestamp"],data["gravity_vy"],"c--",linewidth=0.2,label="raw velocity $\it{v_y}$")
ax2.plot(data["timestamp"],data["gravity_vx_filtered"],"m",label="FFT velocity $\it{v_x}$")
ax2.plot(data["timestamp"],data["gravity_vy_filtered"],"c",label="FFT velocity $\it{v_y}$")
# ax2.plot(data["timestamp"],data["gravity_vx_trend"],"g",label="trend of $\it{v_y}$")
# ax2.plot(data["timestamp"],data["gravity_vy_trend"],"g",label="trend of $\it{v_y}$")
ax2.set_xlabel("Time $\it{t}$ [s]")
ax2.set_ylabel("Velocity $\it{v_x} {v_y}$ [m]")
ax2.legend(loc='upper right', borderaxespad=0)
ax2.grid()
plt.savefig(os.path.split(csvpath)[0]+"/"+os.path.basename(csvpath)[:-8]+"_vel.png",dpi=300)
# plt.show()
# print(data["gravity_vx_filtered"])