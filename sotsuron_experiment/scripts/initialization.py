#! /usr/bin/python3
# -*- coding: utf-8 -*-
import os

header="initialization.py: "

z_csv_path="/home/hayashide/catkin_ws/src/ytlab_hsr/ytlab_hsr_modules/exp_data/z.csv"
z8_csv_path="/home/hayashide/catkin_ws/src/ytlab_hsr/ytlab_hsr_modules/exp_data/z8.csv"
t_csv_path="/home/hayashide/catkin_ws/src/ytlab_hsr/ytlab_hsr_modules/exp_data/t.csv"
zed_csv_path="/home/hayashide/catkin_ws/src/ytlab_hsr/ytlab_hsr_modules/exp_data/zed.csv"

try:
    os.remove(z_csv_path)
    print(header+"delete z.csv")
except FileNotFoundError:
    pass

try:
    os.remove(z8_csv_path)
    print(header+"delete z8.csv")
except FileNotFoundError:
    pass

try:
    os.remove(t_csv_path)
    print(header+"delete t.csv")
except FileNotFoundError:
    pass

try:
    os.remove(zed_csv_path)
    print(header+"delete zed.csv")
except FileNotFoundError:
    pass
