
import config
try:
    import lue.framework as lfr
    import luepcr as pcr
except:
    import pcraster as pcr
    pcr.setclone(config.nRows, config.nCols, config.cellsize, 0, 0)

import numpy as np
from dataclasses import dataclass, field
from typing import Any

#######################################################################################################################
#                        Set min and max for fake data generation                                                     #
#######################################################################################################################
""" Initial Conditions """
interceptStor_min, interceptStor_max = 0.0, 1.0
snowCoverSWE_min, snowCoverSWE_max = 0.0, 10.0
snowFreeWater_min, snowFreeWater_max = 0.0, 5.0

""" Space Time """
lat_min, lat_max = -90.0, 90.0                                                                            # Latitude
doy_min, doy_max = 0.0, 365.0                                                                             # Day of Year  

""" Meteo """
precipitation_m_min, precipitation_m_max = 0.0, 10.0 
temperature2m_K_min, temperature2m_K_max = -300.0, 300.0                                                  # Temperature
dewpoint2m_K_min, dewpoint2m_K_max =  -300.0, 300.0                                                       # Dew Point temperature#    
surface_pressure_Pa_min, surface_pressure_Pa_max =  0.0, 300.0                                         # Surface Pressure   
surface_net_solar_radiation_J_m2_min, surface_net_solar_radiation_J_m2_max =  0.0, 300.0               # Net Solar Radiation 
surface_net_thermal_radiation_J_m2_min, surface_net_thermal_radiation_J_m2_max =  0.0, 300.0           # Net Thermal Radiation 
u10m_m_s_min, u10m_m_s_max = 0.0, 10.0                                                                    # u- windpseed
v10m_m_s_min, v10m_m_s_max = 0.0, 10.0                                                                    # v- windpseed

""" Landsurface """
cropKC_min, cropKC_max = 0.2, 1.5                                                                         # Crop Factor
interceptCap_min, interceptCap_max = 0.2, 0.5                                                             # CanopyInterception?
coverFraction_min, coverFraction_max = 0.1, 0.9

#########################################################################################################################
def create_array(min, max):

    array = np.random.uniform(min, max, config.array_shape)
    array = (array* array) / array
    array = pcr.numpy2pcr(pcr.Scalar, array, config.MV)

    return array


""" Initial Conditions """
def interceptStor():
    return create_array(interceptStor_min, interceptStor_max)

def snowCoverSWE():
    return create_array(snowCoverSWE_min, snowCoverSWE_max)

def snowFreeWater():
    return create_array(snowFreeWater_min, snowFreeWater_max)

""" Space-Time Variables """
def lat_values():
    return create_array(lat_min, lat_max)

def doy():
    return create_array(doy_min, doy_max)   


""" Meteo Variables """
def temperature2m_K():
    return create_array(temperature2m_K_min, temperature2m_K_max)

def dewpoint2m_K():
    return create_array(dewpoint2m_K_min, dewpoint2m_K_max)

def surface_pressure_Pa():
    return create_array(surface_pressure_Pa_min, surface_pressure_Pa_max)

def surface_net_solar_radiation_J_m2():
    return create_array(surface_net_solar_radiation_J_m2_min, surface_net_solar_radiation_J_m2_max)

def surface_net_thermal_radiation_J_m2():
    return create_array(surface_net_thermal_radiation_J_m2_min, surface_net_thermal_radiation_J_m2_max)

def u10m_m_s():
    return create_array(u10m_m_s_min, u10m_m_s_max)

def v10m_m_s():
    return create_array(v10m_m_s_min, v10m_m_s_max)

""" Landsurface Variables """
def cropKC():
    return create_array(cropKC_min, cropKC_max)

def interceptCap():
    return create_array(interceptCap_min, interceptCap_max)

def coverFraction():
    return create_array(interceptCap_min, interceptCap_max)
    
    
if __name__ == "__main__":
    pass
