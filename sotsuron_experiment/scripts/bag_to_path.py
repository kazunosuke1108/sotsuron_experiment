#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import subprocess as sp
from glob import glob

bags=sorted(glob("/media/hayashide/KIOXIA/hayashide/rosbag/1117/*"))
print(bags)

for bag in bags:#[12:]:
    print(bag)
    bag_basename=os.path.basename(bag)
    csv_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/results/0117/csv/"+bag_basename[:-4]+".csv"
    play_cmd=f"roslaunch sotsuron_experiment path_plotter.launch avi_basename:={bag_basename} bag_basename:={bag_basename} bag_path:={bag} csv_path:={csv_path}"
    # runcmd=sp.call(cmd.split())
    # print(runcmd)
    os.system(play_cmd)


"""
rosbag play
path_subscriberでcsvに書き出す
path_plotterで保存
"""