#! /usr/bin/python3
# -*- coding: utf-8 -*-

from glob import glob
import numpy as np
import matplotlib.pyplot as plt

mother_dir="/catkin_ws/src/ytlab_hsr_modules/datas"

dirs=sorted(glob(mother_dir+"/*"))
print(dirs)