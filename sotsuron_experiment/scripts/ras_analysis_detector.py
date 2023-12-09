#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
import numpy as np
import pandas as pd
from glob import glob
import matplotlib.pyplot as plt
import pandas as pd
from pprint import pprint
import pickle

from analysis_management import *
from analysis_initial_processor import *
path_management,csv_labels,color_dict=management_initial()

csvpaths=sorted(glob("/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/exp_log/fast_detector"+"/*_21*.csv"))
for csvpath in csvpaths:
    #import data
    data=pd.read_csv(csvpath,names=csv_labels["detectron2_joint_3d_4"])
    start=time.time()
    # data=initial_processor(csvpath=csvpath,denoise=True)
    print(time.time()-start)

    # integrate
    # data["trunk_x"]=0
    # data["trunk_y"]=0
    # data["trunk_z"]=0
    # data["trunk_0"]=0
    # data["c_base_x"]=0
    # data["c_base_y"]=0
    # data["c_base_z"]=0
    # data["c_base_0"]=0

    # data["trunk_x"]=(data["l_shoulder_x"]+data["r_shoulder_x"]+data["l_base_x"]+data["l_base_x"])/4
    # data["trunk_y"]=(data["l_shoulder_y"]+data["r_shoulder_y"]+data["l_base_y"]+data["l_base_y"])/4
    # data["trunk_z"]=(data["l_shoulder_z"]+data["r_shoulder_z"]+data["l_base_z"]+data["l_base_z"])/4
    # data["c_base_x"]=(data["l_base_x"]+data["l_base_x"])/2
    # data["c_base_y"]=(data["l_base_y"]+data["l_base_y"])/2
    # data["c_base_z"]=(data["l_base_z"]+data["l_base_z"])/2

    # data["trunk_vx"]=0
    # data["trunk_vy"]=0
    # data["trunk_vz"]=0
    # data["trunk_vx"][:-1]=(data["trunk_x"].values[1:]-data["trunk_x"].values[:-1])/(data["timestamp"].values[1:]-data["timestamp"].values[:-1])
    # data["trunk_vy"][:-1]=(data["trunk_y"].values[1:]-data["trunk_y"].values[:-1])/(data["timestamp"].values[1:]-data["timestamp"].values[:-1])
    # data["trunk_vz"][:-1]=(data["trunk_z"].values[1:]-data["trunk_z"].values[:-1])/(data["timestamp"].values[1:]-data["timestamp"].values[:-1])
    # plot
    plt.rcParams["figure.figsize"] = (30,15)
    plt.rcParams["figure.autolayout"] = True
    plt.rcParams['font.family'] = 'Times New Roman'

    fig, ax = plt.subplots() 
    g1=plt.subplot(221)
    g2=plt.subplot(222)
    g3=plt.subplot(223)
    g4=plt.subplot(224)

    for label in csv_labels["detectron2_joint_3d_4"]:
        if label[-1]=="x":
            if  ("gravity" not in label) & ("trunk" not in label):
                g1.plot(data["timestamp"],data[label],"o-",label=label)
            else:
                g4.plot(data["timestamp"],data[label],"o-",label=label)
        if label[-1]=="y":
            if  ("gravity" not in label) & ("trunk" not in label):
                g2.plot(data["timestamp"],data[label],"o-",label=label)
            else:
                g4.plot(data["timestamp"],data[label],"o-",label=label)
        if label[-1]=="z":
            if  ("gravity" not in label) & ("trunk" not in label):
                g3.plot(data["timestamp"],data[label],"o-",label=label)
            else:
                g4.plot(data["timestamp"],data[label],"o-",label=label)
        pass

    g1.set_xlabel("Time [s]")
    g1.set_ylabel("Position x [m]")
    g1.grid()
    g2.set_xlabel("Time [s]")
    g2.set_ylabel("Position y [m]")
    g2.grid()
    g3.set_xlabel("Time [s]")
    g3.set_ylabel("Position z [m]")
    g3.legend()
    g3.grid()
    g4.set_xlabel("Time [s]")
    g4.set_ylabel("Position z [m]")
    g4.legend()
    g4.grid()
    plt.savefig(os.path.split(csvpath)[0]+"/"+os.path.basename(csvpath)[:-4]+"_raw.png")
    # plt.show()
    print(data["timestamp"])
    plt.cla()