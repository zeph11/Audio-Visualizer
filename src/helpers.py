import numpy as np


def altList(lst1, lst2):
    return [sub[item] for item in range(len(lst2))
                      for sub in [lst1, lst2]]

def toNVC(xList, yList, resolution):
  for i in range(len(xList)):
    xList[i] = (xList[i]) / (resolution)
    yList[i] = (yList[i]) / (resolution)
  coordinateList = altList(xList,yList)
  return coordinateList

def toNVC2(lst,resolution):
  for i in range(len(lst)):
    lst[i] = (lst[i]) / (resolution)

  return lst
