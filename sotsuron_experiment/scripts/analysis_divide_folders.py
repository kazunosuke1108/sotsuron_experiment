from glob import glob
from pprint import pprint
import os
import shutil
folderpath="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/png"
files=sorted(glob(folderpath+"/*"))
pprint(files)

rules={"_00_0":"00and01and03_ignore",
       "_01_0":"00and01and03_ignore",
       "_02_0":"others_ignore",
       "_03_0":"00and01and03_ignore",
       "_04_0":"others_ignore",
       "_05_0":"05and10_ignore",
       "_06_0":"06and08_ignore",
       "_07_0":"others_ignore",
       "_08_0":"06and08_ignore",
       "_09_0":"others_ignore",
       "_10_0":"05and10_ignore",
       }

for file in files:
    if file in rules.values():
        continue
    for key in rules.keys():
        if key in file:
            dirpath=folderpath+"/"+rules[key]
            os.makedirs(dirpath,exist_ok=True)
            shutil.copy(file,dirpath+"/"+os.path.basename(file))
            break
