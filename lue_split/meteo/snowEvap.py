 
 def snowMeltHBVSimple(snowfall):
    #TODO is it in Kelvin or DegC

        # changes in snow cover: - melt ; + gain in snow or refreezing
        deltaSnowCover = pcr.ifthenelse(input.meteoData().temperature2m_K <= config.freezingT,
                                        config.refreezingCoeff*input.initialConditions()snowFreeWater,
                                        -pcr.min(input.initialConditions().snowCoverSWE, pcr.max(meteo.temperature - config.freezingT, 0.0) * config.degreeDayFactor)*1.0*1.0)
       
        # update snowCoverSWE
        snowCoverSWE  = pcr.max(0.0, snowfall + deltaSnowCover + input.initialConditions().snowCoverSWE) # SC_L[TYPE] = max(0.0, SC_L[TYPE]+DSC[TYPE]+SNOW)

        # # for reporting snow melt in m/day
        # self.snowMelt = pcr.ifthenelse(deltaSnowCover < 0.0, deltaSnowCover * pcr.scalar(-1.0), pcr.scalar(0.0))

        # update snowFreeWater = liquid water stored above snowCoverSWE
        self.snowFreeWater = self.snowFreeWater - deltaSnowCover + \
                             self.liquidPrecip                          # SCF_L[TYPE] = SCF_L[TYPE]-DSC[TYPE]+PRP;
                                     
        # # netLqWaterToSoil = net liquid transferred to soil
        # self.netLqWaterToSoil = pcr.max(0., self.snowFreeWater - \
        #          self.snowWaterHoldingCap * self.snowCoverSWE)          # Pn = max(0,SCF_L[TYPE]-CWH*SC_L[TYPE])
        
        # # update snowFreeWater (after netLqWaterToSoil) 
        # self.snowFreeWater    = pcr.max(0., self.snowFreeWater - \
        #                                     self.netLqWaterToSoil)      # SCF_L[TYPE] = max(0,SCF_L[TYPE]-Pn)

        # evaporation from snowFreeWater (based on potBareSoilEvap)
        self.actSnowFreeWaterEvap = pcr.min(self.snowFreeWater, \
                                            self.potBareSoilEvap)       # ES_a[TYPE] = min(SCF_L[TYPE],ES_p[TYPE])
                                       
        # # update snowFreeWater and potBareSoilEvap
        # self.snowFreeWater = pcr.max(0.0, \
        #                      self.snowFreeWater - self.actSnowFreeWaterEvap)  
        #                                                                 # SCF_L[TYPE]= SCF_L[TYPE]-ES_a[TYPE]
        # self.potBareSoilEvap = pcr.max(0, \
        #                    self.potBareSoilEvap - self.actSnowFreeWaterEvap) 
        #                                                                 # ES_p[TYPE]= max(0,ES_p[TYPE]-ES_a[TYPE])

        # # update actual evaporation (after evaporation from snowFreeWater) 
        # self.actualET += self.actSnowFreeWaterEvap                      # EACT_L[TYPE]= EACT_L[TYPE]+ES_a[TYPE];

        return deltaSnowCover