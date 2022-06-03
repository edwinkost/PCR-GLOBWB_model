
# ~ import pcraster as pcr
from pcraster import setclone as pcrsetclone

import lue.framework as lfr

import numpy as np


# hack to just get it working, depend on case study
# these should be derived eventually
rows = 87600
cols = 84000
shape1 = 1000
shape2 = 1000
cellsize = 100.0

rows = 4320
cols = 2160
shape1 = 100
shape2 = 100
cellsize = 5./60.

array_shape = (rows, cols)
partition_shape = (shape1, shape2)


# PCRaster ~ LUE

def accuflux(arg1, arg2):
    return lfr.accu(arg1, arg2)


def upstream(arg1, arg2):
    return lfr.upstream(arg1, arg2)


def mapmaximum(arg):
    return lfr.maximum(arg)


def sqrt(arg):
    return lfr.sqrt(arg)


def accuthresholdflux(flow_direction, material, threshold, ts):
    flux, state = lfr.accu_threshold(flow_direction, material, threshold)
    return flux


def accuthresholdstate(flow_direction, material, threshold, ts):
    flux, state = lfr.accu_threshold(flow_direction, material, threshold)
    return state


def ln(arg):
    return lfr.log(arg)


def slope(arg):
    return lfr.slope(arg, cellsize)


def downstream(arg1, arg2):
    return lfr.downstream(arg1, arg2)


def downstreamdist(arg):
    return lfr.downstream_distance(arg, cellsize, np.dtype(np.float32))


def defined(arg):
    return lfr.valid(arg)


def ifthen(arg1, arg2):
    return lfr.where(arg1, arg2)


def ifthenelse(arg1, arg2, arg3):
    return lfr.where(arg1, arg2, arg3)


def cover(arg1, arg2):
    return lfr.where(lfr.valid(arg1), arg1, arg2)

def ldd(arg):
    return lfr.d8_flow_direction(arg)

# Mimic operations not in LUE

def setclone(arg):

    # ~ # Dummy clone for the modelling framework
    # ~ pcr.setclone(5, 4, 3, 2, 1)

    # Set the actual clone
    pcrsetclone(arg)


def celllength():
    return cellsize


def cellarea():
    return cellsize * cellsize


def scalar(arg):
    if type(arg) == lfr.PartitionedArray_float32_2:
        return arg
    elif type(arg) == int or type(arg) == float:
        return float(arg)
    else:
        raise NotImplementedError


def spatial(arg):
    if type(arg) == float:
        return lfr.create_array(array_shape, partition_shape, np.dtype(np.float32), fill_value = arg)
    else:
        raise NotImplementedError

def lddrepair(arg):
    print("Note NO 'lddrepair' function is implemented yet.")
    return lfr.d8_flow_direction(arg)


# ~ def spatial(arg):
    # ~ return arg
    # ~ if type(arg) == lfr.PartitionedArray_float32_2:
        # ~ return arg
    # ~ elif type(arg) == int or type(arg) == float:
        # ~ return float(arg)
    # ~ else:
        # ~ raise NotImplementedError


# to create an array with a value:
# tmp = lfr.create_array(array_shape, partition_shape, np.dtype(np.float32), fill_value=7)