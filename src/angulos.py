#! /usr/bin/python

import matplotlib, math,time

py = open('positions.txt','a')
n = 10
for i in range (0,190,10):
    #p = JointTrajectoryPoint()
    theta1 = i*math.pi/180

    print("Theta1 %f" % (theta1))
    py.write('\n' + "p.positions[%f]" % theta1)

for i in range (0,100,10):
    theta2 = i*math.pi/180
    print("Theta2 %f" % theta2)
    py.write('\n' + "p.positions2[%f]" % theta2)

py.close()

