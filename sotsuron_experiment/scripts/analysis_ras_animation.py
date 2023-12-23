import os
import sys
import pickle
from pprint import pprint
import numpy as np
import pandas as pd
from matplotlib import patches
import matplotlib.pyplot as plt

from analysis_management import *
from analysis_initial_processor import *

class plotSituation():
    def __init__(self,bag_basename="_2023-12-20-19-50-52"):
        self.exp_memo_path=f"C:/Users/hayashide/ytlab_ros_ws/ytlab_nlpmp/ytlab_nlpmp_modules/scripts/memo/exp_memo.csv"
        self.nlpmp_results_dir_path="C:/Users/hayashide/ytlab_ros_ws/ytlab_nlpmp/ytlab_nlpmp_modules/results"
        self.experiment_results_dir_path="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results"

        self.exp_memo=pd.read_csv(self.exp_memo_path,header=0)
        
        path_management,csv_labels,color_dict=management_initial()
        plt.rcParams["figure.figsize"] = (12,8)
        plt.rcParams["figure.autolayout"] = True
        plt.rcParams['font.family'] = 'Times New Roman'

        # tf_data
        self.tfcsvpath=self.experiment_results_dir_path+f"/{bag_basename}/{bag_basename}_tf_raw.csv"
        self.savedirpath=os.path.split(self.tfcsvpath)[0]
        tf_data=initial_processor(self.tfcsvpath,False)
        timestamp_xm5_closest_idx=(tf_data["gravity_x"]-(-5)).abs().idxmin()
        timestamp_xm5_closest=tf_data.iloc[timestamp_xm5_closest_idx]["timestamp"]
        # x_x0_closest=tf_data.iloc[timestamp_x0_closest_idx]["gravity_x"]
        tf_data=tf_data[tf_data["timestamp"]<timestamp_xm5_closest]
        timestamp_x8_closest_idx=(tf_data["gravity_x"]-8).abs().idxmin()
        timestamp_x8_closest=tf_data.iloc[timestamp_x8_closest_idx]["timestamp"]
        # x_x8_closest=tf_data.iloc[timestamp_x8_closest_idx]["gravity_x"]
        tf_data=tf_data[tf_data["timestamp"]>timestamp_x8_closest]
        tf_data=tf_data.reset_index()
        self.tf_data=tf_data

        # oddata
        self.odomcsvpath=self.experiment_results_dir_path+f"/{bag_basename}/{bag_basename}_od_raw.csv"
        # odom_data=pd.read_csv(self.odomcsvpath,header=0,names=csv_labels["odometry"])
        odom_data=initial_processor(self.odomcsvpath,False)
        self.odom_data=odom_data

        # nlpmp_pickle
        print(self.exp_memo)
        self.nlpmp_result_dir_path=self.exp_memo["nlpmp_path"][self.exp_memo["bag_path"]==bag_basename+".bag"]
        print(os.path.basename(str(self.nlpmp_result_dir_path.values[0]))[:8])
        self.nlpmp_result_dir_path=self.nlpmp_results_dir_path+"/"+os.path.basename(str(self.nlpmp_result_dir_path.values[0]))[:8]+"/"+os.path.basename(str(self.nlpmp_result_dir_path.values)[:-2])
        print(self.nlpmp_result_dir_path)
        for candidate in sorted(glob(self.nlpmp_result_dir_path+"/*")):
            if os.path.isdir(candidate):
                self.picklepath=sorted(glob(candidate+"/*.pickle"))[0]
                break
        print(self.picklepath)
        with open(self.picklepath, 'rb') as pickle_file:
            self.pickledata = pickle.load(pickle_file)
        pprint(self.pickledata)
        self.env=self.pickledata["env"]
        self.rbt=self.pickledata["rbt"]
        self.hmn=self.pickledata["hmn"]
        self.sns=self.pickledata["sns"]
    
    def plot_situation(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_aspect("equal", adjustable="box")
        plt.ylim([self.env["ymin"]-0.5,self.env["ymax"]+0.5])
        arc_resolution=100
        plt.plot([-5,10],[self.env["ymax"],self.env["ymax"]],"k")
        plt.plot([-5,10],[self.env["ymin"],self.env["ymin"]],"k")
        plt.plot(self.tf_data["trunk_x"],self.tf_data["trunk_y"],"r",linewidth=1)
        plt.plot(self.odom_data["x"],self.odom_data["y"],"b",linewidth=1)
        for idx,row in self.odom_data.iterrows():
            xR=row["x"]
            yR=row["y"]
            theta=row["theta"]
            pan=row["pan"]
            print(theta)
            arc_rad = np.linspace(theta + pan - self.sns["phi"],
                        theta + pan + self.sns["phi"], arc_resolution)
            arc_r1_x = self.sns["r1"] * np.cos(arc_rad) + xR
            arc_r1_y = self.sns["r1"] * np.sin(arc_rad) + yR
            arc_r2_x = self.sns["r2"] * np.cos(arc_rad) + xR
            arc_r2_y = self.sns["r2"] * np.sin(arc_rad) + yR

            # arc_r1 = plt.plot(arc_r1_x, arc_r1_y, 'g', linewidth=2.5)
            # arc_r2 = plt.plot(arc_r2_x, arc_r2_y, 'g', linewidth=2.5)

            # print(f"{theta}, {pan}")

            arc_r1 = patches.Arc(xy=(xR,yR), width=2*self.sns['r1'], height=2*self.sns['r1'], theta1=180/np.pi*((pan+theta)-self.sns['phi']), theta2=180/np.pi*((pan+theta)+self.sns['phi']), edgecolor="g", linewidth=0.5, label="arc")
            arc_r2 = patches.Arc(xy=(xR,yR), width=2*self.sns['r2'], height=2*self.sns['r2'], theta1=180/np.pi*((pan+theta)-self.sns['phi']), theta2=180/np.pi*((pan+theta)+self.sns['phi']), edgecolor="g", linewidth=0.5, label="arc")
            plt.gca().add_patch(arc_r1)
            plt.gca().add_patch(arc_r2)

            arc_right = plt.plot([arc_r1_x[0], arc_r2_x[0]], [
                                arc_r1_y[0], arc_r2_y[0]], 'g', linewidth=0.1,alpha=0.2)
            arc_left = plt.plot([arc_r1_x[-1], arc_r2_x[-1]],
                                [arc_r1_y[-1], arc_r2_y[-1]], 'g', linewidth=0.1,alpha=0.2)
        plt.show()
    
    def main(self):
        self.plot_situation()

plot=plotSituation("_2023-12-19-12-38-43")
plot.main()