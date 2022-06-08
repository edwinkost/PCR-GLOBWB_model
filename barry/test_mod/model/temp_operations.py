"""
Contains operations not yet implimented in lue

"""

import lue.framework as lfr
import math

def deg2rad(arg):
    'numpy equivelant of deg2rad' 
    rad = lfr.multiply(arg, (math.pi /  180.0))
    return rad

def abs(arg):
    arg_absolute = lfr.where(lfr.greater_than_equal_to(arg, 0), arg, arg*-1)
    return arg_absolute
    