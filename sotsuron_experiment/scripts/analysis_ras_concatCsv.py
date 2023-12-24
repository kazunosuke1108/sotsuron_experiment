import os
import sys
import numpy as np
import pandas as pd
from glob import glob
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from analysis_management import *
from analysis_initial_processor import *

plt.rcParams["figure.figsize"] = (12,8)
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.family'] = 'Times New Roman'

class concatCsv():
    def load_with_vicon(self,viconcsvpath="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/20231220_VICON/alldata/hayashide_robot_03_all.csv"):
        path_management,csv_labels,color_dict=management_initial()
        relationship_data=pd.read_csv("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/20231220_VICON/vicon_history_relationship.csv")
        
        # VICON data
        # Look
        self.viconcsvpath=viconcsvpath
        # self.viconcsvpath="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/20231220_VICON/hayashide_robot_05_modified.csv"
        # humpback
        # self.viconcsvpath="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/20231220_VICON/hayashide_robot_10_modified.csv"
        self.vicon_data=pd.read_csv(self.viconcsvpath,index_col=0,header=0)
        self.vicon_data["robot_robot1_X"]=self.vicon_data["robot_robot1_X"]/1000
        self.vicon_data["robot_robot1_Y"]=self.vicon_data["robot_robot1_Y"]/1000
        self.vicon_data["robot_robot1_Z"]=self.vicon_data["robot_robot1_Z"]/1000
        offset_x=self.vicon_data["robot_robot1_X"].iat[0]
        offset_y=self.vicon_data["robot_robot1_X"].iat[1]
        self.vicon_data["robot_robot1_X"]=self.vicon_data["robot_robot1_X"]-offset_x
        self.vicon_data["robot_robot1_Y"]=self.vicon_data["robot_robot1_Y"]-offset_y
        self.vicon_data["timestamp"]=self.vicon_data.index/60
        try:
            self.vicon_data["hayashide_CentreOfMass_X"]=self.vicon_data["hayashide_CentreOfMass_X"]/1000-offset_x
            self.vicon_data["hayashide_CentreOfMass_Y"]=self.vicon_data["hayashide_CentreOfMass_Y"]/1000
            self.vicon_data["hayashide_CentreOfMass_Z"]=self.vicon_data["hayashide_CentreOfMass_Z"]/1000
        except KeyError:
            pass
        
        tfodomdir_path=relationship_data['sotsuron_experiment'].loc[relationship_data['vicon']==os.path.basename(self.viconcsvpath)[:-8]].values[0]
        
        print(tfodomdir_path)
        # raise TimeoutError

        # tf data
        # try:
        #     self.tfcsvpath=relationship_data['sotsuron_experiment'].loc[relationship_data['vicon']==os.path.basename(self.viconcsvpath)[:-13]]
        # except Exception:
        #     self.tfcsvpath="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-20-20-07-04/_2023-12-20-20-07-04_tf_raw.csv"
        self.tfcsvpath=tfodomdir_path+"/"+os.path.basename(tfodomdir_path)+"_tf_raw.csv"
        self.savedirpath=os.path.split(self.viconcsvpath)[0]
        self.tf_data=initial_processor(self.tfcsvpath,False)

        # odom data
        self.odomcsv_path=tfodomdir_path+"/"+os.path.basename(tfodomdir_path)+"_od_raw.csv"
        self.odom_data=initial_processor(self.odomcsv_path,False)

        # 立ち上がり検知
        # VICON
        for idx in range(len(self.vicon_data)):
            vel_x=(self.vicon_data["robot_robot1_X"].iat[idx+1]-self.vicon_data["robot_robot1_X"].iat[idx])/(self.vicon_data["timestamp"].iat[idx+1]-self.vicon_data["timestamp"].iat[idx])
            if abs(vel_x)>0.2:
                print(idx,"/",len(self.vicon_data))
                vicon_init_idx=idx
                break
        # odom
        for idx in range(len(self.odom_data)):
            vel_x=(self.odom_data["x"].iat[idx+1]-self.odom_data["x"].iat[idx])/(self.odom_data["t"].iat[idx+1]-self.odom_data["t"].iat[idx])
            if abs(vel_x)>0.2:
                print(idx,"/",len(self.odom_data))
                odom_init_idx=idx
                break

        # ピーク検知による時刻同期
        peak_vicon_y_idx=int(self.vicon_data["robot_robot1_Y"].idxmax())
        peak_odom_x_idx=self.odom_data["y"].idxmax()
        print(peak_vicon_y_idx)
        print(peak_odom_x_idx)
        self.vicon_data["timestamp"]=self.vicon_data["timestamp"]+(self.odom_data["t"].iat[peak_odom_x_idx]-self.vicon_data["timestamp"].iat[peak_vicon_y_idx])

        # 不要箇所の削除
        # VICON
        vicon_data_nonNaN=self.vicon_data.dropna(subset=["hayashide_LHeadAngles_X"])
        vicon_data_nonNaN["timestamp_diff1"]=0
        vicon_data_nonNaN["timestamp_diff1"].iloc[:-1]=vicon_data_nonNaN["timestamp"].values[1:]-vicon_data_nonNaN["timestamp"].values[:-1]
        vicon_data_nonNaN["timestamp_diff2"]=0
        vicon_data_nonNaN["timestamp_diff2"].iloc[1:]=vicon_data_nonNaN["timestamp"].values[1:]-vicon_data_nonNaN["timestamp"].values[:-1]
        startpoints=vicon_data_nonNaN["timestamp"][vicon_data_nonNaN["timestamp_diff1"]>5]
        endpoints=vicon_data_nonNaN["timestamp"][vicon_data_nonNaN["timestamp_diff2"]>5]
        print(startpoints.values-endpoints.values)
        first_miss=True
        idxs=[]
        for row1,row2 in zip(startpoints,endpoints):
            idxs.append(self.vicon_data.index[self.vicon_data["timestamp"]==row1].tolist()[0])
            idxs.append(self.vicon_data.index[self.vicon_data["timestamp"]==row2].tolist()[0])
            # print(idx1)
            # print(idx2)
        if len(startpoints)==3:
            idxs=np.arange(idxs[1],idxs[2],1)
        if len(startpoints)==2:
            idxs=np.arange(idxs[1],idxs[2],1)
        if len(startpoints)==1:
            idxs=np.arange(0,idxs[0],1)
        self.vicon_data=self.vicon_data.iloc[idxs]
        print((self.vicon_data["timestamp"].values[1:]-self.vicon_data["timestamp"].values[:-1]).max())
        print((self.vicon_data["timestamp"].values[-1]-self.vicon_data["timestamp"].values[0]))

        # tf
        self.tf_data=self.tf_data[self.tf_data["timestamp"]<self.vicon_data["timestamp"].max()]


        # endpoint_timestamp=vicon_data_nonNaN["timestamp"][vicon_data_nonNaN["timestamp_diff1"]>10].values
        # startpoint_timestamp=[]
        # for endpoint in endpoint_timestamp:
        #     startpoint_timestamp

        # print(vicon_data_nonNaN)
        # # print(self.vicon_data)
        # for idx,row in vicon_data_nonNaN.loc[vicon_init_idx:].iterrows():
        #     # idx=int(idx)
        #     print(vicon_data_nonNaN["timestamp"].at[idx]-vicon_data_nonNaN["timestamp"].at[idx-1])
        #     # print(np.isnan(vicon_data_nonNaN["hayashide_CentreOfMass_X"].at[idx-1]))
        #     if vicon_data_nonNaN["timestamp"].at[idx]-vicon_data_nonNaN["timestamp"].at[idx-1]>10:
        #         end_vicon_idx=idx
        #         break
        # self.vicon_data=self.vicon_data.loc[:end_vicon_idx]
        print(self.vicon_data)
        # raise TimeoutError

    def load(self,tfodomdir_path="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-19-12-38-43"):
        path_management,csv_labels,color_dict=management_initial()
        relationship_data=pd.read_csv("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/20231220_VICON/vicon_history_relationship.csv")
        
        # tf data
        self.tfcsvpath=tfodomdir_path+"/"+os.path.basename(tfodomdir_path)+"_tf_raw.csv"
        self.savedirpath=os.path.split(self.tfcsvpath)[0]
        self.tf_data=initial_processor(self.tfcsvpath,False)

        # odom data
        self.odomcsv_path=tfodomdir_path+"/"+os.path.basename(tfodomdir_path)+"_od_raw.csv"
        self.odom_data=initial_processor(self.odomcsv_path,False)


    def concat_csv(self):
        tf_data_resampled=resampling_processor(self.tf_data,"0.01S")
        odom_data_resampled=resampling_processor(self.odom_data,"0.01S")
        merged_data=pd.merge(tf_data_resampled,odom_data_resampled,on="timestamp_datetime_round",how="inner")
        if 'self.vicon_data' in locals():
            vicon_data_resampled=resampling_processor(self.vicon_data,"0.01S")
            merged_data=pd.merge(merged_data,vicon_data_resampled,on="timestamp_datetime_round",how="inner")
        print(len(merged_data))
        merged_data.drop_duplicates(inplace=True)
        print(len(merged_data))
        print(merged_data)
        merged_data.to_csv(os.path.split(self.tfcsvpath)[0]+"/"+os.path.basename(self.tfcsvpath)[:-11]+"_merged.csv",index=0)
    
    # def main(self):
    #     self.concat_csv()
    
# viconcsvpaths=sorted(glob("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/20231220_VICON/alldata/*.csv"))
# for viconcsvpath in viconcsvpaths:
#     print(viconcsvpath)
#     # try:
#     concatcsv=concatCsv()
#     concatcsv.load_with_vicon(viconcsvpath)
#     concatcsv.concat_csv()
#     # except Exception as e:
#     #         exc_type, exc_obj, exc_tb = sys.exc_info()
#     #         print(f"line {exc_tb.tb_lineno}: {e}")
#     # break

tfodomdirpaths=sorted(glob("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-19*"))
tfodomdirpaths+=sorted(glob("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-21*"))
for tfodomdirpath in tfodomdirpaths:
    print(tfodomdirpath)
    # try:
    concatcsv=concatCsv()
    concatcsv.load(tfodomdirpath)
    concatcsv.concat_csv()
    # break
    # except Exception as e:
    #         exc_type, exc_obj, exc_tb = sys.exc_info()
    #         print(f"line {exc_tb.tb_lineno}: {e}")
    # break