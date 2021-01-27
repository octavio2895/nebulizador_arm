#!/usr/bin/env python

import math, time

n = 15
dt = 0.01
rps = 0.05
for i in range (n):
    theta = math.sin(3.1616)
    x1 = math.asin(theta)
    x2 =  0.5*math.sin(1*theta)

    print(f"Theta: {theta}, x1: {x1}, x2: {x2}")


