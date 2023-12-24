#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
from glob import glob

# pythonpath="/usr/bin/python3"
# scriptsdir="/home/hayashide/catkin_ws/src/sotsuron_experiment/scripts"
# resultsdir="/home/hayashide/catkin_ws/src/sotsuron_experiment/results"
pythonpath="/home/hayashide/anaconda3/bin/python3"
scriptsdir="/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/scripts"
resultsdir="/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results"

trialdirs=sorted(glob(resultsdir+"/_2023-12-21*"))
# trialdirs=[trialdirs[2]]
for trialdir in trialdirs:
    tfcsv_path=trialdir+f"/{os.path.basename(trialdir)}_tf_raw.csv"
    odomcsv_path=trialdir+f"/{os.path.basename(trialdir)}_od_raw.csv"
    avi_path=trialdir+f"/{os.path.basename(trialdir)}.avi"
    print(f"tfcsv_path: {tfcsv_path}")
    print(f"odomcsv_path: {odomcsv_path}")
    print(f"avi_path: {avi_path}")

    # tfcsv_path="/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-13-14-06-23/_2023-12-13-14-06-23_tf_raw.csv"
    # odomcsv_path="/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-13-14-06-23/_2023-12-13-14-06-23_od_raw.csv"
    # avi_path="/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-13-14-06-23/_2023-12-13-14-06-23.avi"

    # os.system(f"{pythonpath} {scriptsdir}/analysis_ras_velocity.py {tfcsv_path} {odomcsv_path}")
    # os.system(f"{pythonpath} {scriptsdir}/analysis_ras_r_foot.py {tfcsv_path} {odomcsv_path}")
    # os.system(f"{pythonpath} {scriptsdir}/analysis_ras_r_humpback.py {tfcsv_path} {odomcsv_path}")
    # os.system(f"{pythonpath} {scriptsdir}/analysis_ras_conv_avi_mp4.py {avi_path}")
    os.system(f"{pythonpath} {scriptsdir}/analysis_ras_wholebody.py {tfcsv_path} {odomcsv_path}")