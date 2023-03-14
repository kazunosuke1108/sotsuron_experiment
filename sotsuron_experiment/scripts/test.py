import numpy as np

test=np.array([1,2,3,4,5,6,7,8,9])
ans=np.where((test<5) & (test>=3))
print(np.array(ans).shape)