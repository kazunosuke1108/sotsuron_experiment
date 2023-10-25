from glob import glob
from pprint import pprint
import os
import subprocess
# from git_auto_push import git_auto_push
import time

# # bag -> avi
# bags=sorted(glob("/home/hayashide/catkin_ws/media/hayashide/KIOXIA/hayashide/rosbag/20231019*/*"))+sorted(glob("/home/hayashide/catkin_ws/media/hayashide/KIOXIA/hayashide/rosbag/2023102*/*"))
# pprint(bags)
avi_dir_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/videos/avi"
# for bag in bags:
#     save_path=avi_dir_path+"/"+os.path.basename(bag)[:-4]+".avi"
#     if os.path.exists(save_path):
#         print(f"Exsit: {save_path}")
#         continue
#     print(save_path)
#     launch_command = f"roslaunch sotsuron_experiment conv_bag_to_avi.launch bag_path:={bag} save_path:={save_path}"
#     subprocess.run(launch_command, shell=True, check=True)


# # avi -> mp4
import cv2

mp4_dir_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/videos/mp4"
# avi_videos=sorted(glob(avi_dir_path+"/*"))
# for videoPath in avi_videos:
#     video_basename=os.path.basename(videoPath)
#     mp4_save_path=mp4_dir_path+"/"+video_basename[:-4]+".mp4"
#     if os.path.exists(mp4_save_path):
#         print(f"Exsit: {mp4_save_path}")
#         continue
#     print("now processing:",videoPath)
#     if video_basename[-4:]==".avi":
#         cap=cv2.VideoCapture(videoPath)
#         ret,frame=cap.read()
#         fourcc = cv2.VideoWriter_fourcc('m','p','4', 'v')
#         size=(frame.shape[1],frame.shape[0])
#         video=cv2.VideoWriter(mp4_save_path,fourcc, 6.0,size)
#         if cap.isOpened():
#             while True:
#                 if ret:
#                     # frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
#                     video.write(frame)
#                 else:
#                     break
#                 ret,frame=cap.read()
#         video.release()
#         del video
#         del cap
#         del fourcc

# mp4 -> skeleton
from detectron2_core import *

mp4_videos=sorted(glob(mp4_dir_path+"/*"))
# mp4_videos=sorted(glob(mp4_dir_path+"/03*"))
skeleton_dir_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/videos/skeleton"
for i, videoPath in enumerate(mp4_videos):
    video_basename=os.path.basename(videoPath)
    skeleton_save_path=skeleton_dir_path+"/"+video_basename[:-4]+"_skeleton.mp4"
    if os.path.exists(skeleton_save_path):
        print(f"Exsit: {skeleton_save_path}")
        continue
    print("now processing:",skeleton_save_path)
    cap=cv2.VideoCapture(videoPath)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc('m','p','4', 'v')
    writer = cv2.VideoWriter(skeleton_save_path,fourcc, fps, (width, height))
    detector=Detector(model_type="KP")

    totalframecount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    for i in range(totalframecount):
        print(videoPath,i)
        ret,frame=cap.read()
        if ret:
            cv2.imshow("source",frame)
            [pred_keypoints,output_img]=detector.onImage(image_mat=frame,return_skeleton=True)
            cv2.imshow("result",output_img)
            writer.write(output_img)


    writer.release()
    cap.release()
    cv2.destroyAllWindows()

    """
    SOTSURON EXP hayashide:~/catkin_ws/src/sotsuron_experiment/scripts$ python3 analysis_video.py 
model_final_a6e10b.pkl: 237MB [00:02, 108MB/s]                                  
Traceback (most recent call last):
  File "analysis_video.py", line 65, in <module>
    cv2.imshow("source",frame)
cv2.error: OpenCV(4.8.0) /io/opencv/modules/highgui/src/window.cpp:1272: error: (-2:Unspecified error) The function is not implemented. Rebuild the library with Windows, GTK+ 2.x or Cocoa support. If you are on Ubuntu or Debian, install libgtk2.0-dev and pkg-config, then re-run cmake or configure script in function 'cvShowImage'
"""