#!/bin/python2
from ds325 import DS325
from SimpleCV import *
#c = 0
depthsense = DS325()
while True:
    iD = depthsense.getDepth() 
    iB = depthsense.getBlob(100,100, 50, 200)

    iD.sideBySide(iB).show()
