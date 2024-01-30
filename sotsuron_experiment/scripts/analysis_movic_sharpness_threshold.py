import sys
import os
import time
import shutil
import numpy as np
import pandas as pd
from glob import glob
import matplotlib.pyplot as plt
from analysis_management import *

path_management,csv_labels,color_dict=management_initial()
plt.rcParams["figure.figsize"] = (15,10)
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.family'] = 'Times New Roman'

images_dir_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/analysis/velocity_error/big_data/hmn_01x_skeleton"
images_4000_dir_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/analysis/velocity_error/big_data/hmn_01x_skeleton_4000"
images_1000_dir_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/analysis/velocity_error/big_data/hmn_01x_skeleton_1000"
csv_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/analysis/velocity_error/_2023-12-21-10-22-39_laplacian_rgb_hmn.csv"
png_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/analysis/velocity_error/_2023-12-21-10-22-39_laplacian_rgb_hmn.png"


csv_data=pd.read_csv(csv_path,names=["timestamp","laplacian","min_x","max_x","min_y","max_y"])

csv_data_sharp_4000=csv_data[csv_data["laplacian"]>=4000]
csv_data_sharp_1000=csv_data[csv_data["laplacian"]<=1000]

for idx, row in csv_data_sharp_4000.iterrows():
    print(images_dir_path+"/"+str(int(row["timestamp"])))
    copyimage=sorted(glob(images_dir_path+"/"+str(int(row["timestamp"]))+"*"))[0]
    shutil.copy(copyimage,images_4000_dir_path+"/"+os.path.basename(copyimage))

for idx, row in csv_data_sharp_1000.iterrows():
    print(images_dir_path+"/"+str(int(row["timestamp"])))
    copyimage=sorted(glob(images_dir_path+"/"+str(int(row["timestamp"]))+"*"))[0]
    shutil.copy(copyimage,images_1000_dir_path+"/"+os.path.basename(copyimage))