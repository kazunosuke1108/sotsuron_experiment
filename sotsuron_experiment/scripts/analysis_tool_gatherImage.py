import os
import shutil
from glob import glob

analysis_ws_dir_path="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/analysis_ws"
original_dir_paths=sorted(glob("C:/Users/hayashide/ytlab_ros_ws/ytlab_nlpmp/ytlab_nlpmp_modules/results/20231219/*"))
original_dir_paths+=sorted(glob("C:/Users/hayashide/ytlab_ros_ws/ytlab_nlpmp/ytlab_nlpmp_modules/results/20231221/*"))
# original_dir_paths=sorted(glob("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-19*"))
# original_dir_paths+=sorted(glob("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-21*"))
roi_suffix="prcd.png"
roi_keyword="_00_"

for original_dir_path in original_dir_paths:
    files=sorted(glob(original_dir_path+f"/*{roi_suffix}"))
    print(files)
    for file in files:
        if roi_keyword in file:
            shutil.copy(file,analysis_ws_dir_path+f"/{os.path.basename(file)}")