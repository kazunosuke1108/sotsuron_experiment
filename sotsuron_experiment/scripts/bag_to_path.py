#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import subprocess as sp
from glob import glob

# bags=sorted(glob("/media/hayashide/KIOXIA/hayashide/rosbag/0203/*"))
# bags=sorted(glob("/home/hayashide/catkin_ws/src/ytlab_hsr/ytlab_hsr_modules/rosbag/EtoE/*"))
bags=sorted(glob("/media/hayashide/KIOXIA/hayashide/rosbag/0214/*"))
print(bags)

partial_bags=[]
for bag in bags:
<<<<<<< HEAD
    if "_02_" in bag:
=======
    if "_06_" in bag:
>>>>>>> e2ee629c0c5d6387edd7609cdaaee2caae4a6f2b
        partial_bags.append(bag)

for bag in partial_bags:
# for bag in bags:
    print(bag)
    bag_basename=os.path.basename(bag)
    csv_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/results/0214/csv/"+bag_basename[:-4]+".csv"
    odom_csv_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/results/0214/odom_csv/"+bag_basename[:-4]+".csv"
    avi_dir_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/results/0214/movie/"
    avi_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/results/0214/movie/"+bag_basename[:-4]+".avi"
    play_cmd=f"roslaunch sotsuron_experiment path_plotter.launch avi_basename:={bag_basename[:-4]} bag_basename:={bag_basename} bag_path:={bag} csv_path:={csv_path} odom_csv_path:={odom_csv_path} save_path:={avi_path}"
    # runcmd=sp.call(cmd.split())
    # print(runcmd)
    os.system(play_cmd)
    
    graph_cmd="python3 path_plotter_14_7F.py"
    os.system(graph_cmd)

    mp4_cmd=f"python3 conv_avi_turn_mp4.py {avi_dir_path}"
    # os.system(mp4_cmd)


"""
rosbag play
path_subscriberでcsvに書き出す
path_plotterで保存
"""