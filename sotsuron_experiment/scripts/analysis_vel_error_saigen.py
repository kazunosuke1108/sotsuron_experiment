import numpy as np
import matplotlib.pyplot as plt

hz_Odom=24
hz_Pose=3
interp_ratio=int(hz_Odom/hz_Pose)
t_H=np.arange(0,10,1/hz_Pose)
t_Odom=np.arange(0,10,1/hz_Odom)
start_Odom=10
start_Pose=int(10/hz_Odom*hz_Pose)
vR=0.8
vH=-1.2

xR=np.zeros_like(t_Odom)
xR[start_Odom:]=vR*(t_Odom[start_Odom:]-t_Odom[start_Odom])
xRH=np.full_like(t_H,5)
xRH[start_Pose:]+=vH*(t_H[start_Pose:]-t_H[start_Pose])
xRH_interp=[]
for xRH_val in xRH:
    for i in range(interp_ratio):
        xRH_interp.append(xRH_val)
xH=xR+xRH_interp
print("xR",xR)
print("xH",xH)
print("xRH",xRH)
print("xRH_interp",xRH_interp)

plt.plot(t_Odom,xR,"o-",label="xR")
plt.plot(t_Odom,xH,"o-",label="xH")
# plt.plot(t_Odom,xRH_interp,"o-",label="xRH_interp")
plt.show()