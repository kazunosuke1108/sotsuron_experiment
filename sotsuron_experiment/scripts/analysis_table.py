import matplotlib.pyplot as plt
from glob import glob
from pprint import pprint
import pandas as pd
from analysis_management import *
import numpy as np

path_management,csv_labels,color_dict=management_initial()

data=pd.read_csv(path_management["result_csv_path"],header=0)#,names=csv_labels["result_chart"])
convert_headers=["n_frames","n_partialout_head","n_partialout_foot","n_partialout_left","n_partialout_right","n_totalout","time_partialout_head","time_partialout_foot","time_partialout_left","time_partialout_right","time_totalout",]
for header in convert_headers:
    data[header]=pd.to_numeric(data[header],errors="coerce")
print(data)

plt.rcParams["figure.figsize"] = (10,8)
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.family'] = 'Times New Roman'
fig, ax = plt.subplots() 
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
print(partialout_head,partialout_foot,partialout_left,partialout_right)
# plt.bar([1,2,3,4],[partialout_head/len(data)*100,partialout_foot/len(data)*100,partialout_left/len(data)*100,partialout_right/len(data)*100],tick_label=["partialout_head","partialout_foot","partialout_left","partialout_right"])
# plt.xlabel("lost parts")
# plt.ylabel("Probability of lost [%]")
# plt.pie([partialout_head,partialout_foot,partialout_left,partialout_right],labels=partialout_parts,startangle=90, autopct="%1.1f%%")
# plt.savefig(path_management["table_pie_path"])
# plt.show()

how_many_times_lost={}
how_many_times_lost["head"]={3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0,16:0}
for idx,row in data.iterrows():
    if row["time_partialout_head"]!=0:
        if row["patient_id"] in how_many_times_lost["head"].keys():
            how_many_times_lost["head"][row["patient_id"]]+=1
        else:
            how_many_times_lost["head"][row["patient_id"]]=1
how_many_times_lost["foot"]={3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0,16:0}
for idx,row in data.iterrows():
    if row["time_partialout_foot"]!=0:
        if row["patient_id"] in how_many_times_lost["foot"].keys():
            how_many_times_lost["foot"][row["patient_id"]]+=1
        else:
            how_many_times_lost["foot"][row["patient_id"]]=1
how_many_times_lost["left"]={3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0,16:0}
for idx,row in data.iterrows():
    if row["time_partialout_left"]!=0:
        if row["patient_id"] in how_many_times_lost["left"].keys():
            how_many_times_lost["left"][row["patient_id"]]+=1
        else:
            how_many_times_lost["left"][row["patient_id"]]=1
how_many_times_lost["right"]={3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0,16:0}
for idx,row in data.iterrows():
    if row["time_partialout_right"]!=0:
        if row["patient_id"] in how_many_times_lost["right"].keys():
            how_many_times_lost["right"][row["patient_id"]]+=1
        else:
            how_many_times_lost["right"][row["patient_id"]]=1

print(how_many_times_lost["head"])
print(how_many_times_lost["foot"])
print(how_many_times_lost["left"])
print(how_many_times_lost["right"])

plt.bar(np.array(list(how_many_times_lost["head"].keys())),how_many_times_lost["head"].values(),tick_label=["takahashi","yoshino","koyama","kosuge","saitou","fujii","otako","shindo","fukui","yoshinari","konishi","suzuki","ohshima","ohnishi"])
plt.xlabel("patient")
plt.ylabel("number of lost trials")
plt.ylim([0,11])
plt.title("head (n=11/person)")
plt.savefig(path_management["table_pie_path"][:-4]+"_head.png")
plt.cla()
plt.bar(how_many_times_lost["foot"].keys(),how_many_times_lost["foot"].values(),tick_label=["takahashi","yoshino","koyama","kosuge","saitou","fujii","otako","shindo","fukui","yoshinari","konishi","suzuki","ohshima","ohnishi"])
plt.xlabel("patient")
plt.ylabel("number of lost trials")
plt.ylim([0,11])
plt.title("foot (n=11/person)")
plt.savefig(path_management["table_pie_path"][:-4]+"_foot.png")
plt.cla()
plt.bar(how_many_times_lost["left"].keys(),how_many_times_lost["left"].values(),tick_label=["takahashi","yoshino","koyama","kosuge","saitou","fujii","otako","shindo","fukui","yoshinari","konishi","suzuki","ohshima","ohnishi"])
plt.xlabel("patient")
plt.ylabel("number of lost trials")
plt.ylim([0,11])
plt.title("left (n=11/person)")
plt.savefig(path_management["table_pie_path"][:-4]+"_left.png")
plt.cla()
plt.bar(how_many_times_lost["right"].keys(),how_many_times_lost["right"].values(),tick_label=["takahashi","yoshino","koyama","kosuge","saitou","fujii","otako","shindo","fukui","yoshinari","konishi","suzuki","ohshima","ohnishi"])
plt.xlabel("patient")
plt.ylabel("number of lost trials")
plt.ylim([0,11])
plt.title("right (n=11/person)")
plt.savefig(path_management["table_pie_path"][:-4]+"_right.png")
plt.cla()