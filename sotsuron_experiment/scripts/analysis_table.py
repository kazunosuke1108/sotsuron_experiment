import matplotlib.pyplot as plt
from glob import glob
from pprint import pprint
import pandas as pd
from analysis_management import *

path_management,csv_labels,color_dict=management_initial()

data=pd.read_csv(path_management["result_csv_path"],header=0)#,names=csv_labels["result_chart"])
convert_headers=["n_frames","n_partialout_head","n_partialout_foot","n_partialout_left","n_partialout_right","n_totalout","time_partialout_head","time_partialout_foot","time_partialout_left","time_partialout_right","time_totalout",]
for header in convert_headers:
    data[header]=pd.to_numeric(data[header],errors="coerce")
print(data)


# 実験type,廊下位置別の成功率
type_id=[i for i in range(12)]
columns=type_id+["left","center","stop"]+["all"]
index=["perfect","only_partial","only_total","others"]
table=pd.DataFrame(columns=columns,index=index)
for idx in index:
    for column in columns:
        if column=="left":
            roi_data=data[(data["type_id"]==0) | (data["type_id"]==1) | (data["type_id"]==3) | (data["type_id"]==6) | (data["type_id"]==8)]
        elif column=="center":
            roi_data=data[(data["type_id"]==2) | (data["type_id"]==4) | (data["type_id"]==7) | (data["type_id"]==9)]
        elif column=="stop":
            roi_data=data[(data["type_id"]==5) | (data["type_id"]==10)]
        elif column=="all":
            roi_data=data
        else:
            roi_data=data[data["type_id"]==column]
        if idx=="perfect":
            try:
                ratio=len(roi_data[roi_data["time_totalout"]==0][roi_data["time_partialout_head"]==0][roi_data["time_partialout_foot"]==0][roi_data["time_partialout_left"]==0][roi_data["time_partialout_right"]==0])/len(roi_data)
                table[column][idx]=ratio
            except ZeroDivisionError:
                pass
        elif idx=="only_partial":
            try:
                ratio=len(roi_data[roi_data["time_totalout"]==0][(roi_data["time_partialout_head"]!=0) |(roi_data["time_partialout_foot"]!=0) |(roi_data["time_partialout_left"]!=0) |(roi_data["time_partialout_right"]!=0)])/len(roi_data)
                table[column][idx]=ratio
            except ZeroDivisionError:
                pass
        elif idx=="only_total":
            try:
                ratio=len(roi_data[roi_data["time_totalout"]!=0][roi_data["time_partialout_head"]==0][roi_data["time_partialout_foot"]==0][roi_data["time_partialout_left"]==0][roi_data["time_partialout_right"]==0])/len(roi_data)
                table[column][idx]=ratio
            except ZeroDivisionError:
                pass
        elif idx=="others":
            try:
                ratio=len(roi_data[roi_data["time_totalout"]!=0][(roi_data["time_partialout_head"]!=0) |(roi_data["time_partialout_foot"]!=0) |(roi_data["time_partialout_left"]!=0) |(roi_data["time_partialout_right"]!=0)])/len(roi_data)
                table[column][idx]=ratio
            except ZeroDivisionError:
                pass

table.to_csv(path_management["table_csv_path"])

# なぜ部分欠損が生じたのか
partialout_parts=["head","foot","left","right"]
partialout_head=len(data[data["time_partialout_head"]!=0])
partialout_foot=len(data[data["time_partialout_foot"]!=0])
partialout_left=len(data[data["time_partialout_left"]!=0])
partialout_right=len(data[data["time_partialout_right"]!=0])

plt.pie([partialout_head,partialout_foot,partialout_left,partialout_right],labels=partialout_parts,startangle=90, autopct="%1.1f%%")
plt.savefig(path_management["table_pie_path"])
plt.show()