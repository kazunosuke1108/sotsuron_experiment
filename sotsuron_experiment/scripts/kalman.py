#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import numpy as np
import scipy as sp
from scipy import linalg
import matplotlib.pyplot as plt

def kalman_filter(z,fps=15):
    po=z # position observed
    # 速度を求める
    dansage=np.insert(z[:-1],0,0)
    vo=z-dansage
    vo[0]=0
    vectors_p=np.column_stack([po,vo])
    print(vectors_p.shape)

    A=np.array([[1,1/fps],[0,1]])
    B=np.array([[0],[1]])
    C=np.array([[1,0],[0,1]])
    # G=np.array([[0],[1]])

    
    R=1 # システム（プロセス）雑音の分散
    Q=1 # 観測雑音の分散

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

    print(n_v[0]@n_v[0])
    print(n_v[0]@n_v[1])
    print(n_v[1]@n_v[1])

    Q=np.array([[1,0],[0,1]])

    P=sp.linalg.solve_continuous_are(A,B,Q,R)
    print(P)
    M=P@C.T@np.linalg.pinv(R+C@P@C.T)
    print(M)
    pHat_k_km1=vectors_p[0]

    estm_list=[]
    estm_list.append(pHat_k_km1)
    for vector_p in vectors_p[1:]: 
        pHat_k_k=pHat_k_km1+M@(vector_p-C@pHat_k_km1)
        pHat_Kp1_k=A@pHat_k_k
        estm_list.append(pHat_Kp1_k)

    return np.array(estm_list)


speed="090"
csv_path=os.environ['HOME']+f"/catkin_ws/src/sotsuron_experiment/scripts/sources/track_results_1216_{speed}.csv"
png_path=os.environ['HOME']+f"/catkin_ws/src/sotsuron_experiment/scripts/sources/1216_{speed}_z.png"

try:
    data=np.loadtxt(csv_path,delimiter=",")
except OSError:
    csv_path=os.environ['HOME']+f"/kazu_ws/sotsuron_experiment/sotsuron_experiment/scripts/sources/track_results_1216_{speed}.csv"
    png_path=os.environ['HOME']+f"/kazu_ws/sotsuron_experiment/sotsuron_experiment/scripts/sources/1216_{speed}_z.png"
    data=np.loadtxt(csv_path,delimiter=",")


t=data[:,0]
x=data[:,1]
y=data[:,2]
z=np.array(data[:,3])

plt.plot(t,z,label=f"{speed}z_raw")

estm_list=kalman_filter(z,fps=15)

plt.plot(t,estm_list[:,0],label=f"{speed}z_kalman")

plt.legend()
plt.savefig(png_path)

