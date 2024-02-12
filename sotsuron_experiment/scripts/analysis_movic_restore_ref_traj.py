import os
import sys
import re
import pickle
import numpy as np
import pandas as pd
from glob import glob
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from exp_commons import ExpCommons


class RestoreRefTraj(ExpCommons):
    def __init__(self,logpath="C:/Users/hayashide/ytlab_ros_ws/ytlab_nlpmp/ytlab_nlpmp_modules/log/20231221/20231221_102255.log"):
        super().__init__()
        
        plt.rcParams["figure.figsize"] = (15,10)
        plt.rcParams["figure.autolayout"] = True
        plt.rcParams["font.size"] = 24
        plt.rcParams['font.family'] = 'Times New Roman'

        self.logpath=logpath
        self.log_data=pd.read_table(self.logpath,names=["raw_txt"])
        self.csvpath=os.path.split(self.logpath)[0]+"/"+os.path.basename(self.logpath)[:-4]+".csv"
        self.pngpath="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/movic_clock"
        try:
            self.csv_data=pd.read_csv(self.csvpath,header=0)
        except FileNotFoundError:
            self.main_generate_csv(export=True)
            self.csv_data=pd.read_csv(self.csvpath,header=0)

    # utilities
    def unpack_2d_array(self,raw_txt):
        reg = '(?<=\[).+?(?=\])'
        array_txt=re.findall(reg, raw_txt)[1]
        if "," in array_txt:
            [val_1,val_2]=array_txt.split(",")
        else:
            [val_1,val_2]=array_txt.split()
            pass
        val_1,val_2=float(val_1),float(val_2)
        return np.array([val_1,val_2])

    def extract_last_string(self,raw_txt):
        extracted_txt=raw_txt.split()[-1]
        return extracted_txt

    def main_generate_csv(self,export=False):
        self.log_data["timestamp_unix"]=0
        self.log_data["timestamp_datetime"]=0
        self.log_data["log_category"]=""
        self.log_data["current_odom_x"]=np.nan
        self.log_data["current_odom_y"]=np.nan
        self.log_data["current_vel_x"]=np.nan
        self.log_data["current_vel_y"]=np.nan
        self.log_data["predicted_odom_x"]=np.nan
        self.log_data["predicted_odom_y"]=np.nan
        self.log_data["control_input_x"]=np.nan
        self.log_data["control_input_y"]=np.nan
        self.log_data["pickle_file_path"]=""
        self.log_data["pickle_file_path_windows"]=""
        self.log_data["pickle_new_version"]=False
        self.log_data["data_extracted_properly"]=False
        self.log_data["new_pickle_used"]=False

        for idx,row in self.log_data.iterrows():
            # timestampの抽出
            timestamp_str=row["raw_txt"][:len("0000-00-00 00:00:00,000")]
            timestamp_datetime=datetime.strptime(timestamp_str,'%Y-%m-%d %H:%M:%S,%f')
            timestamp_unix=timestamp_datetime.timestamp()
            self.log_data.loc[idx,"timestamp_datetime"]=timestamp_datetime
            self.log_data.loc[idx,"timestamp_unix"]=timestamp_unix

            # logのカテゴリ抽出
            if "preparation start" in row["raw_txt"]:
                self.log_data.loc[idx,"log_category"]="prep_start"
            elif "NO plan found" in row["raw_txt"]:
                self.log_data.loc[idx,"log_category"]="no_plan_found"
            elif "plan found" in row["raw_txt"]:
                self.log_data.loc[idx,"log_category"]="plan_found"
            elif "NO pickle found" in row["raw_txt"]:
                self.log_data.loc[idx,"log_category"]="no_pickle_found"
            elif "pickle file path" in row["raw_txt"]:
                self.log_data.loc[idx,"log_category"]="pickle_file_path"
                self.log_data.loc[idx:,"pickle_file_path"]=self.extract_last_string(row["raw_txt"])
                self.log_data.loc[idx:,"pickle_file_path_windows"]="C:/Users/hayashide/ytlab_ros_ws/ytlab_nlpmp"+self.extract_last_string(row["raw_txt"])[len("/home/hayashide/catkin_ws/src"):]
            elif "pickle was recognized as NEW version" in row["raw_txt"]:
                self.log_data.loc[idx,"log_category"]="pickle_new_version"
                self.log_data.loc[idx:,"pickle_new_version"]=True
            elif "pickle was recognized as EXISTING version" in row["raw_txt"]:
                self.log_data.loc[idx,"log_category"]="pickle_existing_version"
                self.log_data.loc[idx:,"pickle_new_version"]=False
            elif "/odom -> /base_link connected" in row["raw_txt"]:
                self.log_data.loc[idx,"log_category"]="tf_checked"
            elif "new data extracted properly" in row["raw_txt"]:
                self.log_data.loc[idx,"log_category"]="data_extracted_properly"
                self.log_data.loc[idx:,"data_extracted_properly"]=True
                self.log_data.loc[idx:,"new_pickle_used"]=True
            elif "new data FAILED to be extracted" in row["raw_txt"]:
                self.log_data.loc[idx,"log_category"]="data_extracted_failed"
                self.log_data.loc[idx:,"data_extracted_properly"]=False
            elif "published" in row["raw_txt"]:
                self.log_data.loc[idx,"log_category"]="published"
            elif "current odom" in row["raw_txt"]:
                self.log_data.loc[idx,"log_category"]="current_odom"
                self.log_data.loc[idx:,"current_odom_x"],self.log_data.loc[idx:,"current_odom_y"]=self.unpack_2d_array(raw_txt=row["raw_txt"])
            elif "current vel" in row["raw_txt"]:
                self.log_data.loc[idx,"log_category"]="current_vel"
                self.log_data.loc[idx:,"current_vel_x"],self.log_data.loc[idx:,"current_vel_y"]=self.unpack_2d_array(raw_txt=row["raw_txt"])
            elif "predicted odom" in row["raw_txt"]:
                self.log_data.loc[idx,"log_category"]="predicted_odom"
                self.log_data.loc[idx:,"predicted_odom_x"],self.log_data.loc[idx:,"predicted_odom_y"]=self.unpack_2d_array(raw_txt=row["raw_txt"])
            elif "control input" in row["raw_txt"]:
                self.log_data.loc[idx,"log_category"]="control_input"
                self.log_data.loc[idx:,"control_input_x"],self.log_data.loc[idx:,"control_input_y"]=self.unpack_2d_array(raw_txt=row["raw_txt"])
            elif "old pickle will be used" in row["raw_txt"]:
                self.log_data.loc[idx,"log_category"]="old_pickle_used"
                self.log_data.loc[idx:,"new_pickle_used"]=False
            elif "arrived goal" in row["raw_txt"]:
                self.log_data.loc[idx,"log_category"]="arrived_goal"
            else:
                print("### 未定義のカテゴリ ###")
                print(f"line: {idx}     ",row["raw_txt"])
                raise Exception

            # メッセージの抽出
        if export:
            print("###")
            self.log_data.to_csv(self.csvpath)

    def concat_traj(self,save_concat_data=True):
        t=np.array([0])
        zR=np.array([[0,0,0,0,0,0]]).T
        roi_data=self.csv_data[(self.csv_data["pickle_new_version"]==True) & (self.csv_data["data_extracted_properly"]==True) & (self.csv_data["new_pickle_used"]==True) & (self.csv_data["log_category"]=="data_extracted_properly")]
        gs = GridSpec(2, 1)
        # 結合処理
        plt.subplot(gs[0])
        for idx, row in roi_data.iterrows():
            timestamp_unix=row["timestamp_unix"]
            pickle_file_path=row["pickle_file_path_windows"]
            with open(pickle_file_path, 'rb') as f:
                pickledata = pickle.load(f)
            t_new=timestamp_unix+pickledata["solution"]["t"]
            zR_new=pickledata["solution"]["zR"]
            cut_idx=np.argwhere(t<timestamp_unix).max()
            t=t[:cut_idx]
            zR=zR[:,:cut_idx]
            t=np.hstack([t,t_new])
            zR=np.hstack([zR,zR_new])
            print(t.shape)
            print(zR.shape)
            plt.plot(t_new,zR_new[0,:],linewidth=0.5)#,label=f"solution at {idx}")

        plt.plot(t,zR[0,:],"o-",linewidth=3,label="global reference traj.")
        plt.legend()
        plt.grid()
        plt.xlabel("Time $\it{t}$ [s]")
        plt.ylabel("Position in hallway direction $\it{x}$ [m]")
        plt.title(f"Restored reference trajectory {os.path.basename(self.logpath[:-4])} {os.path.basename(sys.argv[0])}")
        
        if save_concat_data:
            concat_pickle_data={}
            concat_pickle_data["logpath"]=self.logpath
            concat_pickle_data["t"]=t
            concat_pickle_data["zR"]=zR
            with open(os.path.split(self.logpath)[0]+"/"+os.path.basename(self.logpath)[:-4]+".pickle", mode='wb') as f:
                pickle.dump(concat_pickle_data, f)

        # クロック数の推移を観察
        plt.subplot(gs[1])
        roi_data["clock_hz"]=0
        roi_data["clock_hz"].iloc[1:]=1/(roi_data["timestamp_unix"].values[1:]-roi_data["timestamp_unix"].values[:-1])
        plt.plot(roi_data["timestamp_unix"],roi_data["clock_hz"])
        plt.legend()
        plt.grid()
        plt.xlabel("Time $\it{t}$ [s]")
        plt.ylabel("Planning frequency [Hz]")
        plt.title(f"Frequency {os.path.basename(self.logpath[:-4])} {os.path.basename(sys.argv[0])}")
        plt.savefig(self.pngpath+"/"+os.path.basename(self.logpath)[:-4]+".png")

logpaths_candidate=[]
logpaths_candidate+=sorted(glob("C:/Users/hayashide/ytlab_ros_ws/ytlab_nlpmp/ytlab_nlpmp_modules/log/20231219/*.log"))
logpaths_candidate+=sorted(glob("C:/Users/hayashide/ytlab_ros_ws/ytlab_nlpmp/ytlab_nlpmp_modules/log/20231221/*.log"))
logpaths=[]
for logpath_candidate in logpaths_candidate:
    logpaths_candidate_data=pd.read_table(logpath_candidate,names=["raw_txt"])
    for idx,row in logpaths_candidate_data.iterrows():
        if "TwistTrajPublisher" in row["raw_txt"]:
            logpaths.append(logpath_candidate)
        break
print(logpaths)
for logpath in logpaths:
    try:
        cls=RestoreRefTraj(logpath=logpath)
        # cls.main_generate_csv(export=True)
        cls.concat_traj()
    except Exception:
        pass