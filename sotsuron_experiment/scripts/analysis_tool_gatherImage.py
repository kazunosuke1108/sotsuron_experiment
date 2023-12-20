import os
import shutil
from glob import glob

analysis_ws_dir_path="/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/analysis_ws"
original_dir_paths=sorted(glob("/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-19*"))
roi_keyword="_gravity_trim"

for original_dir_path in original_dir_paths:
    files=sorted(glob(original_dir_path+"/*"))
    for file in files:
        if roi_keyword in file:
            shutil.copy(file,analysis_ws_dir_path+f"/{os.path.basename(file)}")