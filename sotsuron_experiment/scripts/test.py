import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
np_pred_keypoints=np.array(
    [[340,603,0],
    [349,595,1],
    [330,595,1],
    [356,610,1],
    [310,604,0],
    [362,657,0],
    [290,639,0],
    [410,701,1],
    [270,583,0],
    [441,756,1],
    [282,552,0],
    [344,753,0],
    [278,746,0],
    [397,816,0],
    [219,826,0],
    [409,970,0],
    [158,952,0]]
)
after_kp=np.zeros_like(np_pred_keypoints)
after_kp[:,1]=np_pred_keypoints[:,0]
after_kp[:,0]=1280-np_pred_keypoints[:,1]
# after_kp=np.array(
#     [[ 900,380,0],
#  [ 909,371,1],
#  [ 890,390,1],
#  [ 916,364,1],
#  [ 870,410,0],
#  [ 922,358,0],
#  [ 850,430,0],
#  [ 970,310,1],
#  [ 830,450,0],
#  [100,279,1],
#  [ 842,438,0],
#  [ 904,376,0],
#  [ 838,442,0],
#  [ 957,323,0],
#  [ 779,501,0],
#  [ 969,311,0],
#  [ 718,562,0],]
# )
print(np_pred_keypoints)
print(after_kp)
fig, ax = plt.subplots()
ax.invert_yaxis()
# ax.invert_xaxis()
ax.set_aspect('equal', 'box')
ax.scatter(np_pred_keypoints[:,0],np_pred_keypoints[:,1],color="b")
ax.scatter(after_kp[:,0],after_kp[:,1],color="r")
print(after_kp[:,0])
plt.show()