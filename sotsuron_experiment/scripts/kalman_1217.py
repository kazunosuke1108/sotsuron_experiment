#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import numpy as np
import scipy as sp
from scipy import linalg
from control.matlab import lqr
import matplotlib.pyplot as plt

def kalman_filter(z,R,Q11,Q22,fps=15):
    po=z # position observed
    # 速度を求める
    dansage=np.insert(z[:-1],0,0)
    vo=z-dansage
    vo[0]=0
    # vectors_p=np.row_stack([po,vo])
    vectors_p=np.array(po)
    print(vectors_p.shape)

    A=np.array([[1,1/fps],[0,1]])
    B=np.array([[0],[1]])
    C=np.array([[1,0]])
    # G=np.array([[0],[1]])

    
    # システム（プロセス）雑音の分散
    # Q11=1 # 観測雑音の分散
    # Q22=1 # 観測雑音の分散
    Q=(Q11+Q22)/2 # 観測雑音の分散

    n_v=np.random.normal(
        loc   = 0,      # 平均
        scale = np.sqrt(R),      # 標準偏差
        size  = vectors_p.shape,# 出力配列のサイズ(タプルも可)
        )
    
    n_p=np.random.normal(
        loc   = 0,      # 平均
        scale = np.sqrt(Q),      # 標準偏差
        size  = vectors_p.shape,# 出力配列のサイズ(タプルも可)
        )


    Q=np.array([[Q11,0],[0,Q22]])

    K,S,E=lqr(A,B,Q,R)
    P=S
    print(P)
    M=P@C.T/(R+C@P@C.T)
    pHat_k_km1=np.array([[vectors_p[0]],[0]])
    print(P)
    print(M)
    estm_list=[]
    estm_list.append(pHat_k_km1)
    for vector_p in vectors_p[1:]: 
        pHat_k_k=pHat_k_km1+M@(vector_p-C@pHat_k_km1)
        pHat_kp1_k=A@pHat_k_k
        estm_list.append(pHat_kp1_k)
        pHat_k_km1=pHat_k_k
        pHat_k_k=pHat_kp1_k

    return np.array(estm_list)


speed="090"
csv_path=os.environ['HOME']+f"/catkin_ws/src/sotsuron_experiment/scripts/sources/track_results_1216_{speed}.csv"
png_path=os.environ['HOME']+f"/catkin_ws/src/sotsuron_experiment/scripts/sources/1216_{speed}_z_only_p.png"

try:
    data=np.loadtxt(csv_path,delimiter=",")
except OSError:
    csv_path=os.environ['HOME']+f"/kazu_ws/sotsuron_experiment/sotsuron_experiment/scripts/sources/track_results_1216_{speed}.csv"
    png_path=os.environ['HOME']+f"/kazu_ws/sotsuron_experiment/sotsuron_experment/scripts/sources/1216_{speed}_z_only_p.png"

    data=np.loadtxt(csv_path,delimiter=",")


t=data[:,0]
x=data[:,1]
y=data[:,2]
z=np.array(data[:,3])

for R in np.arange(1,100,5):
    for Q11 in np.arange(1,100,5):
        for Q22 in np.arange(1,100,5):
            print(R,Q11,Q22)
            estm_list=kalman_filter(z,R,Q11,Q22,fps=15)
            plt.plot(t,estm_list[:,0],linewidth=0.1)

# R=1
# Q11=100
# Q22=100
# estm_list=kalman_filter(z,R,Q11,Q22,fps=15)

# R=0.1
# Q11=1
# Q22=1
# estm_list=kalman_filter(z,R,Q11,Q22,fps=15)

# plt.plot(t,z,linewidth=1)
plt.legend()
plt.savefig(png_path)


