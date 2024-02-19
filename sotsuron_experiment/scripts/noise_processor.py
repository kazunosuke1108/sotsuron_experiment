import numpy as np
import pandas as pd

def vel_processor(data,labels=["x","y","theta","pan"]):
    for label in labels:
        data[f"v_{label}"]=0
        data[f"v_{label}"][1:]=(data[f"{label}"].values[1:]-data[f"{label}"].values[:-1])/(data["timestamp"].values[1:]-data["timestamp"].values[:-1])

    # data["v_x"]=0
    # data["v_y"]=0
    # data["v_theta"]=0
    # data["v_pan"]=0
    # data["v_x"][1:]=(data["x"].values[1:]-data["x"].values[:-1])/(data["timestamp"].values[1:]-data["timestamp"].values[:-1])
    # data["v_y"][1:]=(data["y"].values[1:]-data["y"].values[:-1])/(data["timestamp"].values[1:]-data["timestamp"].values[:-1])
    # data["v_theta"][1:]=(data["theta"].values[1:]-data["theta"].values[:-1])/(data["timestamp"].values[1:]-data["timestamp"].values[:-1])
    # data["v_pan"][1:]=(data["pan"].values[1:]-data["pan"].values[:-1])/(data["timestamp"].values[1:]-data["timestamp"].values[:-1])
    return data


def time_series_processor(data):
    data=data.sort_values("t")
    data.reset_index(inplace=True, drop=True)
    return data

def outlier_processor(data):
    threshold=0.25 # m/frame
    iteration=5
    for _ in range(iteration):
        droplist=[]
        for i in range(2,len(data)-3):
            if (abs(data["x"].iat[i+1]-data["x"].iat[i])>threshold) or (abs(data["y"].iat[i+1]-data["y"].iat[i])>threshold) or (abs(data["theta"].iat[i+1]-data["theta"].iat[i])>threshold):
                droplist.append(i)
        data.drop(droplist,inplace=True)
        data.reset_index(inplace=True,drop=True)
    return data

def mean_processor(data,span=5):
    data=data.ewm(span=span).mean()# 指数加重移動平均
    data.reset_index(inplace=True,drop=True)
    return data

def interp_processor(data,fps):
    time_length=data["t"].values[-1]-data["t"].values[0]
    new_nFrames=int(time_length*fps)
    t_interp=np.arange(data["t"].values[0],data["t"].values[-1],time_length/new_nFrames)
    data_interp=pd.DataFrame(np.zeros((len(t_interp),len(data.columns))),columns=data.columns)
    data_interp["t"]=t_interp
    for i,col in enumerate(data.columns[1:]):
        data_interp[col]=np.interp(t_interp,data["t"].values,data[col].values)
    return data_interp


def plot_processor(data,msg=""):
    plt.subplot(121)
    plt.plot(data["t"].values,data["x"].values,label=f"x({msg})")
    plt.plot(data["t"].values,data["y"].values,label=f"y({msg})")
    # plt.plot(data["t"].values,data["z"].values,label=f"z({msg})")
    plt.xlabel("time [s]")
    plt.ylabel("position [m]")
    plt.title("position")
    plt.legend()

    plt.subplot(122)
    try:
        data["vx"]
        plt.plot(data["t"].values,data["vx"].values,label=f"vx({msg})")
        plt.plot(data["t"].values,data["vy"].values,label=f"vy({msg})")
        # plt.plot(data["t"].values,data["vz"].values,label=f"vz({msg})")
        plt.xlabel("time [s]")
        plt.ylabel("velocity [m/s]")
        plt.title("velocity")
        plt.ylim([-1.5,1.5])
        plt.legend()
    except KeyError:
        pass

def resampling_processor(data,resample_dt_str="0.01S"):
    # リサンプリング
    # resample_dt_str="0.01S"
    resample_dt_float=float(resample_dt_str[:-1])
    try:
        data["timestamp_datetime"]=pd.to_datetime(data["timestamp"], unit='s',utc=True).dt.tz_convert('Asia/Tokyo')
    except KeyError:
        data["timestamp_datetime"]=pd.to_datetime(data["t"], unit='s',utc=True).dt.tz_convert('Asia/Tokyo')
    data["timestamp_datetime_round"]=data["timestamp_datetime"].dt.round(resample_dt_str)
    data=data.set_index("timestamp_datetime_round")
    # data=data.asfreq(resample_dt_str,method="nearest")
    data=data.drop("timestamp_datetime",axis=1)
    data=data.resample(resample_dt_str).interpolate(method="time")
    return data

def fft_processor(data,labels=["v_x","v_y"],dt=0.01):
    ## resample
    data=resampling_processor(data)
    ## definition
    N=len(data)
    fs=1/dt # サンプリング周波数（標本点の間隔^-1）
    fn=fs/2 # ナイキスト周波数（再現可能な周波数の上限値）
    freq=np.fft.fftfreq(N,d=dt)

    # from scipy import signal
    # window = signal.hann(N)  # ハニング窓関数(開始・終了地点にずれが生じてしまう場合の解消法．トレンド除去済みのデータになら適用できるかも)

    F_list=[]
    Amp_list=[]
    for label in labels:
        F=np.fft.fft(data[label],axis=0)
        Amp=np.abs(F)
        F_list.append(F)
        Amp_list.append(Amp)#[:N//2])

    return freq, Amp_list, F_list
    # return freq[:N//2], Amp_list, F_list