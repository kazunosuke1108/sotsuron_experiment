#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
csv_dir_path=os.environ['HOME']+"/catkin_ws/src/sotsuron_experiment/results/0108/csv"
csv_result_path=os.environ['HOME']+"/catkin_ws/src/sotsuron_experiment/results/0108/results"

csv_paths=sorted(glob(csv_dir_path+"/*"))
for csv_path in csv_paths:
    data=np.loadtxt(csv_path,delimiter=",")

    t_img=data[:,0]
    x=data[:,1]/1000
    y=data[:,2]/1000
    z=data[:,3]/1000
    t_odm=data[:,5]
    xR=data[:,6]
    yR=data[:,7]
    thR=data[:,8]
    pan=data[:,9]

    xH=xR+z*np.cos(thR+pan)+x*np.sin(thR+pan)
    yH=yR+z*np.sin(thR+pan)-x*np.cos(thR+pan)


    plt.plot(xR,yR,label="HSR position by odometry")
    plt.plot(xH,yH,label="gravity zone of the human")
    np.savetxt(csv_result_path+"/csv/"+os.path.basename(csv_path[:-4])+"_results.csv",np.column_stack((xR,yR,xH,yH)),delimiter=",")

    if "_0_" not in os.path.basename(csv_path):
        calib_data=np.loadtxt(csv_result_path+"/csv/20230107_rotation_0_18_yoshinari_yoko_slow_results.csv",delimiter=",")
        err_th=np.arctan(np.average(calib_data[:,2]/1000)/np.average(calib_data[:,3]/1000))
        xH_clbd=xR+z*np.cos(thR+pan+err_th)+x*np.sin(thR+pan+err_th)
        yH_clbd=yR+z*np.sin(thR+pan+err_th)-x*np.cos(thR+pan+err_th)
        plt.plot(xH_clbd,yH_clbd,label="gravity zone of the human (calibrated)")


    # VICON data import

    

    xR_HSR=np.average(xR)
    yR_HSR=np.average(yR)
    xR_VCN=np.average()
    

    # plt.plot(t_img,x,label="x")
    # plt.plot(t_img,y,label="y")
    # plt.plot(t_img,z,label="z")
    # plt.plot(t_odm,xR,label="xR")
    # plt.plot(t_odm,yR,label="yR")
    # plt.plot(t_odm,thR,label="thR")
    # plt.plot(t_img,xH,label="xH")
    # plt.plot(t_img,yH,label="yH")
    # plt.plot(t_img,t_odm-t_img,label="time gap")
    # plt.plot([-2,7],[0,0],label="truth path of the human")
    plt.legend()
    plt.title(os.path.basename(csv_path[:-4]))
    plt.savefig(csv_result_path+"/graph/"+os.path.basename(csv_path[:-4])+".png")
    plt.cla()