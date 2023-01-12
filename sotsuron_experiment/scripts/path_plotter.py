#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
# csv_dir_path=os.environ['HOME']+"/catkin_ws/src/sotsuron_experiment/results/0108/csv"
csv_dir_path=os.environ['HOME']+"/catkin_ws/src/sotsuron_experiment/results/0108/csv/renamed"
csv_result_path=os.environ['HOME']+"/catkin_ws/src/sotsuron_experiment/results/0108/results"

csv_paths=sorted(glob(csv_dir_path+"/*"))
vcn_paths=sorted(glob(os.environ['HOME']+"/catkin_ws/src/sotsuron_experiment/gaits/vicon_processed/*"))

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
    # xH=z*np.cos(thR+pan)+x*np.sin(thR+pan)
    # yH=z*np.sin(thR+pan)-x*np.cos(thR+pan)

    # if "_0_" not in os.path.basename(csv_path):
    # calib_data=np.loadtxt(csv_result_path+"/csv/walk18_results.csv",delimiter=",")
    # err_th0=np.arctan(np.average(calib_data[:,2]/1000)/np.average(calib_data[:,3]/1000))
    # xH=xR+z*np.cos(thR+pan+err_th0)+x*np.sin(thR+pan+err_th0)
    # yH=yR+z*np.sin(thR+pan+err_th0)-x*np.cos(thR+pan+err_th0)
        # plt.plot(xH_clbd,yH_clbd,label="gravity zone of the human (calibrated)")



    # VICON data import
    for i,vcn_path in enumerate(vcn_paths):
        if os.path.basename(csv_path)[:-8] in os.path.basename(vcn_path):
            print(f"HSR data: {os.path.basename(csv_path)}")
            print(f"VCN data: {os.path.basename(vcn_path)}")
            vcn_data=np.genfromtxt(vcn_path,delimiter=",")[3:,:]
            break
    
    try:
        vcn_data
    except NameError:
        print(f"matching HSR <--> VICON failed: {os.path.basename(csv_path)}")
        continue

    # オドメトリ誤差の補償
    init=vcn_data[0,:]
    err_th0=np.average([
        np.arctan((init[6]-init[9])/(init[5]-init[8])),
        np.arctan((init[12]-init[15])/(init[11]-init[14])),
        np.arctan((init[18]-init[21])/(init[17]-init[20])),
        ])
    # err_th=np.arctan((vcn_data[:,6]-vcn_data[:,9])/(vcn_data[:,5]-vcn_data[:,8])),
    vcn_th=np.average([
        np.arctan((vcn_data[:,6]-vcn_data[:,9])/(vcn_data[:,5]-vcn_data[:,8])),
        np.arctan((vcn_data[:,12]-vcn_data[:,15])/(vcn_data[:,11]-vcn_data[:,14])),
        np.arctan((vcn_data[:,18]-vcn_data[:,21])/(vcn_data[:,17]-vcn_data[:,20])),
        ],axis=0)
    vcn_th=vcn_th+np.pi*(vcn_th<0)
    # print(min(vcn_th))
    # plt.plot(np.arange(0,len(vcn_th)),vcn_th)
    # plt.show()
    # plt.cla()
    xH_odm_cps=xR+z*np.cos(thR+pan+err_th0)+x*np.sin(thR+pan+err_th0)
    yH_odm_cps=yR+z*np.sin(thR+pan+err_th0)-x*np.cos(thR+pan+err_th0)

    xR_HSR=xR
    yR_HSR=yR
    dist_cam_marker=0.19
    xR_VCN=-np.average([vcn_data[:,5],vcn_data[:,8],vcn_data[:,11],vcn_data[:,14],vcn_data[:,17],vcn_data[:,20]],axis=0)/1000
    yR_VCN=-np.average([vcn_data[:,6],vcn_data[:,9],vcn_data[:,12],vcn_data[:,15],vcn_data[:,18],vcn_data[:,21]],axis=0)/1000
    xR_VCN=dist_cam_marker*np.cos(vcn_th)-np.average([vcn_data[:,5],vcn_data[:,8],vcn_data[:,11],vcn_data[:,14],vcn_data[:,17],vcn_data[:,20]],axis=0)/1000
    yR_VCN=dist_cam_marker*np.sin(vcn_th)-np.average([vcn_data[:,6],vcn_data[:,9],vcn_data[:,12],vcn_data[:,15],vcn_data[:,18],vcn_data[:,21]],axis=0)/1000

    xH_VCN=-vcn_data[:,2]/1000
    yH_VCN=-vcn_data[:,3]/1000

    # VICONの示すHSR位置をHSR座標系の原点にする
    # print(err_th0)
    xH=xH+np.average(xR_VCN)
    yH=yH+np.average(yR_VCN)
    xH_odm_cps=xH_odm_cps+np.average(xR_VCN)
    yH_odm_cps=yH_odm_cps+np.average(yR_VCN)


    plt.scatter(xR_VCN,yR_VCN,label="HSR position seen from VICON",s=2)
    plt.scatter(xH,yH,label="human estimated by HSR (raw)",s=2)
    plt.scatter(xH_odm_cps,yH_odm_cps,label="human estimated by HSR (odometry compensated)",s=2)
    plt.scatter(xH_VCN,yH_VCN,label="gravity zone of the human estimated by VICON",s=2)

    if "18" not in csv_path:
        np.savetxt(csv_result_path+"/csv/"+os.path.basename(csv_path[:-8])+"_results.csv",np.column_stack((xR,yR,xH,yH)),delimiter=",")


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
    # plt.xlim([-3,3])
    plt.savefig(csv_result_path+"/graph/"+os.path.basename(csv_path[:-8])+".png",dpi=300)
    plt.cla()

    # xH, xH_odm_cps, xH_VCN
    xH_m2t2,yH_m2t2=xH[xH>=-2],yH[xH>=-2]
    xH_m2t2,yH_m2t2=xH_m2t2[xH_m2t2<=2],yH_m2t2[xH_m2t2<=2]
    xH_odm_cps_m2t2,yH_odm_cps_m2t2=xH_odm_cps[xH_odm_cps>=-2],yH_odm_cps[xH_odm_cps>=-2]
    xH_odm_cps_m2t2,yH_odm_cps_m2t2=xH_odm_cps_m2t2[xH_odm_cps_m2t2<=2],yH_odm_cps_m2t2[xH_odm_cps_m2t2<=2]
    xH_VCN_m2t2,yH_VCN_m2t2=xH_VCN[xH_VCN>=-2],yH_VCN[xH_VCN>=-2]
    xH_VCN_m2t2,yH_VCN_m2t2=xH_VCN_m2t2[xH_VCN_m2t2<=2],yH_VCN_m2t2[xH_VCN_m2t2<=2]
    plt.hist(yH_m2t2,bins=80,density = True,label="raw",color="r")
    plt.hist(yH_odm_cps_m2t2,bins=80,density = True,label="odometry compensated",color="g")
    plt.hist(yH_VCN_m2t2,bins=80,density = True,label="VICON",color="b")
    plt.legend()
    plt.savefig(csv_result_path+"/graph/"+os.path.basename(csv_path[:-8])+"_histgram.png")
    plt.cla()