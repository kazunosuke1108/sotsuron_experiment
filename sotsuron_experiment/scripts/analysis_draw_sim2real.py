import sys
from glob import glob
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import pandas as pd
from pprint import pprint
import pickle

from analysis_management import *
from analysis_initial_processor import *

sys.path.append(r'C:/Users/hayashide/ytlab_ros_ws/ytlab_nlpmp/ytlab_nlpmp_modules/scripts')
from getFootprint import *


plt.rcParams["figure.figsize"] = (15,8)
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.family'] = 'Times New Roman'
gs = GridSpec(2, 3, width_ratios=[1,1,1])
path_management,csv_labels,color_dict=management_initial()

usabledata=pd.read_csv(path_management["usabledata_csv_path"])

pickle_paths=[]
for path in sorted(usabledata["sim_path"].values):
    pickle_paths.append(os.path.split(path)[0]+"/concat_traj.pickle")

odom_paths=[]
for path in sorted(usabledata["odom_path"].values):
    odom_paths.append(path[:-4]+"_od.csv")
    pprint(os.path.isfile(path[:-4]+"_od.csv"))

tf_paths=[]
# for path in sorted(usabledata["odom_path"].values):
    # tf_paths.append(path_management["denoise_3d_csv_path"]+"/"+os.path.basename(path[:-4])+"_tf_denoise.csv")
for path in sorted(usabledata["sim_path"].values):
    print(path)
    tf_paths.append(glob(os.path.split(path[:-4])[0]+"/*_tf.csv")[0])

print(len(tf_paths))

for pickle_path,odom_path,tf_path in zip(pickle_paths,odom_paths,tf_paths):
    fig, ax = plt.subplots()

    try:
        with open(pickle_path, 'rb') as f:
            pickle_data = pickle.load(f) 
    except FileNotFoundError:
        continue
    odom_data=pd.read_csv(odom_path,header=0,names=csv_labels["odometry"])
    odom_data=odom_data[odom_data["t"]>0]
    tf_data=pd.read_csv(tf_path,header=0,names=csv_labels["odometry"][:-1])

    zH=pickle_data["solution"]["zH"]
    footprint=getFootprint(pickle_data["solution"]["t"], pickle_data["solution"]["zR"], pickle_data["solution"]["uR"], pickle_data["env"], pickle_data["rbt"], pickle_data["hmn"], pickle_data["sns"], hmn_path=zH)
    
    plt.subplot(gs[0,:])
    plt.plot(odom_data["x"],odom_data["y"],"b",label="odom zR")
    plt.plot(pickle_data["solution"]["zR"][0,:],pickle_data["solution"]["zR"][1,:],"c",label="plan zR")
    plt.plot(tf_data["x"],tf_data["y"],"r",label="measured zH")
    plt.plot(pickle_data["solution"]["zH"][0,:],pickle_data["solution"]["zH"][1,:],"m",label="estimated zH")
    plt.legend()
    plt.xlabel("Hallway direction $\it{x}$ [m]")
    plt.ylabel("Width direction $\it{y}$ [m]")
    plt.xlim([-10,10])
    plt.ylim([-2,2])
    plt.title(os.path.basename(odom_path)[:-7])
    plt.gca().set_aspect('equal', adjustable='box')

    plt.subplot(gs[1,0])
    plt.plot(odom_data["t"],odom_data["x"],"b",label="odom zR")
    plt.plot(pickle_data["solution"]["t"],pickle_data["solution"]["zR"][0,:],"c",label="plan zR")
    plt.plot(tf_data["t"],tf_data["x"],"r",label="measured zH")
    plt.plot(pickle_data["solution"]["t"],pickle_data["solution"]["zH"][0,:],"m",label="estimated zH")
    plt.ylim([-5,15])
    plt.legend()
    plt.ylabel("Hallway direction $\it{x}$ [m]")
    
    plt.subplot(gs[1,1])
    plt.plot(odom_data["t"],odom_data["y"],"b",label="odom zR")
    plt.plot(pickle_data["solution"]["t"],pickle_data["solution"]["zR"][1,:],"c",label="plan zR")
    plt.plot(tf_data["t"],tf_data["y"],"r",label="measured zH")
    plt.plot(pickle_data["solution"]["t"],pickle_data["solution"]["zH"][1,:],"m",label="estimated zH")
    plt.ylim([-2,2])
    plt.legend()
    plt.xlabel("time $\it{t}$ [s]")
    plt.ylabel("Width direction $\it{y}$ [m]")
    
    plt.subplot(gs[1,2])
    plt.plot(odom_data["t"],odom_data["theta"]+odom_data["pan"],"b",label="odom zR")
    plt.plot(pickle_data["solution"]["t"],pickle_data["solution"]["zR"][2,:],"c",label="plan zR")
    # plt.plot(tf_data["t"],tf_data["y"],"r",label="measured zH")
    # plt.plot(pickle_data["solution"]["t"],pickle_data["solution"]["zH"][1,:],"m",label="estimated zH")
    plt.ylim([-np.pi*5/4,np.pi*5/4])
    plt.legend()
    plt.xlabel("time $\it{t}$ [s]")
    plt.ylabel(r"angle $\theta$' [m]")
    # plt.plot(odom_data["x"],odom_data["y"],"b")
    # plt.plot(pickle_data["solution"]["zR"][0,:],pickle_data["solution"]["zR"][1,:],"c")
    
    plt.savefig(path_management["png_dir_path"]+"/sim2real_gap/"+os.path.basename(odom_path)[:-7]+".png")


