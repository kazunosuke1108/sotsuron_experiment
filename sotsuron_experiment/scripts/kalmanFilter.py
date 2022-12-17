import numpy as np
from numpy.random import *
import matplotlib.pyplot as plt

def Kalman(y, xK1, pK1, sigmaW, sigmaV):

    # Predict State Variable
    xK = xK1

    # Update Sigma Variable
    pK = pK1 + sigmaW

    # Update Kalman Gain
    kGain = pK / (pK + sigmaV)

    # Filter State and Variable
    xFilt = xK + kGain * (y - xK)
    pFilt = (1 - kGain) * pK

    return xFilt, pFilt


def CreateFilteredData(measData, initPredVar, sigmaW, sigmaV):

    length = len(measData)
    filteredMeasData = np.zeros(length + 1)
    filteredPredVar = np.zeros(length + 1)
    filteredPredVar[0] = initPredVar

    for i in range(0, length):
        xFilt, pFilt = Kalman(measData[i], filteredMeasData[i], filteredPredVar[i], sigmaW, sigmaV)
        filteredMeasData[i + 1] = xFilt
        filteredPredVar[i + 1] = pFilt

    return np.delete(filteredMeasData, 0), np.delete(filteredPredVar, 0)

def CreateSampleData(height, var, size):

    indexes = [idx for idx in range(0, size)]
    heightListWithNoise = np.random.normal(height, var, size)

    return indexes, heightListWithNoise

if __name__ == '__main__':
    print("Sample Kalman Filter started.")

    height = 1.0
    var = 0.5
    size = 100

    indexes, data = CreateSampleData(height, var, size)
    filteredData, filteredVars = CreateFilteredData(data, 10000, 100, 10000)

    plt.plot(indexes, data)
    plt.plot(indexes, filteredData)
    #plt.plot(indexes, filteredVars)
    plt.show()