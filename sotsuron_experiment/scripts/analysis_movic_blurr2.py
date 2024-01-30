import sys
import os
import time
import cv2
import pandas as pd
from glob import glob
import matplotlib.pyplot as plt
from exp_commons import ExpCommons
from analysis_management import *
path_management,csv_labels,color_dict=management_initial()
plt.rcParams["figure.figsize"] = (15,10)
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.family'] = 'Times New Roman'

images_dir_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/analysis/velocity_error/big_data/rgb"
csv_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/analysis/velocity_error/_2023-12-21-10-22-39_laplacian_rgb.csv"
png_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/analysis/velocity_error/_2023-12-21-10-22-39_laplacian_rgb.png"

## ブレの定量化

images=sorted(glob(images_dir_path+"/*"))
print(images)
for img_path in images:
    frame=cv2.imread(img_path)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    print(float(os.path.basename(img_path)[:-4]))
    ExpCommons.write_csvlog(ExpCommons,[float(os.path.basename(img_path)[:-4]),laplacian.var()],csv_path)
    key =cv2.waitKey(10)
    if key == 27:
        break

# ## ブレを描画
csv_data=pd.read_csv(csv_path,names=["timestamp","laplacian"])
print(csv_data)
plt.plot(csv_data["timestamp"].values,csv_data["laplacian"].values,label="Sharpness")
plt.xlabel("Time $\it{t}$ [s]")
plt.ylabel("Sharpness of the image using laplacian kernel")
plt.legend()
plt.title(f"Sharpness of the image calculated by laplacian kernel ({os.path.basename(sys.argv[0])} _2023-12-21-10-22-39)")
plt.savefig(png_path,dpi=500)