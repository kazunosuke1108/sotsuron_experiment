import numpy as np

a=np.array([[1,2,1,1],[2,np.nan,2,2],[1,2,1,1]])
print(np.nanmedian(a))