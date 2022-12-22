import numpy as np

np.loadtxt("hoge.csv",delimiter=",")
# sample=[]
# sample.append([1,2,3])
# sample.append([1,2,3,4,5])


# for i in range(len(sample)):
	
# 	print(sample[i])

# import numpy as np
# import matplotlib.pyplot as plt
# win=10
# ranges_roi=np.array([25,16,9,4,1,0,1,4,9,16])
# print(ranges_roi)

# ranges_norm=(ranges_roi-min(ranges_roi))/(max(ranges_roi)-min(ranges_roi))
# print(ranges_roi)
# indexes=np.arange(-1,1,0.2)
# print(indexes)
# a,b,c=np.polyfit(indexes,ranges_norm,2)
# print(a)
# print(b)
# print(c)
# estm=a*ranges_norm**2+b*ranges_norm+c
# err=ranges_norm-estm
# print(estm)
# plt.plot(indexes,ranges_norm,label="raw")
# plt.plot(indexes,estm,label="estm")
# plt.plot(indexes,err,label="error")
# plt.legend()
# plt.show()