import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from analysis_management import *
from analysis_initial_processor import *

plt.rcParams["figure.figsize"] = (12,8)
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.family'] = 'Times New Roman'

class analysisVicon():
    def __init__(self):
        path_management,csv_labels,color_dict=management_initial()
        relationship_data=pd.read_csv("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/20231220_VICON/vicon_history_relationship.csv")
        
        # VICON data
        # Look
        self.viconcsvpath="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/20231220_VICON/hayashide_robot_06_modified.csv"
        # humpback
        # self.viconcsvpath="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/20231220_VICON/hayashide_robot_10_modified.csv"
        self.vicon_data=pd.read_csv(self.viconcsvpath,index_col=0,header=0)
        self.vicon_data["hayashide_CentreOfMass_X"]=self.vicon_data["hayashide_CentreOfMass_X"]/1000
        self.vicon_data["hayashide_CentreOfMass_Y"]=self.vicon_data["hayashide_CentreOfMass_Y"]/1000
        self.vicon_data["hayashide_CentreOfMass_Z"]=self.vicon_data["hayashide_CentreOfMass_Z"]/1000
        self.vicon_data["robot_X"]=self.vicon_data["robot_X"]/1000
        self.vicon_data["robot_Y"]=self.vicon_data["robot_Y"]/1000
        self.vicon_data["robot_Z"]=self.vicon_data["robot_Z"]/1000
        self.vicon_data["robot_X"]=self.vicon_data["robot_X"]-self.vicon_data["robot_X"].iat[0]
        self.vicon_data["robot_Y"]=self.vicon_data["robot_Y"]-self.vicon_data["robot_Y"].iat[0]
        self.vicon_data["timestamp"]=self.vicon_data.index/60

        tfodomdir_path=relationship_data['sotsuron_experiment'].loc[relationship_data['vicon']==os.path.basename(self.viconcsvpath)[:-13]].values[0]
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

        # ピーク検知による時刻同期
        peak_vicon_x_idx=int(self.vicon_data["robot_Y"].idxmax())
        peak_odom_x_idx=self.odom_data["y"].idxmax()
        print(peak_vicon_x_idx)
        print(peak_odom_x_idx)
        self.vicon_data["timestamp"]=self.vicon_data["timestamp"]+(self.odom_data["t"].iat[peak_odom_x_idx]-self.vicon_data["timestamp"].iat[peak_vicon_x_idx])

        # 復路を削除
        # for idx,row in self.vicon_data.iterrows():
        #     if row["hayashide_CentreOfMass_X"]<-2:
        #         cutidx=int(idx)
        #         print("cutidx: ",cutidx)
        #         break
        # self.vicon_data=self.vicon_data.iloc[:cutidx]

    def plot_odom(self):
        """
        ロボットのodometryを活用したVICONデータの時刻同期
        """
        # # (没)立ち上がり検知
        # # VICON
        # for idx in range(len(self.vicon_data)):
        #     vel_x=(self.vicon_data["robot_X"].iat[idx+1]-self.vicon_data["robot_X"].iat[idx])/(self.vicon_data["timestamp"].iat[idx+1]-self.vicon_data["timestamp"].iat[idx])
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
        plt.plot(self.vicon_data["robot_X"],self.vicon_data["robot_Y"],"o-",markersize=3,label="robot (VICON)")
        plt.plot(self.odom_data["x"],self.odom_data["y"],"o-",markersize=3,label="robot (odometry)")
        plt.legend()
        plt.xlabel("Hallway direction $/it{x}$ [m]")
        plt.ylabel("Width direction $/it{y}$ [m]")
        plt.gca().set_aspect('equal', adjustable='box')
        plt.subplot(gs[1,0])    
        plt.plot(self.vicon_data["timestamp"],self.vicon_data["robot_X"],"o-",markersize=3,label="robot_X (VICON)")
        plt.plot(self.odom_data["t"],self.odom_data["x"],"o-",markersize=3,label="robot_X (odometry)")
        plt.legend()
        plt.xlabel("Time $/it{t}$ [s]")
        plt.ylabel("Hallway direction $/it{x}$ [m]")
        plt.subplot(gs[1,1])    
        plt.plot(self.vicon_data["timestamp"],self.vicon_data["robot_Y"],"o-",markersize=3,label="robot_Y (VICON)")
        plt.plot(self.odom_data["t"],self.odom_data["y"],"o-",markersize=3,label="robot_Y (odometry)")
        plt.legend()
        plt.xlabel("Time $\it{t}$ [s]")
        plt.ylabel("Hallway direction $\it{y}$ [m]")
        plt.show()

    def plot_gravity(self):
        gs = GridSpec(2, 2, width_ratios=[1,1])
        plt.subplot(gs[0,:])    
        plt.plot(self.vicon_data["hayashide_CentreOfMass_X"],self.vicon_data["hayashide_CentreOfMass_Y"],"o-",markersize=3,label="gravity")
        plt.legend()
        plt.xlabel("Hallway direction $/it{x}$ [m]")
        plt.ylabel("Width direction $/it{y}$ [m]")
        plt.gca().set_aspect('equal', adjustable='box')
        plt.subplot(gs[1,0])    
        plt.plot(self.vicon_data["timestamp"],self.vicon_data["hayashide_CentreOfMass_X"],"o-",markersize=3,label="gravity_x")
        plt.legend()
        plt.xlabel("Time $/it{t}$ [s]")
        plt.ylabel("Hallway direction $/it{x}$ [m]")
        plt.subplot(gs[1,1])    
        plt.plot(self.vicon_data["timestamp"],self.vicon_data["hayashide_CentreOfMass_Y"],"o-",markersize=3,label="gravity_y")
        plt.legend()
        plt.xlabel("Time $\it{t}$ [s]")
        plt.ylabel("Hallway direction $\it{y}$ [m]")
        plt.show()

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
        plt.plot(self.tf_data["timestamp"],self.tf_data["s_trunk_angle_z"]-135,"o-",markersize=3,label="s_trunk_angle_z")
        # plt.plot(self.tf_data["timestamp"],self.tf_data["b_trunk_angle_z"],"o-",markersize=3,label="b_trunk_angle_z")
        plt.xlabel("Time $/it{t}$ [s]")
        plt.ylabel("Yaw of the trunk [deg]")
        plt.legend()
        plt.grid()
        plt.savefig(self.savedirpath+"/"+os.path.basename(self.tfcsvpath)[:-11]+"_trunk_angle")
        # plt.cla()
        plt.show()

        # self.write_log([os.path.basename(self.tfcsvpath),self.tf_data["c_trunk_angle_y"].mean(),self.tf_data["c_trunk_angle_y"].median(),self.tf_data["c_trunk_angle_y"].std(),self.tf_data["c_trunk_angle_y"].min(),self.tf_data["c_trunk_angle_y"].max()],path_management["humpback_csv_path"],fmt="%s")
        pass

    def plot_knee_angle(self):
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
        plt.plot(self.tf_data["timestamp"],self.tf_data["r_hip_angle_x"],"o-",markersize=3,label="r_hip_angle_x")
        plt.plot(self.tf_data["timestamp"],self.tf_data["l_hip_angle_x"],"o-",markersize=3,label="l_hip_angle_x")
        plt.xlabel("Time $/it{t}$ [s]")
        plt.ylabel("Hip angle in (hallway width direction) th_x [deg]")
        plt.legend()
        plt.grid()
        plt.subplot(gs[1])   
        plt.plot(self.tf_data["timestamp"],self.tf_data["r_hip_angle_y"],"o-",markersize=3,label="r_hip_angle_y")
        plt.plot(self.tf_data["timestamp"],self.tf_data["l_hip_angle_y"],"o-",markersize=3,label="l_hip_angle_y")
        plt.xlabel("Time $/it{t}$ [s]")
        plt.ylabel("Hip angle in (hallway direction) th_y [deg]")
        plt.legend()
        plt.grid()
        plt.subplot(gs[2])   
        plt.plot(self.tf_data["timestamp"],self.tf_data["r_hip_angle_z"],"o-",markersize=3,label="r_hip_angle_z")
        plt.plot(self.tf_data["timestamp"],self.tf_data["l_hip_angle_z"],"o-",markersize=3,label="l_hip_angle_z")
        plt.xlabel("Time $/it{t}$ [s]")
        plt.ylabel("Hip angle in (yaw direction) th_z [deg]")
        plt.legend()
        plt.grid()
        plt.savefig(self.savedirpath+"/"+os.path.basename(self.tfcsvpath)[:-11]+"_knee_angle.png")
        plt.cla()
        pass

    def main(self):
        self.plot_odom()
        self.plot_head_angle()
        # self.plot_trunk_angle()

analysisv=analysisVicon()
analysisv.main()