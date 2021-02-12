#!/usr/bin/env python

def _map(x, in_min, in_max, out_min, out_max):
    return int((x-in_min)*(out_max-out_min)/(in_max-in_min)+out_min)

#TEST

y = _map(100,0,1024,0,1024)
print(y)