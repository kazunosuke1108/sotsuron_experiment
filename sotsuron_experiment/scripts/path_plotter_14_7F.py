#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from glob import glob
# csv_dir_path=os.environ['HOME']+"/catkin_ws/src/sotsuron_experiment/results/0108/csv"
csv_dir_path=os.environ['HOME']+"/catkin_ws/src/sotsuron_experiment/results/0214/csv"
odom_csv_dir_path=os.environ['HOME']+"/catkin_ws/src/sotsuron_experiment/results/0214/odom_csv"
csv_result_path=os.environ['HOME']+"/catkin_ws/src/sotsuron_experiment/results/0214/results"

csv_paths=sorted(glob(csv_dir_path+"/*"))
odom_csv_paths=sorted(glob(odom_csv_dir_path+"/*"))
# vcn_paths=sorted(glob(os.environ['HOME']+"/catkin_ws/src/sotsuron_experiment/gaits/vicon_processed/*"))
analysis=[]
for csv_path,odom_csv_path in zip(csv_paths,odom_csv_paths):
    data=np.loadtxt(csv_path,delimiter=",")
    odom_data=np.loadtxt(odom_csv_path,delimiter=",")
    # if "02" in csv_path:
    #     data=data[:254,:]  
    # if "03" in csv_path:
    #     data=data[:238,:]
    # if "06" in csv_path:
    #     data=data[:222,:]
    # if "13" in csv_path:
    #     data=data[:214,:]

    # if "16" in csv_path:
    #     data=data[:208,:]        
    # data=data[376:,:]


    t_img=data[:,0]
    x=data[:,1]/1000
    y=data[:,2]/1000
    z=data[:,3]/1000
    t_odm=data[:,5]
    xR=data[:,6]-data[0,6]#-2.880975666111003086e-01
    yR=data[:,7]-data[0,7]#-(-5.041865853597119612e-02)+0.5
    thR=data[:,8]-data[0,8]
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
    # for i,vcn_path in enumerate(vcn_paths):
    #     if os.path.basename(csv_path)[:-8] in os.path.basename(vcn_path):
    #         print(f"HSR data: {os.path.basename(csv_path)}")
    #         print(f"VCN data: {os.path.basename(vcn_path)}")
    #         vcn_data=np.genfromtxt(vcn_path,delimiter=",")[3:,:]
    #         break
    
    # try:
    #     vcn_data
    # except NameError:
    #     print(f"matching HSR <--> VICON failed: {os.path.basename(csv_path)}")
    #     continue

    # オドメトリ誤差の補償
    # init=vcn_data[0,:]
    # err_th0=np.average([
    #     np.arctan((init[6]-init[9])/(init[5]-init[8])),
    #     np.arctan((init[12]-init[15])/(init[11]-init[14])),
    #     np.arctan((init[18]-init[21])/(init[17]-init[20])),
    #     ])
    # err_th=np.arctan((vcn_data[:,6]-vcn_data[:,9])/(vcn_data[:,5]-vcn_data[:,8])),
    # vcn_th=np.average([
    #     np.arctan((vcn_data[:,6]-vcn_data[:,9])/(vcn_data[:,5]-vcn_data[:,8])),
    #     np.arctan((vcn_data[:,12]-vcn_data[:,15])/(vcn_data[:,11]-vcn_data[:,14])),
    #     np.arctan((vcn_data[:,18]-vcn_data[:,21])/(vcn_data[:,17]-vcn_data[:,20])),
    #     ],axis=0)
    # vcn_th=vcn_th+np.pi*(vcn_th<0)
    # print(min(vcn_th))
    # plt.plot(np.arange(0,len(vcn_th)),vcn_th)
    # plt.show()
    # plt.cla()
    # xH_odm_cps=xR+z*np.cos(thR+pan+err_th0)+x*np.sin(thR+pan+err_th0)
    # yH_odm_cps=yR+z*np.sin(thR+pan+err_th0)-x*np.cos(thR+pan+err_th0)


    xR_HSR=xR
    yR_HSR=yR

    xR_HSR_all=odom_data[:,0]-odom_data[0,0]
    yR_HSR_all=odom_data[:,1]-odom_data[0,1]

    distance=np.sqrt((xH-xR)**2+(yH-yR)**2)
    # flg=distance<6
    flg=distance<100
    observable_xR=xR_HSR*flg
    observable_yR=yR_HSR*flg
    flg=distance<6
    observable_xH=xH*flg
    observable_yH=yH*flg

    # dist_cam_marker=0.19
    # xR_VCN=-np.average([vcn_data[:,5],vcn_data[:,8],vcn_data[:,11],vcn_data[:,14],vcn_data[:,17],vcn_data[:,20]],axis=0)/1000
    # yR_VCN=-np.average([vcn_data[:,6],vcn_data[:,9],vcn_data[:,12],vcn_data[:,15],vcn_data[:,18],vcn_data[:,21]],axis=0)/1000
    # xR_VCN=dist_cam_marker*np.cos(vcn_th)-np.average([vcn_data[:,5],vcn_data[:,8],vcn_data[:,11],vcn_data[:,14],vcn_data[:,17],vcn_data[:,20]],axis=0)/1000
    # yR_VCN=dist_cam_marker*np.sin(vcn_th)-np.average([vcn_data[:,6],vcn_data[:,9],vcn_data[:,12],vcn_data[:,15],vcn_data[:,18],vcn_data[:,21]],axis=0)/1000

    # xH_VCN=-vcn_data[:,2]/1000
    # yH_VCN=-vcn_data[:,3]/1000

    # VICONの示すHSR位置をHSR座標系の原点にする
    # print(err_th0)
    # xH=xH+np.average(xR_VCN)
    # yH=yH+np.average(yR_VCN)
    # xH_odm_cps=xH_odm_cps+np.average(xR_VCN)
    # yH_odm_cps=yH_odm_cps+np.average(yR_VCN)

    # np.savetxt(csv_result_path+"/csv/"+os.path.basename(csv_path[:-8])+"_results_HSR.csv",np.column_stack((xH,yH,xH_odm_cps,yH_odm_cps)),delimiter=",")
    # np.savetxt(csv_result_path+"/csv/"+os.path.basename(csv_path[:-8])+"_results_VCN.csv",np.column_stack((xH_VCN,yH_VCN,xR_VCN,yR_VCN)),delimiter=",")

    # plt.scatter(xH_VCN,yH_VCN,label="VICON: human position",s=2,color="r")
    # plt.scatter(xR_HSR,yR_HSR,label="          \n           ",s=1,color="b")#,label="HSR: HSR position (whole)",s=1,color="k")
    plt.scatter(xR_HSR_all,yR_HSR_all,label="          \n           ",s=1,color="b")#,label="HSR: HSR position (whole)",s=1,color="k")
    # plt.scatter(observable_xR,observable_yR,label="HSR: HSR position (observing)",s=2,color="k")
    plt.scatter(observable_xH,observable_yH,label="          \n           ",s=1,color="r")#,label="HSR: human position (raw)",s=2,color="b")
    # plt.scatter(xH_odm_cps,yH_odm_cps,label="HSR: human position (odometry compensated)",s=2,color="g")
    # plt.scatter(xR_VCN,yR_VCN,label="VICON: HSR position",s=2,color="k")
    plt.xlabel("x (hallway direction) [m]")
    plt.ylabel("y (width direction) [m]")
    # plt.legend(loc='upper left')
    # plt.title(os.path.basename(csv_path[:-4]))
    # plt.ylim([0,3])
    # plt.xlim([-6,10])
    # plt.axis('equal')
    plt.axis([-6, 10, -1, 4]) # x軸、y軸のMin, Maxを指定
    plt.axes().set_aspect('equal')
    plt.savefig(csv_result_path+"/graph/path/"+os.path.basename(csv_path[:-8])+"_shrink.png",dpi=300)
    plt.cla()

    # xH, xH_odm_cps, xH_VCN
    # xH_m2t2,yH_m2t2=xH[xH>=-2],yH[xH>=-2]
    # xH_m2t2,yH_m2t2=xH_m2t2[xH_m2t2<=2],yH_m2t2[xH_m2t2<=2]
    # xH_odm_cps_m2t2,yH_odm_cps_m2t2=xH_odm_cps[xH_odm_cps>=-2],yH_odm_cps[xH_odm_cps>=-2]
    # xH_odm_cps_m2t2,yH_odm_cps_m2t2=xH_odm_cps_m2t2[xH_odm_cps_m2t2<=2],yH_odm_cps_m2t2[xH_odm_cps_m2t2<=2]
    # xH_VCN_m2t2,yH_VCN_m2t2=xH_VCN[xH_VCN>=-2],yH_VCN[xH_VCN>=-2]
    # xH_VCN_m2t2,yH_VCN_m2t2=xH_VCN_m2t2[xH_VCN_m2t2<=2],yH_VCN_m2t2[xH_VCN_m2t2<=2]
    # xR_VCN_m2t2,yR_VCN_m2t2=xR_VCN[xR_VCN>=-2],yR_VCN[xR_VCN>=-2]
    # xR_VCN_m2t2,yR_VCN_m2t2=xR_VCN_m2t2[xR_VCN_m2t2<=2],yR_VCN_m2t2[xR_VCN_m2t2<=2]
    # plt.hist(yH_VCN_m2t2,bins=80,density = True,label="VICON: truth",color="r",alpha=0.7)
    # plt.hist(yH_m2t2,bins=80,density = True,label="HSR: raw",color="b",alpha=0.7)
    # # plt.hist(yH_odm_cps_m2t2,bins=80,density = True,label="HSR: odometry compensated",color="g",alpha=0.7)
    # plt.xlabel("y (width direction) [m]")
    # plt.ylabel("abundance frequency (normalized)")
    # plt.title(os.path.basename(csv_path[:-4]))
    # plt.legend(loc="upper right")
    # plt.savefig(csv_result_path+"/graph/histgram/"+os.path.basename(csv_path[:-8])+"_histgram.png")
    # plt.cla()
    # print(xH_m2t2.shape)
    # print(xH_odm_cps_m2t2.shape)
    # np.savetxt(csv_result_path+"/csv/"+os.path.basename(csv_path[:-8])+"_results_raw_m2t2.csv",np.column_stack((xH_m2t2,yH_m2t2)),delimiter=",")
    # np.savetxt(csv_result_path+"/csv/"+os.path.basename(csv_path[:-8])+"_results_cps_m2t2.csv",np.column_stack((xH_odm_cps_m2t2,yH_odm_cps_m2t2)),delimiter=",")
    # np.savetxt(csv_result_path+"/csv/"+os.path.basename(csv_path[:-8])+"_results_VCN_m2t2.csv",np.column_stack((xH_VCN_m2t2,yH_VCN_m2t2)),delimiter=",")

    # plt.scatter(xH_VCN_m2t2,yH_VCN_m2t2,label="VICON: human position",s=2,color="r")
    # plt.scatter(xH_m2t2,yH_m2t2,label="HSR: human position (raw)",s=2,color="b")
    # plt.scatter(xH_odm_cps_m2t2,yH_odm_cps_m2t2,label="HSR: human position (odometry compensated)",s=2,color="g")
    # plt.scatter(xR_VCN,yR_VCN,label="VICON: HSR position",s=2,color="k")
    # plt.xlabel("x (hallway direction) [m]")
    # plt.ylabel("y (width direction) [m]")
    # plt.legend(loc='lower left')
    # plt.title(os.path.basename(csv_path[:-4]))
    # plt.xlim([-3,3])
    # plt.savefig(csv_result_path+"/graph/path_m2t2/"+os.path.basename(csv_path[:-8])+"_m2t2.png",dpi=300)
    # plt.cla()



    # try:
    #     print(os.path.basename(csv_path))
    #     anl=[int(os.path.basename(csv_path)[-10:-8]),np.mean(xH_m2t2),np.mean(yH_m2t2),np.mean(xH_odm_cps_m2t2),np.mean(yH_odm_cps_m2t2),np.mean(xH_VCN_m2t2),np.mean(yH_VCN_m2t2),np.std(xH_m2t2),np.std(yH_m2t2),np.std(xH_odm_cps_m2t2),np.std(yH_odm_cps_m2t2),np.std(xH_VCN_m2t2),np.std(yH_VCN_m2t2),sp.stats.skew(xH_m2t2),sp.stats.skew(yH_m2t2),sp.stats.skew(xH_odm_cps_m2t2),sp.stats.skew(yH_odm_cps_m2t2),sp.stats.skew(xH_VCN_m2t2),sp.stats.skew(yH_VCN_m2t2),sp.stats.kurtosis(xH_m2t2),sp.stats.kurtosis(yH_m2t2),sp.stats.kurtosis(xH_odm_cps_m2t2),sp.stats.kurtosis(yH_odm_cps_m2t2),sp.stats.kurtosis(xH_VCN_m2t2),sp.stats.kurtosis(yH_VCN_m2t2)]
    #     analysis.append(anl)
    #     np.savetxt(csv_result_path+"/csv/"+"analysis.csv",analysis,delimiter=",")
    # except (TypeError,ValueError):
    #     anl=[0,np.mean(xH_m2t2),np.mean(yH_m2t2),np.mean(xH_odm_cps_m2t2),np.mean(yH_odm_cps_m2t2),np.mean(xH_VCN_m2t2),np.mean(yH_VCN_m2t2),np.std(xH_m2t2),np.std(yH_m2t2),np.std(xH_odm_cps_m2t2),np.std(yH_odm_cps_m2t2),np.std(xH_VCN_m2t2),np.std(yH_VCN_m2t2),sp.stats.skew(xH_m2t2),sp.stats.skew(yH_m2t2),sp.stats.skew(xH_odm_cps_m2t2),sp.stats.skew(yH_odm_cps_m2t2),sp.stats.skew(xH_VCN_m2t2),sp.stats.skew(yH_VCN_m2t2),sp.stats.kurtosis(xH_m2t2),sp.stats.kurtosis(yH_m2t2),sp.stats.kurtosis(xH_odm_cps_m2t2),sp.stats.kurtosis(yH_odm_cps_m2t2),sp.stats.kurtosis(xH_VCN_m2t2),sp.stats.kurtosis(yH_VCN_m2t2)]
    #     analysis.append(anl)
    #     np.savetxt(csv_result_path+"/csv/"+"analysis.csv",analysis,delimiter=",")