import matplotlib.pyplot as plt
from glob import glob
from pprint import pprint
import pandas as pd
from analysis_management import *
import numpy as np

path_management,csv_labels,color_dict=management_initial()

patient_data=pd.read_csv(path_management["patient_csv_path"])
result_data=pd.read_csv(path_management["result_csv_path"][:-4]+"_5to0.csv")
# patient_data["total_height"]=patient_data["height"]+patient_data["shoes"]
# print(patient_data)
# patient_data.to_csv(path_management["patient_csv_path"],index=False)
print(patient_data["total_height"].mean())
print(patient_data["total_height"].max()-patient_data["total_height"].mean())
print(patient_data["total_height"].min()-patient_data["total_height"].mean())

patient_data_low=patient_data[patient_data["total_height"]<170]["patient_id"]
patient_data_high=patient_data[patient_data["total_height"]>=170]["patient_id"]

# print(result_data["patient_id"])
n_perfect_low=0
n_partialout_low=0
n_totalout_low=0
n_dame_low=0
for patient in patient_data_low.values:
    # patient_id=str(patient).zfill(2)
    personal_result_data=result_data[result_data["patient_id"]==patient]
    perfect_data=personal_result_data[(personal_result_data["n_totalout"]==0) & (personal_result_data["n_partialout_head"]==0) & (personal_result_data["n_partialout_foot"]==0) & (personal_result_data["n_partialout_left"]==0) & (personal_result_data["n_partialout_right"]==0)]
    only_partialout_data=personal_result_data[(personal_result_data["n_totalout"]==0) & ((personal_result_data["n_partialout_head"]!=0) | (personal_result_data["n_partialout_foot"]!=0) | (personal_result_data["n_partialout_left"]!=0) | (personal_result_data["n_partialout_right"]!=0))]
    only_totalout_data=personal_result_data[(personal_result_data["n_totalout"]!=0) & (personal_result_data["n_partialout_head"]==0) & (personal_result_data["n_partialout_foot"]==0) & (personal_result_data["n_partialout_left"]==0) & (personal_result_data["n_partialout_right"]==0)]
    dame_data=personal_result_data[(personal_result_data["n_totalout"]!=0) & ((personal_result_data["n_partialout_head"]!=0) | (personal_result_data["n_partialout_foot"]!=0) | (personal_result_data["n_partialout_left"]!=0) | (personal_result_data["n_partialout_right"]!=0))]
    n_perfect_low+=len(perfect_data)
    n_partialout_low+=len(only_partialout_data)
    n_totalout_low+=len(only_totalout_data)
    n_dame_low+=len(dame_data)

n_perfect_high=0
n_partialout_high=0
n_totalout_high=0
n_dame_high=0
for patient in patient_data_high.values:
    # patient_id=str(patient).zfill(2)
    personal_result_data=result_data[result_data["patient_id"]==patient]
    perfect_data=personal_result_data[(personal_result_data["n_totalout"]==0) & (personal_result_data["n_partialout_head"]==0) & (personal_result_data["n_partialout_foot"]==0) & (personal_result_data["n_partialout_left"]==0) & (personal_result_data["n_partialout_right"]==0)]
    only_partialout_data=personal_result_data[(personal_result_data["n_totalout"]==0) & ((personal_result_data["n_partialout_head"]!=0) | (personal_result_data["n_partialout_foot"]!=0) | (personal_result_data["n_partialout_left"]!=0) | (personal_result_data["n_partialout_right"]!=0))]
    only_totalout_data=personal_result_data[(personal_result_data["n_totalout"]!=0) & (personal_result_data["n_partialout_head"]==0) & (personal_result_data["n_partialout_foot"]==0) & (personal_result_data["n_partialout_left"]==0) & (personal_result_data["n_partialout_right"]==0)]
    dame_data=personal_result_data[(personal_result_data["n_totalout"]!=0) & ((personal_result_data["n_partialout_head"]!=0) | (personal_result_data["n_partialout_foot"]!=0) | (personal_result_data["n_partialout_left"]!=0) | (personal_result_data["n_partialout_right"]!=0))]
    n_perfect_high+=len(perfect_data)
    n_partialout_high+=len(only_partialout_data)
    n_totalout_high+=len(only_totalout_data)
    n_dame_high+=len(dame_data)

print(n_perfect_low/len(patient_data_low)/11,
      n_partialout_low/len(patient_data_low)/11,
      n_totalout_low/len(patient_data_low)/11,
      n_dame_low/len(patient_data_low)/11)
print(n_perfect_high/len(patient_data_high)/11,
      n_partialout_high/len(patient_data_high)/11,
      n_totalout_high/len(patient_data_high)/11,
      n_dame_high/len(patient_data_high)/11)

path_management["table_hight_csv_path"]

columns=["below170","over170"]
index=["perfect","only_partial","only_total","others"]
data_array=np.array([
    [n_perfect_low/len(patient_data_low)/11,n_perfect_high/len(patient_data_high)/11],
    [n_partialout_low/len(patient_data_low)/11,n_partialout_high/len(patient_data_high)/11],
    [n_totalout_low/len(patient_data_low)/11,n_totalout_high/len(patient_data_high)/11],
    [n_dame_low/len(patient_data_low)/11,n_dame_high/len(patient_data_high)/11],
    ])
table=pd.DataFrame(data_array,columns=columns,index=index)
table.to_csv(path_management["table_hight_csv_path"])