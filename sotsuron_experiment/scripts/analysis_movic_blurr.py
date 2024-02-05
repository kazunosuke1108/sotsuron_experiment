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

mp4_path='/home/hayashide/catkin_ws/src/sotsuron_experiment/analysis/velocity_error/_2023-12-21-10-22-39_turn.mp4'
images_dir_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/analysis/velocity_error/big_data"
csv_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/analysis/velocity_error/bure.csv"
png_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/analysis/velocity_error/bure.png"

## ブレの定量化

cap=cv2.VideoCapture(mp4_path)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
# fourcc = cv2.VideoWriter_fourcc('m','p','4', 'v')
# writer = cv2.VideoWriter(skeletonVideoPaths[i],fourcc, fps, (width, height))
# detector=Detector(model_type="KP")
print(width)
print(height)
print(fps)
totalframecount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
for i in range(totalframecount):
    start=time.time()
    ret,frame=cap.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("source",frame)
        # cv2.imwrite(images_dir_path+"/"+str(i).zfill(5)+".jpg",frame)
        
        laplacian = cv2.Laplacian(gray, cv2.CV_64F) #ラプラシアン値
        ExpCommons.write_csvlog(ExpCommons,[i,laplacian.var()],csv_path)

        # print("laplacian.var()の値は？",laplacian.var())
        # [pred_keypoints,output_img]=detector.onImage(image_mat=frame,return_skeleton=True)
        # cv2.imshow("result",output_img)
        # writer.write(output_img)

    key =cv2.waitKey(10)
    if key == 27:
        break
    print(time.time()-start)
# writer.release()
cap.release()

## ブレを描画
csv_data=pd.read_csv(csv_path,names=["frame","laplacian"])
print(csv_data)
plt.plot(csv_data["laplacian"])
plt.savefig(png_path,dpi=500)