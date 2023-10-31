from glob import glob
import matplotlib.pyplot as plt
import pandas as pd
from pprint import pprint


from analysis_management import *
from analysis_initial_processor import *
path_management,csv_labels,color_dict=management_initial()

print("answer")
pprint(path_management["ras_od_csv_dir_path_unique"])