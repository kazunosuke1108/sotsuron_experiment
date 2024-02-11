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
plt.rcParams["figure.figsize"] = (7,7)
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.family'] = 'Times New Roman'

csvs=path_management["ras_tf_csv_dir_path"]

for csvpath in csvs:
    # if "12_00_00" not in csvpath:
    #     continue
    try:
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

        # リサンプリング
        resample_dt_str="0.01S"
        resample_dt_float=float(resample_dt_str[:-1])
        data["timestamp_datetime"]=pd.to_datetime(data["timestamp"], unit='s',utc=True).dt.tz_convert('Asia/Tokyo')
        data["timestamp_datetime"]=data["timestamp_datetime"].dt.round(resample_dt_str)
        data=data.set_index("timestamp_datetime")

        # 速度計算
        data["gravity_vx"]=0
        data["gravity_vy"]=0
        data["gravity_vx"].iloc[:-1]=(data["gravity_x"].values[1:]-data["gravity_x"].values[:-1])/(data["timestamp"].values[1:]-data["timestamp"].values[:-1])
        data["gravity_vy"].iloc[:-1]=(data["gravity_y"].values[1:]-data["gravity_y"].values[:-1])/(data["timestamp"].values[1:]-data["timestamp"].values[:-1])

        # FFTに向けてdetrend
        data["gravity_vx_trend"]=0
        data["gravity_vy_trend"]=0
        data["gravity_vx_detrend"]=0
        data["gravity_vy_detrend"]=0
        
        data["gravity_vx_detrend"]=signal.detrend(data["gravity_vx"])
        data["gravity_vx_trend"]=data["gravity_vx"]-data["gravity_vx_detrend"]
        data["gravity_vy_detrend"]=signal.detrend(data["gravity_vy"])
        data["gravity_vy_trend"]=data["gravity_vy"]-data["gravity_vy_detrend"]
        
        # vx_average=vx.mean()
        # vy_average=vy.mean()
        # data["gravity_vx"]=data["gravity_vx"]-vx_average
        # data["gravity_vy"]=data["gravity_vy"]-vy_average

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

        # denoise using FFT
        f_cutoff=0.5
        print(fn)
        F_vx[(freq>fn)]=0
        F_vy[(freq>fn)]=0
        F_vx[(freq>f_cutoff)]=0
        F_vy[(freq>f_cutoff)]=0
        
        data["gravity_vx_filtered"]=0
        data["gravity_vy_filtered"]=0
        data["gravity_vx_filtered"][:-1]=np.real(np.fft.irfft(F_vx))*N
        data["gravity_vy_filtered"][:-1]=np.real(np.fft.irfft(F_vy))*N
        data=data.iloc[:-1]

        # detrendの復元
        data["gravity_vx_filtered"]=data["gravity_vx_filtered"]+data["gravity_vx_trend"]
        data["gravity_vy_filtered"]=data["gravity_vy_filtered"]+data["gravity_vy_trend"]
        # plot
        fig, ax1 = plt.subplots()
        ax1.plot(data["timestamp"],data["gravity_x"],"r-",label="gravity_x")
        ax1.plot(data["timestamp"],data["gravity_y"],"b-",label="gravity_y")
        ax1.set_xlabel("Time $\it{t}$ [s]")
        ax1.set_ylabel("Position $\it{x}$ $\it{y}$ [m]")
        ax1.set_title(f"{os.path.basename(csvpath)[:8]} (resample_dt: {resample_dt_float}[s] f_cutoff: {f_cutoff}[Hz])")
        plt.legend()
        plt.grid()

        ax2 = ax1.twinx()
        ax2.plot(data["timestamp"],data["gravity_vx"],"m--",linewidth=0.2,label="raw velocity $\it{v_x}$")
        ax2.plot(data["timestamp"],data["gravity_vy"],"c--",linewidth=0.2,label="raw velocity $\it{v_y}$")
        ax2.plot(data["timestamp"],data["gravity_vx_filtered"],"m",label="FFT velocity $\it{v_x}$")
        ax2.plot(data["timestamp"],data["gravity_vy_filtered"],"c",label="FFT velocity $\it{v_y}$")
        # ax2.plot(data["timestamp"],data["gravity_vx_trend"],"g",label="trend of $\it{v_y}$")
        # ax2.plot(data["timestamp"],data["gravity_vy_trend"],"g",label="trend of $\it{v_y}$")
        ax2.set_xlabel("Time $\it{t}$ [s]")
        ax2.set_ylabel("Velocity $\it{v_x} {v_y}$ [m]")
        plt.legend()
        plt.grid()

        plt.savefig(path_management["png_dir_path"]+f"/{os.path.basename(csvpath)[:8]}_filtered.png")
        # plt.show()
    except Exception:
        pass