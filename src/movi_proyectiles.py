#!/usr/bin/env python
import numpy as np
import math,time
import matplotlib.pyplot as plt

#Datos
v_0 = 5.0
#t = np.arange(0,50,0.1)
x_0 = 0.0
y_0 = 0.0
fhi = 45.0
g = 9.80
v_y0 = round(v_0*math.sin(fhi*math.pi/180), 1)

v_x0 = round(v_0*math.cos(fhi*math.pi/180), 1)
cos1 = math.cos(fhi*math.pi/180)
sin1 = math.sin(fhi*math.pi/180)
#print(f"Velocidad en x0 {v_x0} y Velocidad en y0 {v_y0}")
print v_y0,v_x0, cos1, sin1

t_amx = round(v_y0/g, 3)
tv = 2*t_amx
print"t de altura maxima: ", t_amx
print"t de vuelo maxima: ", tv
#Movimiento horizontal


#v_x = v_x0
x = x_0 + v_x0 * tv
print "x de recorido maxima", x
#movimiento vertical
#v_y = v_y0 - g*t
y_max = round(y_0 + v_y0 * t_amx - 0.5*g*t_amx**2, 2)
#v_y = v_y0 - math.sqrt(2*g*(y-y_0))
print "Altura maxima", y_max
t=np.arange(0,tv,0.0001)
y = y_0 + v_y0 * t - 0.5*g*t**2
x = x_0 + v_x0 * t

y1 = 0.0*t
plt.plot(x,y1)
plt.title("Movimiento de proyectil")
plt.xlabel("Movimiento en x")
plt.ylabel("Movimirnto en y")
plt.plot(x,y)
plt.show()