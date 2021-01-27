#!/usr/bin/env python

from getkey import getkey, keys
key = getkey()
if key == keys.UP:
  print("hola1")
  # Handle the UP key
elif key == keys.DOWN:
  print("hola2")
  # Handle the DOWN key
elif key == 'a':
  print("hola3")
  # Handle the `a` key
elif key == 'Y':
  print("hola4")
  # Handle `shift-y`
else:
  #Handle other text characters
  buffer += key
  print(buffer)