#!/usr/bin/env python
import matplotlib, math,time

py = open('positions2.txt','a')
n = 10

for i,j in range (0,190,10):
    theta1 = i*math.pi/180
    theta2 = j*math.pi/180
    print("[%f,%f]",theta1,theta2)
    #py.write("p.positions[%f,%f]" % theta2 % theta2)

py.close()