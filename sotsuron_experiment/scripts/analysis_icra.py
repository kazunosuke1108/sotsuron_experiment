#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
from glob import glob
import numpy as np
import pandas as pd

from analysis_management import management_initial

class analysisICRA():
    def __init__(self,csv_path,results_dir_path,output_dir_path):
        # load memo
        self.path_management, self.csv_labels, self.color_dict=management_initial()
        self.exp_memo=pd.read_csv(csv_path,header=0)
        self.results_dir_path=results_dir_path
        self.output_dir_path=output_dir_path

        # initialize analysis output table
        self.output_memo=pd.DataFrame(columns=["person_id","name","type","trial","bag","timelength","trunk_length","gravity_length","trunk_velocity","gravity_velocity"])
        pass
    
    def pipeline(self,trial_dir_path):
        print(f"### {os.path.basename(trial_dir_path)}")
        # 解析csvの読み込み
        od_raw_csv_path=sorted(glob(trial_dir_path+"/*od_raw.csv"))
        if len(od_raw_csv_path)>0:
            od_raw_csv_path=od_raw_csv_path[0]
        else:
            raise Exception
        od_data=pd.read_csv(od_raw_csv_path,names=self.csv_labels["odometry"])
        od_data.dropna(inplace=True)
        start_timestamp=od_data["timestamp"][od_data["x"]>0.1].values[0]
        try:
            end_timestamp=od_data["timestamp"][od_data["x"]>6].values[0]
        except IndexError:
            end_timestamp=start_timestamp+30
        print(start_timestamp)
        # raise TimeoutError
        
        tf_raw_csv_path=sorted(glob(trial_dir_path+"/*tf_raw.csv"))
        if len(tf_raw_csv_path)>0:
            tf_raw_csv_path=tf_raw_csv_path[0]
        else:
            raise Exception
        tf_data=pd.read_csv(tf_raw_csv_path,names=self.csv_labels["detectron2_joint_3d"],skiprows=[0])
        tf_data.dropna(inplace=True)

        # ハズレ値の除去？
        # 出走時刻以前を削除
        tf_data.reset_index()
        print(tf_data.shape[0])
        tf_data=tf_data[tf_data["timestamp"]>start_timestamp]
        tf_data=tf_data[tf_data["timestamp"]<end_timestamp]
        print(tf_data.shape[0])
        # print(tf_data.shape)
        
        
        # 不連続箇所の検出
        open_thre=1
        open_idx=[]
        for idx in range(tf_data.shape[0]-1):
            if tf_data["timestamp"].values[idx+1]-tf_data["timestamp"].values[idx]>open_thre:
                open_idx.append(idx)
        # 最長連続部分の抽出
        if len(open_idx)==0:
            extract_range=([0,tf_data.shape[0]])
        elif len(open_idx)==1:
            zenhan=open_idx[0]
            kouhan=tf_data.shape[0]-open_idx[0]
            if zenhan>kouhan:
                extract_range=([0,open_idx[0]])
            else:
                extract_range=([open_idx[0]+1,tf_data.shape[0]])
        else:
            tuples_candidate=[]
            for i,idx in enumerate(open_idx):
                if i==0:
                    tuples_candidate.append([0,open_idx[i]])
                elif i==len(open_idx)-1:
                    tuples_candidate.append([open_idx[i-1]+1,open_idx[i]])
                    tuples_candidate.append([open_idx[i]+1,tf_data.shape[0]])
                else:
                    tuples_candidate.append([open_idx[i-1]+1,open_idx[i]])
            tuples_candidate=np.array(tuples_candidate)
            tuples_count=tuples_candidate[:,1]-tuples_candidate[:,0]
            print(tuples_count)
            extract_range=(list((tuples_candidate[np.argmax(tuples_count)]).flatten()))
            print(extract_range)
        # print(extract_range)

        tf_data=tf_data[extract_range[0]:extract_range[1]]
        # print(tf_data.shape)


        # 連続撮影時間の算出
        timelength=tf_data["timestamp"].values[-1]-tf_data["timestamp"].values[0]

        # 連続撮影距離の算出
        trunk_length=abs(tf_data["trunk_x"].values[-1]-tf_data["trunk_x"].values[0])
        gravity_length=abs(tf_data["gravity_x"].values[-1]-tf_data["gravity_x"].values[0])

        # 連続撮影区間の速度算出
        trunk_velocity=trunk_length/timelength
        gravity_velocity=gravity_length/timelength

        print("timelength: ",timelength)
        print("trunk_length: ",trunk_length)
        print("gravity_length: ",gravity_length)
        print("trunk_velocity: ",trunk_velocity)
        print("gravity_velocity: ",gravity_velocity)
        
        return timelength,trunk_length,gravity_length,trunk_velocity,gravity_velocity

    def main(self):
        # 1試行ずつ読む
        for idx,row in self.exp_memo.iterrows():
            bag_basename=row["bag"]
            if ".bag" in bag_basename:
                bag_basename=bag_basename[:-4]
            # print(os.path.isdir(self.results_dir_path+"/"+bag_basename))
            
            trial_dir_path=self.results_dir_path+"/"+bag_basename
            timelength,trunk_length,gravity_length,trunk_velocity,gravity_velocity=self.pipeline(trial_dir_path)
            self.output_memo.loc[bag_basename]=[
                row["person_id"],row["name"],row["type"],row["trial"],row["bag"],
                timelength,trunk_length,gravity_length,trunk_velocity,gravity_velocity
            ]
        data_average=[
            np.nan,np.nan,np.nan,np.nan,np.nan,
            self.output_memo["timelength"].mean(),
            self.output_memo["trunk_length"].mean(),
            self.output_memo["gravity_length"].mean(),
            self.output_memo["trunk_velocity"].mean(),
            self.output_memo["gravity_velocity"].mean()
        ]
        data_std=[
            np.nan,np.nan,np.nan,np.nan,np.nan,
            self.output_memo["timelength"].std(),
            self.output_memo["trunk_length"].std(),
            self.output_memo["gravity_length"].std(),
            self.output_memo["trunk_velocity"].std(),
            self.output_memo["gravity_velocity"].std()
        ]
        data_min=[
            np.nan,np.nan,np.nan,np.nan,np.nan,
            self.output_memo["timelength"].min(),
            self.output_memo["trunk_length"].min(),
            self.output_memo["gravity_length"].min(),
            self.output_memo["trunk_velocity"].min(),
            self.output_memo["gravity_velocity"].min()
        ]
        data_max=[
            np.nan,np.nan,np.nan,np.nan,np.nan,
            self.output_memo["timelength"].max(),
            self.output_memo["trunk_length"].max(),
            self.output_memo["gravity_length"].max(),
            self.output_memo["trunk_velocity"].max(),
            self.output_memo["gravity_velocity"].max()
        ]
        self.output_memo.loc["average"]=data_average
        self.output_memo.loc["std"]=data_std
        self.output_memo.loc["min"]=data_min
        self.output_memo.loc["max"]=data_max

        self.output_memo.to_csv(self.output_dir_path+"/analysis_output_memo.csv")

csv_path="/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/exp_memo.csv"
results_dir_path="/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12"
output_dir_path="/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/icra/analysis_output"
cls=analysisICRA(csv_path,results_dir_path,output_dir_path)
cls.main()