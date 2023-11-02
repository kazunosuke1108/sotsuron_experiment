import numpy as np

positions=np.array([[1,0],[3,4],[5,6]])
previous_positions=np.array([[1,2],[0,1],[5,5]])
print(positions)
print(previous_positions)
roi_row=np.unique(np.argwhere(abs(positions-previous_positions)>0.3/31)[:,0])

print(roi_row)

a=[]
b=[1,2,3]
a=a+b
print(a)