"""
Contains scripts for calculating Potential Reference Evapotranspiration using: 

1) Hamon methed - requires air temperature (units) and latitude (-90, 90)

2) Penman-Monteith- 
#TODO fill in required variables here

"""

import lue.framework as lfr
import numpy as np
import math
from temp_operations import abs, deg2rad

#TODO check if units need to be Kelvin or deg c


""" Hamon Method"""

def satPressure(temperature2m_K): 

    satPressure = lfr.where(lfr.greater_than_equal_to(temperature2m_K, 0.0), 

                                0.61078 * lfr.exp (17.26939 * temperature2m_K / (temperature2m_K + 237.3)), 
    
                                0.61078 * lfr.exp (21.87456 * temperature2m_K / (temperature2m_K + 265.5)))
    return satPressure

def dayLength(doy,lat):
    """ daylength fraction of day  """
    lat = deg2rad(lat)
    M_PI_2 = math.pi / 2.0

    dec = lfr.sin((6.224111 + 0.017202  * doy) *  (180.0 / math.pi))
    dec = 0.39785 * lfr.sin((4.868961 + .017203 *  doy + 0.033446 * lfr.sin (dec * 180 / math.pi)) * 180 / math.pi)
    dec = lfr.asin(dec)

    lat_abs = abs(lat) 
    lat = lfr.where(lfr.greater_than(lat_abs, M_PI_2), 
                    (M_PI_2 - 0.01) * lfr.where(lfr.greater_than(lat, 0),  1.0, -1.0),
                    lat)

    arg = lfr.tan(dec ) * lfr.tan(lat * 180.0 / math.pi  ) * -1.0
    
    h = lfr.acos(arg) / (180.0 * math.pi)
    h = lfr.where(lfr.greater_than(arg, 1.0), 
                  0.0,
                  h)                            # /* sun stays below horizon */
    h = lfr.where(lfr.greater_than(arg,  -1.0),
                  math.pi,
                  h)                            # /* sun stays above horizon */
    dayLength = (h /  math.pi)
 
    return dayLength

def hamonPotEvapTrans(temperature2m_K,doy,lat_values):

    rhoSat =  2.167 * (satPressure(temperature2m_K)  / (temperature2m_K + 273.15))

    dayLen = dayLength(doy,lat_values)

    pet = 165.1 * 2.0 * dayLen * rhoSat # // 2 * DAYLEN = daylength as frac
    pet = pet / 1000 # in meters!
    return pet


""" Penman-Monteith Method"""
def penmanMonteithPotEvapTrans( 
                temperature2m_K, 
                dewpoint2m_K, 
                u10m_m_s,
                v10m_m_s,
                surface_net_solar_radiation_J_m2,
                surface_net_thermal_radiation_J_m2,
                surface_pressure_Pa
                  ):

    """
    This is the function that calculate the PET based on the PM method. 
    Adapted from Singer et al. 2020 (https://doi.org/10.1038/s41597-021-01003-9)
    """

    #-------------------------------------------------------------------------------------------------------------------
    # Converstions

    # Convert units, etc of hourly data.
    temperature2m_C = temperature2m_K - 273.15
    dewpoint2m_C = dewpoint2m_K - 273.15
    del temperature2m_K, dewpoint2m_K

    # Wind speed at 2 m (use wind profile to scale from 10 m)
    temp_windspeed10m_m_s = lfr.sqrt(u10m_m_s**2 + v10m_m_s**2)

    windspeed2m_m_s = temp_windspeed10m_m_s*(4.87/(np.log(67.8*10-5.42)))
    del temp_windspeed10m_m_s

    # Surface pressure Pa to KPa.
    surface_pressure_KPa = surface_pressure_Pa / 1000.
    del surface_pressure_Pa

    # Net downward radiation.
    surface_net_solar_radiation_J_m2 = surface_net_solar_radiation_J_m2
    surface_net_thermal_radiation_J_m2 = surface_net_thermal_radiation_J_m2
    net_radiation_MJ_m2 = (surface_net_solar_radiation_J_m2 +
                           surface_net_thermal_radiation_J_m2) / 1e6

    
    #soil heat flux
    #TODO can we drop this change in dtype?
    # change the dtype to 'float16' 
    # row_surface_net_solar_radiation_J_m2 = row_surface_net_solar_radiation_J_m2.astype('float16') 
    soil_hf = net_radiation_MJ_m2
    # soil heat flux (condition, day, night) 
    soil_hf = lfr.where(lfr.greater_than(surface_net_solar_radiation_J_m2, 0.0), soil_hf*0.1, soil_hf*0.5)
    del surface_net_solar_radiation_J_m2, surface_net_thermal_radiation_J_m2

    #-------------------------------------------------------------------------------------------------------------------
    # Constants.
    lmbda = 2.45  # Latent heat of vaporization [MJ kg -1] (simplification in the FAO PenMon (latent heat of about 20°C)
    cp = 1.013e-3 # Specific heat at constant pressure [MJ kg-1 °C-1]
    eps = 0.622   # Ratio molecular weight of water vapour/dry air

    # Soil heat flux density [MJ m-2 day-1] - set to 0 following eq 42 in FAO
    G = soil_hf    
   
    # Atmospheric pressure [kPa] eq 7 in FAO.
    P_kPa = surface_pressure_KPa #101.3*((293.0-0.0065*height_m) / 293.0)**5.26

    # Psychrometric constant (gamma symbol in FAO) eq 8 in FAO.
    psychometric_kPa_c = cp * P_kPa / (eps * lmbda)

    # Saturation vapour pressure, eq 11 in FAO.
    svp_kPa = 0.6108*lfr.exp((17.27*temperature2m_C) / (temperature2m_C+237.3))

    # Delta (slope of saturation vapour pressure curve) eq 13 in FAO.
    delta_kPa_C = 4098.0*svp_kPa / (temperature2m_C + 237.3)**2

    # Actual vapour pressure, eq 14 in FAO.
    avp_kPa = 0.6108*lfr.exp((17.27*dewpoint2m_C) / (dewpoint2m_C+237.3))

    # Saturation vapour pressure deficit.
    svpdeficit_kPa = svp_kPa - avp_kPa

    # Calculate ET0, equation 6 in FAO
    numerator = 0.408*delta_kPa_C*(net_radiation_MJ_m2 - G) + \
        psychometric_kPa_c*(900/(temperature2m_C+273))*windspeed2m_m_s*svpdeficit_kPa

    denominator = delta_kPa_C + psychometric_kPa_c*(1 + 0.34*windspeed2m_m_s)

    ET0_mm_day = numerator / denominator
    
    return ET0_mm_day * 1000.0 #convert to m