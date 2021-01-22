#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Comprobar si el usuario es root
"""

import os
import sys

if os.geteuid() != 0:
    print 'Debes tener privilegios root para este script.'
    sys.exit(1)
else:
    print 'Bienvenido usuario root'