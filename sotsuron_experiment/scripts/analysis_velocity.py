from glob import glob
import matplotlib.pyplot as plt
import pandas as pd
from pprint import pprint
import pickle
from noise_processor import *
from analysis_management import *
from analysis_initial_processor import *

path_management,csv_labels,color_dict=management_initial()
plt.rcParams["figure.figsize"] = (7,7)
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.family'] = 'Times New Roman'

csvs=path_management["ras_tf_csv_dir_path"]

for csvpath in csvs:
    if "12_00_00" not in csvpath:
        continue
    print(csvpath)
    # data=pd.read_csv(csvpath,names=csv_labels["detectron2_joint_3d"],skiprows=1)
    data=initial_processor(csvpath,True)
    # data=mean_processor(data)

    # リアルタイム処理
    pass
    # 後解析処理
    try:
        timestamp_x5_closest_idx=(data["gravity_x"]-5).abs().idxmin()
        timestamp_x5_closest=data.iloc[timestamp_x5_closest_idx]["timestamp"]
        x_x5_closest=data.iloc[timestamp_x5_closest_idx]["gravity_x"]
        timestamp_x0_closest_idx=(data[data["timestamp"]>timestamp_x5_closest]["gravity_x"]-0).abs().idxmin()
        timestamp_x0_closest=data.iloc[timestamp_x0_closest_idx]["timestamp"]
        x_x0_closest=data.iloc[timestamp_x0_closest_idx]["gravity_x"]
    except (TypeError,ValueError):
        continue
    # x=5,0を通過するtimestampを取得
    data=data[data["timestamp"]>timestamp_x5_closest]
    data=data[data["timestamp"]<timestamp_x0_closest]

    vx=(data["gravity_x"].values[1:]-data["gravity_x"].values[:-1])/(data["timestamp"].values[1:]-data["timestamp"].values[:-1])
    vy=(data["gravity_y"].values[1:]-data["gravity_y"].values[:-1])/(data["timestamp"].values[1:]-data["timestamp"].values[:-1])
    data["gravity_vx"]=0
    data["gravity_vy"]=0
    data["gravity_vx"].iloc[:-1]=vx
    data["gravity_vy"].iloc[:-1]=vy
    fig, ax1 = plt.subplots()
    ax1.plot(data["timestamp"],data["gravity_x"],"r-",label="gravity_x")
    ax1.plot(data["timestamp"],data["gravity_y"],"b-",label="gravity_y")
    ax1.set_xlabel("Time $\it{t}$ [s]")
    ax1.set_ylabel("Position $\it{x}$ $\it{y}$ [m]")
    plt.legend()
    plt.grid()

    ax2 = ax1.twinx()
    ax2.plot(data["timestamp"].iloc[:-1],vx,"m--",label="vel_g_x")
    ax2.plot(data["timestamp"].iloc[:-1],vy,"c--",label="vel_g_y")
    ax2.set_xlabel("Time $\it{t}$ [s]")
    ax2.set_ylabel("Velocity $\it{v_x} {v_y}$ [m]")
    plt.legend()
    plt.grid()
    plt.show()

    # リサンプリング
    resample_dt_str="0.01S"
    resample_dt_float=float(resample_dt_str[:-1])
    data["timestamp_datetime"]=pd.to_datetime(data["timestamp"], unit='s',utc=True).dt.tz_convert('Asia/Tokyo')
    data["timestamp_datetime"]=data["timestamp_datetime"].dt.round(resample_dt_str)
    data=data.set_index("timestamp_datetime")
    # data=data.resample(resample_dt_str).interpolate('time')
    print(data)

    vx=(data["gravity_x"].values[1:]-data["gravity_x"].values[:-1])/(data["timestamp"].values[1:]-data["timestamp"].values[:-1])
    vy=(data["gravity_y"].values[1:]-data["gravity_y"].values[:-1])/(data["timestamp"].values[1:]-data["timestamp"].values[:-1])
    data["gravity_vx"]=0
    data["gravity_vy"]=0
    data["gravity_vx"].iloc[:-1]=vx
    data["gravity_vy"].iloc[:-1]=vy

    data.to_csv("temp.csv")
    fig, ax1 = plt.subplots()
    # vx=(data["gravity_x"].values[1:]-data["gravity_x"].values[:-1])/(data["timestamp"].values[1:]-data["timestamp"].values[:-1])
    ax1.scatter(data["timestamp"],data["gravity_vx"],color="m",s=1,label="vel_g_x")
    plt.show()


    # FFT for velocity
    N=len(data)
    dt=resample_dt_float
    # dt=resample_dt_float#(data["timestamp"].values[-1]-data["timestamp"].values[0])/N
    # dt=(data["timestamp"].values[-1]-data["timestamp"].values[0])/N
    fs=1/dt # サンプリング周波数（標本点の間隔^-1）
    fn=fs/2 # ナイキスト周波数（再現可能な周波数の上限値）
    freq=np.fft.rfftfreq(N,d=dt)
    print(N)
    print(dt)
    print(len(freq))
    # raise TimeoutError

    # from scipy import signal
    # window = signal.hann(N)  # ハニング窓関数(開始・終了地点にずれが生じてしまう場合の解消法．トレンド除去済みのデータになら適用できるかも)
    F_x=np.fft.rfft(data["gravity_x"],axis=0)
    F_y=np.fft.rfft(data["gravity_y"],axis=0)

    F_x=F_x/(N/2)
    F_y=F_y/(N/2)

    Amp_x=np.abs(F_x)
    Amp_y=np.abs(F_y)

    plt.rcParams["figure.figsize"] = (7,7)
    fig, ax = plt.subplots()
    ax.plot(freq[:N//2], Amp_x[:N//2],"r",label="gravity $\it{x}$")
    ax.plot(freq[:N//2], Amp_y[:N//2],"b",label="gravity $\it{y}$")
    ax.set_xlabel("Frequency [Hz]")
    ax.set_ylabel("Amplitude")
    ax.legend()
    ax.grid()
    # plt.show()
    plt.savefig(path_management["png_dir_path"]+"/12_00_00_fft_pos.png")

    # denoise using FFT
    f_cutoff=0.5
    print(fn)
    F_x[(freq>fn)]=0
    F_y[(freq>fn)]=0
    F_x[(freq>f_cutoff)]=0
    F_y[(freq>f_cutoff)]=0
    # print(F_x)

    Amp_x=np.abs(F_x)
    Amp_y=np.abs(F_y)
    fig, ax = plt.subplots()
    ax.plot(freq[:N//2], Amp_x[:N//2],"m",label="gravity $\it{v_x}$")
    ax.plot(freq[:N//2], Amp_y[:N//2],"c",label="gravity $\it{v_y}$")
    ax.set_xlabel("Frequency [Hz]")
    ax.set_ylabel("Amplitude")
    ax.legend()
    ax.grid()
    # plt.show()

    data["gravity_x_filtered"]=0
    data["gravity_y_filtered"]=0
    print(len(data["gravity_x_filtered"]))
    print(len(np.real(np.fft.irfft(F_x))))
    data["gravity_x_filtered"][:-1]=np.real(np.fft.irfft(F_x))*N
    # data["gravity_x_filtered"]=np.real(np.fft.irfft(F_x))*N
    data["gravity_y_filtered"][:-1]=np.real(np.fft.irfft(F_y))*N
    # data["gravity_y_filtered"]=np.real(np.fft.irfft(F_y))*N
    data=data.iloc[:-1]

    fig, ax1 = plt.subplots()
    ax1.plot(data["timestamp"],data["gravity_x"],"r-",label="gravity_x")
    ax1.plot(data["timestamp"],data["gravity_y"],"b-",label="gravity_y")
    ax1.set_xlabel("Time $\it{t}$ [s]")
    ax1.set_ylabel("Position $\it{x}$ $\it{y}$ [m]")
    ax1.plot(data["timestamp"],data["gravity_x_filtered"],"r--",label="filtered $\it{x}$")
    ax1.plot(data["timestamp"],data["gravity_y_filtered"],"b--",label="filtered $\it{y}$")
    plt.legend()
    plt.grid()

    ax2 = ax1.twinx()
    vx=(data["gravity_x_filtered"].values[1:]-data["gravity_x_filtered"].values[:-1])/(data["timestamp"].values[1:]-data["timestamp"].values[:-1])
    vy=(data["gravity_y_filtered"].values[1:]-data["gravity_y_filtered"].values[:-1])/(data["timestamp"].values[1:]-data["timestamp"].values[:-1])
    data["gravity_vx"]=0
    data["gravity_vy"]=0
    data["gravity_vx"].iloc[:-1]=vx
    data["gravity_vy"].iloc[:-1]=vy
    ax2.plot(data["timestamp"],data["gravity_vx"],"m",label="$\it{v_x}$")
    ax2.plot(data["timestamp"],data["gravity_vy"],"c",label="$\it{v_y}$")
    ax2.set_xlabel("Time $\it{t}$ [s]")
    ax2.set_ylabel("Velocity $\it{v_x} {v_y}$ [m]")
    plt.legend()
    plt.grid()

    plt.show()
    # plt.savefig(path_management["png_dir_path"]+"/12_00_00_filtered_pos.png")



    # # FFT for velocity
    # N=len(data)
    # dt=(data["timestamp"].values[-1]-data["timestamp"].values[0])/N
    # fs=1/dt # サンプリング周波数（標本点の間隔^-1）
    # fn=fs/2 # ナイキスト周波数（再現可能な周波数の上限値）
    # freq=np.fft.rfftfreq(N,d=dt)

    # F_x=np.fft.rfft(data["gravity_vx"],axis=0)
    # F_y=np.fft.rfft(data["gravity_vy"],axis=0)

    # F_x=F_x/(N/2)
    # F_y=F_y/(N/2)

    # Amp_x=np.abs(F_x)
    # Amp_y=np.abs(F_y)

    # print(data["gravity_vx"])
    # print(data["timestamp"].values[-1]-data["timestamp"].values[0])
    # print(1/dt)

    # plt.rcParams["figure.figsize"] = (7,7)
    # fig, ax = plt.subplots()
    # ax.plot(freq[:N//2], Amp_x[:N//2],"m",label="gravity $\it{v_x}$")
    # ax.plot(freq[:N//2], Amp_y[:N//2],"c",label="gravity $\it{v_y}$")
    # ax.set_xlabel("Frequency [Hz]")
    # ax.set_ylabel("Amplitude")
    # ax.legend()
    # ax.grid()
    # plt.savefig(path_management["png_dir_path"]+"/12_00_00_fft.png")

    # # denoise using FFT
    # f_cutoff=0.5
    # print(fn)
    # F_x[(freq>fn)]=0
    # F_y[(freq>fn)]=0
    # F_x[(freq>f_cutoff)]=0
    # F_y[(freq>f_cutoff)]=0
    # # print(F_x)

    # Amp_x=np.abs(F_x)
    # Amp_y=np.abs(F_y)
    # fig, ax = plt.subplots()
    # ax.plot(freq[:N//2], Amp_x[:N//2],"m",label="gravity $\it{v_x}$")
    # ax.plot(freq[:N//2], Amp_y[:N//2],"c",label="gravity $\it{v_y}$")
    # ax.set_xlabel("Frequency [Hz]")
    # ax.set_ylabel("Amplitude")
    # ax.legend()
    # ax.grid()
    # # plt.show()

    # data["gravity_vx_filtered"]=0
    # data["gravity_vy_filtered"]=0
    # data["gravity_vx_filtered"][:-1]=np.real(np.fft.irfft(F_x))*N
    # data["gravity_vy_filtered"][:-1]=np.real(np.fft.irfft(F_y))*N
    # data=data.iloc[:-1]

    # fig, ax1 = plt.subplots()
    # ax1.plot(data["timestamp"],data["gravity_x"],"r-",label="gravity_x")
    # ax1.plot(data["timestamp"],data["gravity_y"],"b-",label="gravity_y")
    # ax1.set_xlabel("Time $\it{t}$ [s]")
    # ax1.set_ylabel("Position $\it{x}$ $\it{y}$ [m]")
    # plt.legend()
    # plt.grid()
    # ax2 = ax1.twinx()
    # # ax2.plot(data["timestamp"],data["gravity_vx"],"m.",label="raw $\it{v_x}$")
    # # ax2.plot(data["timestamp"],data["gravity_vy"],"c.",label="raw $\it{v_y}$")
    # ax2.plot(data["timestamp"],data["gravity_vx_filtered"],"m",label="filtered $\it{v_x}$")
    # ax2.plot(data["timestamp"],data["gravity_vy_filtered"],"c",label="filtered $\it{v_y}$")
    # ax2.set_xlabel("Time $\it{t}$ [s]")
    # ax2.set_ylabel("Velocity $\it{v_x} {v_y}$ [m]")
    # plt.legend()
    # plt.grid()

    # plt.savefig(path_management["png_dir_path"]+"/12_00_00_filtered.png")



    # # FFT for velocity
    # N=len(data)
    # dt=(data["timestamp"].values[-1]-data["timestamp"].values[0])/N
    # fs=1/dt # サンプリング周波数（標本点の間隔^-1）
    # fn=fs/2 # ナイキスト周波数（再現可能な周波数の上限値）
    # freq=np.fft.rfftfreq(N,d=dt)

    # F_x=np.fft.rfft(data["gravity_vx"],axis=0)
    # F_y=np.fft.rfft(data["gravity_vy"],axis=0)

    # F_x=F_x/(N/2)
    # F_y=F_y/(N/2)

    # Amp_x=np.abs(F_x)
    # Amp_y=np.abs(F_y)

    # print(data["gravity_vx"])
    # print(data["timestamp"].values[-1]-data["timestamp"].values[0])
    # print(1/dt)

    # plt.rcParams["figure.figsize"] = (7,7)
    # fig, ax = plt.subplots()
    # ax.plot(freq[:N//2], Amp_x[:N//2],"m",label="gravity $\it{v_x}$")
    # ax.plot(freq[:N//2], Amp_y[:N//2],"c",label="gravity $\it{v_y}$")
    # ax.set_xlabel("Frequency [Hz]")
    # ax.set_ylabel("Amplitude")
    # ax.legend()
    # ax.grid()
    # plt.savefig(path_management["png_dir_path"]+"/12_00_00_fft.png")

    # # denoise using FFT
    # f_cutoff=0.5
    # print(fn)
    # F_x[(freq>fn)]=0
    # F_y[(freq>fn)]=0
    # F_x[(freq>f_cutoff)]=0
    # F_y[(freq>f_cutoff)]=0
    # # print(F_x)

    # Amp_x=np.abs(F_x)
    # Amp_y=np.abs(F_y)
    # fig, ax = plt.subplots()
    # ax.plot(freq[:N//2], Amp_x[:N//2],"m",label="gravity $\it{v_x}$")
    # ax.plot(freq[:N//2], Amp_y[:N//2],"c",label="gravity $\it{v_y}$")
    # ax.set_xlabel("Frequency [Hz]")
    # ax.set_ylabel("Amplitude")
    # ax.legend()
    # ax.grid()
    # # plt.show()

    # data["gravity_vx_filtered"]=0
    # data["gravity_vy_filtered"]=0
    # data["gravity_vx_filtered"][:-1]=np.real(np.fft.irfft(F_x))*N
    # data["gravity_vy_filtered"][:-1]=np.real(np.fft.irfft(F_y))*N
    # data=data.iloc[:-1]

    # fig, ax1 = plt.subplots()
    # ax1.plot(data["timestamp"],data["gravity_x"],"r-",label="gravity_x")
    # ax1.plot(data["timestamp"],data["gravity_y"],"b-",label="gravity_y")
    # ax1.set_xlabel("Time $\it{t}$ [s]")
    # ax1.set_ylabel("Position $\it{x}$ $\it{y}$ [m]")
    # plt.legend()
    # plt.grid()
    # ax2 = ax1.twinx()
    # # ax2.plot(data["timestamp"],data["gravity_vx"],"m.",label="raw $\it{v_x}$")
    # # ax2.plot(data["timestamp"],data["gravity_vy"],"c.",label="raw $\it{v_y}$")
    # ax2.plot(data["timestamp"],data["gravity_vx_filtered"],"m",label="filtered $\it{v_x}$")
    # ax2.plot(data["timestamp"],data["gravity_vy_filtered"],"c",label="filtered $\it{v_y}$")
    # ax2.set_xlabel("Time $\it{t}$ [s]")
    # ax2.set_ylabel("Velocity $\it{v_x} {v_y}$ [m]")
    # plt.legend()
    # plt.grid()

    # plt.savefig(path_management["png_dir_path"]+"/12_00_00_filtered.png")



    # # FFT for velocity
    # N=len(data)
    # dt=(data["timestamp"].values[-1]-data["timestamp"].values[0])/N
    # fs=1/dt # サンプリング周波数（標本点の間隔^-1）
    # fn=fs/2 # ナイキスト周波数（再現可能な周波数の上限値）
    # freq=np.fft.rfftfreq(N,d=dt)

    # F_x=np.fft.rfft(data["gravity_vx"],axis=0)
    # F_y=np.fft.rfft(data["gravity_vy"],axis=0)

    # F_x=F_x/(N/2)
    # F_y=F_y/(N/2)

    # Amp_x=np.abs(F_x)
    # Amp_y=np.abs(F_y)

    # print(data["gravity_vx"])
    # print(data["timestamp"].values[-1]-data["timestamp"].values[0])
    # print(1/dt)

    # plt.rcParams["figure.figsize"] = (7,7)
    # fig, ax = plt.subplots()
    # ax.plot(freq[:N//2], Amp_x[:N//2],"m",label="gravity $\it{v_x}$")
    # ax.plot(freq[:N//2], Amp_y[:N//2],"c",label="gravity $\it{v_y}$")
    # ax.set_xlabel("Frequency [Hz]")
    # ax.set_ylabel("Amplitude")
    # ax.legend()
    # ax.grid()
    # plt.savefig(path_management["png_dir_path"]+"/12_00_00_fft.png")

    # # denoise using FFT
    # f_cutoff=0.5
    # print(fn)
    # F_x[(freq>fn)]=0
    # F_y[(freq>fn)]=0
    # F_x[(freq>f_cutoff)]=0
    # F_y[(freq>f_cutoff)]=0
    # # print(F_x)

    # Amp_x=np.abs(F_x)
    # Amp_y=np.abs(F_y)
    # fig, ax = plt.subplots()
    # ax.plot(freq[:N//2], Amp_x[:N//2],"m",label="gravity $\it{v_x}$")
    # ax.plot(freq[:N//2], Amp_y[:N//2],"c",label="gravity $\it{v_y}$")
    # ax.set_xlabel("Frequency [Hz]")
    # ax.set_ylabel("Amplitude")
    # ax.legend()
    # ax.grid()
    # # plt.show()

    # data["gravity_vx_filtered"]=0
    # data["gravity_vy_filtered"]=0
    # data["gravity_vx_filtered"][:-1]=np.real(np.fft.irfft(F_x))*N
    # data["gravity_vy_filtered"][:-1]=np.real(np.fft.irfft(F_y))*N
    # data=data.iloc[:-1]

    # fig, ax1 = plt.subplots()
    # ax1.plot(data["timestamp"],data["gravity_x"],"r-",label="gravity_x")
    # ax1.plot(data["timestamp"],data["gravity_y"],"b-",label="gravity_y")
    # ax1.set_xlabel("Time $\it{t}$ [s]")
    # ax1.set_ylabel("Position $\it{x}$ $\it{y}$ [m]")
    # plt.legend()
    # plt.grid()
    # ax2 = ax1.twinx()
    # # ax2.plot(data["timestamp"],data["gravity_vx"],"m.",label="raw $\it{v_x}$")
    # # ax2.plot(data["timestamp"],data["gravity_vy"],"c.",label="raw $\it{v_y}$")
    # ax2.plot(data["timestamp"],data["gravity_vx_filtered"],"m",label="filtered $\it{v_x}$")
    # ax2.plot(data["timestamp"],data["gravity_vy_filtered"],"c",label="filtered $\it{v_y}$")
    # ax2.set_xlabel("Time $\it{t}$ [s]")
    # ax2.set_ylabel("Velocity $\it{v_x} {v_y}$ [m]")
    # plt.legend()
    # plt.grid()

    # plt.savefig(path_management["png_dir_path"]+"/12_00_00_filtered.png")

    # plt.show()
    maybe_truth_vel_x=(data["gravity_x"].values[-1]-data["gravity_x"].values[0])/(data["timestamp"].values[-1]-data["timestamp"].values[0])
    maybe_truth_vel_y=(data["gravity_y"].values[-1]-data["gravity_y"].values[0])/(data["timestamp"].values[-1]-data["timestamp"].values[0])
    print(maybe_truth_vel_x,maybe_truth_vel_y)
    maybe_truth_vel_vx=data["gravity_vx"].mean()
    maybe_truth_vel_vy=data["gravity_vy"].mean()
    print(maybe_truth_vel_vx,maybe_truth_vel_vy)
    
    raise TimeoutError
    plt.savefig(path_management["png_dir_path"]+"/12_00_00_denoise_5to0.png")




    # plt.show()
    