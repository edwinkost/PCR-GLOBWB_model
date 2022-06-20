try:
    import luepcr as pcr
except:
    import pcraster as pcr

import meteo.refPotEvap_func as refPotEvap_func
import config
import temp_operations as tmp
# import pre_process.input

import time

class Meteo: 

    def __init__(self, landSurfaceData, meteoData, statesData, gridData):
        """ Initialiase Data Imports"""

        """ Start Calculating Evaporation""" 
        corrected_cropKC = pcr.max(landSurfaceData.cropKC, config.minCropKC)

        """Landcover specific potential evapotranspiartion"""
        self.totalPotET = corrected_cropKC * refPotEvap_func.referencePotentialEvaporation(gridData, meteoData)

        """Landcover specific bare soil evaporation and transpiartion from plants"""
        self.bareSoilPotET = config.minCropKC * self.totalPotET
        self.transpirationPotET = self.totalPotET - self.bareSoilPotET
        self.transpirationPotET = pcr.ifthenelse(self.transpirationPotET > 0.0, 
                                                 self.transpirationPotET,     
                                                 0.0)  

        """ Calculation of Evaporation arising from intercepted precipitation"""
        interceptCap = landSurfaceData.interceptCap * landSurfaceData.coverFraction
        interceptCap = pcr.max(interceptCap, config.minInterceptCap)

        # throughfall = surplus above the interception storage threshold 
        throughfall = statesData.interceptStor + meteoData.precipitation - interceptCap
        throughfall = pcr.max(throughfall, 0.0)   

        # update interception storage after throughfall 
        interceptStor = statesData.interceptStor + meteoData.precipitation - throughfall
        interceptStor = pcr.max(interceptStor, 0.0)                              
                                    
        # potential interception flux (m/day)                 
        potInterceptionFlux = self.totalPotET
    
        # evaporation from intercepted water (based on potInterceptionFlux) - based on Van Beek et al. (2011)
        self.interceptEvap= potInterceptionFlux * (tmp.getValDivZero(interceptStor, interceptCap, config.smallNumber, 0.) ** (2.00/3.00))
        self.interceptEvap = pcr.min(interceptStor, self.interceptEvap)
        del potInterceptionFlux

        # update interception storage 
        interceptStor = pcr.max(0.0, interceptStor - self.interceptEvap)   
        
        # update potBareSoilEvap and potTranspiration after interceptEvap
        # fraction of potential bare soil evaporation and transpiration
        fracPotBareSoilEvap = pcr.max(0.0, pcr.min(1.0, tmp.getValDivZero(self.bareSoilPotET, 
                                                                            self.bareSoilPotET + self.transpirationPotET, 
                                                                            config.smallNumber, 0.0)))
        fracPotTranspiration = pcr.scalar(1.0 - fracPotBareSoilEvap)
        # substract interceptEvap from potBareSoilEvap and potTranspiration
        self.bareSoilPotET  = pcr.max(0.0, self.bareSoilPotET  - fracPotBareSoilEvap  * self.interceptEvap)
        self.transpirationPotET = pcr.max(0.0, self.transpirationPotET -  fracPotTranspiration * self.interceptEvap)   

        """ Calculation of Evaporation arising from snowFreeWater """
        # partitioning throughfall into snowfall and liquid Precipitation:
        estimSnowfall = pcr.ifthenelse(meteoData.temperature2m_K < config.freezingT,
                                meteoData.precipitation,
                                0.0)         

        # - snowfall (m/day)
        snowfall = estimSnowfall * tmp.getValDivZero(throughfall, meteoData.precipitation, config.smallNumber, 0.)   
        del estimSnowfall

        # - liquid precipitation (m/day)
        liquidPrecip = pcr.max(0.0, throughfall - snowfall)

        # changes in snow cover: - melt ; + gain in snow or refreezing
        deltaSnowCover = pcr.ifthenelse(meteoData.temperature2m_K <= config.freezingT,
                                        config.refreezingCoeff * statesData.snowFreeWater,
                                        # - pcr.min(input.initialConditions().snowCoverSWE, 
                                        (-1.0) * (pcr.min(statesData.snowCoverSWE, 
                                                 pcr.max(meteoData.temperature2m_K - config.freezingT, 0.0) * config.degreeDayFactor)*1.0*1.0))
        
        # update snowCoverSWE
        snowCoverSWE  = pcr.max(0.0, snowfall + deltaSnowCover + statesData.snowCoverSWE)

        snowFreeWater = statesData.snowFreeWater - deltaSnowCover + liquidPrecip  
        # netLqWaterToSoil = net liquid transferred to soil
        netLqWaterToSoil = pcr.max(0.0, snowFreeWater - config.snowWaterHoldingCap * snowCoverSWE)
        
        # update snowFreeWater (after netLqWaterToSoil) 
        snowFreeWater = pcr.max(0.0, snowFreeWater - netLqWaterToSoil)      

        # evaporation from snowFreeWater (based on potBareSoilEvap)
        self.actSnowFreeWaterEvap = pcr.min(snowFreeWater, \
                                            self.bareSoilPotET)       
                                       
        # update snowFreeWater and potBareSoilEvap
        snowFreeWater = pcr.max(0.0, snowFreeWater - self.actSnowFreeWaterEvap)  
                                                                     
        self.potBareSoilEvap = pcr.max(0, self.bareSoilPotET - self.actSnowFreeWaterEvap) 
                                                                    
        # update actual evaporation (after evaporation from snowFreeWater) 
        self.actualET = self.actSnowFreeWaterEvap + self.interceptEvap
               


if __name__ == "__main__":
    pass