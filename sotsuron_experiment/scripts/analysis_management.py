#! /usr/bin/python3
# -*- coding: utf-8 -*-

from glob import glob
import json
import os
import numpy as np

def management_initial():

    ## パス管理dict作成
    path_management={}
    if os.name == "nt":
        home = os.path.expanduser("~")
    else:
        home=os.environ['HOME']
    path_management["exp_memo_csv_path"]=f"{home}/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/exp_memo.csv"
    path_management["velocity_table_path"]=f"{home}/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/velocity_table.csv"
    path_management["stride_table_path"]=f"{home}/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/stride_table.csv"
    path_management["humpback_table_path"]=f"{home}/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/humpback_table.csv"
    path_management["vicon_humpback_table_path"]=f"{home}/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/20231220_VICON/accuracy_table/vicon_humpback.csv"
    path_management["vicon_hip_table_path"]=f"{home}/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/20231220_VICON/accuracy_table/vicon_hip.csv"
    path_management["velocity_csv_path"]=f"{home}/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/velocity.csv"
    path_management["stride_csv_path"]=f"{home}/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/stride.csv"
    path_management["humpback_csv_path"]=f"{home}/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/humpback.csv"
    path_management["json_dir_path"]=f"{home}/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/json"
    path_management["png_dir_path"]=f"{home}/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/png"
    path_management["csv_dir_path"]=f"{home}/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/csv"
    path_management["debug_csv_path"]=path_management["csv_dir_path"]+"/debug.csv"
    path_management["denoise_3d_csv_path"]=path_management["csv_dir_path"]+"/denoise_3d"
    path_management["patient_csv_path"]=path_management["csv_dir_path"]+"/patient_data.csv"
    path_management["result_csv_path"]=path_management["csv_dir_path"]+"/result.csv"
    path_management["table_csv_path"]=path_management["csv_dir_path"]+"/table.csv"
    path_management["table_hight_csv_path"]=path_management["csv_dir_path"]+"/table_height.csv"
    path_management["comparefiles_csv_path"]=path_management["csv_dir_path"]+"/comparefiles.csv"
    path_management["usabledata_csv_path"]=path_management["csv_dir_path"]+"/usabledata.csv"
    path_management["table_pie_path"]=path_management["png_dir_path"]+"/pie_why_partialout.png"
    path_management["ras_tf_csv_dir_path"]=sorted(glob(f"{home}/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/ras_csv/*_tf.csv"))
    path_management["ras_2d_csv_dir_path"]=sorted(glob(f"{home}/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/ras_csv/*_2d.csv"))
    path_management["ras_od_csv_dir_path"]=[]
    path_management["ras_od_csv_dir_path_temp"]=sorted(glob(f"{home}/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/ras_csv/*.csv"))
    for ras_od_csv_candidate in path_management["ras_od_csv_dir_path_temp"]:
        if ("_tf" not in ras_od_csv_candidate) and ("_2d" not in ras_od_csv_candidate) and ("_kp" not in ras_od_csv_candidate):
                        path_management["ras_od_csv_dir_path"].append(ras_od_csv_candidate)
    path_management["denoise_3d_csv_dir_path"]=f"{home}/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/csv/denoise_3d"
    path_management["denoise_2d_csv_dir_path"]=f"{home}/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/csv/denoise_2d"
    
    ### 重複のない試行を取得
    path_management["ras_tf_csv_dir_path_unique"]=[]
    for trial in path_management["ras_tf_csv_dir_path"]:
        if trial not in path_management["ras_tf_csv_dir_path_unique"]:
            same_trial=sorted(glob(os.path.split(trial)[0]+"/"+os.path.split(trial)[1][:6]+"*_tf.csv"))
            if same_trial[-1] not in path_management["ras_tf_csv_dir_path_unique"]:
                path_management["ras_tf_csv_dir_path_unique"].append(same_trial[-1])

    path_management["ras_2d_csv_dir_path_unique"]=[]
    for trial in path_management["ras_2d_csv_dir_path"]:
        if trial not in path_management["ras_2d_csv_dir_path_unique"]:
            same_trial=sorted(glob(os.path.split(trial)[0]+"/"+os.path.split(trial)[1][:6]+"*_2d.csv"))
            if same_trial[-1] not in path_management["ras_2d_csv_dir_path_unique"]:
                path_management["ras_2d_csv_dir_path_unique"].append(same_trial[-1])

    path_management["ras_od_csv_dir_path_unique"]=[]
    for trial in path_management["ras_od_csv_dir_path"]:
        if trial not in path_management["ras_od_csv_dir_path_unique"]:
            same_trial=sorted(glob(os.path.split(trial)[0]+"/"+os.path.split(trial)[1][:6]+"*.csv"))
            same_trial2=[]
            for same_trial_candidate in same_trial:
                 if ("_tf" not in same_trial_candidate) and ("_kp" not in same_trial_candidate) and ("_2d" not in same_trial_candidate):
                      same_trial2.append(same_trial_candidate)
            # print(same_trial)
            if same_trial2[-1] not in path_management["ras_od_csv_dir_path_unique"]:
                path_management["ras_od_csv_dir_path_unique"].append(same_trial2[-1])
    # csvのnames作成
    csv_labels={}
    csv_labels["odometry"]=["timestamp","x","y","theta","pan"]
    csv_labels["command_velocity"]=["timestamp","v_x","v_y","v_z","omg_x","omg_y","omg_z"]
    csv_labels["detectron2_joint"]=["gravity","nose","l_eye","r_eye","l_ear","r_ear","l_shoulder","r_shoulder","l_elbow","r_elbow","l_hand","r_hand","l_base","r_base","l_knee","r_knee","l_foot","r_foot"]
    csv_labels["detectron2_joint_trunk"]=["gravity","trunk","nose","l_eye","r_eye","l_ear","r_ear","l_shoulder","r_shoulder","l_elbow","r_elbow","l_hand","r_hand","l_base","r_base","l_knee","r_knee","l_foot","r_foot"]
    csv_labels["detectron2_joint_2d"]=["timestamp"]
    csv_labels["detectron2_joint_3d"]=["timestamp"]
    csv_labels["detectron2_joint_3d_4"]=["timestamp"]
    for joint_name in csv_labels["detectron2_joint"][1:]:
        suffixes=["_x","_y","_z"]
        for suffix in suffixes:
            csv_labels["detectron2_joint_2d"].append(joint_name+suffix)
    
    for joint_name in csv_labels["detectron2_joint_trunk"]:
        suffixes=["_x","_y","_z"]
        for suffix in suffixes:
            csv_labels["detectron2_joint_3d"].append(joint_name+suffix)
    
    for joint_name in csv_labels["detectron2_joint_trunk"]:
        suffixes=["_x","_y","_z","_0"]
        for suffix in suffixes:
            csv_labels["detectron2_joint_3d_4"].append(joint_name+suffix)

    csv_labels["result_chart"]=["patient_id","type_id","trial_id","n_frames","n_partialout_head","n_partialout_foot","n_partialout_left","n_partialout_right","n_totalout","time_partialout_head","time_partialout_foot","time_partialout_left","time_partialout_right","time_totalout","csvpath"]
    csv_labels["imu"]=["timestamp","orien_x","orien_y","orien_z","orien_w","ang_vel_x","ang_vel_y","ang_vel_z","lin_acc_x","lin_acc_y","lin_acc_z"]
    cov_list=["orien_cov","ang_vel_cov","lin_acc_cov"]
    for cov_name in cov_list:
        for i in np.arange(1,10,1):
            csv_labels["imu"].append(cov_name+"_"+str(i).zfill(2))
    

    # 実験種別と色の対応表
    color_dict={"00":"r",
            "01":"r",
            "02":"k",
            "03":"m",
            "04":"k",
            "05":"k",
            "06":"b",
            "07":"k",
            "08":"c",
            "09":"k",
            "10":"k",
            "11":"k",
            }
    
    return path_management,csv_labels,color_dict


def json_saver(path_management,csv_labels,color_dict):
    json_dict={
    "path_management":path_management,
    "csv_labels":csv_labels,
    "color_dict":color_dict,
    }
    tf = open(path_management["json_dir_path"]+f"/analysis_database.json", "w")
    json.dump(json_dict, tf)
    tf.close()