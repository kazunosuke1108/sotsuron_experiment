#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import subprocess as sp
from glob import glob

bags=sorted(glob("/media/hayashide/KIOXIA/hayashide/rosbag/0203/*"))
print(bags)

for bag in bags:#[12:]:
    print(bag)
    bag_basename=os.path.basename(bag)
    csv_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/results/0203/csv/"+bag_basename[:-4]+".csv"
    avi_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/results/0203/movie/"+bag_basename[:-4]+".avi"
    play_cmd=f"roslaunch sotsuron_experiment path_plotter.launch avi_basename:={bag_basename[:-4]} bag_basename:={bag_basename} bag_path:={bag} csv_path:={csv_path} save_path:={avi_path}"
    # runcmd=sp.call(cmd.split())
    # print(runcmd)
    os.system(play_cmd)
    graph_cmd="python3 path_plotter_14_7F.py"
    os.system(graph_cmd)
    mp4_cmd=f"python3 conv_avi_turn_mp4.py {avi_path}"
    os.system(mp4_cmd)


"""
rosbag play
path_subscriberでcsvに書き出す
path_plotterで保存
"""