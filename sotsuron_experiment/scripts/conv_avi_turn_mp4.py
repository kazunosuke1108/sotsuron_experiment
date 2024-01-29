import os
import sys
import cv2
import time
from glob import glob

# videos=sorted(glob("/home/hayashide/catkin_ws/src/sotsuron_experiment/results/20230605/movie/*"))
try:
    avi_path=sys.argv[1]
except Exception:
    avi_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/analysis/velocity_error/_2023-12-21-10-22-39.mp4"
videos=[avi_path]

for videoPath in videos:
    video_basename=os.path.basename(videoPath)
    print("now processing:",video_basename)
    # if video_basename[-4:]==".avi":
    cap=cv2.VideoCapture(videoPath)
    ret,frame=cap.read()
    fourcc = cv2.VideoWriter_fourcc('m','p','4', 'v')
    print(frame)
    size=(frame.shape[0],frame.shape[1])
    # size=(frame.shape[1],frame.shape[0])
    video=cv2.VideoWriter(videoPath[:-4]+"_turn.mp4",fourcc, 30.0,size)
    if cap.isOpened():
        while True:
            if ret:
                frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
                video.write(frame)
                print("added a frame at:",time.time(),"frame shape:",(frame.shape[0],frame.shape[1]))
            else:
                break
            ret,frame=cap.read()
    video.release()
    del video
    del cap
    del fourcc