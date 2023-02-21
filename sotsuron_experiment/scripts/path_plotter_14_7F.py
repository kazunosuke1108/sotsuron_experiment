#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from glob import glob
# csv_dir_path=os.environ['HOME']+"/catkin_ws/src/sotsuron_experiment/results/0108/csv"

csv_dir_path=os.environ['HOME']+"/catkin_ws/src/sotsuron_experiment/results/0220/csv"
odom_csv_dir_path=os.environ['HOME']+"/catkin_ws/src/sotsuron_experiment/results/0220/odom_csv"
csv_result_path=os.environ['HOME']+"/catkin_ws/src/sotsuron_experiment/results/0220/results"

csv_paths=sorted(glob(csv_dir_path+"/*"))
odom_csv_paths=sorted(glob(odom_csv_dir_path+"/*"))

print(csv_paths)
print(odom_csv_paths)
# odom_csvの修正
# zero_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/scripts/sources/odom_zero.csv"

# zero_data=np.loadtxt(zero_path,delimiter=",")
# for csv_path,odom_csv_path in zip(csv_paths,odom_csv_paths):
#     data=np.loadtxt(odom_csv_path,delimiter=",")
#     data[:,0]+=np.average(zero_data[:,0])*2
#     data[:,1]+=np.average(zero_data[:,1])*2
#     data[:,2]+=np.average(zero_data[:,2])*2
#     np.savetxt(odom_csv_path,data,delimiter=",")


# vcn_paths=sorted(glob(os.environ['HOME']+"/catkin_ws/src/sotsuron_experiment/gaits/vicon_processed/*"))
analysis=[]
for csv_path,odom_csv_path in zip(csv_paths,odom_csv_paths):
    data=np.loadtxt(csv_path,delimiter=",")
    odom_data=np.loadtxt(odom_csv_path,delimiter=",")
    # hayashide
    # if "_02_" in csv_path:
    #     data=data[:-115,:]  
    # if "_03_" in csv_path:
    #     data=data[:862,:]  
    # if "_04_" in csv_path:
    #     data=data[:827,:]
    # if "_06_" in csv_path:
    #     data=data[:785,:]
    # if "_07_" in csv_path:
    #     data=data[:670,:]        
    # if "_08_" in csv_path:
    #     data=data[:750,:]
    # if "_09_" in csv_path:
    #     data=data[:572,:]
    # if "03" in csv_path:
    #     data=data[:238,:]
    # if "06" in csv_path:
    #     data=data[:222,:]
    # if "13" in csv_path:
    #     data=data[:214,:]
    # if "16" in csv_path:
    #     data=data[:208,:]        
    # data=data[376:,:]
    shingo
    if "30" in csv_path:
        data=data[:490,:]



    t_img=data[:,0]
    x=data[:,1]/1000
    y=data[:,2]/1000
    z=data[:,3]/1000
    t_odm=data[:,5]
    xR=data[:,6]-data[0,6]
    yR=data[:,7]-data[0,7]-np.average(data[295:300,7])+1##
    # xR=data[:,6]-odom_data[0,0]#-2.880975666111003086e-01
    # yR=data[:,7]-odom_data[0,1]#-(-5.041865853597119612e-02)+0.5
    thR=data[:,8]-data[0,8]
    pan=data[:,9]-data[0,9]

    xH=xR+z*np.cos(thR+pan)+x*np.sin(thR+pan)
    yH=yR+z*np.sin(thR+pan)-x*np.cos(thR+pan)
    print(csv_path)

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

    
    if "30" in csv_path:
        observable_xH=observable_xH[30:]
        observable_yH=observable_yH[30:]
    
    # plt.scatter(xR_HSR,yR_HSR,label="          \n           ",s=1,color="k")#,label="HSR: HSR position (whole)",s=1,color="k")
    plt.scatter(xR_HSR_all,yR_HSR_all,label="          \n           ",s=0.5,color="b")#,label="HSR: HSR position (whole)",s=1,color="k")
    plt.scatter(observable_xH,observable_yH,label="          \n           ",s=2,color="r")#,label="HSR: human position (raw)",s=2,color="b")
    plt.xlabel("x (hallway direction) [m]")
    plt.ylabel("y (width direction) [m]")
    plt.axis([-1, 11, -0.5, 3.5]) # x軸、y軸のMin, Maxを指定
    plt.axes().set_aspect('equal')
    plt.savefig(csv_result_path+"/graph/path/"+os.path.basename(csv_path[:-8])+"_shrink.png",dpi=300)
    plt.cla()