#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os

tfcsv_path="/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-13-14-06-23/_2023-12-13-14-06-23_tf_raw.csv"
odomcsv_path="/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-13-14-06-23/_2023-12-13-14-06-23_od_raw.csv"
avi_path="/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-13-14-06-23/_2023-12-13-14-06-23.avi"

os.system(f"/home/hayashide/anaconda3/bin/python /home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/scripts/analysis_ras_velocity.py {tfcsv_path} {odomcsv_path}")
# os.system(f"/home/hayashide/anaconda3/bin/python /home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/scripts/analysis_ras_r_foot.py {tfcsv_path} {odomcsv_path}")
# os.system(f"/home/hayashide/anaconda3/bin/python /home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/scripts/analysis_ras_r_humpback.py {tfcsv_path} {odomcsv_path}")
# os.system(f"/home/hayashide/anaconda3/bin/python /home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/scripts/analysis_ras_conv_avi_mp4.py {avi_path}")
# os.system(f"/home/hayashide/anaconda3/bin/python /home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/scripts/analysis_ras_wholebody.py {tfcsv_path} {odomcsv_path}")