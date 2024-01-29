import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from analysis_management import *
from analysis_initial_processor import *
from noise_processor import *

plt.rcParams["figure.figsize"] = (10,8)
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.family'] = 'Times New Roman'

path_management,csv_labels,color_dict=management_initial()
csvpath="/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-13-14-06-23/_2023-12-13-14-06-23_tf_raw.csv"

# data=pd.read_csv(csvpath)
data=initial_processor(csvpath=csvpath,denoise=True)
print(data)
# raise TimeoutError
# data.to_csv(csvpath[:-4]+"_prcd.csv",index=None)
# labels=csv_labels["detectron2_joint_3d"]
# print(len(labels))

print(np.average(data["timestamp"].values[1:]-data["timestamp"].values[:-1]))

data["gravity_vx"]=0
data["gravity_vx"].iloc[:-1]=(data["gravity_x"].values[1:]-data["gravity_x"].values[:-1])/(data["timestamp"].values[1:]-data["timestamp"].values[:-1])
data["gravity_vy"]=0
data["gravity_vy"].iloc[:-1]=(data["gravity_x"].values[1:]-data["gravity_x"].values[:-1])/(data["timestamp"].values[1:]-data["timestamp"].values[:-1])

fig,ax=plt.subplots()
for label in ["gravity"]:
    ax.plot(data["timestamp"],data[label+"_x"],"o-",color="r",markersize=2,label=label+"_raw")
    ax2=ax.twinx()
    ax2.plot(data["timestamp"],data[label+"_vx"],"o-",color="r",markersize=2,label=label+"_raw")
data_timestamp=data["timestamp"]
data=mean_processor(data,20)
data["timestamp"]=data_timestamp
for label in ["gravity"]:
    ax.plot(data["timestamp"],data[label+"_x"],"o-",markersize=2,label=label)
    ax2=ax.twinx()
    ax2.plot(data["timestamp"],data[label+"_vx"],"o-",markersize=2,label=label)
    # ax.plot(data[label+"_x"],data[label+"_y"],"o-",label=label)
ax.legend()
ax2.legend()
# ax.set_aspect("equal")
plt.grid()
plt.savefig(os.path.split(csvpath)[0]+"/"+os.path.basename(csvpath)[:-8]+"_lab.png",dpi=300)