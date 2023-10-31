from glob import glob
import matplotlib.pyplot as plt
import pandas as pd
from pprint import pprint
import pickle

from analysis_management import *
from analysis_initial_processor import *
path_management,csv_labels,color_dict=management_initial()

def export_comparefile_csv():
    print("answer")
    odom_paths=path_management["ras_od_csv_dir_path_unique"]
    pprint(odom_paths)

    sim_paths_temp=sorted(glob("C:/Users/hayashide/ytlab_ros_ws/ytlab_nlpmp/ytlab_nlpmp_modules/results/2023102*/*/*_od.csv"))
    sim_paths=[]
    for candidate in sim_paths_temp:
        if ("_hayashide" not in candidate) and ("iter" not in candidate):
            sim_paths.append(candidate)
        else:
            print("not test data")
    pprint(sim_paths)

    skeleton_paths=sorted(glob("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/mp4/skeleton/*"))
    skeleton_paths_unique=[]
    for trial in skeleton_paths:
        if trial not in skeleton_paths_unique:
            same_trial=sorted(glob(os.path.split(trial)[0]+"/"+os.path.split(trial)[1][:6]+"*.mp4"))
            if same_trial[-1] not in skeleton_paths_unique:
                skeleton_paths_unique.append(same_trial[-1])
    exp_time=[]
    last_x=[]
    for sim_path in sim_paths:
        temp=pd.read_csv(sim_path)
        exp_time.append(len(temp))
        last_x.append(temp.values[-1,1])
    pd_dict={}
    pd_dict["sim_paths"]=sim_paths
    pd_dict["exp_time"]=exp_time
    pd_dict["last_x"]=last_x
    pd_dict["odom_paths"]=odom_paths
    pd_dict["skeleton_paths"]=skeleton_paths_unique


    data=pd.DataFrame((dict([ (k,pd.Series(v)) for k,v in pd_dict.items() ])))
    print(len(odom_paths))
    print(len(sim_paths))
    print(len(skeleton_paths))
    print(data)
    data.to_csv(path_management["comparefile_csv_path"])

def export_usabledata_csv():
    inputcsv="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/csv/input.csv"
    data=pd.read_csv(inputcsv,header=0,names=["sim_path","odom_path","skeleton_path"])
    data["sim_path"]="C:/Users/hayashide/ytlab_ros_ws/ytlab_nlpmp/ytlab_nlpmp_modules/results/"+data["sim_path"]
    data["odom_path"]="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/ras_csv/"+data["odom_path"]
    data["skeleton_path"]="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/mp4/skeleton/"+data["skeleton_path"]

    print(len(data))
    data=data[~data["sim_path"].str.contains('missing')]
    data=data[~data["odom_path"].str.contains('missing')]
    data=data[~data["skeleton_path"].str.contains('missing')]
    print(len(data))

    data.to_csv(path_management["usabledata_csv_path"],index=False)


pathdata=pd.read_csv(path_management["usabledata_csv_path"],header=0)

for index, row in pathdata.iterrows():
    plt.rcParams["figure.figsize"] = (10,8)
    plt.rcParams["figure.autolayout"] = True
    plt.rcParams['font.family'] = 'Times New Roman'
    fig, ax = plt.subplots() 
    odomdata=pd.read_csv(row["odom_path"],names=["tH","xH","yH","thH","zero","t","x","y","theta","pan"])
    # simdata=pd.read_csv(row["sim_path"],names=["t","x","y","theta"])
    try:
        with open(os.path.split(row["sim_path"])[0]+"/concat_traj.pickle", 'rb') as pickle_file:
            pickledata = pickle.load(pickle_file)
    except FileNotFoundError:
        continue
    simdata_dict={}
    simdata_dict["t"]=pickledata["solution"]["t"]
    if index>1:
        simdata_dict["t"]*=5
    simdata_dict["x"]=pickledata["solution"]["zR"][0,:]
    simdata_dict["y"]=pickledata["solution"]["zR"][1,:]
    simdata_dict["theta"]=pickledata["solution"]["zR"][2,:]
    simdata=pd.DataFrame(simdata_dict)
    print(simdata_dict["t"])

    odomdata=odomdata[odomdata["x"]>1e-2]
    simdata=simdata[simdata["x"]>1e-2]
    try:
        odomdata["t"]=odomdata["t"]-odomdata["t"].iat[0]
        simdata["t"]=simdata["t"]-simdata["t"].iat[0]
        err=""
    except IndexError:
        err="_error"
        pass

    g=plt.subplot(221)
    g.plot(simdata["x"],simdata["y"],"c",label="plan")
    g.plot(odomdata["x"],odomdata["y"],"b",label="odom")
    g.set_aspect('equal')
    g.set_xlabel("Hallway direction $\it{x}$ [m]")
    g.set_ylabel("Width direction $\it{y}$ [m]")
    g.set_title(os.path.basename(row["odom_path"])[:-4]+err)
    g.legend()
    g=plt.subplot(222)
    g.plot(simdata["t"],simdata["x"],"c",label="plan")
    g.plot(odomdata["t"],odomdata["x"],"b",label="odom")
    g.set_xlabel("time $\it{t}$ [s]")
    g.set_ylabel("Hallway direction $\it{x}$ [m]")
    g.legend()
    g=plt.subplot(223)
    g.plot(simdata["t"],simdata["y"],"c",label="plan")
    g.plot(odomdata["t"],odomdata["y"],"b",label="odom")
    g.set_xlabel("time $\it{t}$ [s]")
    g.set_ylabel("Hallway direction $\it{y}$ [m]")
    g.legend()
    g=plt.subplot(224)
    g.plot(simdata["t"],simdata["theta"],"c",label="plan")
    g.plot(odomdata["t"],odomdata["theta"]+odomdata["pan"],"b",label="odom")
    g.set_xlabel("time $\it{t}$ [s]")
    g.set_ylabel("Hallway direction $\it{\Theta}$ [m]")
    g.legend()
    print(os.path.basename(row["odom_path"])[:-4])
    plt.savefig(path_management["png_dir_path"]+"/odom_sim_gap/"+os.path.basename(row["odom_path"])[:-4]+".png")
