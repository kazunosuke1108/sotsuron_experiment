import re
import numpy as np
import pandas as pd
from datetime import datetime
from glob import glob
import matplotlib.pyplot as plt
from exp_commons import ExpCommons
from analysis_management import *
from noise_processor import *
from matplotlib.gridspec import GridSpec

class MovicManagement(ExpCommons):
    def __init__(self):
        super().__init__()
        self.path_management,self.csv_labels,self.color_dict=management_initial()
        plt.rcParams["figure.figsize"] = (15,10)
        plt.rcParams["figure.autolayout"] = True
        plt.rcParams["font.size"] = 24
        plt.rcParams['font.family'] = 'Times New Roman'
        
        self.exp_memo_path="C:/Users/hayashide/ytlab_ros_ws/ytlab_nlpmp/ytlab_nlpmp_modules/scripts/memo/exp_memo.csv"
        self.exp_memo_data=pd.read_csv(self.exp_memo_path,header=0)
        self.log_paths=sorted(glob("C:/Users/hayashide/ytlab_ros_ws/ytlab_nlpmp/ytlab_nlpmp_modules/log/20231219/*.log"))+sorted(glob("C:/Users/hayashide/ytlab_ros_ws/ytlab_nlpmp/ytlab_nlpmp_modules/log/20231221/*.log"))
        pass

    def connect_log_and_exp_memo(self):
        # bag_pathからrosbag取得timestampを判別し，記入
        self.exp_memo_data["timestamp"]=np.nan
        for idx, row in self.exp_memo_data.iterrows():
            if row["bag_path"]=="データ容量オーバーで削除":
                continue
            try:
                self.exp_memo_data.loc[idx,"timestamp"]=datetime.strptime(row["bag_path"],'_%Y-%m-%d-%H-%M-%S.bag').timestamp()
            except ValueError:
                self.exp_memo_data.loc[idx,"timestamp"]=datetime.strptime(row["bag_path"],'_%Y-%m-%d-%H-%M-%S.bag.active').timestamp()
            except (TypeError,KeyError):
                pass
            print(row["bag_path"])
            print(idx,self.exp_memo_data.loc[idx,"timestamp"])
            pass

        # logを読んでlogの作成日時とlogの出元pythonファイル名を判別し，exp_memoに記入
        self.exp_memo_data["log_exp_main"]=""
        self.exp_memo_data["log_exp_TwistTraj"]=""
        self.exp_memo_data["log_exp_calib_zed_tf_publisher"]=""
        self.exp_memo_data["log_exp_odom_subscriber"]=""
        self.exp_memo_data["log_exp_tf_listener"]=""
        
        for log_path in self.log_paths:
            self.log_data=pd.read_table(log_path,names=["raw_txt"])
            try:
                timestamp_str=self.log_data.loc[0,"raw_txt"][:len("0000-00-00 00:00:00,000")]
            except KeyError:# logが白紙だった場合
                continue
            timestamp_datetime=datetime.strptime(timestamp_str,'%Y-%m-%d %H:%M:%S,%f')
            timestamp_unix=timestamp_datetime.timestamp()
            py_filename=self.extract_py_filename(self.log_data.loc[0,"raw_txt"])
            exp_memo_match_idx=(abs(timestamp_unix-self.exp_memo_data["timestamp"])).argmin()

            self.exp_memo_data.loc[exp_memo_match_idx,f"log_{py_filename}"]=log_path
            
        self.exp_memo_data.to_csv(self.exp_memo_path,index=0)

    


cls=MovicManagement()
print(cls.exp_memo_data.loc[0,"nlpmp_path"])
# cls.connect_log_and_exp_memo()