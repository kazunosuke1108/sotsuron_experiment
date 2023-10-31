import numpy as np

a=np.array([0,1,2,3,4,])
b=np.array([0,2,4,5,7])
print(np.unique(np.concatenate([b,a])))

print(np.array([]))