import os
import numpy as np
import pandas as pd
from glob import glob
import matplotlib.pyplot as plt
from noise_processor import vel_processor,resampling_processor
from analysis_management import *

path_management,csv_labels,color_dict=management_initial()
exp_memo_path="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/exp_memo_all.csv"
exp_memo_data=pd.read_csv(exp_memo_path,header=0)
exp_memo_data=exp_memo_data[(exp_memo_data["type"]==0) | (exp_memo_data["type"]==1) | (exp_memo_data["type"]==2)]
# print(exp_memo_data)
# raise TimeoutError
for idx,row in exp_memo_data.iterrows():
    if (str(row["bag_path"])!="nan") & (str(row["nlpmp_path"])!="nan") :
        result_path="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/"+row["bag_path"][:-4]
        nlpmp_path="C:/Users/hayashide/"+row["nlpmp_path"][len("/home/hayashide/"):]
        # print(result_path)
        # print(nlpmp_path)
        try:
            # print(sorted(glob(nlpmp_path+"/*")))
            # slow_data_path=sorted(glob(os.path.join(result_path,"*tf_raw.csv")))[0]
            # print("loaded slow data")
            fast_prcd_data_path=sorted(glob(os.path.join(nlpmp_path,"*prcd.csv")))[0]
            # print("loaded fast prcd data")
            fast_raw_data_path=sorted(glob(os.path.join(nlpmp_path,"*tf.csv")))[0]
            # print("loaded fast raw data")
            odom_data_path=sorted(glob(os.path.join(nlpmp_path,"*od.csv")))[0]
            # print("loaded odom data")
        except IndexError:
            print("IndexError:",nlpmp_path)
            continue
        # raise TimeoutError
        # slow_data_path="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-21-10-22-39/_2023-12-21-10-22-39_tf_raw.csv"
        # fast_prcd_data_path="C:/Users/hayashide/ytlab_ros_ws/ytlab_nlpmp/ytlab_nlpmp_modules/results/20231221/20231221_102252_20231221_06_00_02_murayama/20231221_102306_prcd.csv"
        # fast_raw_data_path="C:/Users/hayashide/ytlab_ros_ws/ytlab_nlpmp/ytlab_nlpmp_modules/results/20231221/20231221_102252_20231221_06_00_02_murayama/20231221_102306_tf.csv"
        # odom_data_path="C:/Users/hayashide/ytlab_ros_ws/ytlab_nlpmp/ytlab_nlpmp_modules/results/20231221/20231221_102252_20231221_06_00_02_murayama/20231221_102302_od.csv"

        # slow_data=pd.read_csv(slow_data_path,names=csv_labels["detectron2_joint_3d"])
        # slow_data.rename(columns={"timestamp":"t","trunk_x":"x","trunk_y":"y","trunk_z":"z"},inplace=True)
        # # slow_data=slow_data[["t","x","y","z"]].iloc[1:]
        # # # slow_cut_idx=(slow_data["t"][slow_data["t"]<slow_data["t"].min()+50].idxmax())
        # # slow_data=slow_data[:slow_cut_idx]
        # # slow_data=vel_processor(slow_data)
        # slow_data.to_csv("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/analysis_ws/slow.csv")
        # raise TimeoutError

        fast_prcd_data=pd.read_csv(fast_prcd_data_path,names=["t","x","y","z"])
        fast_prcd_data=vel_processor(fast_prcd_data)
        fast_cut_idx=(fast_prcd_data["t"][fast_prcd_data["t"]<fast_prcd_data["t"].min()+50].idxmax())
        fast_prcd_data=fast_prcd_data[:fast_cut_idx]
        fast_prcd_data.to_csv("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/analysis_ws/fast_prcd.csv")

        fast_raw_data=pd.read_csv(fast_raw_data_path,names=["t","x","y","z"])
        fast_raw_data=vel_processor(fast_raw_data)
        fast_cut_idx=(fast_raw_data["t"][fast_raw_data["t"]<fast_raw_data["t"].min()+50].idxmax())
        fast_raw_data=fast_raw_data[:fast_cut_idx]
        fast_raw_data.to_csv("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/analysis_ws/fast_raw.csv")

        odom_data=pd.read_csv(odom_data_path,names=["t","x","y","z","ph"])
        odom_data=resampling_processor(odom_data,"0.1S")
        odom_data=vel_processor(odom_data)
        odom_data.to_csv("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/analysis_ws/odom.csv")

        plt.rcParams["figure.figsize"] = (10,8)
        plt.rcParams["figure.autolayout"] = True
        plt.rcParams['font.family'] = 'Times New Roman'

        fig, ax1 = plt.subplots()
        ax1.plot(fast_prcd_data["t"],fast_prcd_data["x"],"-",label="x (fast prcd)")
        ax1.plot(fast_raw_data["t"],fast_raw_data["x"],"-",label="x (fast raw)")
        # # ax1.plot(slow_data["t"],slow_data["x"],"-",label="x (slow)")
        ax1.plot(odom_data["t"],odom_data["x"],"-",label="x (odom)")
        ax1.plot([odom_data["t"][odom_data["x"]<0.1].max(),odom_data["t"][odom_data["x"]<0.1].max()],[-5,10],"r",label="robot start")
        ax1.legend()
        ax1.set_xlabel("Time [s]")
        ax1.set_ylabel("Position [m]")
        ax2 = ax1.twinx()
        # ax2.plot(fast_prcd_data["t"],fast_prcd_data["vx"],"--",label="vx (fast)")
        # ax2.plot(fast_raw_data["t"],fast_raw_data["vx"],"--",label="vx (raw)")
        # ax2.plot(slow_data["t"],slow_data["vx"],"--",label="vx (slow)")
        ax2.plot(odom_data["t"],odom_data["vx"],"-",linewidth=0.5,label="vx (odom)")
        ax2.legend()
        ax2.set_ylabel("Velocity [m/s]")
        try:
            plt.savefig(result_path+"/"+os.path.basename(fast_prcd_data_path)[:-4]+"_check_start_noise.png")
        except FileNotFoundError:
            plt.savefig("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/analysis_ws"+"/"+os.path.basename(fast_prcd_data_path)[:-4]+"_check_start_noise.png")

        # print(slow_data["t"].min())
        # print(slow_data["t"].max())
        plt.pause(0.1)

# for i in range(5,len(data)):
#     fast_prcd_data=data.iloc[:i]
#     fast_prcd_data=mean_processor(fast_prcd_data)
#     fast_prcd_data=vel_processor(fast_prcd_data)
#     fast_prcd_data=mean_processor(fast_prcd_data)

#     # fig, ax1 = plt.subplots()
#     plt.plot(fast_prcd_data["t"],fast_prcd_data["x"],"o-",label="x")
#     plt.plot(fast_prcd_data["t"],fast_prcd_data["y"],"o-",label="y")
#     # plt.plot(fast_prcd_data["t"],fast_prcd_data["theta"],"o-",label="theta")
#     # plt.plot(fast_prcd_data["t"],fast_prcd_data["pan"],"o-",label="pan")
#     # ax2 = ax1.twinx()
#     plt.plot(fast_prcd_data["t"],fast_prcd_data["vx"],"o--",label="vx")
#     plt.plot(fast_prcd_data["t"],fast_prcd_data["vy"],"o--",label="vy")
#     plt.legend()
#     # ax2.legend()
#     plt.pause(0.01)
#     plt.cla()