import numpy as np
import pandas as pd

def vel_processor(data):
    data["vx"]=0
    data["vy"]=0
    data["vz"]=0
    data["vx"][1:]=(data["x"].values[1:]-data["x"].values[:-1])/(data["t"].values[1:]-data["t"].values[:-1])
    data["vy"][1:]=(data["y"].values[1:]-data["y"].values[:-1])/(data["t"].values[1:]-data["t"].values[:-1])
    data["vz"][1:]=(data["z"].values[1:]-data["z"].values[:-1])/(data["t"].values[1:]-data["t"].values[:-1])
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