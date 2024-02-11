import os
import shutil
import pandas as pd
from glob import glob
from pprint import pprint

exp_memo_01_data=pd.read_csv("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/discussion/exp_memo_01.csv",header=0)

analysis_ws_dir_path="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/analysis_ws"
# original_dir_paths=sorted(glob("C:/Users/hayashide/ytlab_ros_ws/ytlab_nlpmp/ytlab_nlpmp_modules/results/20231219/*"))
# original_dir_paths+=sorted(glob("C:/Users/hayashide/ytlab_ros_ws/ytlab_nlpmp/ytlab_nlpmp_modules/results/20231221/*"))
original_dir_paths=sorted(glob("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-19*"))
original_dir_paths+=sorted(glob("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-21*"))
roi_suffix=".png"
roi_keyword="start"

for original_dir_path in original_dir_paths:
    # print(original_dir_path)
    if os.path.basename(original_dir_path)+".bag" in exp_memo_01_data["bag_path"].values:
        files=sorted(glob(original_dir_path+f"/*{roi_suffix}"))
        # print(files)
        pprint(files)
        for file in files:
            if roi_keyword in file:
                shutil.copy(file,analysis_ws_dir_path+f"/{os.path.basename(file)}")
                print(file)