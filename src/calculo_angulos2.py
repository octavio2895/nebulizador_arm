#!/usr/bin/env python

import numpy as np


ang1 = 90*np.pi/180
ang2 = 45*np.pi/180

pas1 = 10*np.pi/180
pas2 = 20*np.pi/180

max1 = ang1 + pas2
max2 = ang2 + pas1

x1 =np.arange(-1*ang1,max1,pas2)
x2 =np.arange(-1*ang2,max2,pas1)

import itertools
x=10
y=10
#for i, j in itertools.product(x1,y1):
for i, j in zip(x1,x2):
    print(f"{i}, {j}")

#for i in x1:
#    print(i)