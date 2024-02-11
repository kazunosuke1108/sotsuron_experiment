<<<<<<< HEAD
import time
from detectron2_core import *
import cv2

img_path="000000000785.jpg"
for i in range(10):
    start=time.time()
    img=cv2.imread(img_path)
    detector=Detector(model_type="KP")
    pred_keypoints_t=detector.onImage(image_mat=img)
    print("######################################",time.time()-start)
=======
import numpy as np
import pandas as pd

data=pd.read_csv("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/20231220_VICON/mahi12.csv",header=None)
data=data.iloc[:3]

for column in data.columns:
    data[column].iat[2]=str(data[column].iat[0])+"_"+str(data[column].iat[1])
print(data)

data_out=data.iloc[2]
print(data_out)
data_out.to_csv("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/20231220_VICON/prefix_mahi12.csv")
>>>>>>> 49dde8d1dfbb3ab150cff7f4692fe72c780bf7ba
