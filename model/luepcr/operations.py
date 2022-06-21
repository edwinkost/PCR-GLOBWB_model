
# ~ import pcraster as pcr
from pcraster import setclone as pcr_setclone
from pcraster import numpy2pcr as pcr_numpy2pcr
from pcraster import aguila as pcr_aguila
from pcraster import Scalar as pcr_Scalar

import pcraster as pcraster_call

import lue.framework as lfr

import numpy as np

import os

import random

# Global variables:
MV = -9999.99
smallNumber = 1.0e-39


# hack to just get it working, depend on case study
# these should be derived eventually
# ~ rows = 87600
# ~ cols = 84000
# ~ shape1 = 1000
# ~ shape2 = 1000
# ~ cellsize = 100.0

rows = 4320
cols = 2160
shape1 = 1000
shape2 = 1000
cellsize = 5./60.

#~ rows = 4320
#~ cols = 2160
#~ shape1 = 1500
#~ shape2 = 1500
#~ cellsize = 5./60.

#~ rows = 4320
#~ cols = 2160
#~ shape1 = 50
#~ shape2 = 50
#~ cellsize = 5./60.

# ~ rows = 43200
# ~ cols = 21600
# ~ shape1 = 1000
# ~ shape2 = 1000
# ~ cellsize = 0.5/60.

# ~ rows = 8000
# ~ cols = 6000
# ~ shape1 = 1000
# ~ shape2 = 1000
# ~ cellsize = 0.5/60.

array_shape = (rows, cols)
partition_shape = (shape1, shape2)

debug = False

# PCRaster ~ LUE

def accuflux(arg1, arg2):
    return lfr.accu(arg1, arg2)


def upstream(arg1, arg2):
    return lfr.upstream(arg1, arg2)


def mapmaximum(arg):
    return lfr.maximum(arg)

def mapminimum(arg):
    return lfr.minimum(arg)

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


def cover(arg1, arg2, check_with_aguila = False):
    if check_with_aguila: aguila(arg1)
        check = lfr.where(lfr.valid(arg1), arg1, arg2)
        aguila(check)
    return lfr.where(lfr.valid(arg1), arg1, arg2)

#~ def cover(arg1, arg2):
    #~ if type(arg2) == float:
        #~ spatial_arg2 = lfr.create_array(array_shape, partition_shape, np.dtype(np.float32), fill_value = arg2)
    #~ else:    
        #~ spatial_arg2 = arg2
    #~ # ~ print("this")
    #~ # ~ aguila(spatial_arg2)
    #~ # ~ cover_map = lfr.where(lfr.valid(arg1), arg1, spatial_arg2)
    #~ cover_map = lfr.where(lfr.valid(arg1) == 1, arg1, spatial_arg2)
    #~ # ~ cover_map = lfr.where(cover_map < 10.0, cover_map, spatial_arg2)
    #~ # ~ aguila(cover_map)
    #~ print(cover_map)
    #~ return cover_map

# ~ def cover(arg1, arg2):
    # ~ if type(arg2) == float:
        # ~ spatial_arg2 = lfr.create_array(array_shape, partition_shape, np.dtype(np.float32), fill_value = arg2)
        # ~ test = lfr.where(lfr.valid(arg1), arg1, spatial_arg2)
        # ~ print("this")
        # ~ aguila(test)
        # ~ return lfr.where(lfr.valid(arg1), arg1, spatial_arg2)
    # ~ else:    
        # ~ test = lfr.where(lfr.valid(arg1), arg1, arg2)
        # ~ print(arg2)
        # ~ aguila(test)
        # ~ return lfr.where(lfr.valid(arg1), arg1, arg2)


def ldd(arg):
    if type(arg) == lfr.PartitionedArray_float32_2:
        return lfr.d8_flow_direction(arg)
    elif type(arg) == lfr.PartitionedArray_uint8_2:
        return arg
    else:
        raise NotImplementedError


# Mimic operations not in LUE

def setclone(arg):

    # ~ # Dummy clone for the modelling framework
    # ~ pcr.setclone(5, 4, 3, 2, 1)

    # Set the actual clone
    pcr_setclone(arg)


def celllength():
    return cellsize


def cellarea():
    return cellsize * cellsize


def scalar(arg):
    if type(arg) == lfr.PartitionedArray_float32_2:
        return arg
    # ~ elif type(arg) == lfr.PartitionedArray_uint8_2:
        # ~ return arg
    elif type(arg) == int or type(arg) == float:
        return float(arg)
    else:
        print(arg)
        raise NotImplementedError
    # ~ else:
        # ~ try:
            # ~ return arg
        # ~ except:
            # ~ print(arg)
            # ~ raise NotImplementedError


def spatial(arg):
    if type(arg) == float:
        return lfr.create_array(array_shape, partition_shape, np.dtype(np.float32), fill_value = arg)
    else:
        return arg


def ycoordinate(arg):
    if debug: print("Note 'pcraster.ycoordinate' function is NOT implemented on LUE yet.")
    return lfr.create_array(array_shape, partition_shape, np.dtype(np.float32), fill_value = 0.0)


def lddrepair(arg):
    if debug: print("Note 'pcraster.lddrepair' function is NOT implemented on LUE yet.")
    return ldd(arg)


def lddmask(arg1, arg2):
    if debug: print("Note 'pcraster.lddmask' function is NOT implemented on LUE yet.")
    # ~ return lfr.where(arg2, arg1)
    return lfr.where(defined(arg2), arg1)


def ldddist(arg1, arg2, arg3):
    if debug: print("Note 'pcraster.ldddist' function is NOT implemented on LUE yet.")
    return arg3

def numpy2pcr(arg1, arg2, arg3):
    if debug: print("Note 'pcraster.numpy2pcr' function is PARTIALLY implemented on LUE yet.")

    #~ return lfr.from_numpy(np.transpose(np.float32(arg2)), partition_shape, arg3)
    #~ return lfr.from_numpy(np.transpose(np.float32(arg2)), partition_shape)
    # ~ return cover(lfr.from_numpy(np.transpose(np.float32(arg2)), partition_shape), 0.0)
    
    # ~ check_lfr      = lfr.from_numpy(np.transpose(np.float32(arg2)), partition_shape, arg3)
    # ~ check_np       = np.transpose(lfr.to_numpy(check_lfr, arg3))
    # ~ check_pcraster = pcr_numpy2pcr(pcr_Scalar, check_np, arg3)
    
    # ~ pcr_aguila(check_pcraster)
    # ~ input("Press Enter to continue...")

    return lfr.from_numpy(np.transpose(np.float32(arg2)), partition_shape, arg3)


def nominal(arg):
    if debug: print("Note 'pcraster.nominal' function is NOT implemented on LUE yet.")
    return arg


def Scalar():
    if debug: print("Note 'pcraster.Scalar' is NOT implemented on LUE yet.")
    pass


def boolean(arg):
    if debug: print("Note 'pcraster.boolean' is NOT implemented on LUE yet.")
    if arg == 1.0:
        return lfr.valid(lfr.create_array(array_shape, partition_shape, np.dtype(np.float32), fill_value = 1.0))
    elif arg == 0.0:
        return lfr.valid(lfr.create_array(array_shape, partition_shape, np.dtype(np.float32), fill_value = 1.0))
    else:
        print(arg)
        raise NotImplementedError


def max(arg1, arg2):
    if debug: print("Note 'pcraster.max' function is PARTIALLY implemented on LUE yet.")
    # ~ print(arg1)
    # ~ print(arg2)
    # ~ return lfr.where(lfr.greater_than_equal_to(arg1, arg2), arg1, arg2)
    return ifthenelse(arg1 > arg2, arg1, arg2)


def min(arg1, arg2):
    if debug: print("Note 'pcraster.min' function is PARTIALLY implemented on LUE yet.")
    return ifthenelse(arg1 > arg2, arg2, arg1)

    # ~ if type(arg1) == float: spatial_arg1 = spatial(arg1) 
    # ~ if type(arg2) == float: spatial_arg1 = spatial(arg2) 
    # ~ return ifthenelse(spatial_arg1 > spatial_arg2, spatial_arg2, spatial_arg1)


def cellvalue(arg1, arg2):
    if debug: print("Note 'pcraster.cellvalue' function is NOT implemented on LUE yet.")
    return [arg1, "dummy"]


def maptotal(arg):
    if debug: print("Note 'pcraster.maptotal' function is NOT implemented on LUE yet.")
    return 0.0


def report(arg1, arg2):
    if debug: print("Note 'pcraster.report' function is NOT implemented on LUE yet.")
    pass


def sin(arg):
    if type(arg) == float: return lfr.sin(spatial(arg))
    if type(arg) == lfr.PartitionedArray_float32_2: return lfr.sin(arg)


def cos(arg):
    if type(arg) == float: return lfr.cos(spatial(arg))
    if type(arg) == lfr.PartitionedArray_float32_2: return lfr.cos(arg)


def tan(arg):
    if type(arg) == float: return lfr.tan(spatial(arg))
    if type(arg) == lfr.PartitionedArray_float32_2: return lfr.tan(arg)


def asin(arg):
    if type(arg) == float: return lfr.asin(spatial(arg))
    if type(arg) == lfr.PartitionedArray_float32_2: return lfr.asin(arg)


def acos(arg):
    if type(arg) == float: return lfr.acos(spatial(arg))
    if type(arg) == lfr.PartitionedArray_float32_2: return lfr.acos(arg)


def atan(arg):
    if type(arg) == float: return lfr.atan(spatial(arg))
    if type(arg) == lfr.PartitionedArray_float32_2: return lfr.atan(arg)


def abs(arg):
    return lfr.where(lfr.greater_than_equal_to(arg, 0), arg, arg*-1)


def exp(arg):
    return lfr.exp(arg)


def roundoff(arg):
    if debug: print("Note 'pcraster.roundoff' function is NOT implemented on LUE yet.")
    return arg


def rounddown(arg):
    if debug: print("Note 'pcraster.rounddown' function is NOT implemented on LUE yet.")
    return arg


def roundup(arg):
    if debug: print("Note 'pcraster.roundup' function is NOT implemented on LUE yet.")
    return arg


def pcr2numpy(arg1, arg2):
    return lfr.to_numpy(arg1, arg2)


def uniform(whatever, min_value = 0.0, max_value = 1.0): 
    return lfr.uniform(lfr.create_array(array_shape, partition_shape, np.dtype(np.float32), fill_value=0.0), min_value, max_value)

def get_random_word(wordLen):
    word = ''
    for i in range(wordLen):
        word += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
    return word

def aguila(arg1):
    if debug: print("Note 'pcraster.aguila' function is PARTIALLY implemented on LUE yet.")

    check_np        = np.transpose(lfr.to_numpy(arg1, MV))
    check_pcraster  = pcr_numpy2pcr(pcr_Scalar, check_np, MV)
    
    pcrmap_tmp_file = get_random_word(8) + ".map" 
    
    pcraster_call.report(check_pcraster, pcrmap_tmp_file)
    cmd = "aguila " + pcrmap_tmp_file 
    os.system(cmd)
    cmd = "rm " + pcrmap_tmp_file 
    os.system(cmd)


# to create an array with a value:
# tmp = lfr.create_array(array_shape, partition_shape, np.dtype(np.float32), fill_value=7)
