import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from analysis_management import *
path_management,csv_labels,color_dict=management_initial()
plt.rcParams["figure.figsize"] = (15,10)
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.family'] = 'Times New Roman'

results_dir_path="/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2024-02-04-17-23-27"
base_accurate_imu_csv_path=results_dir_path+"/base_accurate_imu_1.csv"
base_imu_csv_path=results_dir_path+"/base_imu_1.csv"
head_imu_csv_path=results_dir_path+"/imu_1.csv"

base_accurate_imu_data=pd.read_csv(base_accurate_imu_csv_path,names=csv_labels["imu"])
base_imu_data=pd.read_csv(base_imu_csv_path,names=csv_labels["imu"])
head_imu_data=pd.read_csv(head_imu_csv_path,names=csv_labels["imu"])

print(base_accurate_imu_data)
print(csv_labels["imu"])
plt.plot(base_accurate_imu_data["timestamp"],base_accurate_imu_data["lin_acc_x"],label="lin_acc_x")
plt.plot(base_accurate_imu_data["timestamp"],base_accurate_imu_data["lin_acc_y"],label="lin_acc_y")
plt.plot(base_accurate_imu_data["timestamp"],base_accurate_imu_data["lin_acc_z"],label="lin_acc_z")
plt.show()