#!/usr/bin/env python
import lue.framework as lfr
import docopt
import numpy as np
import os.path
import sys

import luepcr as pcr
import math

# LUE demo script, for showing how to use LUE:
# - Import of package
# - Start / stop runtime
# - Array size, partition size


@lfr.runtime_scope

def hello_lue(
        array_shape,
        partition_shape):
    array = lfr.create_array(
        array_shape=array_shape, partition_shape=partition_shape,
        dtype=np.dtype(np.float32), fill_value=5.5)

#
# def dayLength(doy,lat):
#     """ daylength fraction of day  """
#     lat = lat * pcr.scalar(math.pi) /  180.0
#     M_PI_2 = pcr.spatial(pcr.scalar(math.pi / 2.0))
#     dec = pcr.sin( (6.224111 + 0.017202  * doy) *  180. / math.pi)
#     dec = pcr.scalar(0.39785 * pcr.sin ((4.868961 + .017203 *  doy + 0.033446 * pcr.sin (dec*   180 / math.pi)) *  180 / math.pi))
#     dec = pcr.scalar(pcr.asin(dec))
#     lat = pcr.ifthenelse(pcr.abs(lat) > M_PI_2, (M_PI_2 - pcr.scalar(0.01)) * pcr.ifthenelse(lat > 0,  pcr.scalar(1.0), pcr.scalar(-1.0))  ,lat )
#     arg = pcr.tan(dec ) *  pcr.tan(lat * 180.0 / math.pi  ) * -1.0
#     h = pcr.scalar( pcr.acos(arg ) )
#     h = h / 180. * math.pi
#     h = pcr.ifthenelse(arg > 1.0, 0.0,h) # /* sun stays below horizon */
#     h = pcr.ifthenelse(arg <  -1.0 ,math.pi,h) # /* sun stays above horizon */
#     return (h /  math.pi)
#
#
# def satPressure ( airT):
#     """ calculates saturated vp from airt temperature Murray (1967) """
#     # airT      - air temperature [degree C] */
#     satPressure = pcr.ifthenelse(airT >= 0.0 , 0.61078 * pcr.exp (17.26939 * airT / (airT + 237.3)) ,\
#         0.61078 * pcr.exp (21.87456 * airT / (airT + 265.5)))
#     return satPressure
#
# def HamonPotET(airT,doy,lat):
#     # Note that all following functions use trigonometric function in degres.
#     reset_globaloption_to_radians = False
#     if float(pcr.sin(90.0)) < 1.0:
#         pcr.setglobaloption("degrees")
#         reset_globaloption_to_radians = True
#     rhoSat =  2.167 * satPressure (airT) / (airT + 273.15)
#     dayLen = dayLength(doy,lat)
#     pet     = 165.1 * 2.0 * dayLen * rhoSat # // 2 * DAYLEN = daylength as frac
#     pet = pet / 1000 # in meters!
#     if reset_globaloption_to_radians: pcr.setglobaloption("radians")
#
#     return pet



usage = """\
Demonstrate how use LUE

Usage:
    {command} <array> <partition>

Options:
    array           Shape of array: nr_rows,nrcols
    partition       Shape of partition: nr_rows,nrcols
    -h --help       Show this screen
""".format(command = os.path.basename(sys.argv[0]))


def parse_tuple(string):

    return tuple([token.strip() for token in string.split(",")])


def parse_shape(string):

    return tuple([int(element) for element in parse_tuple(string)])


if __name__ == "__main__":
    # Filter out arguments meant for the HPX runtime
    argv = [arg for arg in sys.argv[1:] if not arg.startswith("--hpx")]
    arguments = docopt.docopt(usage, argv)

    array_shape = parse_shape(arguments["<array>"])
    partition_shape = parse_shape(arguments["<partition>"])
    hello_lue(array_shape, partition_shape)


# #######################################################################################
# FROM PCRASTER

#  LET OP!! PCR Pythong computes trigonometric function in degres by default. UNLIKE C, UNLIKE PYTON!
# Convert all arguments to deg using * 180 / pi

# Note that all following functions use trigonometric function in degres.

# ~ >>> pcr.setglobaloption("degrees")
# ~ >>> float(pcr.sin(90.0))
# ~ 1.0
# ~ >>> pcr.setglobaloption("radians")
# ~ >>> float(pcr.sin(90.0))
# ~ 0.8939966559410095

# def HamonPotET(airT,doy,lat):
#
#     # Note that all following functions use trigonometric function in degres.
#
#     reset_globaloption_to_radians = False
#     if float(pcr.sin(90.0)) < 1.0:
#         pcr.setglobaloption("degrees")
#         reset_globaloption_to_radians = True
#
#     rhoSat =  2.167 * satPressure (airT) / (airT + 273.15)
#
#     # ~ vos.plot_variable(rhoSat)
#
#     dayLen = dayLength(doy,lat)
#
#     # ~ vos.plot_variable(dayLen)
#
#     pet     = 165.1 * 2.0 * dayLen * rhoSat # // 2 * DAYLEN = daylength as frac
#     pet = pet / 1000 # in meters!
#
#     if reset_globaloption_to_radians: pcr.setglobaloption("radians")
#
#     return pet
#
#
# def dayLength(doy,lat):
#     """ daylength fraction of day  """
#     lat = lat * pcr.scalar(math.pi) /  180.0
#     M_PI_2 = pcr.spatial(pcr.scalar(math.pi / 2.0))
#     dec = pcr.sin( (6.224111 + 0.017202  * doy) *  180. / math.pi)
#     dec = pcr.scalar(0.39785 * pcr.sin ((4.868961 + .017203 *  doy + 0.033446 * pcr.sin (dec*   180 / math.pi)) *  180 / math.pi))
#     dec = pcr.scalar(pcr.asin(dec))
#     lat = pcr.ifthenelse(pcr.abs(lat) > M_PI_2, (M_PI_2 - pcr.scalar(0.01)) * pcr.ifthenelse(lat > 0,  pcr.scalar(1.0), pcr.scalar(-1.0))  ,lat )
#     arg = pcr.tan(dec ) *  pcr.tan(lat * 180.0 / math.pi  ) * -1.0
#     h = pcr.scalar( pcr.acos(arg ) )
#     h = h / 180. * math.pi
#     h = pcr.ifthenelse(arg > 1.0, 0.0,h) # /* sun stays below horizon */
#     h = pcr.ifthenelse(arg <  -1.0 ,math.pi,h) # /* sun stays above horizon */
#     return (h /  math.pi)
#
#
# def satPressure ( airT):
#     """ calculates saturated vp from airt temperature Murray (1967) """
#     # airT      - air temperature [degree C] */
#     satPressure = pcr.ifthenelse(airT >= 0.0 , 0.61078 * pcr.exp (17.26939 * airT / (airT + 237.3)) ,\
#         0.61078 * pcr.exp (21.87456 * airT / (airT + 265.5)))
#     return satPressure
