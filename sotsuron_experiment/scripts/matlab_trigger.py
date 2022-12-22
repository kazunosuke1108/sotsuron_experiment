#! /usr/bin/python3
# -*- coding: utf-8 -*-

from glob import glob
import os
import time

# print(os.environ['HOME'])
# current_dir=os.getcwd()
# print(current_dir)

# jsn_path=os.environ['HOME']+"/catkin_ws/src/sotsuron_experiment/scripts/monitor/velocity.json"


# while True:
#     if os.path.isfile(jsn_path):
#         print("### file found ###")
#         break
#     else:
#         print("### file not found")
#         time.sleep(0.5)
# print(os.environ['HOME']+"src/")

matlab_ws=sorted(glob(os.environ['HOME']+"/catkin_ws/src/sotsuron_simulator/matlab_ws/*"))

print(matlab_ws)
latest_dir=matlab_ws[-4]
os.chdir(latest_dir)
print(os.getcwd())
os.system(f"python3 {latest_dir}/main.py")

"""
全体の流れ

# 巡回
・zed起動
・human_tracker.pyを回して臨戦態勢
・HSRは等速直線運動

# 検知
・100フレーム撮ってhuman_tracker.pyがjsonを吐いて死ぬ

# 計算
・main.py経由でmain_funcが回る（csvを見に行く）


"""