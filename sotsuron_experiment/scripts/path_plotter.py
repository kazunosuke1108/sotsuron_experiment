#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib.pyplot as plt

csv_path=os.environ['HOME']+"/catkin_ws/src/sotsuron_experiment/gaits/0105_cover.csv"
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

# plt.plot(t_img,x,label="x")
# plt.plot(t_img,y,label="y")
# plt.plot(t_img,z,label="z")
# plt.plot(t_odm,xR,label="xR")
# plt.plot(t_odm,yR,label="yR")
# plt.plot(t_odm,thR,label="thR")
# plt.plot(t_img,xH,label="xH")
# plt.plot(t_img,yH,label="yH")
# plt.plot(t_img,t_odm-t_img,label="time gap")

plt.plot(xR,yR,label="HSR position by odometry")
plt.plot(xH,yH,label="gravity zone of the human")
plt.plot([-2,7],[0,0],label="truth path of the human")
plt.legend()
plt.show()