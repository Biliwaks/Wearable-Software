# just a random second comment #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 10:16:00 2018

@author: matteomacchini
"""

import numpy as np
import haptic_device

north = np.array([8,5,2])
south = np.array([2,5,8])
east = np.array([4,5,6])
west = np.array([6,5,4])
northwest = np.array([1,5,9])
northest = np.array([3,5,7])
southest = np.array([9,5,1])
southwest = np.array([7,5,3])


my_device = haptic_device.haptic_device()

print (my_device.matteo)

my_device.impulsion_command(1, 'linear',1, southwest)
