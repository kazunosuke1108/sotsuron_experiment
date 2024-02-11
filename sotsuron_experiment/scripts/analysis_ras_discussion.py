import os
import shutil
import numpy as np
import pandas as pd
from glob import glob
from pprint import pprint
import pickle
import matplotlib.pyplot as plt
from noise_processor import vel_processor


import os
from glob import glob

if os.name == "nt":
    pythonpath = f"C:/Users/hayashide/AppData/Local/anaconda3/python"
    scriptsdirpath=f"C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/scripts"
    resultsdirpath = f"C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results"
else:
    # if os.path.exists("/home/hayashide/catkin_ws"):
    #     pythonpath = f"/usr/bin/python3"
    #     resultsdirpath = f"/home/hayashide/catkin_ws/src/ytlab_nlpmp_modules/results"
    #     scriptsdirpath = f"/home/hayashide/catkin_ws/src/ytlab_nlpmp_modules/scripts"
    # else:
    pythonpath="/home/hayashide/anaconda3/bin/python3"
    resultsdirpath = f"/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results"
    scriptsdirpath = f"/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/scripts"

class Discussion():
    def __init__(self):
        self.exp_memo_takahashi_path="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/exp_memo_takahashi.csv"
        self.exp_memo_all_path="C:/Users/hayashide/ytlab_ros_ws/ytlab_nlpmp/ytlab_nlpmp_modules/scripts/memo/exp_memo.csv"

        self.exp_memo_data=pd.read_csv(self.exp_memo_takahashi_path,header=0)
        self.exp_memo_data=self.exp_memo_data[(self.exp_memo_data["type"]==0) | (self.exp_memo_data["type"]==1) | (self.exp_memo_data["type"]==2)]
        self.exp_memo_data.reset_index(inplace=True)
        # print(self.exp_memo_data)
        self.exp_memo_all_data=pd.read_csv(self.exp_memo_all_path,header=0)
        self.exp_memo_all_data=self.exp_memo_all_data[(self.exp_memo_all_data["type"]==0) | (self.exp_memo_all_data["type"]==1) | (self.exp_memo_all_data["type"]==2)]
        self.exp_memo_all_data.reset_index(inplace=True)
        # print(self.exp_memo_all_data)

    def pickup_prcd_png(self):
        self.exp_memo_all_data["result"]=0
        for idx,row in self.exp_memo_all_data.iterrows():
            if str(row["nlpmp_path"]) != "nan" and (row["type"]==0 or row["type"]==1):
                nlpmp_path="C:/Users/hayashide"+row["nlpmp_path"][len("/home/hayashide"):]
                # print(nlpmp_path)
                try:
                    prcdpath=sorted(glob(nlpmp_path+"/*prcd.png"))[0]
                    # basename=f"{int(row['person_id'])}".zfill(2)+"_"+f"{int(row['type'])}".zfill(2)+"_"+f"{int(row['trial'])}".zfill(2)+"_"+os.path.basename(prcdpath)
                    basename=f"{int(row['person_id'])}".zfill(2)+"_"+f"{int(row['type'])}".zfill(2)+"_"+f"{int(row['trial'])}".zfill(2)+"_"+os.path.basename(prcdpath)
                    if row["nlpmp_path"] in self.exp_memo_data["nlpmp"].values:
                        # self.read_pickle_history(nlpmp_path)
                        plt.savefig("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/discussion/0or1/"+basename)
                        plt.cla()
                        shutil.copy(prcdpath,"C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/discussion/prcd/success/"+basename)
                        print(basename)
                        self.exp_memo_all_data["result"].iat[idx]=1

                    else:
                        # self.read_pickle_history(nlpmp_path)
                        plt.savefig("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/discussion/0or1/"+basename)
                        plt.cla()
                        # shutil.copy(prcdpath,"C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/discussion/prcd/failure/"+basename)
                        # self.read_pickle_history(nlpmp_path)
                    #     print(nlpmp_path)
                    #     print(self.exp_memo_data["nlpmp"].values)

                except IndexError:
                    pass
        self.exp_memo_all_data.to_csv("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/discussion/mp4/exp_memo_all_data.csv",index=0)
    def read_pickle_history(self,trialdirpath="C:/Users/hayashide/ytlab_ros_ws/ytlab_nlpmp/ytlab_nlpmp_modules/results/20231219/20231219_201042_20231219_05_01_00_inoue"):
        timestamp_list=[]
        x_list=[]
        y_list=[]
        vx_list=[]
        vy_list=[]
        for plandir in sorted(glob(trialdirpath+"/*")):
            if os.path.isdir(plandir):
                # print(plandir)
                try:
                    picklepath=sorted(glob(plandir+"/*.pickle"))[0]
                    print(picklepath)
                    with open(picklepath, 'rb') as pickle_file:
                        try:
                            data = pickle.load(pickle_file)
                            # pprint(data["log"])
                            # raise TimeoutError
                            # print(f"pickle file loaded: {picklepath}")
                        except EOFError:
                            print(f"pickle file broken: {picklepath}")
                            continue
                except IndexError:
                    continue
                timestamp_list.append(data["time_management"]["last_calc_end"]-data["time_management"]["cal_start2cal_end"])
                x_list.append(data["hmn"]["x0"])
                y_list.append(data["hmn"]["y0"])
                vx_list.append(data["hmn"]["vx"])
                vy_list.append(data["hmn"]["vy"])
                # print(data["time_management"]["last_calc_end"],data["hmn"]["x0"],data["hmn"]["y0"],)
                pprint(data["time_management"]["cal_start2cal_end"])

        prcdcsvpath=sorted(glob(trialdirpath+"/*prcd.csv"))[0]

        data=pd.read_csv(prcdcsvpath,names=["t","x","y","z"])
        prcd_data=data
        # prcd_data=outlier_processor(prcd_data)
        # prcd_data=mean_processor(prcd_data)
        prcd_data=vel_processor(prcd_data)
        # prcd_data=mean_processor(prcd_data)

        plt.rcParams["figure.figsize"] = (10,8)
        plt.rcParams["figure.autolayout"] = True
        plt.rcParams['font.family'] = 'Times New Roman'
        fig, ax1 = plt.subplots()
        ax1.plot(prcd_data["t"],prcd_data["x"],"--",label="x")
        ax1.plot(prcd_data["t"],prcd_data["y"],"--",label="y")
        # ax1.plot(prcd_data["t"],prcd_data["z"],"--",label="z")
        ax1.plot(timestamp_list,x_list,"o",label="x (motion planning)")
        ax1.plot(timestamp_list,y_list,"o",label="y (motion planning)")
        ax1.legend()
        ax1.set_xlabel("Time [s]")
        ax1.set_ylabel("Position [m]")
        ax2 = ax1.twinx()
        ax2.plot(prcd_data["t"],prcd_data["vx"],label="vx")
        ax2.plot(prcd_data["t"],prcd_data["vy"],label="vy")
        ax2.plot(timestamp_list,vx_list,linewidth=2,label="vx (motion planning)")
        ax2.legend()
        ax2.set_ylabel("Velocity [m/s]")

        # plt.show()
        
    def init_theta_traj(self,trialdirpaths):
        for trialdirpath in trialdirpaths:
            timestamp_list=[]
            timelist=[]
            print(trialdirpath)
            os.system(f"C:/Users/hayashide/AppData/Local/anaconda3/python.exe c:/Users/hayashide/ytlab_ros_ws/ytlab_nlpmp/ytlab_nlpmp_modules/scripts/drawConcatPath.py {trialdirpath}")
            # print(trialdirpath)
            # concatpicklepath=sorted(glob(trialdirpath+"/*.pickle"))[0]
            # with open(concatpicklepath, 'rb') as pickle_file:
            #     try:
            #         data = pickle.load(pickle_file)
            #     except EOFError:
            #         print(f"pickle file broken: {concatpicklepath}")
            #         continue
            #     # try:
            #     t=data["solution"]["t"]
            #     theta=data["solution"]["zR"][2,:]
            #     print(t)
            #     if "/home/hayashide"+trialdirpath[len("C:/Users/hayashide"):] in self.exp_memo_data["nlpmp"].values:  
            #         plt.plot(t,theta,"b",alpha=0.5)
            #     else:
            #         plt.plot(t,theta,"r",alpha=0.5)
            # plandirs=sorted(glob(trialdirpath+"/*"))
            
            # for plandir in sorted(glob(trialdirpath+"/*")):
            #     if os.path.isdir(plandir):
            #         # print(plandir)
            #         try:
            #             picklepath=sorted(glob(plandir+"/*.pickle"))[0]
            #             print(picklepath)
            #             with open(picklepath, 'rb') as pickle_file:
            #                 try:
            #                     data = pickle.load(pickle_file)
            #                 except EOFError:
            #                     print(f"pickle file broken: {picklepath}")
            #                     continue
            #                 try:
            #                     t=data["solution"]["t"]
            #                     theta=data["solution"]["zR"][2,:]
            #                     print(t)
            #                     if "/home/hayashide"+trialdirpath[len("C:/Users/hayashide"):] in self.exp_memo_data["nlpmp"].values:  
            #                         plt.plot(t,theta,"b",alpha=0.5)
            #                     else:
            #                         plt.plot(t,theta,"r",alpha=0.5)
            #                     break
            #                 except KeyError:
            #                     continue
            #         except IndexError:
            #             continue
        plt.show()



    def compare_time(self,trialdirpaths):
        for trialdirpath in trialdirpaths:
            timestamp_list=[]
            timelist=[]
            for plandir in sorted(glob(trialdirpath+"/*")):
                if os.path.isdir(plandir):
                    # print(plandir)
                    try:
                        picklepath=sorted(glob(plandir+"/*.pickle"))[0]
                        print(picklepath)
                        with open(picklepath, 'rb') as pickle_file:
                            try:
                                data = pickle.load(pickle_file)
                                # pprint(data["log"])
                                # raise TimeoutError
                                # print(f"pickle file loaded: {picklepath}")
                            except EOFError:
                                print(f"pickle file broken: {picklepath}")
                                continue
                    except IndexError:
                        continue
                    # print(data["time_management"]["last_calc_end"],data["hmn"]["x0"],data["hmn"]["y0"],)
                    timestamp_list.append(data["time_management"]["last_calc_end"]-data["time_management"]["cal_start2cal_end"])
                    timelist.append(data["time_management"]["cal_start2cal_end"])   
            if len(timestamp_list)>0:   
                if "/home/hayashide"+trialdirpath[len("C:/Users/hayashide"):] in self.exp_memo_data["nlpmp"].values:  
                    plt.plot(np.array(timestamp_list)-timestamp_list[0],timelist,"b",label=os.path.basename(trialdirpath))
                else:
                    plt.plot(np.array(timestamp_list)-timestamp_list[0],timelist,"r",label=os.path.basename(trialdirpath))


        plt.legend()
        plt.savefig("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/discussion/timestamp.png")
        plt.show()


    def main(self):
        trialdirpaths=[]
        # self.pickup_prcd_png()
        for idx,row in self.exp_memo_all_data.iterrows():
            if str(row["nlpmp_path"]) != "nan":
                nlpmp_path="C:/Users/hayashide"+row["nlpmp_path"][len("/home/hayashide"):]
                trialdirpaths.append(nlpmp_path)
        # self.init_theta_traj(trialdirpaths)
        for trialdirpath in trialdirpaths:
            tfcsv_path=trialdirpath+f"/{os.path.basename(trialdirpath)}_tf_raw.csv"
            odomcsv_path=trialdirpath+f"/{os.path.basename(trialdirpath)}_od_raw.csv"
            os.system(f"{pythonpath} {scriptsdirpath}/analysis_ras_wholebody.py {tfcsv_path} {odomcsv_path}")
        
        # self.pickup_prcd_png()
        # trialdirpath1="C:/Users/hayashide/ytlab_ros_ws/ytlab_nlpmp/ytlab_nlpmp_modules/results/20231219/20231219_201042_20231219_05_01_00_inoue"
        # trialdirpath2="C:/Users/hayashide/ytlab_ros_ws/ytlab_nlpmp/ytlab_nlpmp_modules/results/20231219/20231219_191011_20231219_04_02_05_ohnishi"
        # trialdirpath="C:/Users/hayashide/ytlab_ros_ws/ytlab_nlpmp/ytlab_nlpmp_modules/results/20231219/20231219_201042_20231219_05_01_00_inoue"
        # self.read_pickle_history(trialdirpath=trialdirpath2)
        # self.compare_time(trialdirpath1,trialdirpath2)

disc=Discussion()
disc.main()