import numpy as np
import pandas as pd

print(np.arctan(-21.846114))
print(np.arctan(1.181057))


data=pd.Series([0,0.5,1,np.inf])
print(data)
print(np.arctan(data))