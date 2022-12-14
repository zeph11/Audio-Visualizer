import numpy as np


def altList(lst1, lst2):
    return [sub[item] for item in range(len(lst2))
                      for sub in [lst1, lst2]]

def toNVC(xList, yList, resolution):
  i = 0
  for x in xList:
    xList[i] = (xList[i]) / (resolution)
    yList[i] = (yList[i]) / (resolution)
    i += 1
  coordinateList = altList(xList,yList)
  return coordinateList