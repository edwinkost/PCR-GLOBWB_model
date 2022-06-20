#INPUT OPTIONS#
array_shape = (4320, 2160)
partitionShape = (1000, 1000)
nRows = 4320
nCols = 2160
cellsize = 5./60.



########################################################################################
#                            METEO OPTIONS                                             #
########################################################################################

# potEvapMethod = 'Penman-Monteith' #or 'Hamon'  or OWN_INPUT
# referencePotentialEvaporation_Method = 'Penman-Monteith'
referencePotentialEvaporation_Method = 'Hamon'

########################################################################################
#                            LANDCOVER OPTIONS                                         #
########################################################################################

minCropKC = 0.2         #Default = 0.2
minInterceptCap = 0.0   #Default = 0.0

# snow module properties
freezingT           =  0.0
degreeDayFactor     =  0.0025
snowWaterHoldingCap =  0.1
refreezingCoeff     =  0.05

########################################################################################
#                            ODD BITS                                                  #
########################################################################################

smallNumber = 1E-39
MV = 1E20