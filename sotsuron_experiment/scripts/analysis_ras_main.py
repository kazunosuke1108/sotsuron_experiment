#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
from glob import glob

if os.name == "nt":
    pythonpath = f"C:/Users/hayashide/AppData/Local/anaconda3/python"
    scriptsdirpath=f"C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/scripts"
    resultsdirpath = f"C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results"
else:
    if os.path.exists("/home/hayashide/catkin_ws"):
        self.resultsdirpath = f"/home/hayashide/catkin_ws/src/ytlab_nlpmp_modules/results"
        self.scriptsdirpath = f"/home/hayashide/catkin_ws/src/ytlab_nlpmp_modules/scripts"
    else:
        self.resultsdirpath = f"/home/hayashide/ytlab_ros_ws/ytlab_nlpmp/ytlab_nlpmp_modules/results"
        self.scriptsdirpath = f"/home/hayashide/ytlab_ros_ws/ytlab_nlpmp/ytlab_nlpmp_modules/scripts"


trialdirs=sorted(glob(resultsdirpath+"/_2023-12-20*"))
print(trialdirs)
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
    os.system(f"{pythonpath} {scriptsdirpath}/analysis_ras_wholebody.py {tfcsv_path} {odomcsv_path}")