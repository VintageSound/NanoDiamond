import pandas as pd
import numpy as np
from scipy import signal

def getIntegraionOfPump(time, data):
    pump_timestep, image_timestep = getPulsesTimesteps(time, data)

    if len(pump_timestep) < 2:
        return 0
    
    integration = np.trapz(y=data[pump_timestep[0]:pump_timestep[1]], x=time[pump_timestep[0]:pump_timestep[1]])

    return integration

def getIntegraionOfImage(time, data):
    pump_timestep, image_timestep = getPulsesTimesteps(time, data)

    if len(image_timestep) < 2:
        return 0 

    integration = np.trapz(y=data[image_timestep[0]:image_timestep[1]], x=time[image_timestep[0]:image_timestep[1]])

    return integration

def getOnlyImage(time, data):
    pump, image = getPulsesTimesteps(time, data)

    time_image = np.array(time[image[0]:(image[1]+5)]) - time[image[0]] 
    data_image = np.array(data[image[0]:(image[1]+5)])

    # time_image = np.array(time[image[0]:(image[1])]) - time[image[0]] 
    # data_image = np.array(data[image[0]:(image[1])])

    return time_image, data_image

def getOnlyPump(time, data):
    pump, image = getPulsesTimesteps(time, data)

    time_pump = np.array(time[pump[0]:(pump[1]+5)]) - time[pump[0]]
    data_pump = np.array(data[pump[0]:(pump[1]+5)])
    
    # time_pump = np.array(time[pump[0]:(pump[1])]) - time[pump[0]]
    # data_pump = np.array(data[pump[0]:(pump[1])])

    return time_pump, data_pump

def getIntegraionOfImageBegining(time, data, untilIndex = 50):
    pump_timestep, image_timestep = getPulsesTimesteps(time, data)

    if len(image_timestep) < 2:
        return 0 

    integration = np.trapz(y=data[image_timestep[0]:(image_timestep[0] + untilIndex)], x=time[image_timestep[0]:(image_timestep[0] + untilIndex)])

    return integration

def getPulsesTimesteps(time, data):
    derivative = getDerivativeOfDataframe(time, data)
    max = findTwoBiggestPeaks(derivative)
    min = findTwoLowestMimina(derivative)
    
    pump_timestep = [max[0], min[0]]
    image_timestep = [max[1], min[1]]

    return pump_timestep, image_timestep

def findTwoBiggestPeaks(arr):
    peak_indices, peak_dict = signal.find_peaks(arr, height=-1000)
    peak_heights = peak_dict ['peak_heights']

    if len(peak_heights) < 2:
        return (0,0)

    highest_peak_index = peak_indices [np.argmax (peak_heights)]
    second_highest_peak_index = peak_indices [np.argpartition (peak_heights,-2) [-2]]

    if highest_peak_index < second_highest_peak_index:
        return (highest_peak_index, second_highest_peak_index)
    else:
        return (second_highest_peak_index, highest_peak_index)

def findTwoLowestMimina(arr):
    return findTwoBiggestPeaks(-1* arr)

def getDerivativeOfDataframe(time, data):
    dx = np.diff(time)
    dy = np.diff(data)
    dydx = dy/dx

    return dydx
