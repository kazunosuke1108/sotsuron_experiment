import os
import shutil
from glob import glob

analysis_ws_dir_path="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/analysis_ws"
original_dir_paths=sorted(glob("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-19*"))
original_dir_paths+=sorted(glob("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-21*"))
roi_keyword="colormap_log"

for original_dir_path in original_dir_paths:
    files=sorted(glob(original_dir_path+"/*"))
    for file in files:
        if roi_keyword in file:
            shutil.copy(file,analysis_ws_dir_path+f"/{os.path.basename(file)}")