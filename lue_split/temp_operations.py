"""
Bits and bobs

"""
try:
    import luepcr as pcr
except:
    import pcraster as pcr
    import config
    pcr.setclone(config.nRows, config.nCols, config.cellsize, 0, 0)
import math


def deg2rad(arg):
    'numpy equivelant of deg2rad' 
    rad = arg * (math.pi /  180.0)
    return rad


def getValDivZero(x, y, y_lim, z_def=0.0):
  #-returns the result of a division that possibly involves a zero
  # denominator; in which case, a default value is substituted:
  # x/y= z in case y > y_lim,
  # x/y= z_def in case y <= y_lim, where y_lim -> 0.
  # z_def is set to zero if not otherwise specified
  return pcr.ifthenelse(y > y_lim,
                   x/y,
                   z_def)
