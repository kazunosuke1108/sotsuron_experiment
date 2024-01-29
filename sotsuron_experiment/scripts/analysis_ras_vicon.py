import sys
import pandas as pd
from glob import glob
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from analysis_management import *
from analysis_initial_processor import *
from scipy import signal
import statistics
import seaborn as sns

plt.rcParams["figure.figsize"] = (6,4)
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 12

class analysisVicon():
    def __init__(self,viconcsvpath="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/20231220_VICON/alldata/hayashide_robot_03_all.csv"):
        path_management,csv_labels,color_dict=management_initial()
        relationship_data=pd.read_csv(r"C:\Users\mitsuhiro\Documents\workspace\hayashide_202312\takahashi_ws\results\20231220_VICON\vicon_history_relationship.csv")
        
        # VICON data
        # Look
        self.viconcsvpath=viconcsvpath
        # self.viconcsvpath="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/20231220_VICON/hayashide_robot_05_modified.csv"
        # humpback
        # self.viconcsvpath="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/20231220_VICON/hayashide_robot_10_modified.csv"
        self.vicon_data=pd.read_csv(self.viconcsvpath,index_col=0,header=0)
        print(self.vicon_data.shape)
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
            self.vicon_data["hayashide_RAJC_X"]=self.vicon_data["hayashide_RAJC_X"]/1000-offset_x
            self.vicon_data["hayashide_RAJC_Y"]=self.vicon_data["hayashide_RAJC_Y"]/1000
            self.vicon_data["hayashide_RAJC_Z"]=self.vicon_data["hayashide_RAJC_Z"]/1000
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
        print(f"peak_vicon_y_idx: {peak_vicon_y_idx}")

        valid_indices = self.vicon_data['hayashide_RAJC_X'].dropna().index
        peak_vicon_y_idx_limited = int(self.vicon_data.loc[valid_indices, 'robot_robot1_Y'].idxmax())
        print(f"peak_vicon_y_idx_limited: {peak_vicon_y_idx_limited}")

        print(peak_odom_x_idx)
        self.vicon_data["timestamp"]=self.vicon_data["timestamp"]+(self.odom_data["t"].iat[peak_odom_x_idx]-self.vicon_data["timestamp"].iat[peak_vicon_y_idx_limited])

        # 不要箇所の削除
        # VICON
        # vicon_data_nonNaN=self.vicon_data.dropna(subset=["hayashide_LHeadAngles_X"])
        vicon_data_nonNaN=self.vicon_data.dropna(subset=["hayashide_RAJC_X"])
        print(vicon_data_nonNaN)
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

    def plot_odom(self):
        """
        ロボットのodometryを活用したVICONデータの時刻同期
        """
        # # (没)立ち上がり検知
        # # VICON
        # for idx in range(len(self.vicon_data)):
        #     vel_x=(self.vicon_data["robot_robot1_X"].iat[idx+1]-self.vicon_data["robot_robot1_X"].iat[idx])/(self.vicon_data["timestamp"].iat[idx+1]-self.vicon_data["timestamp"].iat[idx])
        #     if abs(vel_x)>0.2:
        #         print(idx,"/",len(self.vicon_data))
        #         vicon_init_idx=idx
        #         break
        # # odom
        # for idx in range(len(self.odom_data)):
        #     vel_x=(self.odom_data["x"].iat[idx+1]-self.odom_data["x"].iat[idx])/(self.odom_data["t"].iat[idx+1]-self.odom_data["t"].iat[idx])
        #     if abs(vel_x)>0.2:
        #         print(idx,"/",len(self.odom_data))
        #         odom_init_idx=idx
        #         break
        # self.vicon_data=self.vicon_data.iloc[vicon_init_idx:]
        # self.odom_data=self.odom_data.iloc[odom_init_idx:]
        # self.vicon_data=self.vicon_data.reset_index()
        # self.odom_data=self.odom_data.reset_index()
        # self.odom_data["t"]=self.odom_data["t"]-self.odom_data["t"].iat[0]

        gs = GridSpec(2, 2, width_ratios=[1,1])
        plt.subplot(gs[0,:])    
        plt.title(os.path.basename(self.tfcsvpath)[:-11])   
        plt.plot(self.vicon_data["robot_robot1_X"],self.vicon_data["robot_robot1_Y"],"o-",markersize=3,label="robot (VICON)")
        plt.plot(self.odom_data["x"],self.odom_data["y"],"o-",markersize=3,label="robot (odometry)")
        plt.legend()
        plt.xlabel("Hallway direction $/it{x}$ [m]")
        plt.ylabel("Width direction $/it{y}$ [m]")
        plt.gca().set_aspect('equal', adjustable='box')
        plt.subplot(gs[1,0])    
        plt.plot(self.vicon_data["timestamp"],self.vicon_data["robot_robot1_X"],"o-",markersize=3,label="robot_robot1_X (VICON)")
        plt.plot(self.odom_data["t"],self.odom_data["x"],"o-",markersize=3,label="robot_robot1_X (odometry)")
        plt.legend()
        plt.xlabel("Time $/it{t}$ [s]")
        plt.ylabel("Hallway direction $/it{x}$ [m]")
        plt.subplot(gs[1,1])    
        plt.plot(self.vicon_data["timestamp"],self.vicon_data["robot_robot1_Y"],"o-",markersize=3,label="robot_robot1_Y (VICON)")
        plt.plot(self.odom_data["t"],self.odom_data["y"],"o-",markersize=3,label="robot_robot1_Y (odometry)")
        plt.legend()
        plt.xlabel("Time $\it{t}$ [s]")
        plt.ylabel("Hallway direction $\it{y}$ [m]")
        # plt.show()

    def plot_gravity(self):
        gs = GridSpec(2, 2, width_ratios=[1,1])
        plt.subplot(gs[0,:])    
        plt.title(os.path.basename(self.tfcsvpath)[:-11])   
        self.tf_data["base_x"]=(self.tf_data["r_base_x"]+self.tf_data["l_base_x"])/2
        self.tf_data["base_y"]=(self.tf_data["r_base_y"]+self.tf_data["l_base_y"])/2
        plt.plot(self.vicon_data["hayashide_CentreOfMass_X"],self.vicon_data["hayashide_CentreOfMass_Y"],"o-",markersize=3,label="gravity (VICON)")
        plt.plot(self.tf_data["base_x"],self.tf_data["base_y"],"o-",markersize=3,label="trunk")
        plt.legend()
        plt.xlabel("Hallway direction $/it{x}$ [m]")
        plt.ylabel("Width direction $/it{y}$ [m]")
        plt.gca().set_aspect('equal', adjustable='box')

        plt.subplot(gs[1,0])    
        plt.plot(self.vicon_data["timestamp"],self.vicon_data["hayashide_CentreOfMass_X"],"o-",markersize=3,label="gravity_x (VICON)")
        plt.plot(self.tf_data["timestamp"],self.tf_data["base_x"],"o-",markersize=3,label="gravity")
        plt.legend()
        plt.xlabel("Time $/it{t}$ [s]")
        plt.ylabel("Hallway direction $/it{x}$ [m]")

        plt.subplot(gs[1,1])    
        plt.plot(self.vicon_data["timestamp"],self.vicon_data["hayashide_CentreOfMass_Y"],"o-",markersize=3,label="gravity_y (VICON)")
        plt.plot(self.tf_data["timestamp"],self.tf_data["base_y"],"o-",markersize=3,label="gravity")
        plt.legend()
        plt.xlabel("Time $\it{t}$ [s]")
        plt.ylabel("Hallway direction $\it{y}$ [m]")
        plt.savefig(self.savedirpath+"/"+os.path.basename(self.tfcsvpath)[:-11]+"gravity")
        plt.cla()
        # plt.show()

    def plot_head_angle(self):
        """
        体幹のロール・ピッチ・ヨーを求める
        """

        self.tf_data["ear_head_angle_x"]=0 # 耳で見るロール
        self.tf_data["eye_head_angle_x"]=0 # 目で見るロール
        self.tf_data["r_ear_head_angle_y"]=0 # 右耳と鼻で見るピッチ
        self.tf_data["l_ear_head_angle_y"]=0 # 左耳と鼻で見るピッチ
        self.tf_data["r_eye_head_angle_y"]=0 # 右目と鼻で見るピッチ
        self.tf_data["l_eye_head_angle_y"]=0 # 左目と鼻で見るピッチ
        self.tf_data["ear_head_angle_z"]=0 # 耳で見るヨー
        self.tf_data["eye_head_angle_z"]=0 # 目で見るヨー
        
        # self.tf_data["ear_head_angle_x"]=np.rad2deg(np.arctan((self.tf_data["r_ear_z"]-self.tf_data["l_ear_z"])/(self.tf_data["r_ear_y"]-self.tf_data["l_ear_y"])))
        self.tf_data["eye_head_angle_x"]=np.rad2deg(np.arctan((self.tf_data["r_eye_z"]-self.tf_data["l_eye_z"])/(self.tf_data["r_eye_y"]-self.tf_data["l_eye_y"])))
        self.tf_data["r_ear_head_angle_y"]=np.rad2deg(np.arctan((self.tf_data["nose_z"]-self.tf_data["r_ear_z"])/(self.tf_data["nose_x"]-self.tf_data["r_ear_x"])))
        # self.tf_data["l_ear_head_angle_y"]=np.rad2deg(np.arctan((self.tf_data["nose_z"]-self.tf_data["l_ear_z"])/(self.tf_data["nose_x"]-self.tf_data["l_ear_x"])))
        # self.tf_data["r_eye_head_angle_y"]=np.rad2deg(np.arctan((self.tf_data["nose_z"]-self.tf_data["r_eye_z"])/(self.tf_data["nose_x"]-self.tf_data["r_eye_x"])))
        # self.tf_data["l_eye_head_angle_y"]=np.rad2deg(np.arctan((self.tf_data["nose_z"]-self.tf_data["l_eye_z"])/(self.tf_data["nose_x"]-self.tf_data["l_eye_x"])))
        # self.tf_data["ear_head_angle_z"]=np.rad2deg(np.arctan((self.tf_data["r_ear_x"]-self.tf_data["l_ear_x"])/(self.tf_data["r_ear_y"]-self.tf_data["l_ear_y"])))
        self.tf_data["eye_head_angle_z"]=np.rad2deg(np.arctan((self.tf_data["r_eye_x"]-self.tf_data["l_eye_x"])/(self.tf_data["r_eye_y"]-self.tf_data["l_eye_y"])))
        for idx in range(len(self.tf_data)):
            if self.tf_data["eye_head_angle_z"].iat[idx]<0:
                self.tf_data["eye_head_angle_z"].iat[idx]=self.tf_data["eye_head_angle_z"].iat[idx]+180

        gs = GridSpec(3, 1)
        plt.subplot(gs[0]) 
        plt.title(os.path.basename(self.tfcsvpath)[:-11])   
        plt.plot(self.vicon_data["timestamp"],self.vicon_data["hayashide_LHeadAngles_X"],"o-",markersize=3,label="hayashide_LHeadAngles_X")
        # plt.plot(self.vicon_data["timestamp"],self.vicon_data["hayashide_RHeadAngles_X"],"o-",markersize=3,label="hayashide_RHeadAngles_X")
        plt.plot(self.tf_data["timestamp"],self.tf_data["eye_head_angle_x"],"o-",markersize=3,label="eye_head_angle_x")
        plt.xlabel("Time $/it{t}$ [s]")
        plt.ylabel("Roll of the head [deg]")
        plt.legend()
        plt.grid()
        plt.subplot(gs[1])   
        plt.plot(self.vicon_data["timestamp"],self.vicon_data["hayashide_LHeadAngles_Y"],"o-",markersize=3,label="hayashide_LHeadAngles_Y")
        # plt.plot(self.vicon_data["timestamp"],self.vicon_data["hayashide_RHeadAngles_Y"],"o-",markersize=3,label="hayashide_RHeadAngles_Y")
        plt.plot(self.tf_data["timestamp"],self.tf_data["r_ear_head_angle_y"],"o-",markersize=3,label="r_ear_head_angle_y")
        plt.xlabel("Time $/it{t}$ [s]")
        plt.ylabel("Pitch of the head [deg]")
        plt.legend()
        plt.grid()
        plt.subplot(gs[2])   
        self.tf_data["eye_head_angle_z"]=mean_processor(self.tf_data["eye_head_angle_z"])
        plt.plot(self.vicon_data["timestamp"],self.vicon_data["hayashide_LHeadAngles_Z"],"o-",markersize=3,label="hayashide_LHeadAngles_Z")
        # plt.plot(self.vicon_data["timestamp"],self.vicon_data["hayashide_RHeadAngles_Z"],"o-",markersize=3,label="hayashide_RHeadAngles_Z")
        # plt.plot(self.tf_data["timestamp"],self.tf_data["ear_head_angle_z"],"o-",markersize=3,label="ear_head_angle_z")
        plt.plot(self.tf_data["timestamp"],self.tf_data["eye_head_angle_z"],"o-",markersize=3,label="eye_head_angle_z")
        plt.xlabel("Time $/it{t}$ [s]")
        plt.ylabel("Yaw of the head [deg]")
        plt.legend()
        plt.grid()
        plt.savefig(self.savedirpath+"/"+os.path.basename(self.tfcsvpath)[:-11]+"_head_angle")
        plt.cla()
        # plt.show()
        # plt.cla()
        
        pass

    def plot_trunk_angle(self):
        """
        体幹のロール・ピッチ・ヨーを求める
        """
        self.tf_data["c_shoulder_x"]=0
        self.tf_data["c_shoulder_y"]=0
        self.tf_data["c_shoulder_z"]=0
        self.tf_data["c_base_x"]=0
        self.tf_data["c_base_y"]=0
        self.tf_data["c_base_z"]=0
        self.tf_data["c_shoulder_x"]=(self.tf_data["r_shoulder_x"]+self.tf_data["l_shoulder_x"])/2
        self.tf_data["c_shoulder_y"]=(self.tf_data["r_shoulder_y"]+self.tf_data["l_shoulder_y"])/2
        self.tf_data["c_shoulder_z"]=(self.tf_data["r_shoulder_z"]+self.tf_data["l_shoulder_z"])/2
        self.tf_data["c_base_x"]=(self.tf_data["r_base_x"]+self.tf_data["l_base_x"])/2
        self.tf_data["c_base_y"]=(self.tf_data["r_base_y"]+self.tf_data["l_base_y"])/2
        self.tf_data["c_base_z"]=(self.tf_data["r_base_z"]+self.tf_data["l_base_z"])/2

        self.tf_data["r_trunk_angle_x"]=0 # 右半身で見るロール
        self.tf_data["r_trunk_angle_y"]=0 # 右半身で見るピッチ
        self.tf_data["l_trunk_angle_x"]=0 # 左半身
        self.tf_data["l_trunk_angle_y"]=0
        self.tf_data["c_trunk_angle_x"]=0 # 中央
        self.tf_data["c_trunk_angle_y"]=0
        self.tf_data["trunk_angle_z"]=0 # ヨー
        
        self.tf_data["r_trunk_angle_x"]=np.rad2deg(np.arctan((self.tf_data["r_shoulder_y"]-self.tf_data["r_base_y"])/(self.tf_data["r_shoulder_z"]-self.tf_data["r_base_z"])))
        self.tf_data["r_trunk_angle_y"]=np.rad2deg(np.arctan((self.tf_data["r_shoulder_x"]-self.tf_data["r_base_x"])/(self.tf_data["r_shoulder_z"]-self.tf_data["r_base_z"])))
        self.tf_data["l_trunk_angle_x"]=np.rad2deg(np.arctan((self.tf_data["l_shoulder_y"]-self.tf_data["l_base_y"])/(self.tf_data["l_shoulder_z"]-self.tf_data["l_base_z"])))
        self.tf_data["l_trunk_angle_y"]=np.rad2deg(np.arctan((self.tf_data["l_shoulder_x"]-self.tf_data["l_base_x"])/(self.tf_data["l_shoulder_z"]-self.tf_data["l_base_z"])))
        self.tf_data["c_trunk_angle_x"]=np.rad2deg(np.arctan((self.tf_data["c_shoulder_y"]-self.tf_data["c_base_y"])/(self.tf_data["c_shoulder_z"]-self.tf_data["c_base_z"])))
        self.tf_data["c_trunk_angle_y"]=np.rad2deg(np.arctan((self.tf_data["c_shoulder_x"]-self.tf_data["c_base_x"])/(self.tf_data["c_shoulder_z"]-self.tf_data["c_base_z"])))
        self.tf_data["s_trunk_angle_z"]=np.rad2deg(np.arctan((self.tf_data["r_shoulder_x"]-self.tf_data["l_shoulder_x"])/(self.tf_data["r_shoulder_y"]-self.tf_data["l_shoulder_y"])))
        self.tf_data["b_trunk_angle_z"]=np.rad2deg(np.arctan((self.tf_data["r_base_x"]-self.tf_data["l_base_x"])/(self.tf_data["r_base_y"]-self.tf_data["l_base_y"])))

        gs = GridSpec(3, 1)
        plt.subplot(gs[0]) 
        plt.title(os.path.basename(self.tfcsvpath)[:-11])   
        plt.plot(self.vicon_data["timestamp"],self.vicon_data["hayashide_LThoraxAngles_X"],"o-",markersize=3,label="hayashide_LThoraxAngles_X")
        plt.plot(self.tf_data["timestamp"],self.tf_data["r_trunk_angle_x"],"o-",markersize=3,label="r_trunk_angle_x")
        # plt.plot(self.tf_data["timestamp"],self.tf_data["l_trunk_angle_x"],"o-",markersize=3,label="l_trunk_angle_x")
        # plt.plot(self.tf_data["timestamp"],self.tf_data["c_trunk_angle_x"],"o-",markersize=3,label="c_trunk_angle_x")
        plt.xlabel("Time $/it{t}$ [s]")
        plt.ylabel("Roll of the trunk [deg]")
        plt.legend()
        plt.grid()
        plt.subplot(gs[1])   
        plt.plot(self.vicon_data["timestamp"],self.vicon_data["hayashide_LThoraxAngles_Y"],"o-",markersize=3,label="hayashide_LThoraxAngles_Y")
        plt.plot(self.tf_data["timestamp"],self.tf_data["r_trunk_angle_y"],"o-",markersize=3,label="r_trunk_angle_y")
        # plt.plot(self.tf_data["timestamp"],self.tf_data["l_trunk_angle_y"],"o-",markersize=3,label="l_trunk_angle_y")
        # plt.plot(self.tf_data["timestamp"],self.tf_data["c_trunk_angle_y"],"o-",markersize=3,label="c_trunk_angle_y")
        plt.xlabel("Time $/it{t}$ [s]")
        plt.ylabel("Pitch of the trunk [deg]")
        plt.legend()
        plt.grid()
        plt.subplot(gs[2])   
        plt.plot(self.vicon_data["timestamp"],self.vicon_data["hayashide_LThoraxAngles_Z"],"o-",markersize=3,label="hayashide_LThoraxAngles_Z")
        plt.plot(self.tf_data["timestamp"],self.tf_data["s_trunk_angle_z"],"o-",markersize=3,label="s_trunk_angle_z")
        # plt.plot(self.tf_data["timestamp"],self.tf_data["b_trunk_angle_z"],"o-",markersize=3,label="b_trunk_angle_z")
        plt.xlabel("Time $/it{t}$ [s]")
        plt.ylabel("Yaw of the trunk [deg]")
        plt.legend()
        plt.grid()
        plt.savefig(self.savedirpath+"/"+os.path.basename(self.tfcsvpath)[:-11]+"_trunk_angle")
        plt.cla()
        # plt.cla()
        # plt.show()

        # self.write_log([os.path.basename(self.tfcsvpath),self.tf_data["c_trunk_angle_y"].mean(),self.tf_data["c_trunk_angle_y"].median(),self.tf_data["c_trunk_angle_y"].std(),self.tf_data["c_trunk_angle_y"].min(),self.tf_data["c_trunk_angle_y"].max()],path_management["humpback_csv_path"],fmt="%s")
        pass

    def plot_hip_angle(self):
        """
        股関節の前後進展角度を求める
        """
        self.tf_data["r_hip_angle_x"]=0
        self.tf_data["r_hip_angle_y"]=0
        self.tf_data["r_hip_angle_z"]=0
        self.tf_data["l_hip_angle_x"]=0
        self.tf_data["l_hip_angle_y"]=0
        self.tf_data["l_hip_angle_z"]=0
        self.tf_data["r_hip_angle_x"]=np.rad2deg(np.arctan((self.tf_data["r_knee_y"]-self.tf_data["r_base_y"])/(self.tf_data["r_knee_z"]-self.tf_data["r_base_z"])))
        self.tf_data["r_hip_angle_y"]=np.rad2deg(np.arctan((self.tf_data["r_knee_x"]-self.tf_data["r_base_x"])/(self.tf_data["r_knee_z"]-self.tf_data["r_base_z"])))
        self.tf_data["r_hip_angle_z"]=np.rad2deg(np.arctan((self.tf_data["r_knee_y"]-self.tf_data["r_base_y"])/(self.tf_data["r_knee_x"]-self.tf_data["r_base_x"])))
        self.tf_data["l_hip_angle_x"]=np.rad2deg(np.arctan((self.tf_data["l_knee_y"]-self.tf_data["l_base_y"])/(self.tf_data["l_knee_z"]-self.tf_data["l_base_z"])))
        self.tf_data["l_hip_angle_y"]=np.rad2deg(np.arctan((self.tf_data["l_knee_x"]-self.tf_data["l_base_x"])/(self.tf_data["l_knee_z"]-self.tf_data["l_base_z"])))
        self.tf_data["l_hip_angle_z"]=np.rad2deg(np.arctan((self.tf_data["l_knee_y"]-self.tf_data["l_base_y"])/(self.tf_data["l_knee_x"]-self.tf_data["l_base_x"])))

        gs = GridSpec(3, 1) 
        plt.subplot(gs[0]) 
        plt.title(os.path.basename(self.tfcsvpath)[:-11])   
        plt.plot(self.vicon_data["timestamp"],self.vicon_data["hayashide_RHipAngles_X"],"o-",markersize=3,label="hayashide_RHipAngles_X")
        # plt.plot(self.vicon_data["timestamp"],self.vicon_data["hayashide_LHipAngles_X"],"o-",markersize=3,label="hayashide_LHipAngles_X")
        plt.plot(self.tf_data["timestamp"],self.tf_data["r_hip_angle_y"],"o-",markersize=3,label="r_hip_angle_y")
        # plt.plot(self.tf_data["timestamp"],self.tf_data["l_hip_angle_x"],"o-",markersize=3,label="l_hip_angle_x")
        plt.xlabel("Time $/it{t}$ [s]")
        plt.ylabel("Hip angle in (hallway width direction) th_x [deg]")
        plt.legend()
        plt.grid()
        plt.subplot(gs[1])   
        plt.plot(self.vicon_data["timestamp"],self.vicon_data["hayashide_RHipAngles_Y"],"o-",markersize=3,label="hayashide_RHipAngles_Y")
        # # plt.plot(self.vicon_data["timestamp"],self.vicon_data["hayashide_LHipAngles_Y"],"o-",markersize=3,label="hayashide_LHipAngles_Y")
        # # plt.plot(self.tf_data["timestamp"],self.tf_data["l_hip_angle_y"],"o-",markersize=3,label="l_hip_angle_y")
        plt.plot(self.tf_data["timestamp"],self.tf_data["r_hip_angle_z"],"o-",markersize=3,label="r_hip_angle_z")
        plt.xlabel("Time $/it{t}$ [s]")
        plt.ylabel("Hip angle in (hallway direction) th_y [deg]")
        plt.legend()
        plt.grid()
        plt.subplot(gs[2])   
        plt.plot(self.vicon_data["timestamp"],self.vicon_data["hayashide_RHipAngles_Z"],"o-",markersize=3,label="hayashide_RHipAnglesZ")
        # plt.plot(self.vicon_data["timestamp"],self.vicon_data["hayashide_LHipAngles_Z"],"o-",markersize=3,label="hayashide_LHipAnglesZ")
        plt.plot(self.tf_data["timestamp"],self.tf_data["r_hip_angle_x"],"o-",markersize=3,label="r_hip_angle_x")
        # # plt.plot(self.tf_data["timestamp"],self.tf_data["l_hip_angle_z"],"o-",markersize=3,label="l_hip_angle_z")
        plt.xlabel("Time $/it{t}$ [s]")
        plt.ylabel("Hip angle in (yaw direction) th_z [deg]")
        plt.legend()
        plt.grid()
        plt.savefig(self.savedirpath+"/"+os.path.basename(self.tfcsvpath)[:-11]+"_hip_angle.png")
        plt.cla()
        pass

    def get_stride(self):
        print("get_stride")
        print(self.vicon_data["hayashide_RAJC_X"])
        # data=self.tf_data.iloc[self.start_idx:self.end_idx]       
        data=self.tf_data       

       
        # 一緒に描画
        kde_data_1 = sns.kdeplot(data['r_foot_x'], bw_method=0.05, color='blue', label='bw=0.05').get_lines()[0].get_data()
        plt.clf()
        kde_data_vicon = sns.kdeplot(self.vicon_data["hayashide_RAJC_X"], bw_method=0.05, color='blue', label='bw=0.05').get_lines()[0].get_data()
        plt.clf()

        fig, ax1 = plt.subplots()
        
        cmap = plt.cm.tab10
        colors = cmap(np.linspace(0, 1, 4))
        
        ax1.plot(data["timestamp"],data["r_foot_x"],"-",markersize=2,color="orange",label="r_foot_x (Proposed)")
        # ax1.plot(self.vicon_data["timestamp"],self.vicon_data["hayashide_RAJC_X"],"o-",markersize=2,color="orange",label="r_foot_x (VICON)")
        ax2 = ax1.twiny() # 二つ目の軸を定義
        # ax2 = plt.twiny()
        # plt.grid(True)
        # plt.xlabel("Time $/it{t}$ [s]")
        # plt.ylabel("Hallway direction $/it{x}$ [m]")
        
        kde_x_1, kde_y_1 = kde_data_1[0], kde_data_1[1]
        # print(f"kde_y_1: {kde_y_1}")
        # print(kde_y_1)
        peaks_1, _ = signal.find_peaks(kde_y_1,distance=10,prominence=0.05)
        print(f"peaks_1: {kde_x_1[peaks_1]}")
        stride_1 = kde_x_1[peaks_1[1:]]-kde_x_1[peaks_1[0:-1]]
        print(stride_1)

        kde_x_vicon, kde_y_vicon = kde_data_vicon[0], kde_data_vicon[1]
        # print(f"kde_y_vicon: {kde_y_vicon}")
        # print(kde_y_1)
        peaks_vicon, _ = signal.find_peaks(kde_y_vicon,distance=10,prominence=0.05)
        print(f"peaks_vicon: {kde_x_vicon[peaks_vicon]}")
        stride_vicon = kde_x_vicon[peaks_vicon[1:]]-kde_x_vicon[peaks_vicon[0:-1]]
        print(stride_vicon)
        
        ax2.plot(kde_y_1,kde_x_1,color=colors[1],label="probability")
        ax2.plot(kde_y_1[peaks_1],kde_x_1[peaks_1], "x",color=colors[2])
        ax2.hlines(y=kde_x_1[peaks_1], xmin=0, xmax=5, color=colors[2], linestyle='--', linewidth=1,label='estimated step position')
        # ax1.plot(data["timestamp"],data["r_foot_x"],"o",markersize=2,label="r_foot_x")
        ax1.plot(self.vicon_data["timestamp"],self.vicon_data["hayashide_RAJC_X"],"-",markersize=0.5,color="green",label="r_foot_x (VICON)",alpha=0.5)

        # plt.title('kernel')
        ax1.set_xlabel("Time $\it{t}$ [s]")
        ax1.set_ylabel('Hallway direction $\it{x}$ [m]')
        ax2.set_xlabel('Probability')
        ax2.set_xlim(0,5)
        # plt.xticks([])

        # plt.ylabel('Hallway direction $/it{x}$ [m]')
        # plt.grid(True)
        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        legend = ax2.legend(h1+h2, l1+l2, loc='upper right',facecolor='white')
        # legend.get_frame().set_alpha(1)
        plt.savefig(os.path.split(self.tfcsvpath)[0]+"/"+os.path.basename(self.tfcsvpath)[:-8]+"_stride_kernel.png")
        plt.cla()
        print(os.path.split(self.tfcsvpath)[0]+"/"+os.path.basename(self.tfcsvpath)[:-8]+"_stride_kernel.png")
        # self.write_log([os.path.basename(self.tfcsvpath),sum(stride_1)/len(stride_1),statistics.median(stride_1),statistics.stdev(stride_1),min(stride_1),max(stride_1)],path_management["stride_csv_path"],fmt="%s")

        

        df1 = pd.DataFrame(kde_x_1[peaks_1], columns=['steppos'])
        df2 = pd.DataFrame(stride_1, columns=['stride'])
        df3 = pd.DataFrame(kde_x_vicon[peaks_vicon], columns=['vicon_steppos'])
        df4 = pd.DataFrame(stride_vicon, columns=['vicon_stride'])
        result_df = pd.concat([df1, df2, df3, df4], axis=1)
        result_df.to_csv(os.path.basename(self.tfcsvpath)+'output_stride_vicon.csv', index=False)

        return
    
    def get_velocity(self):
        best_err=100
        best_start_x=0
        best_start_t=0
        best_end_x=0
        best_end_t=0
        for idx,row in self.tf_data.iterrows():
            start_x=row["gravity_x"]
            start_t=row["timestamp"]
            end_idx=((start_x-self.tf_data["gravity_x"])-(5)).abs().idxmin()
            end_x=self.tf_data.iloc[end_idx]["gravity_x"]
            end_t=self.tf_data.iloc[end_idx]["timestamp"]
            # print(start_x,end_x)
            if abs(start_x-end_x-5)<best_err:
                best_err=abs(start_x-end_x-5)
                best_start_x=start_x
                best_start_t=start_t
                best_end_x=end_x
                best_end_t=end_t

        # self.write_log([os.path.basename(self.tfcsvpath),(best_end_x-best_start_x)/(best_end_t-best_start_t),best_err,best_start_x,best_start_t,best_end_x,best_end_t],path_management["velocity_csv_path"], fmt="%s")
        print(os.path.basename(self.tfcsvpath),(best_end_x-best_start_x)/(best_end_t-best_start_t),best_err,best_start_x,best_start_t,best_end_x,best_end_t)
        return best_start_x,best_start_t,best_end_x,best_end_t
    
    def get_featured_section(self):
        data=self.tf_data
        data["r_base_vx"]=0
        data["r_base_vx_diff"]=0
        try:
            data["r_base_vx"].iloc[:-1]=(data["r_base_x"].values[1:]-data["r_base_x"].values[:-1])/(data["timestamp"].values[1:]-data["timestamp"].values[:-1])
        except ValueError:
            data["r_base_vx"]=(data["r_base_x"].values[1:]-data["r_base_x"].values[:-1])/(data["timestamp"].values[1:]-data["timestamp"].values[:-1])
        # print(data["r_base_vx"])
        median_base_vx = statistics.median(data["r_base_vx"])
        print(f"median_base_vx:{median_base_vx}")
        data["r_base_vx_diff"]= data["r_base_vx"] - median_base_vx

        data["sumdiff_r_base_vx"]=0
        data["sumdiff_end_idx"]=0

        fail_idx_start = -1
        for idx,row in self.tf_data.iterrows():
            start_x=row["r_base_x"]
            if start_x >10:
                continue
            elif fail_idx_start == -1:
                fail_idx_start = idx

            start_t=row["timestamp"]
            end_idx=((start_x-self.tf_data["r_base_x"][idx:])-(5)).abs().idxmin()
            end_x=self.tf_data.iloc[end_idx]["r_base_x"]
            end_t=self.tf_data.iloc[end_idx]["timestamp"]
            if end_x - start_x > -4.9 :
                fail_idx_end = idx
                # print(fail_idx_end)
                # print(f"end_x:{end_x}")
                # print(f"start_x:{start_x}")
                break
            elif end_t-start_t < 4 :
                continue
        
            else:
                data["sumdiff_r_base_vx"][idx] = sum(abs(data["r_base_vx_diff"][idx:end_idx]))/(end_idx-idx)
                data["sumdiff_end_idx"][idx]=end_idx

        target_diff_range = data["sumdiff_r_base_vx"][ data["sumdiff_r_base_vx"]!=0]
        target_start_idx = target_diff_range.idxmin()
        target_end_idx = data["sumdiff_end_idx"][target_start_idx]

        self.start_idx = target_start_idx
        self.start_t = self.tf_data["timestamp"][target_start_idx]
        self.start_x = self.tf_data["r_base_x"][target_start_idx]
        self.end_idx = target_end_idx
        self.end_t = self.tf_data["timestamp"][target_end_idx]
        self.end_x = self.tf_data["r_base_x"][target_end_idx]
        # print(data["sumdiff_r_base_vx"][fail_idx_start:fail_idx_end])
        # print(target_start_idx)
        # print(data["sumdiff_r_base_vx"][target_start_idx])
     

        # plt.plot(self.tf_data["timestamp"],self.tf_data["r_base_vx"],"o",markersize=3,label="r_base_vx")
        # plt.plot(self.tf_data["timestamp"],self.tf_data["r_base_vx_diff"],"o",markersize=3,label="r_base_vx_diff")
        plt.plot(self.tf_data["timestamp"],self.tf_data["r_base_x"],"o-",markersize=3,label="r_base_x")
        plt.vlines(self.tf_data["timestamp"][target_start_idx], -5, 10, color='r', linestyles='solid',label="start")        
        plt.vlines(self.tf_data["timestamp"][target_end_idx], -5, 10, color='r', linestyles='solid',label="end")
        plt.vlines(self.tf_data["timestamp"][fail_idx_start], -5, 10, color='b', linestyles='dotted',label="end")
        plt.vlines(self.tf_data["timestamp"][fail_idx_end], -5, 10, color='b', linestyles='dotted',label="end")
        # plt.plot(self.tf_data["timestamp"],self.tf_data["r_foot_x"],"o-",markersize=3,label="r_foot_x")
        # plt.plot(self.tf_data["timestamp"],self.tf_data["r_base_x"],"o-",markersize=3,label="r_base_x")
        # plt.vlines(best_start_t, -5, 5, color='r', linestyles='dotted',label="start")        
        # plt.vlines(best_end_t, -5, 5, color='r', linestyles='dotted',label="end")
        # plt.plot(self.odom_data["t"],self.odom_data["x"],"^-",markersize=3,label="robot_x")
        plt.legend()
        plt.xlabel("Time $/it{t}$ [s]")
        plt.ylabel("Hallway direction $/it{x}$ [m]")
        plt.savefig(self.savedirpath+"/"+os.path.basename(self.tfcsvpath)[:-11]+"_r_base_vx_trim")
        plt.cla()

        # self.write_log([os.path.basename(self.tfcsvpath),(self.end_x-self.start_x)/(self.end_t-self.start_t),self.start_x,self.start_t,self.end_x,self.end_t],path_management["velocity_csv_path"], fmt="%s")
        print(os.path.basename(self.tfcsvpath),(self.end_x-self.start_x)/(self.end_t-self.start_t),self.start_x,self.start_t,self.end_x,self.end_t)


    def write_log(self,output_data,csvpath,fmt="%s"):
        print(csvpath)
        try:
            with open(csvpath, 'a') as f_handle:
                np.savetxt(f_handle,[output_data],delimiter=",")
        except TypeError:
            with open(csvpath, 'a') as f_handle:
                np.savetxt(f_handle,[output_data],delimiter=",",fmt=fmt)    
        except FileNotFoundError:
            np.savetxt(csvpath,[output_data],delimiter=",")
        pass 

    def calc_MAE(self):
        print("calc MAE")


    def main(self):
        # self.plot_odom()
        # self.plot_gravity()
        # self.plot_head_angle()
        # self.plot_trunk_angle()
        # self.plot_hip_angle()
        # self.get_featured_section()
        # self.plot_r_leg_x()
        print("get_stride")
        self.get_stride()


viconcsvpaths=sorted(glob(r"C:\Users\mitsuhiro\Documents\workspace\hayashide_202312\takahashi_ws\results\20231220_VICON\alldata/*.csv"))
for viconcsvpath in viconcsvpaths:
    print(viconcsvpath)
    try:
        analysisv=analysisVicon(viconcsvpath)
        analysisv.main()
    except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(f"line {exc_tb.tb_lineno}: {e}")

    analysisv=analysisVicon(viconcsvpath)
    analysisv.main()
