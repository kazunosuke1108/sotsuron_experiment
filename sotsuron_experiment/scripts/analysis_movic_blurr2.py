import sys
import os
import time
import numpy as np
import cv2
import torch
import pandas as pd
from glob import glob
import matplotlib.pyplot as plt
from exp_commons import ExpCommons
from analysis_management import *
from detectron2_core import *
# sudo pip3 uninstall -y opencv-python && sudo apt update && sudo apt install -y libgtk2.0-dev pkg-config && sudo pip3 install opencv-python

path_management,csv_labels,color_dict=management_initial()
plt.rcParams["figure.figsize"] = (15,10)
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.family'] = 'Times New Roman'

images_dir_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/analysis/velocity_error/big_data/rgb_01x"
csv_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/analysis/velocity_error/_2023-12-21-10-22-39_laplacian_rgb_hmn_01x.csv"
png_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/analysis/velocity_error/_2023-12-21-10-22-39_laplacian_rgb_hmn_01x.png"

## ブレの定量化

images=sorted(glob(images_dir_path+"/*"))
print(images)
detector=Detector(model_type="KP")
for img_path in images:
    frame=cv2.imread(img_path)
    pred_keypoints=detector.onImage(image_mat=frame)
    try:
        np_pred_keypoints=pred_keypoints.to(torch.device('cpu')).detach().clone().numpy()[0]
    except IndexError:
        continue
    np_pred_keypoints=np_pred_keypoints.astype('int32')
    min_x=np.max([0,np.min(np_pred_keypoints[:,0])-20])
    min_y=np.max([0,np.min(np_pred_keypoints[:,1])-20])
    max_x=np.min([frame.shape[1],np.max(np_pred_keypoints[:,0])+20])
    max_y=np.min([frame.shape[0],np.max(np_pred_keypoints[:,1])+20])
    print(min_x,max_x,min_y,max_y)
    human_img=frame[min_y:max_y,min_x:max_x,:]
    cv2.imwrite(f"/home/hayashide/catkin_ws/src/sotsuron_experiment/analysis/velocity_error/big_data/hmn_01x/{os.path.basename(img_path)[:-4]}_hmn.jpg",human_img)
    gray = cv2.cvtColor(human_img, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    print(laplacian.var())
    ExpCommons.write_csvlog(ExpCommons,[float(os.path.basename(img_path)[:-4]),laplacian.var(),min_x,max_x,min_y,max_y],csv_path)
    key =cv2.waitKey(10)
    if key == 27:
        break

# ## ブレを描画
# csv_data=pd.read_csv(csv_path,names=["timestamp","laplacian","min_x","max_x","min_y","max_y"])
# print(csv_data)
# fig,ax1=plt.subplots()
# ax1.plot(csv_data["timestamp"].values,csv_data["laplacian"].values,label="Sharpness")
# ax1.set_xlabel("Time $\it{t}$ [s]")
# ax1.set_ylabel("Sharpness of the image using laplacian kernel")
# ax1.legend(loc="upper left")
# ax2=ax1.twinx()
# ax2.plot(csv_data["timestamp"].values,csv_data["max_x"].values-csv_data["min_x"].values,"r",marker="o",label="width of the image")
# ax2.plot(csv_data["timestamp"].values,csv_data["max_y"].values-csv_data["min_y"].values,"b",marker="o",label="height of the image")
# ax2.set_ylabel("size of the image [pixel]")
# ax2.legend(loc="upper right")
# plt.title(f"Sharpness of the image calculated by laplacian kernel ({os.path.basename(sys.argv[0])} _2023-12-21-10-22-39)")
# plt.savefig(png_path,dpi=500)