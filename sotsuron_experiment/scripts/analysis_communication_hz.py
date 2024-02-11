import os
from glob import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from analysis_management import *

path_management,csv_labels,color_dict=management_initial()
plt.rcParams["figure.figsize"] = (10,8)
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.family'] = 'Times New Roman'

tf_csv_path="C:/Users/hayashide/ytlab_ros_ws/ytlab_nlpmp/ytlab_nlpmp_modules/results/20231221/20231221_102252_20231221_06_00_02_murayama/20231221_102306_tf.csv"
od_csv_path="C:/Users/hayashide/ytlab_ros_ws/ytlab_nlpmp/ytlab_nlpmp_modules/results/20231221/20231221_102252_20231221_06_00_02_murayama/20231221_102302_od.csv"
od_raw_csv_path="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-21-10-22-39/_2023-12-21-10-22-39_od_raw.csv"

ras_fast_detector_csv_path="C:/Users/hayashide/ytlab_ros_ws/ytlab_nlpmp/ytlab_nlpmp_modules/results/20231221/20231221_102252_20231221_06_00_02_murayama/20231221_102223_ytpc2021b.csv"
image_csv_path="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/velocity_error/_2023-12-21-10-22-39_laplacian_rgb_01x.csv"

csv_path=od_raw_csv_path

# data=pd.read_csv(csv_path,names=["t","x","y","z"],dtype=np.float64)
# data=pd.read_csv(csv_path,names=["t","laplacian"],dtype=np.float64)
data=pd.read_csv(csv_path,names=["t","x","y","z","ph"],dtype=np.float64)
# data=pd.read_csv(csv_path,names=csv_labels["detectron2_joint_3d_4"],dtype=np.float64)
# data.rename(columns={"timestamp":"t"},inplace=True)
data["dt"]=0
data["hz"]=0
data["dt"].iloc[:-1]=data["t"].values[1:]-data["t"].values[:-1]
data["hz"].iloc[:-1]=1/data["dt"].values[:-1]
print(data["dt"])
# raise TimeoutError
# plt.hist(data["hz"].iloc[:-1],bins=100)
plt.xlabel("Frequency [Hz]")
plt.ylabel("Number")
# plt.savefig("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/discussion/hz/"+os.path.basename(csv_path)[:-4]+".png")
print(data["hz"].mean())
print(data["hz"].std())
print(data["hz"].median())
print(data["hz"].mode())
print(data["hz"].max())
print(data["hz"].min())