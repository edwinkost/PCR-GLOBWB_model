#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# PCR-GLOBWB (PCRaster Global Water Balance) Global Hydrological Model
#
# Copyright (C) 2016, Edwin H. Sutanudjaja, Rens van Beek, Niko Wanders, Yoshihide Wada, 
# Joyce H. C. Bosmans, Niels Drost, Ruud J. van der Ent, Inge E. M. de Graaf, Jannis M. Hoch, 
# Kor de Jong, Derek Karssenberg, Patricia López López, Stefanie Peßenteiner, Oliver Schmitz, 
# Menno W. Straatsma, Ekkamol Vannametee, Dominik Wisser, and Marc F. P. Bierkens
# Faculty of Geosciences, Utrecht University, Utrecht, The Netherlands
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import types
#import routing

from pcraster.framework import *
import pcraster as pcr

import logging
logger = logging.getLogger(__name__)


import virtualOS as vos

class WaterBodies(object):

    def __init__(self, iniItems, landmask,landSurface,  onlyNaturalWaterBodies = False, lddMap = None):
        object.__init__(self)

        # clone map file names, temporary directory and global/absolute path of input directory
        self.landSurface = landSurface # INITIALIZE THE LAND COVER
        
        self.cloneMap = iniItems.cloneMap
        self.tmpDir   = iniItems.tmpDir
        self.inputDir = iniItems.globalOptions['inputDir']
        self.landmask = landmask
        
        self.iniItems = iniItems
                
        # upper and lower bound operating rule for reservoirs (in netcdf files)
        self.upper_bound_res_nc = None
        self.lower_bound_res_nc = None
        if "upper_bound_res_nc" in iniItems.routingOptions.keys(): self.upper_bound_res_nc = vos.getFullPath(iniItems.routingOptions["upper_bound_res_nc"], self.inputDir)
        if "lower_bound_res_nc" in iniItems.routingOptions.keys(): self.lower_bound_res_nc = vos.getFullPath(iniItems.routingOptions["lower_bound_res_nc"], self.inputDir)
        
        # local drainage direction:
        if lddMap is None:
            self.lddMap = vos.readPCRmapClone(iniItems.routingOptions['lddMap'],
                                                  self.cloneMap,self.tmpDir,self.inputDir,True)
            self.lddMap = pcr.lddrepair(pcr.ldd(self.lddMap))
            self.lddMap = pcr.lddrepair(self.lddMap)
        else:    
            self.lddMap = lddMap

        # the following is needed for a modflowOfflineCoupling run
        if 'modflowOfflineCoupling' in list(iniItems.globalOptions.keys()) and iniItems.globalOptions['modflowOfflineCoupling'] == "True" and 'routingOptions' not in iniItems.allSections: 
            logger.info("The 'routingOptions' are not defined in the configuration ini file. We will adopt them from the 'modflowParameterOptions'.")
            iniItems.routingOptions = iniItems.modflowParameterOptions

        print('logger worked')
        # option to activate water balance check
        self.debugWaterBalance = True
        if 'debugWaterBalance' in list(iniItems.routingOptions.keys()) and iniItems.routingOptions['debugWaterBalance'] == "False":
            self.debugWaterBalance = False
        
        # option to perform a run with only natural lakes (without reservoirs)
        self.onlyNaturalWaterBodies = onlyNaturalWaterBodies
        if "onlyNaturalWaterBodies" in list(iniItems.routingOptions.keys()) and iniItems.routingOptions['onlyNaturalWaterBodies'] == "True":
            logger.info("Using only natural water bodies identified in the year 1900. All reservoirs in 1900 are assumed as lakes.")
            self.onlyNaturalWaterBodies  = True
            self.dateForNaturalCondition = "1900-01-01"                  # The run for a natural condition should access only this date.   
        
        # names of files containing water bodies parameters
        self.useNetCDF = True
        if iniItems.routingOptions['waterBodyInputNC'] == str(None):
            self.useNetCDF = False
            self.fracWaterInp    = iniItems.routingOptions['fracWaterInp']
            self.waterBodyIdsInp = iniItems.routingOptions['waterBodyIds']
            self.waterBodyTypInp = iniItems.routingOptions['waterBodyTyp']
            self.resMaxCapInp    = iniItems.routingOptions['resMaxCapInp']
            self.resSfAreaInp    = iniItems.routingOptions['resSfAreaInp']
        else:
            self.useNetCDF = True
            self.ncFileInp       = vos.getFullPath(\
                                   iniItems.routingOptions['waterBodyInputNC'],\
                                   self.inputDir)

        # minimum width (m) used in the weir formula  # TODO: define minWeirWidth based on the GLWD, GRanD database and/or bankfull discharge formula 
        self.minWeirWidth = 10.

        # lower and upper limits at which reservoir release is terminated and 
        #                        at which reservoir release is equal to long-term average outflow
        # - default values
        

        self.minResvrFrac = 0.10
        self.maxResvrFrac = 0.75
        # - from the ini file
        if "minResvrFrac" in list(iniItems.routingOptions.keys()):
            minResvrFrac = iniItems.routingOptions['minResvrFrac']
            self.minResvrFrac = vos.readPCRmapClone(minResvrFrac,
                                                    self.cloneMap, self.tmpDir, self.inputDir)
        if "maxResvrFrac" in list(iniItems.routingOptions.keys()):
            maxResvrFrac = iniItems.routingOptions['maxResvrFrac']
            self.maxResvrFrac = vos.readPCRmapClone(maxResvrFrac,
                                                    self.cloneMap, self.tmpDir, self.inputDir)

        print('min fraction worked')
    def getParameterFiles(self,currTimeStep ,cellArea,ldd,\
                               initial_condition_dictionary = None,\
                               currTimeStepInDateTimeFormat = False):

        # parameters for Water Bodies: fracWat              
        #                              waterBodyIds
        #                              waterBodyOut
        #                              waterBodyArea 
        #                              waterBodyTyp
        #                              waterBodyCap
        
        # cell surface area (m2) and ldd
        self.cellArea = cellArea
        ldd = pcr.ifthen(self.landmask, ldd)
        
        # date used for accessing/extracting water body information
        if currTimeStepInDateTimeFormat:
            date_used = currTimeStep
            year_used = currTimeStep.year
        else:
            date_used = currTimeStep.fulldate
            year_used = currTimeStep.year
        if self.onlyNaturalWaterBodies == True:
            date_used = self.dateForNaturalCondition
            year_used = self.dateForNaturalCondition[0:4] 
        
        # fracWat = fraction of surface water bodies (dimensionless)
        self.fracWat = pcr.spatial(pcr.scalar(0.0))
        ## ADD FLOOD AND CONSERVATION FILES HERE
        
        ### I THINK THIS JUST READS IN FIELS ONCE.....
        #  # read in file
        # file_name = '/scratch/steya001/reservoir_operations/Turner_netcdfs/Turner_all.nc'
        day_val= currTimeStep.day
        month_val = currTimeStep.month
        # print(day_val)
        # print(month_val)
        #date = datetime.datetime(year_val, month_val, day_val)
        date = '2000-'+ str(month_val)+'-'+ str(day_val)
        print(date)
        file_name = '/scratch/depfg/steya001/final_turner_inputs/10_param_RF_bounds_final/' + date +".nc"
        # rhine
        #file_name = '/scratch/steya001/reservoir_operations/Turner_netcdfs_week_rhine/' + date +".nc"
        #print(file_name)
        #flood_pcr = vos.netcdf2PCRobjClone(file_name,varName='flood',  cloneMapFileName =self.cloneMap) # DOUBLE CHECK THIS
        #conservation_pcr = vos.netcdf2PCRobjClone(file_name,  varName ='conservation', cloneMapFileName =self.cloneMap) # DOUBLE CHECK THIS
        
        if currTimeStep.isFirstTimestep():
            self.turnerConservation = vos.netcdf2PCRobjClone(file_name,  varName ='conservation', cloneMapFileName =self.cloneMap) # DOUBLE CHECK THIS
            self.turnerFlood = vos.netcdf2PCRobjClone(file_name,  varName ='flood', cloneMapFileName =self.cloneMap) # DOUBLE CHECK THIS
        else:
            conservation_prior = vos.netcdf2PCRobjClone(file_name,  varName ='conservation', cloneMapFileName =self.cloneMap) # DOUBLE CHECK THIS
            self.turnerConservation = (self.turnerConservation *pcr.scalar(6/7)) + (pcr.scalar(1/7)* conservation_prior)
            flood_prior = vos.netcdf2PCRobjClone(file_name,varName='flood',  cloneMapFileName =self.cloneMap) # DOUBLE CHECK THIS
            self.turnerFlood =(self.turnerFlood *pcr.scalar(6/7)) + (pcr.scalar(1/7)* flood_prior)
        
        #self.turnerFlood= flood_pcr
        #self.turnerConservation = conservation_pcr
        print('started to read Turner files')
        command_area_file = '/scratch/depfg/steya001/final_turner_inputs/250_id_map_geodar_final.nc'
        #command_area_file = '/scratch/depfg/steya001/1km_rhine_command_area_10km_spread_final.nc'
        ca = vos.netcdf2PCRobjCloneWithoutTime(command_area_file,varName='area',  cloneMapFileName =self.cloneMap) # DOUBLE CHECK THIS
        self.sos_command_area = ca
        pcr.report(self.sos_command_area,'/scratch/depfg/steya001/ca_test.map')
        main_use_file = '/scratch/depfg/steya001/final_turner_inputs/reservoir_use.nc'
        use_check = vos.netcdf2PCRobjClone(main_use_file,varName='use_check',  cloneMapFileName =self.cloneMap) # DOUBLE CHECK THIS
        self.use = use_check
        print('finished reading Turner files')
        # command_area_650_file = '/scratch/steya001/command_areas/650_id_map_grand_final.nc'
        # ca_650 = vos. netcdf2PCRobjCloneWithoutTime(command_area_650_file,varName='area',  cloneMapFileName =self.cloneMap) # DOUBLE CHECK THIS
        # self.sos_650_ca = ca_650
        # command_area_1100_file = '/scratch/steya001/command_areas/1100_id_map_grand_final.nc'
        # ca_1100 = vos. netcdf2PCRobjCloneWithoutTime(command_area_1100_file,varName='area',  cloneMapFileName =self.cloneMap) # DOUBLE CHECK THIS
        # self.sos_1100_ca = ca_1100


        if self.useNetCDF:
            self.fracWat = vos.netcdf2PCRobjClone(self.ncFileInp,'fracWaterInp', \
                           date_used, useDoy = 'yearly',\
                           cloneMapFileName = self.cloneMap)
        else:
            if self.fracWaterInp != "None":
                self.fracWat = vos.readPCRmapClone(\
                               self.fracWaterInp+str(year_used)+".map",
                               self.cloneMap,self.tmpDir,self.inputDir)
        
        self.fracWat = pcr.cover(self.fracWat, pcr.spatial(pcr.scalar(0.0)))
        self.fracWat = pcr.max(0.0, self.fracWat)
        self.fracWat = pcr.min(1.0, self.fracWat)
        
        self.waterBodyIds  = pcr.spatial(pcr.nominal(0))    # waterBody ids
        self.waterBodyOut  = pcr.spatial(pcr.boolean(0))    # waterBody outlets
        self.waterBodyArea = pcr.spatial(pcr.scalar(0.))    # waterBody surface areas

        # water body ids
        if self.useNetCDF:
            self.waterBodyIds = vos.netcdf2PCRobjClone(self.ncFileInp,'waterBodyIds', \
                                date_used, useDoy = 'yearly',\
                                cloneMapFileName = self.cloneMap)
        else:
            if self.waterBodyIdsInp != "None":
                self.waterBodyIds = vos.readPCRmapClone(\
                    self.waterBodyIdsInp+str(year_used)+".map",\
                    self.cloneMap,self.tmpDir,self.inputDir,False,None,True)
        #
        self.waterBodyIds = pcr.ifthen(\
                            pcr.scalar(self.waterBodyIds) > 0.,\
                            pcr.nominal(self.waterBodyIds))    

        # water body outlets (correcting outlet positions)
        wbCatchment = pcr.catchmenttotal(pcr.scalar(1),ldd)
        self.waterBodyOut = pcr.ifthen(wbCatchment ==\
                            pcr.areamaximum(wbCatchment, \
                            self.waterBodyIds),\
                            self.waterBodyIds) # = outlet ids           # This may give more than two outlets, particularly if there are more than one cells that have largest upstream areas      
        # - make sure that there is only one outlet for each water body 
        self.waterBodyOut = pcr.ifthen(\
                            pcr.areaorder(pcr.scalar(self.waterBodyOut), \
                            self.waterBodyOut) == 1., self.waterBodyOut)
        self.waterBodyOut = pcr.ifthen(\
                            pcr.scalar(self.waterBodyIds) > 0.,\
                            self.waterBodyOut)
        
        # TODO: Please also consider endorheic lakes!                    

        # correcting water body ids
        self.waterBodyIds = pcr.ifthen(\
                            pcr.scalar(self.waterBodyIds) > 0.,\
                            pcr.subcatchment(ldd,self.waterBodyOut))
        
        # boolean map for water body outlets:   
        self.waterBodyOut = pcr.ifthen(\
                            pcr.scalar(self.waterBodyOut) > 0.,\
                            pcr.spatial(pcr.boolean(1)))

        # reservoir surface area (m2):
        if self.useNetCDF:
            resSfArea = 1000. * 1000. * \
                        vos.netcdf2PCRobjClone(self.ncFileInp,'resSfAreaInp', \
                        date_used, useDoy = 'yearly',\
                        cloneMapFileName = self.cloneMap)
        else:
            if self.resSfAreaInp != "None":
                resSfArea = 1000. * 1000. * vos.readPCRmapClone(
                       self.resSfAreaInp+str(year_used)+".map",\
                       self.cloneMap,self.tmpDir,self.inputDir)
            else:
                resSfArea = pcr.spatial(pcr.scalar(0.0))
        resSfArea = pcr.areaaverage(resSfArea,self.waterBodyIds)                        
        resSfArea = pcr.cover(resSfArea,0.)                        

        # water body surface area (m2): (lakes and reservoirs)
        self.waterBodyArea = pcr.max(pcr.areatotal(\
                             pcr.cover(\
                             self.fracWat*self.cellArea, 0.0), self.waterBodyIds),
                             pcr.areaaverage(\
                             pcr.cover(resSfArea, 0.0) ,       self.waterBodyIds))
        self.waterBodyArea = pcr.ifthen(self.waterBodyArea > 0.,\
                             self.waterBodyArea)
                                
        # correcting water body ids and outlets (exclude all water bodies with surfaceArea = 0)
        self.waterBodyIds = pcr.ifthen(self.waterBodyArea > 0.,
                            self.waterBodyIds)               
        self.waterBodyOut = pcr.ifthen(pcr.boolean(self.waterBodyIds),
                                                   self.waterBodyOut)

        # water body types:
        # - 2 = reservoirs (regulated discharge)
        # - 1 = lakes (weirFormula)
        # - 0 = non lakes or reservoirs (e.g. wetland)
        self.waterBodyTyp = pcr.nominal(0)
        
        if self.useNetCDF:
            self.waterBodyTyp = vos.netcdf2PCRobjClone(self.ncFileInp,'waterBodyTyp', \
                                date_used, useDoy = 'yearly',\
                                cloneMapFileName = self.cloneMap)
        else:
            if self.waterBodyTypInp != "None":
                self.waterBodyTyp = vos.readPCRmapClone(
                    self.waterBodyTypInp+str(year_used)+".map",\
                    self.cloneMap,self.tmpDir,self.inputDir,False,None,True)

        # excluding wetlands (waterBodyTyp = 0) in all functions related to lakes/reservoirs 
        #
        self.waterBodyTyp = pcr.ifthen(\
                            pcr.scalar(self.waterBodyTyp) > 0,\
                            pcr.nominal(self.waterBodyTyp))    
        self.waterBodyTyp = pcr.ifthen(\
                            pcr.scalar(self.waterBodyIds) > 0,\
                            pcr.nominal(self.waterBodyTyp))    
        self.waterBodyTyp = pcr.areamajority(self.waterBodyTyp,\
                                             self.waterBodyIds)     # choose only one type: either lake or reservoir                  
        self.waterBodyTyp = pcr.ifthen(\
                            pcr.scalar(self.waterBodyTyp) > 0,\
                            pcr.nominal(self.waterBodyTyp))    
        self.waterBodyTyp = pcr.ifthen(pcr.boolean(self.waterBodyIds),
                                                   self.waterBodyTyp)

        # correcting lakes and reservoirs ids and outlets
        self.waterBodyIds = pcr.ifthen(pcr.scalar(self.waterBodyTyp) > 0,
                                                  self.waterBodyIds)               
        self.waterBodyOut = pcr.ifthen(pcr.scalar(self.waterBodyIds) > 0,
                                                  self.waterBodyOut)

        # reservoir maximum capacity (m3):
        self.resMaxCap = pcr.scalar(0.0)
        self.waterBodyCap = pcr.scalar(0.0)
                                      

        if self.useNetCDF:
            self.resMaxCap = 1000. * 1000. * \
                             vos.netcdf2PCRobjClone(self.ncFileInp,'resMaxCapInp', \
                             date_used, useDoy = 'yearly',\
                             cloneMapFileName = self.cloneMap)
        else:
            if self.resMaxCapInp != "None":
                self.resMaxCap = 1000. * 1000. * vos.readPCRmapClone(\
                    self.resMaxCapInp+str(year_used)+".map", \
                    self.cloneMap,self.tmpDir,self.inputDir)

        self.resMaxCap = pcr.ifthen(self.resMaxCap > 0.,\
                                    self.resMaxCap)
        pcr.report(self.resMaxCap, '/scratch/depfg/steya001/cap_M44_pre.map') 
        self.resMaxCap = pcr.areaaverage(self.resMaxCap,\
                                         self.waterBodyIds)
        pcr.report(self.resMaxCap, '/scratch/depfg/steya001/cap_M44_post.map') 
        self.soswater_storage_check = self.resMaxCap                 
        # water body capacity (m3): (lakes and reservoirs)
        self.waterBodyCap = pcr.cover(self.resMaxCap,0.0)               # Note: Most of lakes have capacities > 0.
        self.waterBodyCap = pcr.ifthen(pcr.boolean(self.waterBodyIds),
                                                   self.waterBodyCap)
        
        #self.soswater_storage_check = self.waterBodyCap                               
        # correcting water body types:                                  # Reservoirs that have zero capacities will be assumed as lakes.
        self.waterBodyTyp = \
                 pcr.ifthen(pcr.scalar(self.waterBodyTyp) > 0.,\
                                       self.waterBodyTyp) 
        self.waterBodyTyp = pcr.ifthenelse(self.waterBodyCap > 0.,\
                                           self.waterBodyTyp,\
                 pcr.ifthenelse(pcr.scalar(self.waterBodyTyp) == 2,\
                                           pcr.nominal(1),\
                                           self.waterBodyTyp)) 
        pcr.report(self.waterBodyTyp, '/scratch/depfg/steya001/wb_type.map')                                

        # final corrections:
        self.waterBodyTyp = pcr.ifthen(self.waterBodyArea > 0.,\
                                       self.waterBodyTyp)                     # make sure that all lakes and/or reservoirs have surface areas
        self.waterBodyTyp = \
                 pcr.ifthen(pcr.scalar(self.waterBodyTyp) > 0.,\
                                       self.waterBodyTyp)                     # make sure that only types 1 and 2 will be considered in lake/reservoir functions
        self.waterBodyIds = pcr.ifthen(pcr.scalar(self.waterBodyTyp) > 0.,\
                            self.waterBodyIds)                                # make sure that all lakes and/or reservoirs have ids
        self.waterBodyOut = pcr.ifthen(pcr.scalar(self.waterBodyIds) > 0.,\
                                                  self.waterBodyOut)          # make sure that all lakes and/or reservoirs have outlets
        
        
        # for a natural run (self.onlyNaturalWaterBodies == True) 
        # which uses only the year 1900, assume all reservoirs are lakes
        if self.onlyNaturalWaterBodies == True and date_used == self.dateForNaturalCondition:
            logger.info("Using only natural water bodies identified in the year 1900. All reservoirs in 1900 are assumed as lakes.")
            self.waterBodyTyp = \
             pcr.ifthen(pcr.scalar(self.waterBodyTyp) > 0.,\
                        pcr.nominal(1))                         
        
        # check that all lakes and/or reservoirs have types, ids, surface areas and outlets:
        test = pcr.defined(self.waterBodyTyp) & pcr.defined(self.waterBodyArea) &\
               pcr.defined(self.waterBodyIds) & pcr.boolean(pcr.areamaximum(pcr.scalar(self.waterBodyOut), self.waterBodyIds))
        a,b,c = vos.getMinMaxMean(pcr.cover(pcr.scalar(test), 1.0) - pcr.scalar(1.0))
        threshold = 1e-3
        if abs(a) > threshold or abs(b) > threshold:
            logger.warning("Missing information in some lakes and/or reservoirs.")

        # at the beginning of simulation period (timeStepPCR = 1)
        # - we have to define/get the initial conditions 
        #
        if initial_condition_dictionary != None and currTimeStep.timeStepPCR == 1:
            self.getICs(initial_condition_dictionary)
        
        # For each new reservoir (introduced at the beginning of the year)
        # initiating storage, average inflow and outflow
        # PS: THIS IS NOT NEEDED FOR OFFLINE MODFLOW RUN! 
        #
        try:
            self.waterBodyStorage = pcr.cover(self.waterBodyStorage,0.0)
            self.avgInflow        = pcr.cover(self.avgInflow ,0.0)
            self.avgOutflow       = pcr.cover(self.avgOutflow,0.0)
            self.waterBodyStorage = pcr.ifthen(self.landmask, self.waterBodyStorage)
            self.avgInflow        = pcr.ifthen(self.landmask, self.avgInflow       )
            self.avgOutflow       = pcr.ifthen(self.landmask, self.avgOutflow      )
        except:
            # PS: FOR OFFLINE MODFLOW RUN!
            pass
        # TODO: Remove try and except    

        # cropping only in the landmask region:
        self.fracWat           = pcr.ifthen(self.landmask, self.fracWat         )
        self.waterBodyIds      = pcr.ifthen(self.landmask, self.waterBodyIds    ) 
        self.waterBodyOut      = pcr.ifthen(self.landmask, self.waterBodyOut    )
        self.waterBodyArea     = pcr.ifthen(self.landmask, self.waterBodyArea   )
        self.waterBodyTyp      = pcr.ifthen(self.landmask, self.waterBodyTyp    )  
        self.waterBodyCap      = pcr.ifthen(self.landmask, self.waterBodyCap    )

    def getICs(self,initial_condition):

        avgInflow  = initial_condition['avgLakeReservoirInflowShort']  
        avgOutflow = initial_condition['avgLakeReservoirOutflowLong'] 

        if initial_condition['waterBodyStorage'] is not None:
            # read directly 
            waterBodyStorage = initial_condition['waterBodyStorage']
        else:
            # calculate waterBodyStorage at cells where lakes and/or reservoirs are defined
            #
            storageAtLakeAndReservoirs = pcr.cover(\
             pcr.ifthen(pcr.scalar(self.waterBodyIds) > 0., initial_condition['channelStorage']), 0.0)
            #
            # - move only non negative values and use rounddown values
            storageAtLakeAndReservoirs = pcr.max(0.00, pcr.rounddown(storageAtLakeAndReservoirs))
            #
            # lake and reservoir storages = waterBodyStorage (m3) ; values are given for the entire lake / reservoir cells
            waterBodyStorage = pcr.ifthen(pcr.scalar(self.waterBodyIds) > 0., \
                                          pcr.areatotal(storageAtLakeAndReservoirs,\
                                                        self.waterBodyIds))
        
        self.avgInflow        = pcr.cover(avgInflow , 0.0)              # unit: m3/s 
        self.avgOutflow       = pcr.cover(avgOutflow, 0.0)              # unit: m3/s
        self.waterBodyStorage = pcr.cover(waterBodyStorage, 0.0)        # unit: m3

        self.avgInflow        = pcr.ifthen(self.landmask, self.avgInflow)
        self.avgOutflow       = pcr.ifthen(self.landmask, self.avgOutflow)
        self.waterBodyStorage = pcr.ifthen(self.landmask, self.waterBodyStorage)                                            

    def update(self,newStorageAtLakeAndReservoirs,\
                              timestepsToAvgDischarge,\
                           maxTimestepsToAvgDischargeShort,\
                           maxTimestepsToAvgDischargeLong,\
                           currTimeStep,\
                           env_flow,\
                           avgChannelDischarge,\
                           length_of_time_step = vos.secondsPerDay(),\
                           downstreamDemand = None):

        if self.debugWaterBalance:\
           preStorage = self.waterBodyStorage    # unit: m
     
        self.timestepsToAvgDischarge = timestepsToAvgDischarge          # TODO: include this one in "currTimeStep"     
        
        #self.readTurner(date)
        # obtain inflow (and update storage)
        self.moveFromChannelToWaterBody(\
         newStorageAtLakeAndReservoirs,\
             timestepsToAvgDischarge,\
             maxTimestepsToAvgDischargeShort,\
             length_of_time_step)
        #print(currTimeStep)
        # calculate outflow (and update storage)

        self.getWaterBodyOutflow(\
             maxTimestepsToAvgDischargeLong,\
             avgChannelDischarge,\
             env_flow,\
             length_of_time_step,\
             downstreamDemand,
             currTimeStep)
        
        if self.debugWaterBalance:\
           vos.waterBalanceCheck([          pcr.cover(self.inflow/self.waterBodyArea,0.0)],\
                                 [pcr.cover(self.waterBodyOutflow/self.waterBodyArea,0.0)],\
                                 [           pcr.cover(preStorage/self.waterBodyArea,0.0)],\
                                 [pcr.cover(self.waterBodyStorage/self.waterBodyArea,0.0)],\
                                   'WaterBodyStorage (unit: m)',\
                                  True,\
                                  currTimeStep.fulldate,threshold=5e-3)
        
        self.waterBodyBalance = (pcr.cover(self.inflow/self.waterBodyArea, 0.0) - pcr.cover(self.waterBodyOutflow/self.waterBodyArea,0.0)) -\
                                (pcr.cover(self.waterBodyStorage/self.waterBodyArea,0.0) - pcr.cover(preStorage/self.waterBodyArea,0.0))
                                  

    def moveFromChannelToWaterBody(self,\
                                   newStorageAtLakeAndReservoirs,\
                                   timestepsToAvgDischarge,\
                                   maxTimestepsToAvgDischargeShort,\
                                   length_of_time_step = vos.secondsPerDay()):
        # new lake and/or reservoir storages (m3)
        newStorageAtLakeAndReservoirs = pcr.cover(\
                                        pcr.areatotal(newStorageAtLakeAndReservoirs,\
                                                      self.waterBodyIds),0.0)

        # incoming volume (m3)
        self.inflow = newStorageAtLakeAndReservoirs - self.waterBodyStorage
        
        # TODO: Please check whether this inflow term includes evaporation loss?
        
        # inflowInM3PerSec (m3/s)                                       
        self.inflowInM3PerSec = self.inflow / length_of_time_step

        # updating (short term) average inflow (m3/s) ; 
        # - needed to constrain lake outflow:
        #
        temp = pcr.max(1.0, pcr.min(maxTimestepsToAvgDischargeShort, self.timestepsToAvgDischarge - 1.0 + length_of_time_step / vos.secondsPerDay()))
        deltaInflow = self.inflowInM3PerSec - self.avgInflow  
        R = deltaInflow * ( length_of_time_step / vos.secondsPerDay() ) / temp
        self.avgInflow = self.avgInflow + R                
        self.avgInflow = pcr.max(0.0, self.avgInflow)
        #
        # for the reference, see the "weighted incremental algorithm" in http://en.wikipedia.org/wiki/Algorithms_for_calculating_variance                        

        # updating waterBodyStorage (m3)
        self.waterBodyStorage = newStorageAtLakeAndReservoirs

        #self.getWaterBodyOutflow(\
        #     maxTimestepsToAvgDischargeLong,\
        #     avgChannelDischarge,\
        #     env_flow,\
        #     length_of_time_step,\
        #     downstreamDemand)
    def getWaterBodyOutflow(self,\
                            maxTimestepsToAvgDischargeLong,\
                            avgChannelDischarge,\
                            env_flow,\
                            length_of_time_step = vos.secondsPerDay(),\
                            downstreamDemand = None,
                            currTimeStep = None):

        # outflow in volume from water bodies with lake type (m3): 
        lakeOutflow = self.getLakeOutflow(avgChannelDischarge,length_of_time_step)  
             
        # outflow in volume from water bodies with reservoir type (m3): 
        if downstreamDemand is None:
            downstreamDemand = pcr.scalar(0.0)
        #length_of_time_step = vos.secondsPerDay()
        # THIS IS THE LINE TO !!!!! 
        # import numpy as np
        # discharge_map  = pcr.pcr2numpy(avgChannelDischarge, np.nan)
        # print("channel discharge " + str(np.nanmean(discharge_map)))
        
        # timestep = length_of_time_step#pcr.pcr2numpy(length_of_time_step, np.nan)
        # print("timestep " + str(timestep))
        
        # demand_map  = pcr.pcr2numpy(downstreamDemand, np.nan)
        # print("downstream demand " + str(np.nanmean(demand_map)))
        # irrigation = pcr.pcr2numpy(self.landSurface.irrGrossDemand, np.nan)
        # print("irrigation " + str(np.nanmean(irrigation)))
        
        # non_irrigation = pcr.pcr2numpy(self.landSurface.nonIrrGrossDemand, np.nan)
        # print("nonirrigation " + str(np.nanmean(non_irrigation)))
        
        #env_flow_np = pcr.pcr2numpy(env_flow, np.nan)
        #print("environmental flow  " + str(np.nanmean(env_flow_np)))
        
        reservoirOutflow= self.getReservoirOutflow_Turner(avgChannelDischarge,length_of_time_step,downstreamDemand, self.landSurface.irrGrossDemand, \
             self.landSurface.nonIrrGrossDemand, env_flow, currTimeStep)  # this is the one with Turner and right now we are turning it on manually 
        reservoirOutflow_old = self.getReservoirOutflow(avgChannelDischarge,length_of_time_step,downstreamDemand )  
        print(reservoirOutflow_old)
        #self.RensReduction = pcr.scalar(0)
        #pcr.report(reservoirOutflow_old, '/scratch/depfg/steya001/old_outflow_map_mri.map')
        # outgoing/release volume from lakes and/or reservoirs
        #print('reservoir infor ware read correctly')
        self.waterBodyOutflow = pcr.cover(reservoirOutflow, lakeOutflow)  
        
        #print('broke the waterbodies')
        # make sure that all water bodies have outflow:
        self.waterBodyOutflow = pcr.max(0.,
                                pcr.cover(self.waterBodyOutflow,0.0))

        # limit outflow to available storage
       
        factor = 0.25  # to avoid flip flop 
        self.waterBodyOutflow = pcr.min(self.waterBodyStorage * factor,\
                                        self.waterBodyOutflow)                    # unit: m3
        # use round values 
        self.waterBodyOutflow = pcr.rounddown(self.waterBodyOutflow/1.)*1.        # unit: m3
        
        # outflow rate in m3 per sec
        waterBodyOutflowInM3PerSec = self.waterBodyOutflow / length_of_time_step  # unit: m3/s

        # updating (long term) average outflow (m3/s) ; 
        # - needed to constrain/maintain reservoir outflow:
        #
        temp = pcr.max(1.0, pcr.min(maxTimestepsToAvgDischargeLong, self.timestepsToAvgDischarge - 1.0 + length_of_time_step / vos.secondsPerDay()))
        deltaOutflow    = waterBodyOutflowInM3PerSec - self.avgOutflow
        R = deltaOutflow * ( length_of_time_step / vos.secondsPerDay() ) / temp
        self.avgOutflow = self.avgOutflow + R                
        self.avgOutflow = pcr.max(0.0, self.avgOutflow)
        #
        # for the reference, see the "weighted incremental algorithm" in http://en.wikipedia.org/wiki/Algorithms_for_calculating_variance                        

        # update waterBodyStorage (after outflow):
        pre_storage = self.waterBodyStorage
        #pre_channel_stor = self.channelStorage
        self.waterBodyStorage = self.waterBodyStorage -\
                                self.waterBodyOutflow


        #post_channel = self.channelStorage
        self.waterBodyStorage = pcr.max(0.0, self.waterBodyStorage)  # PUT BACK IN                       
        #self.turner_current_stor = pcr.max(0.0, self.waterBodyStorage)
        #self.sos_outflow = waterBodyOutflowInM3PerSec
        #post_storage = self.waterBodyStorage
        #stor_difference = pre_storage - post_storage
        #check = pcr.max(pcr.abs(stor_difference))
        #value = pcr.cellvalue(check, 1,1)
        #pcr.report(post_storage, '/scratch/depfg/steya001/post_storage.map')
        #pcr.report(pre_storage, '/scratch/depfg/steya001/pre_storage.map')
        #print(value, "water body storage")
        #if value[0] >0:
        #    exit()
    def weirFormula(self,waterHeight,weirWidth): # output: m3/s
        sillElev  = pcr.scalar(0.0) 
        weirCoef  = pcr.scalar(1.0)
        weirFormula = \
         (1.7*weirCoef*pcr.max(0,waterHeight-sillElev)**1.5) *\
             weirWidth # m3/s
        return (weirFormula)

    def getLakeOutflow(self,\
        avgChannelDischarge,length_of_time_step = vos.secondsPerDay()):

        # waterHeight (m): temporary variable, a function of storage:
        minWaterHeight = 0.001 # (m) Rens used 0.001 m as the limit # this is to make sure there is always lake outflow,    
                                                                    # but it will be still limited by available self.waterBodyStorage 
        waterHeight = pcr.cover(
                      pcr.max(minWaterHeight, \
                      (self.waterBodyStorage - \
                      pcr.cover(self.waterBodyCap, 0.0))/\
                      self.waterBodyArea),0.)

        # weirWidth (m) : 
        # - estimated from avgOutflow (m3/s) using the bankfull discharge formula
        # 
        avgOutflow = self.avgOutflow
        avgOutflow = pcr.ifthenelse(\
                     avgOutflow > 0.,\
                     avgOutflow,
                     pcr.max(avgChannelDischarge,self.avgInflow,0.001))            # This is needed when new lakes/reservoirs introduced (its avgOutflow is still zero).
        avgOutflow = pcr.areamaximum(avgOutflow,self.waterBodyIds)              
        #
        bankfullWidth = pcr.cover(\
                        pcr.scalar(4.8) * \
                        ((avgOutflow)**(0.5)),0.)
        weirWidthUsed = bankfullWidth
        weirWidthUsed = pcr.max(weirWidthUsed,self.minWeirWidth)                   # TODO: minWeirWidth based on the GRanD database
        weirWidthUsed = pcr.cover(
                        pcr.ifthen(\
                        pcr.scalar(self.waterBodyIds) > 0.,\
                        weirWidthUsed),0.0)

        # avgInflow <= lakeOutflow (weirFormula) <= waterBodyStorage
        lakeOutflowInM3PerSec = pcr.max(\
                                self.weirFormula(waterHeight,weirWidthUsed),\
                                self.avgInflow)                                    # unit: m3/s
        
        # estimate volume of water relased by lakes
        lakeOutflow = lakeOutflowInM3PerSec * length_of_time_step                  # unit: m3
        lakeOutflow = pcr.min(self.waterBodyStorage, lakeOutflow)
        #
        lakeOutflow = pcr.ifthen(pcr.scalar(self.waterBodyIds) > 0., lakeOutflow)
        lakeOutflow = pcr.ifthen(pcr.scalar(self.waterBodyTyp) == 1, lakeOutflow)
        
        # TODO: Consider endorheic lake/basin. No outflow for endorheic lake/basin!

        return (lakeOutflow) 
    def getReservoirOutflow(self,\
        avgChannelDischarge,length_of_time_step,downstreamDemand):

        # avgOutflow (m3/s)
        avgOutflow = self.avgOutflow
        # The following is needed when new lakes/reservoirs introduced (its avgOutflow is still zero).
        #~ # - alternative 1
        #~ avgOutflow = pcr.ifthenelse(\
                     #~ avgOutflow > 0.,\
                     #~ avgOutflow,
                     #~ pcr.max(avgChannelDischarge, self.avgInflow, 0.001))
        # - alternative 2
        avgOutflow = pcr.ifthenelse(\
                     avgOutflow > 0.,\
                     avgOutflow,
                     pcr.max(avgChannelDischarge, self.avgInflow))
        avgOutflow = pcr.ifthenelse(\
                     avgOutflow > 0.,\
                     avgOutflow, pcr.downstream(self.lddMap, avgOutflow))
        avgOutflow = pcr.areamaximum(avgOutflow,self.waterBodyIds)              

        #self.current_stor_old = self.waterBodyStorage
        
        
        # calculate resvOutflow (m2/s) (based on reservoir storage and avgDischarge): 
        # - using reductionFactor in such a way that:
        #   - if relativeCapacity < minResvrFrac : release is terminated
        #   - if relativeCapacity > maxResvrFrac : longterm average
        reductionFactor = \
         pcr.cover(\
         pcr.min(1.,
         pcr.max(0., \
          self.waterBodyStorage - self.minResvrFrac*self.waterBodyCap)/\
             (self.maxResvrFrac - self.minResvrFrac)*self.waterBodyCap),0.0)
        #
        #self.RensReduction = reductionFactor
        resvOutflow = reductionFactor * avgOutflow * length_of_time_step                      # unit: m3

        # maximum release <= average inflow (especially during dry condition)
        resvOutflow  = pcr.max(0, pcr.min(resvOutflow, self.avgInflow * length_of_time_step)) # unit: m3                                          

        # downstream demand (m3/s)
        # reduce demand if storage < lower limit
        reductionFactor  = vos.getValDivZero(downstreamDemand, self.minResvrFrac*self.waterBodyCap, vos.smallNumber)
        reductionFactor  = pcr.cover(reductionFactor, 0.0)
        downstreamDemand = pcr.min(
                           downstreamDemand,
                           downstreamDemand*reductionFactor)
        # resvOutflow > downstreamDemand
        resvOutflow  = pcr.max(resvOutflow, downstreamDemand * length_of_time_step)           # unit: m3       

        # floodOutflow: additional release if storage > upper limit
        ratioQBankfull = 2.3
        estmStorage  = pcr.max(0.,self.waterBodyStorage - resvOutflow)
        floodOutflow = \
           pcr.max(0.0, estmStorage - self.waterBodyCap) +\
           pcr.cover(\
           pcr.max(0.0, estmStorage - self.maxResvrFrac*\
                                      self.waterBodyCap)/\
              ((1.-self.maxResvrFrac)*self.waterBodyCap),0.0)*\
           pcr.max(0.0,ratioQBankfull*avgOutflow* vos.secondsPerDay()-\
                                      resvOutflow)
        floodOutflow = pcr.max(0.0,
                       pcr.min(floodOutflow,\
                       estmStorage - self.maxResvrFrac*\
                                     self.waterBodyCap*0.75)) # maximum limit of floodOutflow: bring the reservoir storages only to 3/4 of upper limit capacities
        #self.sos_overtopping = self.waterBodyStorage + (self.avgInflow * length_of_time_step) - self.waterBodyCap
        # update resvOutflow after floodOutflow
        resvOutflow  = pcr.cover(resvOutflow , 0.0) +\
                       pcr.cover(floodOutflow, 0.0)                                            

        # maximum release if storage > upper limit : bring the reservoir storages only to 3/4 of upper limit capacities
        resvOutflow  = pcr.ifthenelse(self.waterBodyStorage > 
                       self.maxResvrFrac*self.waterBodyCap,\
                       pcr.min(resvOutflow,\
                       pcr.max(0,self.waterBodyStorage - \
                       self.maxResvrFrac*self.waterBodyCap*0.75)),
                       resvOutflow)                                            

        # if storage > upper limit : resvOutflow > avgInflow
        resvOutflow  = pcr.ifthenelse(self.waterBodyStorage > 
                       self.maxResvrFrac*self.waterBodyCap,\
                       pcr.max(0.0, resvOutflow, self.avgInflow),
                       resvOutflow)                                            
        
        # resvOutflow < waterBodyStorage
        resvOutflow = pcr.min(self.waterBodyStorage, resvOutflow)
        
        resvOutflow = pcr.ifthen(pcr.scalar(self.waterBodyIds) > 0., resvOutflow)
        resvOutflow = pcr.ifthen(pcr.scalar(self.waterBodyTyp) == 2, resvOutflow)
        self.sos_outflow= resvOutflow
        return (resvOutflow) # unit: m3  


    def getReservoirOutflow_Turner(self,avgChannelDischarge,length_of_time_step,downstreamDemand,\
                                irrGrossDemand, nonIrrGrossDemand, environmental_flow, currTimeStep = None):
        
        # get the upper and lower bound values from the self.upper_bound_res_nc and self.lower_bound_res_nc
        self.upper_bound_res = pcr.scalar(1.0)
        if self.upper_bound_res_nc is not None:
            date_used = currTimeStep.fulldate
            self.upper_bound_res = vos.netcdf2PCRobjClone(self.upper_bound_res_nc,\
                                                           varName = 'automatic', date_used, useDoy = 'yearly',\
                                                           cloneMapFileName = self.cloneMap)
        self.lower_bound_res = pcr.scalar(1.0)
        if self.lower_bound_res_nc is not None:
            date_used = currTimeStep.fulldate
            self.lower_bound_res = vos.netcdf2PCRobjClone(self.lower_bound_res_nc, \
                                                           varName = 'automatic', date_used, useDoy = 'yearly',\
                                                           cloneMapFileName = self.cloneMap)

        #import xarray as xr 
        # import numpy as np
        # discharge_map  = pcr.pcr2numpy(avgChannelDischarge, np.nan)
        # print("channel discharge in model  " + str(np.nanmean(discharge_map)))
        
        # timestep = length_of_time_step#pcr.pcr2numpy(length_of_time_step, np.nan)
        # print("timestep in model " + str(timestep))



        # #timestep = pcr.pcr2numpy(length_of_time_step, np.nan)
        # #print("timestep in model " + str(np.nanmean(timestep)))
        

        # demand_map  = pcr.pcr2numpy(downstreamDemand, np.nan)
        # print("downstream demand in model " + str(np.nanmean(demand_map)))
        # irrigation = pcr.pcr2numpy(irrGrossDemand, np.nan)
        # print("irrigation in model " + str(np.nanmean(irrigation)))
        
        # non_irrigation = pcr.pcr2numpy(nonIrrGrossDemand, np.nan)
        # print("nonirrigation in model " + str(np.nanmean(non_irrigation)))
        
        #env_flow_np = environmental_flow
        #print("environmental in model " + str(np.nanmean(env_flow_np)))
        
        ##### GET OUTFLOW OF RESERVOIR TO START #####
        # avgOutflow (m3/s)
        avgOutflow = self.avgOutflow
        
        # The following is needed when new lakes/reservoirs introduced (its avgOutflow is still zero).
        #~ # - alternative 1
        #~ avgOutflow = pcr.ifthenelse(\
                     #~ avgOutflow > 0.,\
                     #~ avgOutflow,
                     #~ pcr.max(avgChannelDischarge, self.avgInflow, 0.001))
        # - alternative 2

        avgOutflow = pcr.ifthenelse(\
                     avgOutflow > 0.,\
                     avgOutflow,
                     pcr.max(avgChannelDischarge, self.avgInflow))
        avgOutflow = pcr.ifthenelse(\
                     avgOutflow > 0.,\
                     avgOutflow, pcr.downstream(self.lddMap, avgOutflow))
        avgOutflow = pcr.areamaximum(avgOutflow,self.waterBodyIds)              
        self.sos_outflow_beginning = avgOutflow
        
        resvOutflow = (avgOutflow * length_of_time_step) # units = m3
        
        
        ## output sos_outflow_new, outflow * reduction factor, rf, check after irrigation, check after hydropower (1029), final outflow
       
        
        ## self turner flood and flood read/waterBodyCap
        
        
        #### CALCULATE THE FLOOD AND CONSERVATION POOLS #####
        #~ flood_read = self.turnerFlood/100 * self.waterBodyCap
        flood_read = pcr.min(self.upper_bound_res * self.waterBodyCap, self.waterBodyCap)
        
        #print('flood max is' + str(np.nanmax(pcr.pcr2numpy(self.turnerFlood, mv = np.nan))))
        #~ conserve_read = self.turnerConservation/100 *self.waterBodyCap
        conserve_read = self.lower_bound_res * self.waterBodyCap
        
        flood_read = pcr.max(conserve_read, flood_read)

        #print('enter get res and tried to cover')
        self.flood_cap1 = flood_read/self.waterBodyCap
        fill_factor = 1
        flood_final = pcr.min(flood_read, self.waterBodyCap*fill_factor) # fills in missing values in flood with waterbody cap
        conservation_final = pcr.ifthenelse(conserve_read <0, self.waterBodyCap*0.1, conserve_read)
        
        ## MAYBE ADD IN 
        ####conservation_final = pcr.ifthenelse(conservation_positive ==0, self.waterBodyCap*0.1, conservation_positive) # make sure we can't have 0
        #conservation_final = pcr.ifthenelse(conservation_positive ==0, self.waterBodyCap*0.1, conservation_positive)

        #conservation_final = pcr.max(conserve_read, waterBodyCap*0.1)
        #print(pcr.pcr2numpy(xflood_final, mv = -99))

        self.turnerFloodF = flood_read
        self.turnerConserveF = conservation_final
        #print('cover worked')\

        ### INITIALIZE THE ENV FLOW, INFLOW AND CURRENT STORAGE
        #environmental_flow
        bankfull = 2.3

        inflow_res = pcr.ifthenelse(self.inflowInM3PerSec < 0. , pcr.scalar(0), self.inflowInM3PerSec)*86400
        #inflow_res = self.inflow_pcr
        self.sos_inflow = inflow_res
        # TODO IS WATER BODY STORAGE CUBED! CHECK UNITS
        self.turner_starting_storage = self.waterBodyStorage #pcr.cover(current_storage, pcr.scalar(0.0)) - pcr.cover(resvOutflow, pcr.scalar(0))

        current_storage = self.waterBodyStorage #####+ pcr.max(inflow_res, pcr.scalar(0)) # this gives
        self.sos_overtopping = current_storage - self.waterBodyCap
        # CHANGE
        #self.turner_starting_storage = current_storage
        ### CALCULATE REDUCTION FACTORS ####
        #max((current_storage -conservation)/(flood - conservation)* bankfull, 0)
        
        floodFactor = pcr.scalar(1.5)     
        #RF_bankfull = pcr.ifthenelse((current_storage =< flood_final), ((current_storage-conservation_final)/(flood_final - conservation_final) * floodFactor), floodFactor)
   
        RF_bankfull = pcr.ifthenelse((current_storage <= flood_final), ((current_storage-conservation_final)/(flood_final - conservation_final) * floodFactor), floodFactor)
        RF_bankfull = pcr.ifthenelse((current_storage > flood_final), ((current_storage-flood_final)/(self.waterBodyCap - flood_final)*(pcr.scalar(2.3)-floodFactor) + RF_bankfull),RF_bankfull)
        #RF_bankfull = ((current_storage-conservation_final)/(flood_final - conservation_final)) #*pcr.scalar(bankfull)
        #RF_bankfull = pcr.ifthenelse((current_storage > flood_final), (current_storage-flood_final)/(self.waterBodyCap - flood_final),RF_bankfull)
        #self.turnerReduction = RF_bankfull
        reduction_factor = pcr.max(pcr.min(RF_bankfull, pcr.scalar(2.3)), pcr.scalar(0)) #pcr.max(RF_bankfull, pcr.scalar(0))
        #reduction_factor = pcr.ifthenelse((reduction_factor > bankfull) & (current_storage > flood_final), bankfull, reduction_factor)
        #pcr.report( RF_bankfull <0, '/scratch/steya001/pcrglobwb2_reservoirs/negstorage_stability_check.map'))
        self.turnerReduction = reduction_factor

        #self.turnerReduction = reduction_factor
        
        ### CAP this at 1?
        rf_demand_calculation = (current_storage - 0.1*self.waterBodyCap)/(flood_final - 0.1*self.waterBodyCap) #(conservation_final - 0.1*self.waterBodyCap)
        #demand_reduction_factor_initial = pcr.ifthenelse((rf_demand_calculation >1), pcr.scalar(1), rf_demand_calculation)

        demand_reduction_factor = pcr.max(rf_demand_calculation,pcr.scalar(0))
        demand_reduction_factor = pcr.min(demand_reduction_factor, pcr.scalar(1))
        self.reductionFactorDemand = self.waterBodyCap#demand_reduction_factor

        
        non_hydropower_check = pcr.scalar(self.use)#* pcr.scalar(0)
        self.hydropower_check = non_hydropower_check
        
        self.sw_abstraction_check = pcr.ifthenelse((non_hydropower_check == pcr.scalar(1)), demand_reduction_factor, pcr.scalar(0))
        ###### CALCULATE TOTAL DEMAND ######

        # Total demand = irrigation plus non irrigation
        demand_tot = irrGrossDemand + nonIrrGrossDemand # each is in m/day

        # # demand tot = 0.00609 cell area at the point in question is68010392.0 so the multiplication should be 41445.5328848
        downstreamDemand= demand_tot*self.cellArea # DEMAND IS IN m/day after this step to get to m3/day it needs to be multiplied by cell area

        # ## THIS IS FOR THE AREA
        downstreamDemand = pcr.cover(pcr.areatotal(downstreamDemand, pcr.nominal(self.sos_command_area)),pcr.scalar(0)) # this aggregates all the demand over the things with the same number
        #pcr.report(downstreamDemand, '/scratch/steya001/test_demand.map') # writes out the map so I can make sure that it's right

        # ## THIS IS FOR THE SINGLE POINT 
        #downstreamDemand =  pcr.ifthen(pcr.scalar(self.waterBodyTyp)==2.0, downstreamDemand)
        #downstreamDemand =  pcr.ifthen(pcr.scalar(self.waterBodyIds) >0., downstreamDemand)
        #downstreamDemand =  pcr.ifthen(pcr.scalar(self.waterBodyIds) >0., downstreamDemand)

        #max_demand = total_demand_pcr
        
        ### CHANGE THIS 
        max_demand = downstreamDemand #* pcr.scalar(0)
        self.sosdemand = max_demand

        resvOutflow = resvOutflow * reduction_factor # output
        self.sos_outflow_reduction = resvOutflow
        environmental_flow = environmental_flow * length_of_time_step
        
        #pcr.report(((current_storage - resvOutflow ) > self.waterBodyCap), '/scratch/steya001/pcrglobwb2_reservoirs/flood_check.map')

        ##### ACTIVE STORAGE FOR NON HYDROPOWER ######
        ### NOT GOING IN HERE ##### 
        resvOutflow  = pcr.ifthenelse(((resvOutflow  < max_demand) &(non_hydropower_check ==pcr.scalar(1))), (max_demand*demand_reduction_factor), resvOutflow )        
        #$pcr.report(((resvOutflow  < max_demand) &(non_hydropower_check ==pcr.scalar(1))), '/scratch/steya001/pcrglobwb2_reservoirs/active_storage_nonhydropower.map')
        self.resoutflow_irrigation = resvOutflow
        
        ### ACTIVE STORAGE FOR HYDROPOWER #### # TODO CHECK THIS ONE
        resvOutflow_hydropower =  pcr.ifthenelse(((resvOutflow  < max_demand) & (non_hydropower_check ==pcr.scalar(0))),(max_demand*reduction_factor/bankfull), resvOutflow )
        #resvOutflow_hydropower =  pcr.ifthenelse(((resvOutflow  < max_demand) & (non_hydropower_check ==pcr.scalar(0))),(max_demand*reduction_factor), resvOutflow )
        
        current_storage_hydropower = current_storage - resvOutflow_hydropower
        #pcr.report((max_demand*reduction_factor/bankfull), '/scratch/steya001/pcrglobwb2_reservoirs/max_demand.map')
        #pcr.report(((resvOutflow  < max_demand) & (non_hydropower_check ==pcr.scalar(0))), '/scratch/steya001/pcrglobwb2_reservoirs/active_stroage_hydropower.map')
        hydropower_release = pcr.max((current_storage - conservation_final), 0)

        # WENT IN HERE FOR NO HYDROPOWR
        #I think I want this to  work whether or not it's less than conseration
        # ithink this is greater than
        #resvOutflow  = pcr.ifthenelse( ((current_storage_hydropower < conservation_final) &(non_hydropower_check ==pcr.scalar(0)) ),hydropower_release, resvOutflow )
        resvOutflow  = pcr.ifthenelse( ((current_storage_hydropower < conservation_final) &(non_hydropower_check ==pcr.scalar(0)) ),hydropower_release, resvOutflow_hydropower )
        self.resoutflow_hydropower = resvOutflow # first run  
        #pcr.report(((current_storage_hydropower < conservation_final)&(non_hydropower_check ==pcr.scalar(0))), '/scratch/steya001/pcrglobwb2_reservoirs/storage_less_conservation.map')

        hydropower_storage_stable_check = current_storage - resvOutflow
        resvOutflow = pcr.ifthenelse(((hydropower_storage_stable_check < conservation_final) & (non_hydropower_check ==pcr.scalar(0))), environmental_flow, resvOutflow)
        #pcr.report(((hydropower_storage_stable_check < conservation_final) & (non_hydropower_check ==pcr.scalar(0))), '/scratch/steya001/pcrglobwb2_reservoirs/hydrostorage_stability_check.map')
        self.resoutflow_hydropower = resvOutflow # second run 
###### FLOOD VALUES ######



        # TODO CHECK UNITS

        #### NON NEGATIVE STORAGE CHECK
        #test_storage_non_neg = current_storage - resvOutflow 
        #release = release/bankfull * (1-flood/cap_215)
        #resvOutflow  = pcr.ifthenelse(test_storage_non_neg <0, pcr.roundoff((resvOutflow /bankfull * (1-flood_final/self.waterBodyCap))), resvOutflow )
        #resvOutflow  = pcr.ifthenelse(test_storage_non_neg <0, pcr.roundoff((resvOutflow * (1-flood_final/self.waterBodyCap))), resvOutflow )
        #resvOutflow  = pcr.ifthenelse(test_storage_non_neg <0, current_storage - 0.1*self.waterBodyCap, resvOutflow )
        #pcr.report(test_storage_non_neg <0, '/scratch/steya001/pcrglobwb2_reservoirs/negstorage_stability_check.map')

        ### ENV FLOW CHECK
        test_env_flow = current_storage - environmental_flow
        resvOutflow = pcr.ifthenelse((resvOutflow < environmental_flow) & (test_env_flow >0), environmental_flow, resvOutflow)
        #pcr.report((resvOutflow < environmental_flow) & (test_env_flow >0), '/scratch/steya001/pcrglobwb2_reservoirs/envflow_check.map')
        ## CATCH FOR DEAD STORAGE

        low_storage = current_storage - resvOutflow
        new_release = current_storage - 0.1*self.waterBodyCap
        resvOutflow = pcr.ifthenelse(((low_storage < (0.1*self.waterBodyCap)) & (non_hydropower_check == pcr.scalar(1))), pcr.max(new_release,0), resvOutflow)

        resvOutflow = pcr.ifthenelse(((current_storage - resvOutflow) < conservation_final ) & (non_hydropower_check ==pcr.scalar(0)), pcr.max((current_storage - conservation_final),0),resvOutflow)

        #resvOutflow = pcr.ifthen(pcr.scalar(self.waterBodyIds) > 0., resvOutflow)
        #resvOutflow = pcr.ifthen(pcr.scalar(self.waterBodyTyp) == 2, resvOutflow)
    
        flood_difference = current_storage - resvOutflow  - self.waterBodyCap
        resvOutflow  = pcr.ifthenelse(((current_storage - resvOutflow ) > self.waterBodyCap), (resvOutflow +flood_difference), resvOutflow )

   
        #TODO DOUBLE CHECK THAT WATERBODY STORGE GETS UPDATED 

        resvOutflow = pcr.ifthen(pcr.scalar(self.waterBodyIds) > 0., resvOutflow)
        resvOutflow = pcr.ifthen(pcr.scalar(self.waterBodyTyp) == 2, resvOutflow)



        ## CHECK STORAGE 
        #self.sos_outflow = resvOutflow
        self.turner_current_stor = pcr.cover(current_storage, pcr.scalar(0.0)) - pcr.cover(resvOutflow, pcr.scalar(0))
        self.sos_outflow_end = resvOutflow
        #self.sos_outlfow_final = resvOutflow
        #print('ready to return it all')
        #print('ready to return it all')
        self.fraction_stor= (current_storage - resvOutflow )/self.waterBodyCap
        pcr.report(self.turner_current_stor/self.waterBodyCap, '/scratch/depfg/steya001/fractional_storage.map')

        return (resvOutflow) # unit: m3 /s 

