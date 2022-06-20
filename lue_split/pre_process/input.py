from dataclasses import dataclass, field
from typing import Any
import pre_process.default_data as default
import config

if config.referencePotentialEvaporation_Method == 'Hamon':
    @dataclass
    class statesData():
        """ Initial Conditions"""
        interceptStor: Any = field(default_factory = default.interceptStor)
        snowCoverSWE: Any = field(default_factory = default.snowCoverSWE)
        snowFreeWater: Any = field(default_factory = default.snowFreeWater)

    @dataclass
    class gridData:
        """ Space Time"""
        lat_values: Any = field(default_factory = default.lat_values)
        doy: Any = field(default_factory = default.doy)


    @dataclass
    class meteoData:

        """ Meteo """
        precipitation: Any = field(default_factory=default.temperature2m_K)
        temperature2m_K: Any = field(default_factory=default.temperature2m_K)

    @dataclass
    class landSurfaceData:
        
        """ Landsurface """
        cropKC: Any = field(default_factory=default.cropKC)
        interceptCap: Any = field(default_factory=default.interceptCap)
        coverFraction: Any = field(default_factory=default.coverFraction)

if config.referencePotentialEvaporation_Method == 'Penman-Monteith':

    @dataclass
    class statesData():
        """ Initial Conditions"""
        interceptStor: Any = field(default_factory = default.interceptStor)
        snowCoverSWE: Any = field(default_factory = default.snowCoverSWE)
        snowFreeWater: Any = field(default_factory = default.snowFreeWater)


    @dataclass
    class gridData:
        """ Space Time"""
        lat_values: Any = None
        doy: Any = None


    @dataclass
    class meteoData:

        """ Meteo """
        precipitation: Any = field(default_factory=default.temperature2m_K)
        temperature2m_K: Any = field(default_factory=default.temperature2m_K)
        dewpoint2m_K: Any = field(default_factory=default.dewpoint2m_K)
        surface_pressure_Pa: Any = field(default_factory=default.surface_pressure_Pa)
        surface_net_solar_radiation_J_m2: Any = field(default_factory=default.surface_net_solar_radiation_J_m2)
        surface_net_thermal_radiation_J_m2: Any = field(default_factory=default.surface_net_thermal_radiation_J_m2)
        u10m_m_s: Any = field(default_factory=default.u10m_m_s)
        v10m_m_s: Any = field(default_factory=default.v10m_m_s)


    @dataclass
    class landSurfaceData:
        
        """ Landsurface """
        cropKC: Any = field(default_factory=default.cropKC)
        interceptCap: Any = field(default_factory=default.interceptCap)
        coverFraction: Any = field(default_factory=default.coverFraction)

if __name__ == "__main__":
    pass