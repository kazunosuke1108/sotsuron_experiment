import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from analysis_management import *
path_management,csv_labels,color_dict=management_initial()

odom_to_zed_csv_path="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-21-10-22-39/_2023-12-21-10-22-39_tf_raw.csv"

zR=pd.read_csv(odom_to_zed_csv_path,names=csv_labels["detectron2_joint_3d"])
zR_trunk_x=zR[["r_shoulder_x","l_shoulder_x","r_base_x","l_base_x"]]
print(zR_trunk_x.median(axis=1))
plt.plot(zR["timestamp"],zR["r_shoulder_x"],"-",markersize=1,label="r_shoulder_x")
plt.plot(zR["timestamp"],zR["l_shoulder_x"],"-",markersize=1,label="l_shoulder_x")
plt.plot(zR["timestamp"],zR["r_base_x"],"-",markersize=1,label="r_base_x")
plt.plot(zR["timestamp"],zR["l_base_x"],"-",markersize=1,label="l_base_x")
plt.plot(zR["timestamp"],zR_trunk_x.median(axis=1),label="median")
plt.legend()
plt.show()