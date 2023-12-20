import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error,confusion_matrix
from noise_processor import *
from analysis_management import *
from analysis_initial_processor import *
from scipy import signal


class analysisRas():
    path_management,csv_labels,color_dict=management_initial()
    def __init__(self):
        self.exp_memo_csv_path=path_management["exp_memo_csv_path"]
        self.exp_memo_table=pd.read_csv(self.exp_memo_csv_path,header=0)
        self.exp_memo_table["estm_velocity"]=abs(self.exp_memo_table["estm_velocity"])
        print(self.exp_memo_table)
    
    def analyze_velocity(self):
        vel_table=pd.DataFrame(index=["0_1_normal","2_avoid","3_humpback","4_paralysis","all"],columns=["truth_velocity_mean[m/s]","estm_velocity_mean[m/s]","RMSE[m/s]","err_std[m/s]"])
        for idx in vel_table.index:
            if "normal" in idx:
                flag=(self.exp_memo_table["type"]==0) | (self.exp_memo_table["type"]==1)
            elif "avoid" in idx:
                flag=(self.exp_memo_table["type"]==2)
            elif "humpback" in idx:
                flag=(self.exp_memo_table["type"]==3)
            elif "paralysis" in idx:
                flag=(self.exp_memo_table["type"]==4)
            elif "all" in idx:
                flag=(self.exp_memo_table["type"]!=np.nan)

            vel_table["truth_velocity_mean[m/s]"][idx]=self.exp_memo_table["truth_velocity"][flag].mean()
            vel_table["estm_velocity_mean[m/s]"][idx]=self.exp_memo_table["estm_velocity"][flag].mean()
            vel_table["RMSE[m/s]"][idx]=mean_squared_error(self.exp_memo_table["estm_velocity"][flag],self.exp_memo_table["truth_velocity"][flag])
            vel_table["err_std[m/s]"][idx]=(self.exp_memo_table["estm_velocity"][flag]-self.exp_memo_table["truth_velocity"][flag]).std()
        
        print(vel_table)
        vel_table.to_csv(path_management["velocity_table_path"])

    def analyze_stride(self):
        stride_table=pd.DataFrame(index=["0_1_normal","2_avoid","3_humpback","4_paralysis","all"],columns=["truth_stride_mean[m]","estm_stride_mean[m]","RMSE[m]","err_std[m]"])
        for idx in stride_table.index:
            if "normal" in idx:
                flag=(self.exp_memo_table["type"]==0) | (self.exp_memo_table["type"]==1)
            elif "avoid" in idx:
                flag=(self.exp_memo_table["type"]==2)
            elif "humpback" in idx:
                flag=(self.exp_memo_table["type"]==3)
            elif "paralysis" in idx:
                flag=(self.exp_memo_table["type"]==4)
            elif "all" in idx:
                flag=(self.exp_memo_table["type"]!=np.nan)

            stride_table["truth_stride_mean[m]"][idx]=self.exp_memo_table["truth_stride"][flag].mean()
            stride_table["estm_stride_mean[m]"][idx]=self.exp_memo_table["estm_stride_mean"][flag].mean()
            stride_table["RMSE[m]"][idx]=mean_squared_error(self.exp_memo_table["estm_stride_mean"][flag],self.exp_memo_table["truth_stride"][flag])
            stride_table["err_std[m]"][idx]=(self.exp_memo_table["estm_stride_mean"][flag]-self.exp_memo_table["truth_stride"][flag]).std()
        
        print(stride_table)
        stride_table.to_csv(path_management["stride_table_path"])

    def analyze_humpback(self):
        stride_table=pd.DataFrame(index=["0_1_normal","2_avoid","3_humpback","4_paralysis","all"],columns=["truth_humpback","estm_humpback_mean","","err_std[m]"])
        answer_binary=self.exp_memo_table["truth_humpback"]
        pred_binary=abs(self.exp_memo_table["estm_humpback_median"])>45/2
        confusion_mtx=confusion_matrix(answer_binary,pred_binary)
        print(pred_binary)
        conf_mat_table=pd.DataFrame(confusion_mtx,index=["truth_negative","truth_positive"],columns=["estm_negative","estm_positive"])
        conf_mat_table.to_csv(path_management["humpback_table_path"])
        # for idx in stride_table.index:
        #     if "normal" in idx:
        #         flag=(self.exp_memo_table["type"]==0) | (self.exp_memo_table["type"]==1)
        #     elif "avoid" in idx:
        #         flag=(self.exp_memo_table["type"]==2)
        #     elif "humpback" in idx:
        #         flag=(self.exp_memo_table["type"]==3)
        #     elif "paralysis" in idx:
        #         flag=(self.exp_memo_table["type"]==4)
        #     elif "all" in idx:
        #         flag=(self.exp_memo_table["type"]!=np.nan)

        #     stride_table["truth_stride_mean[m]"][idx]=self.exp_memo_table["truth_stride"][flag].mean()
        #     stride_table["estm_stride_mean[m]"][idx]=self.exp_memo_table["estm_stride_mean"][flag].mean()
        #     stride_table["RMSE[m]"][idx]=mean_squared_error(self.exp_memo_table["estm_stride_mean"][flag],self.exp_memo_table["truth_stride"][flag])
        #     stride_table["err_std[m]"][idx]=(self.exp_memo_table["estm_stride_mean"][flag]-self.exp_memo_table["truth_stride"][flag]).std()
        
        # print(stride_table)
        # stride_table.to_csv(path_management["stride_table_path"])

    def main(self):
        # self.analyze_velocity()
        # self.analyze_stride()
        self.analyze_humpback()
analysis=analysisRas()
analysis.main()
