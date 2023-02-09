import os
import sys
import cv2
import time
from glob import glob

videos=sorted(glob("/home/hayashide/catkin_ws/src/sotsuron_experiment/results/0203/movie/*"))
try:
    avi_path=sys.argv[1]
except Exception:
    avi_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/results/0203/movie/"

for videoPath in videos:
    video_basename=os.path.basename(videoPath)
    print("now processing:",video_basename)
    if video_basename[-4:]==".avi":
        cap=cv2.VideoCapture(videoPath)
        ret,frame=cap.read()
        fourcc = cv2.VideoWriter_fourcc('m','p','4', 'v')
        size=(frame.shape[1],frame.shape[0])
        video=cv2.VideoWriter(avi_path+video_basename[:-4]+".mp4",fourcc, 15.0,size)
        if cap.isOpened():
            while True:
                if ret:
                    # frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
                    video.write(frame)
                    print("added a frame at:",time.time(),"frame shape:",(frame.shape[0],frame.shape[1]))
                else:
                    break
                ret,frame=cap.read()
        video.release()
        del video
        del cap
        del fourcc