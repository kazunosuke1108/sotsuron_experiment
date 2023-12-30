import os
import sys
import pickle
from pprint import pprint
import numpy as np
import pandas as pd
from matplotlib import patches
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from analysis_management import *
from analysis_initial_processor import *

class plotSituation():
    def __init__(self,bag_basename="_2023-12-19-20-10-31"):
        self.bag_basename=bag_basename
        self.exp_memo_path=f"C:/Users/hayashide/ytlab_ros_ws/ytlab_nlpmp/ytlab_nlpmp_modules/scripts/memo/exp_memo.csv"
        self.nlpmp_results_dir_path="C:/Users/hayashide/ytlab_ros_ws/ytlab_nlpmp/ytlab_nlpmp_modules/results"
        self.experiment_results_dir_path="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results"

        self.exp_memo=pd.read_csv(self.exp_memo_path,header=0)
        
        path_management,csv_labels,color_dict=management_initial()
        plt.rcParams["figure.figsize"] = (7,3.5)
        plt.rcParams["figure.autolayout"] = True
        plt.rcParams['font.family'] = 'Times New Roman'

        # tf_data
        self.tfcsvpath=self.experiment_results_dir_path+f"/{bag_basename}/{bag_basename}_tf_raw.csv"
        self.savedirpath=os.path.split(self.tfcsvpath)[0]
        tf_data=initial_processor(self.tfcsvpath,True)
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
        # odom_data=odom_data[odom_data["t"]<timestamp_xm5_closest]
        odom_data=odom_data[odom_data["t"]>timestamp_x8_closest]
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

    def objF_kukei(self, t, z, u, env, rbt, hmn, sns,zH):
        zR = z
        # if hmn['path_prediction'] == "SFM":
        #     zH, _ = getHumanPath_SFM_paper(t, z, env, rbt, hmn, sns)
        # else:
        #     zH = getHumanPath(t, hmn)

        try:
            vec_HR = np.vstack((zH[0] - zR[0], zH[1] - zR[1]))
        except Exception:
            vec_HR = np.vstack((zH[0] - np.transpose(zR[0]), zH[1] - np.transpose(zR[1])))
        norm_HR = np.sqrt(vec_HR[0] ** 2 + vec_HR[1] ** 2)
        vec_HR = np.vstack(((norm_HR - hmn["sizer"]) / norm_HR, (norm_HR - hmn["sizer"]) / norm_HR) * vec_HR)
        norm_HR = np.sqrt(vec_HR[0] ** 2 + vec_HR[1] ** 2)
        deg_HR = np.arctan2(vec_HR[1], vec_HR[0])
        deg_compensate1 = np.logical_and((vec_HR[0] < 0), (vec_HR[1] > 0))
        deg_compensate2 = np.logical_and((vec_HR[0] < 0), (vec_HR[1] < 0))
        deg_diff = deg_HR - z[2]

        # 条件式の作成
        condition0 = norm_HR <= sns["r1"]
        condition1 = np.logical_and(sns["r1"] <= norm_HR, norm_HR <= env["ymax"] - env["ymin"] - hmn["sizer"] - rbt["sizer"])
        condition2 = np.logical_and(env["ymax"] - env["ymin"] - hmn["sizer"] - rbt["sizer"] <= norm_HR,
                                    norm_HR <= (sns["r1"] + sns["r2"]) / 2)
        condition3 = np.logical_and((sns["r1"] + sns["r2"]) / 2 <= norm_HR, norm_HR <= sns["r2"])
        condition4 = sns["r2"] < norm_HR

        # 評価関数の定義
        eval_func1_alpha = (0 - 1) / (sns["r1"] - (env["ymax"] - env["ymin"] - hmn["sizer"] - rbt["sizer"]))
        eval_func1_beta = 0 - eval_func1_alpha * sns["r1"]
        eval_func3_alpha = (1 - 0) / ((sns["r1"] + sns["r2"]) / 2 - sns["r2"])
        eval_func3_beta = 1 - eval_func3_alpha * (sns["r1"] + sns["r2"]) / 2

        # 関数の評価
        score_r = (eval_func1_alpha * norm_HR + eval_func1_beta) * condition1
        score_r += 1 * condition2
        score_r += (eval_func3_alpha * norm_HR + eval_func3_beta) * condition3

        mu_phi = 0
        sgm_phi = 1 / 6 * 2 * sns["phi"]
        score_p = np.exp(-(deg_diff - mu_phi) ** 2 / (2 * sgm_phi ** 2)) / (sgm_phi * np.sqrt(2 * np.pi))

        J_kari = np.dot(score_r, score_p.T)
        J = -J_kari

        return J
        
    
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

            arc_r1 = patches.Arc(xy=(xR,yR), width=2*self.sns['r1'], height=2*self.sns['r1'], theta1=180/np.pi*((pan+theta)-self.sns['phi']), theta2=180/np.pi*((pan+theta)+self.sns['phi']), edgecolor="g", linewidth=0.5, label="measurable area")
            arc_r2 = patches.Arc(xy=(xR,yR), width=2*self.sns['r2'], height=2*self.sns['r2'], theta1=180/np.pi*((pan+theta)-self.sns['phi']), theta2=180/np.pi*((pan+theta)+self.sns['phi']), edgecolor="g", linewidth=0.5)
            plt.gca().add_patch(arc_r1)
            plt.gca().add_patch(arc_r2)

            arc_right = plt.plot([arc_r1_x[0], arc_r2_x[0]], [
                                arc_r1_y[0], arc_r2_y[0]], 'g', linewidth=0.1,alpha=0.2)
            arc_left = plt.plot([arc_r1_x[-1], arc_r2_x[-1]],
                                [arc_r1_y[-1], arc_r2_y[-1]], 'g', linewidth=0.1,alpha=0.2)
        plt.show()

    def add_plot_ougi(self,row):
        arc_resolution=100
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

        arc_r1 = patches.Arc(xy=(xR,yR), width=2*self.sns['r1'], height=2*self.sns['r1'], theta1=180/np.pi*((pan+theta)-self.sns['phi']), theta2=180/np.pi*((pan+theta)+self.sns['phi']), edgecolor="g", linewidth=3, label="measurable area")
        arc_r2 = patches.Arc(xy=(xR,yR), width=2*self.sns['r2'], height=2*self.sns['r2'], theta1=180/np.pi*((pan+theta)-self.sns['phi']), theta2=180/np.pi*((pan+theta)+self.sns['phi']), edgecolor="g", linewidth=3)
        plt.gca().add_patch(arc_r1)
        plt.gca().add_patch(arc_r2)

        arc_right = plt.plot([arc_r1_x[0], arc_r2_x[0]], [
                            arc_r1_y[0], arc_r2_y[0]], 'g', linewidth=3,alpha=1)
        arc_left = plt.plot([arc_r1_x[-1], arc_r2_x[-1]],
                            [arc_r1_y[-1], arc_r2_y[-1]], 'g', linewidth=3,alpha=1)
        arc_right_support = plt.plot([xR,arc_r1_x[0]], [
                            yR,arc_r1_y[0]], 'g--', linewidth=3,alpha=1)
        arc_left_support = plt.plot([xR,arc_r1_x[-1]],
                            [yR,arc_r1_y[-1]], 'g--', linewidth=3,alpha=1)
        
    def add_plot_others(self,row):
        arc_resolution=100
        xR=row["x"]
        yR=row["y"]
        theta=row["theta"]
        pan=row["pan"]
        rbt_position = plt.Circle((xR, yR),
                                     radius=self.rbt["sizer"], edgecolor='b', facecolor='w')#,label="robot")
        plt.gca().add_patch(rbt_position)
        rbt_direction = plt.plot([xR, xR + self.rbt["sizer"] * np.cos(theta + pan)],
                                 [yR, yR + self.rbt["sizer"] * np.sin(theta + pan)], 'b', linewidth=2)
        hmn_position = plt.Circle((self.tf_data["trunk_x"][abs(self.tf_data["timestamp"]-row["t"]).idxmin()], self.tf_data["trunk_y"][abs(self.tf_data["timestamp"]-row["t"]).idxmin()]),
                                     radius=self.hmn["sizer"], edgecolor='r', facecolor='w')#,label="human")
        plt.gca().add_patch(hmn_position)
        print(self.tf_data["trunk_x"][abs(self.tf_data["timestamp"]-row["t"]).idxmin()], self.tf_data["trunk_y"][abs(self.tf_data["timestamp"]-row["t"]).idxmin()])
        # raise TimeoutError
        # plt.gca().add_patch(arc_right)
        # plt.gca().add_patch(arc_left)
        
    def plot_colormap(self):
        # fig = plt.figure()
        # ax = fig.add_subplot(111)
        # ax.set_aspect("equal", adjustable="box")
        # plt.ylim([self.env["ymin"]-0.5,self.env["ymax"]+0.5])

        t=0
        z=np.zeros(6)
        u=np.zeros(3)
        x_array=np.arange(-5,10,0.1)
        y_array=np.arange(-1.2,1.2,0.1)

        X, Y = np.meshgrid(x_array, y_array)
        J_list=np.zeros_like(X)

        print(J_list.shape)
        pprint(self.sns)

        # x_list=[]
        # y_list=[]
        # J_list=[]
        fig = plt.figure()
        ax = fig.subplots()
        ax.set_aspect("equal")
        first_iter=True
        for idx,row in self.odom_data.iterrows():
            if idx%5==0:
                print(f"plotting...: {self.bag_basename} {idx}/{len(self.odom_data)}")
                xR=row["x"]
                yR=row["y"]
                theta=row["theta"]
                pan=row["pan"]
                z[0]=xR
                z[1]=yR
                z[2]=theta+pan
                for idx_x,x in enumerate(x_array):
                    for idx_y,y in enumerate(y_array):
                        zH=np.array([x,y,0,0,0,0])
                        J=-self.objF_kukei(t,z,u,self.env,self.rbt,self.hmn,self.sns,zH)
                        J_list[idx_y][idx_x]+=J
            
            if idx==900 or idx==1000 or idx==1100 or idx==1200 or idx==1300 or idx==1400: # [self.odom_data["t"]<=row["t"]]
                J_list_log=np.log(J_list)
                J_list_log=np.where(J_list_log<0,0,J_list_log)
                ax.pcolor(x_array,y_array,J_list_log,cmap="jet",alpha=0.25)
                plt.plot(self.odom_data["x"][self.odom_data["t"]<=row["t"]],self.odom_data["y"][self.odom_data["t"]<=row["t"]],"b")
                # plt.plot(self.tf_data["trunk_x"],self.tf_data["trunk_y"],"r",label="human")
                self.add_plot_ougi(row)
                self.add_plot_others(row)
                plt.legend()
                plt.xlabel("Hallway direction $\it{x}$ [m]")
                plt.ylabel("Width direction $\it{y}$ [m]")
                plt.xlim([-4,7])
                plt.ylim([-2,2])
                plt.savefig(os.path.split(self.tfcsvpath)[0]+"/"+os.path.basename(self.tfcsvpath)[:-11]+f"_colormap_1229_{idx}.png")
                plt.cla()
                self.add_plot_others(row)
                # fig = plt.figure()
                # # ax = Axes3D(fig)

                # ax = fig.add_subplot(111,projection='3d')
                # ax.plot_surface(X, Y, J_list, cmap='jet', linewidth=0)
                # ax.set_xlabel("Hallway direction $/it{x}$ [m]")
                # ax.set_ylabel("Width direction $/it{y}$ [m]")
                # ax.set_zlabel("Value of the function $/it{J}$")

                # ax.plot([0,10],[-2,-2],"k")
                # ax.plot([0,10],[2,2],"k")
                # ax.view_init(elev=90, azim=180)
                # plt.pause(1)
                # plt.cla()
                if idx==1400:
                    break
            # break
        # ax.pcolor(x_array,y_array,J_list,cmap="jet",alpha=0.25)
        # plt.plot(self.odom_data["x"],self.odom_data["y"],"b",label="robot")
        # plt.plot(self.tf_data["trunk_x"],self.tf_data["trunk_y"],"r",label="human")
        # plt.savefig(os.path.split(self.tfcsvpath)[0]+"/"+os.path.basename(self.tfcsvpath)[:-11]+"_colormap.png")
        # plt.cla()
        # fig = plt.figure()
        # ax = fig.subplots()
        # ax.set_aspect("equal")
        J_list_log=np.log(J_list)
        J_list_log=np.where(J_list_log<0,0,J_list_log)
        ax.pcolor(x_array,y_array,J_list_log,cmap="jet",alpha=0.25)
        plt.plot(self.odom_data["x"],self.odom_data["y"],"b")#,label="robot")
        # plt.plot(self.tf_data["trunk_x"],self.tf_data["trunk_y"],"r",label="human")
        plt.savefig(os.path.split(self.tfcsvpath)[0]+"/"+os.path.basename(self.tfcsvpath)[:-11]+"_colormap_1229.png")
        plt.legend()
        plt.xlabel("Hallway direction $\it{x}$ [m]")
        plt.ylabel("Width direction $\it{y}$ [m]")
        # ax = fig.add_subplot(111,projection='3d')
        # ax.plot_surface(X, Y, J_list, cmap='jet', linewidth=0)
        # ax.set_xlabel("Hallway direction $/it{x}$ [m]")
        # ax.set_ylabel("Width direction $/it{y}$ [m]")
        # ax.set_zlabel("Value of the function $/it{J}$")
        # ax.set_xlim([-10,10])
        # ax.set_ylim([-10,10])

        # ax.plot([0,10],[-1.2,-1.2],"k")
        # ax.plot([0,10],[1.2,1.2],"k")
        # ax.view_init(elev=90, azim=180)

        # plt.show()

    def main(self):
        # self.plot_situation()
        self.plot_colormap()

exp_memo_01_data=pd.read_csv("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/discussion/exp_memo_01.csv",header=0)


# trialdirpaths=sorted(glob("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-19*"))
# trialdirpaths+=sorted(glob("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-21*"))
# for trialdirpath in trialdirpaths[2:]:
#     if os.path.basename(trialdirpath)+".bag" in exp_memo_01_data["bag_path"].values:
#         try:
#             plot=plotSituation(os.path.basename(trialdirpath))
#             plot.main()
#         except Exception as e:
#             exc_type, exc_obj, exc_tb = sys.exc_info()
#             print(f"line {exc_tb.tb_lineno}: {e}")

    # break

plot=plotSituation()
plot.main()




# plt.savefig("C:/Users/hayashide/latex_ws/20231201_midtermReport/images/objF_potential_top.png")
# plt.show()