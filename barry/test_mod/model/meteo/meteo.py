import lue.framework as lfr

'Run the meteo module in lue'
import config
import meteo.potEvap as potEvap
from pre_process.input import data


def evap():

    if config.potEvapMethod == 'Hamon': 

        pet = potEvap.hamonPotEvapTrans(temperature2m_K = data().temperature2m_K, 
                                        doy = data().doy,   
                                        lat_values = data().lat_values)

    if config.potEvapMethod == 'Penman-Monteith': 

        pet = potEvap.penmanMonteithPotEvapTrans(
                            temperature2m_K = data().temperature2m_K, 
                            dewpoint2m_K = data().dewpoint2m_K, 
                            u10m_m_s = data().u10m_m_s,
                            v10m_m_s = data().v10m_m_s,
                            surface_net_solar_radiation_J_m2 = data().surface_net_solar_radiation_J_m2,
                            surface_net_thermal_radiation_J_m2 = data().surface_net_thermal_radiation_J_m2,
                            surface_pressure_Pa = data().surface_pressure_Pa)
    
    return pet         

if __name__ == "__main__":
    evap()