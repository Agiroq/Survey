import numpy as np
import sympy as sp
import math
from math import atan2


def getAzimut(v1, v2):
    v = np.array(v2) - np.array(v1)
    print(v)
    C = 0
    if(v[1]<0):
        C =400
    return ((atan2(v[1],v[0])*200)/np.pi)+C

def getVertAngle(v1, v2):
    v = np.array(v2) - np.array(v1)
    print(v)
    C = 0
    if(v[1]<0):
        C =400
    return ((atan2(v[1],v[2])*200)/np.pi)+C

def getRGeoDist(v1, v2):
    v = np.array(v2) - np.array(v1)
    return math.sqrt((v[0]**2)+(v[1]**2))

print(getVertAngle((0,0,0),(0,3,0)))
print(getVertAngle((0,1,0),(0,3,3)))
