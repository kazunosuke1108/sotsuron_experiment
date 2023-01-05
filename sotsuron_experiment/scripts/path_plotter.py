#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib.pyplot as plt

csv_path=os.environ['HOME']+"/catkin_ws/src/sotsuron_experiment/gaits/test1734.csv"
data=np.loadtxt(csv_path,delimiter=",")

t_img=data[:,0]
x=data[:,1]
y=data[:,2]
z=data[:,3]
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

plt.plot(xR,yR)
plt.plot(xH,yH)

plt.legend()
plt.show()