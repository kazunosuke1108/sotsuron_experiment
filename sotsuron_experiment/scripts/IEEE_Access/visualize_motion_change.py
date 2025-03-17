import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob
import pickle
from pprint import pprint
import matplotlib.colors as mcolors
plt.rcParams["figure.figsize"] = (15/2.54,10/2.54)
plt.subplot().set_aspect('equal')
plt.rcParams["figure.autolayout"] = True
plt.rcParams["font.size"] = 16
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'stix' # math fontの設定
plt.rcParams["legend.edgecolor"] = 'black' # edgeの色を変更
plt.rcParams["legend.handlelength"] = 1 # 凡例の線の長さを調節

csv_labels={}
csv_labels["detectron2_joint"]=["trunk","gravity","nose","l_eye","r_eye","l_ear","r_ear","l_shoulder","r_shoulder","l_elbow","r_elbow","l_hand","r_hand","l_base","r_base","l_knee","r_knee","l_foot","r_foot"]
csv_labels["detectron2_joint_3d"]=["timestamp"]
for joint_name in csv_labels["detectron2_joint"]:
    suffixes=["_x","_y","_z"]
    for suffix in suffixes:
        csv_labels["detectron2_joint_3d"].append(joint_name+suffix)
csv_labels["odometry"]=["timestamp","x","y","theta","pan"]

def load_picklelog(picklepath):
    with open(picklepath,mode="rb") as f:
        try:
            data=pickle.load(f)
        except ModuleNotFoundError:
            # python2系列で書かれた場合
            data=pickle.load(f,fix_imports=True)
    return data        

def add_plot_ougi(xR,yR,theta,pan,sns,previous):
    alpha=0.5 if previous else 1
    arc_resolution=100
    arc_rad = np.linspace(theta + pan - sns["phi"],
                theta + pan + sns["phi"], arc_resolution)
    arc_r1_x = sns["r1"] * np.cos(arc_rad) + xR
    arc_r1_y = sns["r1"] * np.sin(arc_rad) + yR
    arc_r2_x = sns["r2"] * np.cos(arc_rad) + xR
    arc_r2_y = sns["r2"] * np.sin(arc_rad) + yR

    arc_r1 = plt.plot(arc_r1_x, arc_r1_y, 'g', linewidth=1,alpha=alpha)
    arc_r2 = plt.plot(arc_r2_x, arc_r2_y, 'g', linewidth=1,alpha=alpha)


    arc_right = plt.plot([arc_r1_x[0], arc_r2_x[0]], [
                        arc_r1_y[0], arc_r2_y[0]], color='g', linewidth=1,alpha=alpha)
    arc_left = plt.plot([arc_r1_x[-1], arc_r2_x[-1]],
                        [arc_r1_y[-1], arc_r2_y[-1]], color='g', linewidth=1,alpha=alpha)
    
def add_plot_others(xR,yR,theta,pan,rbt,previous):
    alpha=0.5 if previous else 1
    arc_resolution=100
    rbt_position = plt.Circle((xR, yR),
                                    radius=rbt["sizer"], edgecolor='b', facecolor='w',alpha=alpha)#,label="robot")
    plt.gca().add_patch(rbt_position)
    rbt_direction = plt.plot([xR, xR + rbt["sizer"] * np.cos(theta + pan)],
                                [yR, yR + rbt["sizer"] * np.sin(theta + pan)], 'b', linewidth=2,alpha=alpha)

# データのインポート
sotsuron_exp_trial_name="_2023-12-19-20-10-31"
sotsuron_exp_dir_path=f"C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12/{sotsuron_exp_trial_name}"
nlpmp_trial_name=""
nlpmp_dir_path="C:/Users/hayashide/ytlab_ros_ws/ytlab_nlpmp/ytlab_nlpmp_modules/results/20231219/20231219_201042_20231219_05_01_00_inoue"

tf_csv_path=sotsuron_exp_dir_path+f"/{sotsuron_exp_trial_name}_tf_raw.csv"
tf_data=pd.read_csv(tf_csv_path,names=csv_labels["detectron2_joint_3d"])
tf_data=tf_data.dropna(how="all")
tf_data=tf_data.rolling(20).mean()

od_csv_path=sotsuron_exp_dir_path+f"/{sotsuron_exp_trial_name}_od_raw.csv"
od_data=pd.read_csv(od_csv_path,names=csv_labels["odometry"])
od_data=od_data.dropna(how="all")
od_data=od_data.rolling(20).mean()

# トリミング
start_timestamp=od_data.loc[900,"timestamp"]
end_timestamp=od_data.loc[1600,"timestamp"]
# tf_data=tf_data[((tf_data["timestamp"]>=start_timestamp) & (tf_data["timestamp"]<=end_timestamp))]
# od_data=od_data[((od_data["timestamp"]>=start_timestamp) & (od_data["timestamp"]<=end_timestamp))]
pickeup_idxes=np.arange(1000,1601,100)
# pickeup_idxes=np.arange(900,1601,150)
pickup_timestamps=od_data.loc[pickeup_idxes,"timestamp"]
cmap = mcolors.LinearSegmentedColormap.from_list("blue_red", ["white", "blue"], N=len(pickup_timestamps))

# 切り出すタイミング
picklepaths=sorted(glob(nlpmp_dir_path+"/*/*.pickle"))
pickup_picklepaths=[]
pickle_timestamps=[]
for picklepath in picklepaths:
    pickle_data=load_picklelog(picklepath=picklepath)
    pickle_timestamps.append(pickle_data["time_management"]["last_calc_end"])

for pickup_timestamp in pickup_timestamps.values:
    idx=abs(np.array(pickle_timestamps)-pickup_timestamp).argmin()
    pickup_picklepaths+=[picklepaths[idx]]

print(pickup_timestamps)
for i,_ in enumerate(pickup_picklepaths):
    if i==0:
        continue
    # 直前
    pickle_data=load_picklelog(pickup_picklepaths[i-1])
    # 人
    ## 自己位置
    tf_idx=np.argmin(abs(tf_data["timestamp"]-pickup_timestamps.values[i-1]))
    plt.scatter(tf_data.loc[tf_idx,"trunk_x"],tf_data.loc[tf_idx,"trunk_y"],s=100,label="Previous human position",c=(0.5,0,0))
    ## 矢印

    
    # ロボット
    ## 計画軌道
    data=pd.DataFrame(pickle_data["solution"]["zR"].T,columns=["x","y","theta","vx","vy","omg"])
    plt.plot(data["x"],data["y"],label="Previous planning result", color=cmap(2 / (len(pickup_picklepaths) - 1)),linewidth=2)
    ## 扇
    add_plot_ougi(xR=data["x"].values[0],yR=data["y"].values[0],theta=data["theta"].values[0],pan=0,sns=pickle_data["sns"],previous=True)
    ## 自己位置
    add_plot_others(xR=data["x"].values[0],yR=data["y"].values[0],theta=data["theta"].values[0],pan=0,rbt=pickle_data["rbt"],previous=True)

    # od_idx=np.argmin(abs(od_data["timestamp"]-pickup_timestamps.values[i-1]))
    # plt.scatter(od_data.loc[od_idx,"x"],od_data.loc[od_idx,"y"],s=100,label="Previous robot position",c=(0,0,0.5))
    
    # 最新
    pickle_data=load_picklelog(pickup_picklepaths[i])
    # 人
    ## 軌道
    tf_idx=np.argmin(abs(tf_data["timestamp"]-pickup_timestamps.values[i]))
    ## 自己位置
    plt.plot(tf_data.loc[:tf_idx,"trunk_x"],tf_data.loc[:tf_idx,"trunk_y"],"r")
    plt.scatter(tf_data.loc[tf_idx,"trunk_x"],tf_data.loc[tf_idx,"trunk_y"],s=100,label="Latest human position",c=(1,0,0))

    # ロボット
    ## オドメトリ
    od_idx=np.argmin(abs(od_data["timestamp"]-pickup_timestamps.values[i]))
    plt.plot(od_data.loc[1000:od_idx,"x"],od_data.loc[1000:od_idx,"y"],linewidth=1,label="Robot odometry",c=(0,0,0))
    ## 計画軌道
    data=pd.DataFrame(pickle_data["solution"]["zR"].T,columns=["x","y","theta","vx","vy","omg"])
    plt.plot(data["x"],data["y"],label="Latest planning result", color=(0,0,1),linewidth=2)
    ## 扇
    add_plot_ougi(xR=data["x"].values[0],yR=data["y"].values[0],theta=data["theta"].values[0],pan=0,sns=pickle_data["sns"],previous=False)
    ## 自己位置
    add_plot_others(xR=data["x"].values[0],yR=data["y"].values[0],theta=data["theta"].values[0],pan=0,rbt=pickle_data["rbt"],previous=False)


    plt.xlim([-4,8])
    plt.ylim([-2,2])
    plt.xlabel("Hallway direction $\it{x}$ [m]")
    plt.ylabel("Width direction $\it{y}$ [m]")
    if i==1:
        plt.legend(loc='lower center', bbox_to_anchor=(.5, 1.1), ncol=2)
        plt.rcParams["figure.figsize"] = (15/2.54,13/2.54)
        plt.subplot().set_aspect('equal')
        plt.rcParams['font.family'] = 'Times New Roman'
    else:
        plt.rcParams["figure.figsize"] = (15/2.54,6/2.54)
        plt.subplot().set_aspect('equal')
    plt.savefig(f"C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/scripts/IEEE_Access/{i}.pdf")
    plt.cla()
raise NotImplementedError






# 人の軌跡をプロットしてみる
plt.plot(tf_data["trunk_x"],tf_data["trunk_y"],label="Pedestrian")

# ロボットの軌跡をプロットしてみる
plt.plot(od_data["x"],od_data["y"])

# 動作計画結果をプロットしてみる

pprint(pickup_picklepaths)
# raise NotImplementedError

for i,picklepath in enumerate(pickup_picklepaths):
    pickle_data=load_picklelog(picklepath=picklepath)

    # raise NotImplementedError
    data=pd.DataFrame(pickle_data["solution"]["zR"].T,columns=["x","y","theta","vx","vy","omg"])
    data["timestamp"]=pickle_data["solution"]["t"]+pickle_data["time_management"]["last_calc_end"]
    # data=data[((data["timestamp"]>=start_timestamp) & (data["timestamp"]<=end_timestamp))]
    plt.plot(data["x"],data["y"],label=os.path.basename(picklepath), color=cmap(i / (len(pickup_picklepaths) - 1)))
    add_plot_ougi(xR=data["x"].values[0],yR=data["y"].values[0],theta=data["theta"].values[0],pan=0,sns=pickle_data["sns"])
    add_plot_others(xR=data["x"].values[0],yR=data["y"].values[0],theta=data["theta"].values[0],pan=0,rbt=pickle_data["rbt"])

# plt.legend()
    if i%2==0:
        plt.savefig(f"C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/scripts/IEEE_Access/{i}.png")