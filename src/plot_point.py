#!/usr/bin/evn python
import os
import numpy as np
import math
import matplotlib.pyplot as plt
#import decimal

ang1 = 45*np.pi/180
ang2 = 90*np.pi/180
ang3 = 10*np.pi/180
ang4 = ang1 + ang3
ang5 = ang2 + ang3

x1 =np.arange(-1*ang2,ang5,ang3)
file1 = open("joint_azim.txt","w")
for i in x1:
    theta1 = i
    print("Theta1 %f" % theta1)
    file1.write('\n' + "p.positions[%f]" % theta1)
file1.close()

x2 =np.arange(-1*ang1,ang4,ang3)
file2 = open("joint_elev.txt","w")
for k in x2:
    theta2 = k
    print("Theta2 %f" % theta2)
    file2.write('\n' + "p.positions[%f]" % theta2)
file2.close()

y1 = 4*np.sin(x1)
y2 = 4 + 4*np.sin(x2)
plt.plot(x1,y1)
plt.plot(x2,y2)
plt.show()