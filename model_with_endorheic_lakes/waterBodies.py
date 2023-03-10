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

from copy import copy

from pcraster.framework import *
import pcraster as pcr

import logging
logger = logging.getLogger(__name__)


import virtualOS as vos

# global variable
NoneType = type(None)

class WaterBodies(object):

    def __init__(self, iniItems, landmask, onlyNaturalWaterBodies = False, lddMap = None):
        object.__init__(self)

        # clone map file names, temporary directory and global/absolute path of input directory
        self.cloneMap = iniItems.cloneMap
        self.tmpDir   = iniItems.tmpDir
        self.inputDir = iniItems.globalOptions['inputDir']
        self.landmask = landmask
        
        self.iniItems = iniItems
                
        # local drainage direction:
        if isinstance(lddMap, types.NoneType):
            self.lddMap = vos.readPCRmapClone(iniItems.routingOptions['lddMap'],
                                                  self.cloneMap,self.tmpDir,self.inputDir,True)
            self.lddMap = pcr.lddrepair(pcr.ldd(self.lddMap))
            self.lddMap = pcr.lddrepair(self.lddMap)
        else:    
            self.lddMap = lddMap

        # the following is needed for a modflowOfflineCoupling run
        if 'modflowOfflineCoupling' in iniItems.globalOptions.keys() and iniItems.globalOptions['modflowOfflineCoupling'] == "True" and 'routingOptions' not in iniItems.allSections: 
            logger.info("The 'routingOptions' are not defined in the configuration ini file. We will adopt them from the 'modflowParameterOptions'.")
            iniItems.routingOptions = iniItems.modflowParameterOptions


        # option to activate water balance check
        self.debugWaterBalance = True
        if 'debugWaterBalance' in iniItems.routingOptions.keys() and iniItems.routingOptions['debugWaterBalance'] == "False":
            self.debugWaterBalance = False
        
        # option to perform a run with only natural lakes (without reservoirs)
        self.onlyNaturalWaterBodies = onlyNaturalWaterBodies
        if "onlyNaturalWaterBodies" in iniItems.routingOptions.keys() and iniItems.routingOptions['onlyNaturalWaterBodies'] == "True":
            logger.info("Using only natural water bodies identified in the year 1900. All reservoirs in 1900 are assumed as lakes.")
            self.onlyNaturalWaterBodies  = True
        self.dateForNaturalCondition = "1900-01-01"                  # The run for a natural condition should access only this date.   

        # RvB Oct 2019: water outlets and endorheic lakes added as default
        self.waterBodyOutInp = None
        self.endorheicLakesInp = None
        
        # names of files containing water bodies parameters
        if iniItems.routingOptions['waterBodyInputNC'] == str(None):
            self.useNetCDF = False
            self.fracWaterInp    = iniItems.routingOptions['fracWaterInp']
            self.waterBodyIdsInp = iniItems.routingOptions['waterBodyIds']
            self.waterBodyTypInp = iniItems.routingOptions['waterBodyTyp']
            self.resMaxCapInp    = iniItems.routingOptions['resMaxCapInp']
            self.resSfAreaInp    = iniItems.routingOptions['resSfAreaInp']

            # RvB Oct 2019: water outlets and endorheic lakes added
            if 'waterBodyOutInp' in iniItems.routingOptions.keys():
                self.waterBodyOutInp = iniItems.routingOptions['waterBodyOutInp']
            if 'endorheicLakes'in iniItems.routingOptions.keys():
                self.endorheicLakes = iniItems.routingOptions['endorheicLakes']

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
        if "minResvrFrac" in iniItems.routingOptions.keys():
            minResvrFrac = iniItems.routingOptions['minResvrFrac']
            self.minResvrFrac = vos.readPCRmapClone(minResvrFrac,
                                                    self.cloneMap, self.tmpDir, self.inputDir)
        if "maxResvrFrac" in iniItems.routingOptions.keys():
            maxResvrFrac = iniItems.routingOptions['maxResvrFrac']
            self.maxResvrFrac = vos.readPCRmapClone(maxResvrFrac,
                                                    self.cloneMap, self.tmpDir, self.inputDir)

    def getParameterFiles(self, current_time_step, cellarea, ldd,\
                               initial_condition_dictionary = None,\
                               current_time_step_as_date = False):

        # variables for water bodies:  fracWat
        #                              waterBodyIds
        #                              waterBodyOut
        #                              waterBodyLoc
        #                              waterBodyArea 
        #                              waterBodyTyp
        #                              waterBodyCap
        #                              endorheicLakes

        # NOTE: the use of a separate LDD in this function may not be
        #       be compatible with the LDD specified in this class!

        # the following is included to make this function compatible with
        # python 3
        # cell surface area (m2), ldd, clone and land mask
        cellarea = pcr.ifthen(self.landmask, cellarea)
        ldd = pcr.ifthen(self.landmask, ldd)
        clone    = self.cloneMap
        landmask = self.landmask
        tmpdir   = self.tmpDir
        inputdir = self.inputDir
        
        only_natural_waterbodies = self.onlyNaturalWaterBodies
        date_natural_condition   = self.dateForNaturalCondition

        read_nc_field  = vos.netcdf2PCRobjClone
        read_pcr_field = vos.readPCRmapClone
        
        read_nc_input = self.useNetCDF
        if read_nc_input:
            ncfile = self.ncFileInp
        else:
            ncfile = None
        
        # this may be modified accordingly later

        # the following is intended to facilitate reading in the variable fields
        # from the different input types
        waterbody_variable_info = {}
        
        # create dummy input for PCRaster files if they do not exist: set them
        # to None
        # waterBodyIds waterBodyTyp waterBodyOut endorheicLakes fracWaterInp resMaxCapInp resSfAreaInp
        for pcr_inp_name in [\
                             'fracWaterInp', \
                             'waterBodyIds', \
                             'waterBodyOutInp', \
                             'waterBodyTypInp', \
                             'resSfAreaInp', \
                             'resMaxCapInp', \
                             'endorheicLakesInp', \
                             ]:
            if pcr_inp_name not in vars(self).keys():
                setattr(self, pcr_inp_name, None)

        # fraction water
        variable_name = 'fraction_water'
        var_inp_name  = 'fracWaterInp'
        alt_var_name  = 'fracWat'
        pcr_inp_name  = self.fracWaterInp
        pcr_data_type = pcr.scalar
        waterbody_variable_info[variable_name] = { \
                        'var_inp_name'  : var_inp_name, \
                        'alt_var_name'  : alt_var_name, \
                        'pcr_inp_name'  : pcr_inp_name, \
                        'pcr_data_type' : pcr_data_type, \
                        }
        # water body ID
        variable_name = 'water_body_id'
        var_inp_name  = 'waterBodyIds'
        alt_var_name  = 'waterBodyIds'
        pcr_inp_name  = self.waterBodyIds
        pcr_data_type = pcr.nominal
        waterbody_variable_info[variable_name] = { \
                        'var_inp_name'  : var_inp_name, \
                        'alt_var_name'  : alt_var_name, \
                        'pcr_inp_name'  : pcr_inp_name, \
                        'pcr_data_type' : pcr_data_type, \
                        }
        # water body type
        variable_name = 'water_body_type'
        var_inp_name  = 'waterBodyTyp'
        alt_var_name  = 'waterBodyTyp'
        pcr_inp_name  = self.waterBodyTypInp
        pcr_data_type = pcr.nominal
        waterbody_variable_info[variable_name] = { \
                        'var_inp_name'  : var_inp_name, \
                        'alt_var_name'  : alt_var_name, \
                        'pcr_inp_name'  : pcr_inp_name, \
                        'pcr_data_type' : pcr_data_type, \
                        }
        # water body outlet
        variable_name = 'water_body_out'
        var_inp_name  = 'waterBodyOut'
        alt_var_name  = 'waterBodyOut'
        pcr_inp_name  = self.waterBodyOutInp
        pcr_data_type = pcr.nominal
        waterbody_variable_info[variable_name] = { \
                        'var_inp_name'  : var_inp_name, \
                        'alt_var_name'  : alt_var_name, \
                        'pcr_inp_name'  : pcr_inp_name, \
                        'pcr_data_type' : pcr_data_type, \
                        }
        # water body area
        variable_name = 'water_body_area'
        var_inp_name  = 'resSfAreaInp'
        alt_var_name  = 'waterBodyArea'
        pcr_inp_name  = self.resSfAreaInp
        pcr_data_type = pcr.scalar
        waterbody_variable_info[variable_name] = { \
                        'var_inp_name'  : var_inp_name, \
                        'alt_var_name'  : alt_var_name, \
                        'pcr_inp_name'  : pcr_inp_name, \
                        'pcr_data_type' : pcr_data_type, \
                        }

        # water body capacity
        variable_name = 'water_body_capacity'
        var_inp_name  = 'resMaxCapInp'
        alt_var_name  = 'waterBodyCap'
        pcr_inp_name  = self.resMaxCapInp
        pcr_data_type = pcr.scalar
        waterbody_variable_info[variable_name] = { \
                        'var_inp_name'  : var_inp_name, \
                        'alt_var_name'  : alt_var_name, \
                        'pcr_inp_name'  : pcr_inp_name, \
                        'pcr_data_type' : pcr_data_type, \
                        }
        # endorheic lakes
        variable_name = 'endorheic_lakes'
        var_inp_name  = 'endorheicLakes'
        alt_var_name  = 'endorheicLakes'
        pcr_inp_name  = self.endorheicLakesInp
        pcr_data_type = pcr.boolean
        waterbody_variable_info[variable_name] = { \
                        'var_inp_name'  : var_inp_name, \
                        'alt_var_name'  : alt_var_name, \
                        'pcr_inp_name'  : pcr_inp_name, \
                        'pcr_data_type' : pcr_data_type, \
                        }

        # setting dates and general variables
        # date used for accessing/extracting water body information
        if current_time_step_as_date:
            date_used = current_time_step
            year_used = current_time_step.year
        else:
            date_used = current_time_step.fulldate
            year_used = current_time_step.year
        if only_natural_waterbodies:
            date_used = date_natural_condition
            year_used = date_natural_condition[0:4] 

        # read in all variables for the current year
        for variable_name, var_info in waterbody_variable_info.items():

            # get the information from the variable name
            var_inp_name  = var_info['var_inp_name']
            pcr_inp_name  = var_info['pcr_inp_name']
            pcr_data_type = var_info['pcr_data_type']
        
            # read the input; set default value of the variable to None
            var_field = None
            pcrfile   = None
            
            if read_nc_input:
                
                try:
                
                    nc_date_used = date_used
                    if variable_name == 'endorheic_lakes':
                        nc_date_used = date_natural_condition
                    var_field = read_nc_field(ncfile, var_inp_name, nc_date_used, \
                                              useDoy = 'yearly', \
                                              cloneMapFileName = clone)

                    message_str = 'Information on %s for %s read from netCDF file' % \
                                  (variable_name, str(year_used))

                except:
                    
                    message_str = 'No information on %s for %s could be read from netCDF file' % \
                                  (variable_name, str(year_used))

            else:

                try:
                    pcrfile = str.join(''\
                                       (pcr_inp_name, str(year_used),'.map'))
                    var_field = read_pcr_field(pcrfile, clone, tmpdir, inputdir)

                    message_str = 'Information on %s for %s read from PCRaster file' % \
                                (variable_name, str(year_used))

                except:

                    message_str = 'No information on %s for %s could be read from PCRaster file' % \
                                (variable_name, str(year_used))

            #set the variable
            if not isinstance(var_field, NoneType):
                setattr(self, variable_name, pcr_data_type(pcr.ifthen(landmask, \
                        var_field)))
            else:
                setattr(self, variable_name, var_field)

            # log info
            logger.info(message_str)

        # all direct input read, progressively develop all fields
        # if no information is provided, set a default value;
        # and clip it to the correct extent
        
        # set local water area
        self.water_area = self.fraction_water * cellarea
        
        # water bodies
        pcr_data_type = waterbody_variable_info['water_body_id']['pcr_data_type']
        if isinstance(self.water_body_id, NoneType):
            
            pcr_data_type = waterbody_variable_info['water_body_id']['pcr_data_type']
            self.water_body_id = pcr_data_type(0)

        self.water_body_id = pcr.ifthen(landmask, pcr.cover(self.water_body_id, 0))

        # water body type
        pcr_data_type = waterbody_variable_info['water_body_type']['pcr_data_type']
        if isinstance(self.water_body_id, NoneType):
            
            pcr_data_type = waterbody_variable_info['water_body_type']['pcr_data_type']
            self.water_body_type = pcr_data_type(0)

        self.water_body_type = pcr.ifthen(landmask, pcr.cover(self.water_body_type, 0))

        # water body outlets
        pcr_data_type = waterbody_variable_info['water_body_out']['pcr_data_type']
        if isinstance(self.water_body_out, NoneType):
            
            self.water_body_out = pcr_data_type(0)

        self.water_body_out = pcr.ifthen(landmask, pcr.cover(self.water_body_out, 0))

        # water body area
        pcr_data_type = waterbody_variable_info['water_body_area']['pcr_data_type']
        if isinstance(self.water_body_area, NoneType):
            
            pcr_data_type = waterbody_variable_info['water_body_area']['pcr_data_type']
            self.water_body_area = pcr_data_type(0)
            
        self.water_body_area = pcr.ifthen(landmask, \
                                          1.0e6 * pcr.cover(self.water_body_area, 0))

        # water body capacity
        pcr_data_type = waterbody_variable_info['water_body_capacity']['pcr_data_type']
        if isinstance(self.water_body_capacity, NoneType):
            
            pcr_data_type = waterbody_variable_info['water_body_capacity']['pcr_data_type']
            self.water_body_capacity = pcr_data_type(0)
            
        self.water_body_capacity = pcr.ifthen(landmask,  \
                                          1.0e6 * pcr.cover(self.water_body_capacity, 0))

        # endorheic lakes
        pcr_data_type = waterbody_variable_info['endorheic_lakes']['pcr_data_type']
        if isinstance(self.endorheic_lakes, NoneType):
            
            pcr_data_type = waterbody_variable_info['endorheic_lakes']['pcr_data_type']
            self.endorheic_lakes = pcr_data_type(0)
            
        self.endorheic_lakes = pcr.ifthen(landmask, pcr.cover(self.endorheic_lakes, 0))

        # set the water body type to lakes if only natural water bodies are
        # considered
        if only_natural_waterbodies:
            
            # set the water body type to 1
            pcr_data_type = waterbody_variable_info['water_body_type']['pcr_data_type']
            self.water_body_type = pcr.ifthenelse(self.water_body_type != 0, \
                    pcr_data_type(1), pcr_data_type(0))

            # log message
            logger.info('Using only natural water bodies identified in the year %s. All reservoirs at that time are treated as lakes.' % \
                        str(year_used))

        # *** water bodies are tested and corrected from here ***
        # correct the input: create masks of valid lakes and reservoirs
        lake_mask = self.water_body_type == 1
        reservoir_mask = self.water_body_type == 2
        valid_mask = (self.water_body_id != 0) & (self.water_body_type != 0)

        # initial test the input: check that all lakes and/or reservoirs have types, ids and outlets:
        # test on reservoirs
        number_lakes, valid_count = pcr.cellvalue( \
                                pcr.maptotal(pcr.scalar(pcr.areaorder(cellarea, \
                                pcr.ifthen(lake_mask, \
                                self.water_body_id)) == 1)), 1)
        if not valid_count: number_lakes = 0
        number_reservoirs, valid_count = pcr.cellvalue( \
                                pcr.maptotal(pcr.scalar(pcr.areaorder(cellarea, \
                                pcr.ifthen(reservoir_mask, \
                                self.water_body_id)) == 1)), 1)
        if not valid_count: number_reservoirs = 0
        valid_number_lakes, valid_count = pcr.cellvalue( \
                                pcr.maptotal(pcr.scalar(pcr.areaorder(cellarea, \
                                pcr.ifthen(lake_mask & valid_mask, \
                                self.water_body_id)) == 1)), 1)
        if not valid_count: valid_number_lakes = 0
        valid_number_reservoirs, valid_count = pcr.cellvalue( \
                                pcr.maptotal(pcr.scalar(pcr.areaorder(cellarea, \
                                pcr.ifthen(reservoir_mask & valid_mask, \
                                self.water_body_id)) == 1)), 1)
        if not valid_count: valid_number_reservoirs = 0
        # test on outlets
        test_out = valid_mask & (self.water_body_out  != 0)
        valid_number_lake_out, valid_count = pcr.cellvalue( \
                                pcr.maptotal(pcr.scalar(lake_mask & test_out)), 1)
        if not valid_count: valid_number_lake_out = 0
        valid_number_reservoir_out, valid_count = pcr.cellvalue( \
                                pcr.maptotal(pcr.scalar(reservoir_mask & test_out)), 1)
        if not valid_count: valid_number_lake_out = 0
        
        # log initial information on the water bodies
        logger.info('water body information for %s prior to any corrections' % str(year_used))
        logger.info('%10s: %d in total, %d valid, %d with outlets' \
                                                    % ('lakes', number_lakes, \
                                                                valid_number_lakes, \
                                                                valid_number_lake_out))
        logger.info('%10s: %d in total, %d valid, %d with outlets' \
                                                    % ('reservoirs', number_reservoirs, \
                                                                valid_number_reservoirs, \
                                                                valid_number_reservoir_out))
        # test and warn
        if  number_lakes != valid_number_lakes or \
            number_reservoirs != valid_number_reservoirs and \
            valid_number_reservoirs != valid_number_reservoir_out:
                
                # warn
                logger.warning('Missing information in some lakes and/or reservoirs.')

        # next, patch the information on the lakes and reservoirs
        # keep only the valid water bodies
        self.water_body_id = pcr.ifthenelse(valid_mask, self.water_body_id, 0)
        self.water_body_type = pcr.ifthenelse(valid_mask, self.water_body_type, 0)
        self.water_body_out = pcr.ifthenelse(valid_mask, self.water_body_out, 0)
        self.water_body_area = pcr.ifthenelse(valid_mask, self.water_body_area, 0)
        self.water_body_capacity = pcr.ifthenelse(valid_mask, self.water_body_capacity, 0)
        self.endorheic_lakes = pcr.ifthenelse(valid_mask, self.endorheic_lakes, 0)
        
        # patch the water body area if it is not yet set [million m2]
        default_water_body_area = pcr.ifthenelse(self.water_body_id != 0, \
                                  pcr.areatotal(self.water_area, \
                                  self.water_body_id), 0)
        # correct the water body area where data are provided
        correction_factor = vos.getValDivZero(self.water_body_area, \
                                              default_water_body_area, \
                                              vos.smallNumber)
        correction_factor = pcr.ifthenelse(self.water_body_area > 0, \
                            correction_factor, 1.0)
        # correct the water area at cell and water body level
        self.water_body_area = correction_factor * default_water_body_area
        self.water_area      = correction_factor * self.water_area
        self.fraction_water  = correction_factor * self.fraction_water
        
        # set the default outlets to use if no input is provided;
        # this is kept to be downward compatible
        number_upstream_cells = pcr.catchmenttotal(pcr.scalar(1),ldd)
        default_water_body_out = pcr.ifthenelse(number_upstream_cells ==\
                        pcr.areamaximum(number_upstream_cells, \
                        self.water_body_id), self.water_body_id, 0)
        default_water_body_out = pcr.ifthen(landmask, pcr.cover(default_water_body_out, 0))

        # check and correct outlets
        self.water_body_out = pcr.ifthenelse(self.water_body_out == self.water_body_id, \
                                        self.water_body_out, 0)
        self.water_body_out = pcr.ifthenelse(self.water_body_id != 0, \
                                        self.water_body_out, 0) 

        # identify water bodies without outlets
        number_outlets = pcr.ifthenelse(self.water_body_id != 0, \
                                pcr.areatotal(pcr.scalar(self.water_body_out != 0), \
                                              self.water_body_id), 0)

        # identify fixes
        no_outlet    = (number_outlets == 0) & (self.water_body_id != 0)
        more_outlets = (number_outlets >= 2) & (self.water_body_id != 0)

        # find reservoirs where the capacity is zero
        no_capacity = (self.water_body_capacity == 0) & \
                      reservoir_mask & valid_mask

        # check on the outlets; add one to all water bodies that do not have one
        # or keep one in case there are more
        preferred_outlet = more_outlets & (self.water_body_id == default_water_body_out)
        preferred_outlet = preferred_outlet | \
                           pcr.ifthenelse(pcr.areatotal(pcr.scalar(preferred_outlet), \
                                          more_outlets) == 0, default_water_body_out != 0, 0)
        preferred_outlet = preferred_outlet & \
                           pcr.ifthenelse(no_outlet, default_water_body_out != 0, 0)
        self.water_body_out = pcr.ifthenelse(no_outlet | more_outlets, \
                                    pcr.ifthenelse(preferred_outlet, \
                                                   default_water_body_out, 0), \
                                                   self.water_body_out)

        # add any water bodies that are lakes but do not have an outlet
        # to the endorheic lakes
        self.endorheic_lakes = self.endorheic_lakes | \
                               (no_outlet & lake_mask)

        # remove any reservoirs without capacity
        exclusion_mask = reservoir_mask & no_capacity
        reservoir_mask = reservoir_mask & pcr.pcrnot(no_capacity)
        self.water_body_id = pcr.ifthenelse(pcr.pcrnot(exclusion_mask), \
                       self.water_body_id, 0)
        self.water_body_type = pcr.ifthenelse(pcr.pcrnot(exclusion_mask), \
                       self.water_body_type, 0)
        self.water_body_out = pcr.ifthenelse(pcr.pcrnot(exclusion_mask), \
                       self.water_body_out, 0)
        self.water_body_area = pcr.ifthenelse(pcr.pcrnot(exclusion_mask), \
               self.water_body_area, 0)

        # and remove capacity where there is not a valid reservoir
        self.water_body_capacity = pcr.ifthenelse(reservoir_mask & valid_mask, \
                    self.water_body_capacity, 0)

        # remove any reservoirs from the endorheic lakes
        self.endorheic_lakes = self.endorheic_lakes & pcr.pcrnot(reservoir_mask) 


        # make a copy of all outlets of any lake or reservoir
        self.water_body_loc = pcr.nominal(self.water_body_out)
        
        # and remove outlets for endorheic lakes
        self.water_body_out = pcr.ifthenelse(pcr.pcrnot(self.endorheic_lakes), \
                                self.water_body_out, 0)
        
        # final test the input: check that all lakes and/or reservoirs have types, ids and outlets:
        # test on reservoirs
        number_lakes, valid_count = pcr.cellvalue( \
                                pcr.maptotal(pcr.scalar(pcr.areaorder(cellarea, \
                                pcr.ifthen(lake_mask, \
                                self.water_body_id)) == 1)), 1)
        if not valid_count: number_lakes = 0
        number_reservoirs, valid_count = pcr.cellvalue( \
                                pcr.maptotal(pcr.scalar(pcr.areaorder(cellarea, \
                                pcr.ifthen(reservoir_mask, \
                                self.water_body_id)) == 1)), 1)
        if not valid_count: number_reservoirs = 0
        valid_number_lakes, valid_count = pcr.cellvalue( \
                                pcr.maptotal(pcr.scalar(pcr.areaorder(cellarea, \
                                pcr.ifthen(lake_mask & valid_mask, \
                                self.water_body_id)) == 1)), 1)
        if not valid_count: valid_number_lakes = 0
        valid_number_reservoirs, valid_count = pcr.cellvalue( \
                                pcr.maptotal(pcr.scalar(pcr.areaorder(cellarea, \
                                pcr.ifthen(reservoir_mask & valid_mask, \
                                self.water_body_id)) == 1)), 1)
        if not valid_count: valid_number_reservoirs = 0
        # test on outlets
        test_out = valid_mask & (self.water_body_out  != 0)
        valid_number_lake_out, valid_count = pcr.cellvalue( \
                                pcr.maptotal(pcr.scalar(lake_mask & test_out)), 1)
        if not valid_count: valid_number_lake_out = 0
        valid_number_reservoir_out, valid_count = pcr.cellvalue( \
                                pcr.maptotal(pcr.scalar(reservoir_mask & test_out)), 1)
        if not valid_count: valid_number_lake_out = 0
        
        # log initial information on the water bodies
        logger.info('water body information for %s after any corrections' % str(year_used))
        logger.info('%10s: %d in total, %d valid, %d with outlets' \
                                                    % ('lakes', number_lakes, \
                                                                valid_number_lakes, \
                                                                valid_number_lake_out))
        logger.info('%10s: %d in total, %d valid, %d with outlets' \
                                                    % ('reservoirs', number_reservoirs, \
                                                                valid_number_reservoirs, \
                                                                valid_number_reservoir_out))
        # test and warn
        if  number_lakes != valid_number_lakes or \
            number_reservoirs != valid_number_reservoirs and \
            valid_number_reservoirs != valid_number_reservoir_out:
                
                # warn
                logger.error('Missing information in some lakes and/or reservoirs.')
                sys.exit()

        # *** this patch is needed to link the module to the 
        #     subsequent part ***
        # finally, set the variables for the remainder of the module
        for variable_name, var_info in waterbody_variable_info.items():

            # get the information from the variable name
            alt_var_name  = var_info['alt_var_name']
            pcr_data_type = var_info['pcr_data_type']
            
            # get the variable field
            var_field = getattr(self, variable_name)

            # remove zero values if the data type is not scalar
            #~ if pcr_data_type != pcr.scalar:
            #~ var_field = pcr.ifthen(var_field != 0, var_field)

            # set the variable to None and add the old variable name
            setattr(self, alt_var_name, var_field)
            setattr(self, variable_name, None)

            # and delete the variable
            var_field = getattr(self, variable_name)
            del var_field

        # make a copy of the locations
        self.waterBodyLoc = pcr.nominal(self.water_body_loc)
        self.water_body_loc = None
        del self.water_body_loc

        # and set the cell area
        self.waterBodyCellArea = self.water_area
        self.water_area = None
        del self.water_area

        # and set the outflow points as a boolean map
        self.waterBodyOut = self.waterBodyOut != 0

        # at the beginning of simulation, at the first time step, we have to set
        # the initial conditions when the dictionary is zero

        if not isinstance(initial_condition_dictionary, NoneType) \
                        and current_time_step.timeStepPCR == 1:
            self.getICs(initial_condition_dictionary)
        
        # For each new reservoir (introduced at the beginning of the year)
        # initiating storage, average inflow and outflow
        # PS: THIS IS NOT NEEDED FOR OFFLINE MODFLOW RUN! 
        #
        try:
            self.waterBodyStorage = pcr.ifthen(landmask, pcr.cover(self.waterBodyStorage,0.0))
            self.avgInflow        = pcr.ifthen(landmask, pcr.cover(self.avgInflow ,0.0))
            self.avgOutflow       = pcr.ifthen(landmask, pcr.cover(self.avgOutflow,0.0))
        except:
            # PS: FOR OFFLINE MODFLOW RUN!
            pass
        # TODO: Remove try and except    
        
        # echo message
        logger.info('Water bodies for %s initialized' % str(year_used))

        # return None
        return None

    #~ def getParameterFiles_old(self,currTimeStep,cellArea,ldd,\
                               #~ initial_condition_dictionary = None,\
                               #~ currTimeStepInDateTimeFormat = False):
#~ 
        #~ # parameters for Water Bodies: fracWat              
        #~ #                              waterBodyIds
        #~ #                              waterBodyOut
        #~ #                              waterBodyArea 
        #~ #                              waterBodyTyp
        #~ #                              waterBodyCap
        #~ 
        #~ # cell surface area (m2) and ldd
        #~ self.cellArea = cellArea
        #~ ldd = pcr.ifthen(self.landmask, ldd)
        #~ 
        #~ # date used for accessing/extracting water body information
        #~ if currTimeStepInDateTimeFormat:
            #~ date_used = currTimeStep
            #~ year_used = currTimeStep.year
        #~ else:
            #~ date_used = currTimeStep.fulldate
            #~ year_used = currTimeStep.year
        #~ if self.onlyNaturalWaterBodies == True:
            #~ date_used = self.dateForNaturalCondition
            #~ year_used = self.dateForNaturalCondition[0:4] 
        #~ 
        #~ # fracWat = fraction of surface water bodies (dimensionless)
        #~ self.fracWat = pcr.scalar(0.0)
        #~ 
        #~ if self.useNetCDF:
            #~ self.fracWat = vos.netcdf2PCRobjClone(self.ncFileInp,'fracWaterInp', \
                           #~ date_used, useDoy = 'yearly',\
                           #~ cloneMapFileName = self.cloneMap)
        #~ else:
            #~ self.fracWat = vos.readPCRmapClone(\
                           #~ self.fracWaterInp+str(year_used)+".map",
                           #~ self.cloneMap,self.tmpDir,self.inputDir)
        #~ 
        #~ self.fracWat = pcr.cover(self.fracWat, 0.0)
        #~ self.fracWat = pcr.max(0.0,self.fracWat)
        #~ self.fracWat = pcr.min(1.0,self.fracWat)
        #~ 
        #~ self.waterBodyIds   = pcr.nominal(0)    # waterBody ids
        #~ self.waterBodyOut   = pcr.boolean(0)    # waterBody outlets
        #~ self.endorheicLakes = pcr.boolean(0)    # endorheic lakes
        #~ self.waterBodyArea  = pcr.scalar(0.)    # waterBody surface areas
#~ 
        #~ # water body ids
        #~ if self.useNetCDF:
            #~ self.waterBodyIds = vos.netcdf2PCRobjClone(self.ncFileInp,'waterBodyIds', \
                                #~ date_used, useDoy = 'yearly',\
                                #~ cloneMapFileName = self.cloneMap)
        #~ else:
            #~ self.waterBodyIds = vos.readPCRmapClone(\
                #~ self.waterBodyIdsInp+str(year_used)+".map",\
                #~ self.cloneMap,self.tmpDir,self.inputDir,False,None,True)
        #~ 
        #~ # RvB: October 2019: this is the original patch by Edwin for
        #~ # water bodies with multiple outlets; this has been kept
        #~ # but the line has been added where the outlets of endorheic lakes
        #~ # are removed.
        #~ self.waterBodyIds = pcr.ifthen(\
                            #~ pcr.scalar(self.waterBodyIds) > 0.,\
                            #~ pcr.nominal(self.waterBodyIds))    
#~ 
        #~ # water body outlets (correcting outlet positions): these are the default
        #~ # outlets to use if no input is provided;
        #~ # RvB: October 2019: this is kept to be downwards compatible!
        #~ wbCatchment = pcr.catchmenttotal(pcr.scalar(1),ldd)
        #~ defaultWaterBodyOut = pcr.ifthen(wbCatchment ==\
                            #~ pcr.areamaximum(wbCatchment, \
                            #~ self.waterBodyIds),\
                            #~ self.waterBodyIds)     # = outlet ids   
        #~ defaultWaterBodyOut = pcr.ifthen(\
                            #~ (pcr.scalar(self.waterBodyIds) > 0.),\
                            #~ defaultWaterBodyOut)
#~ 
        #~ # RvB: October 2019: added the processing of any outlets for endorheic lakes.
        #~ # This requires that the actual outlets and information on endorheic lakes are
        #~ # read from file.
#~ 
        #~ # first, read in the outlets if available
        #~ if self.useNetCDF:
            #~ try:
                #~ self.waterBodyOut = vos.netcdf2PCRobjClone(self.ncFileInp,'waterBodyOut', \
                                    #~ date_used, useDoy = 'yearly',\
                                    #~ cloneMapFileName = self.cloneMap)
                #~ logger.info("Outlets of water bodies read from netCDF file.")
            #~ except:
                #~ # log warning
                #~ logger.warning("Outlets of water bodies have not been read from netCDF.")
        #~ elif not self.waterBodyOutInp is None:
            #~ self.waterBodyOut = vos.readPCRmapClone(\
                #~ self.waterBodyOutInp+'_'+str(year_used)+".map",\
                #~ self.cloneMap,self.tmpDir,self.inputDir,False,None,True)
            #~ logger.info("Outlets of water bodies read from map file.")
#~ 
        #~ # next, read in the endorheic lakes if available
        #~ if self.useNetCDF:
            #~ try:
                #~ self.endorheicLakes = vos.netcdf2PCRobjClone(self.ncFileInp,'endorheicLakes', \
                                    #~ date_used, useDoy = 'yearly',\
                                    #~ cloneMapFileName = self.cloneMap)
                #~ logger.info("Endorheic lakes read from netCDF file.")
            #~ except:
                #~ # log warning
                #~ logger.warning("Endorheic lakes have not been read from netCDF.")
        #~ elif not self.endorheicLakesInp is None:
            #~ self.endorheicLakes = vos.readPCRmapClone(\
                #~ self.endorheicLakesInp+'_'+str(year_used)+".map",\
                #~ self.cloneMap,self.tmpDir,self.inputDir,False,None,True)
            #~ logger.info("Information on endorheic lakes read from map file.")
#~ 
        #~ # RvB: October, 2019: all information on endorheic lakes and waterbody
        #~ # outlets read or prepared; patch all information
        #~ # clip the information to the relevant land mask
        #~ self.waterBodyIds = pcr.ifthen(pcr.defined(ldd), pcr.nominal(self.waterBodyIds))
        #~ self.waterBodyOut = pcr.ifthen(pcr.defined(ldd), pcr.nominal(self.waterBodyOut))
        #~ self.endorheicLakes = pcr.ifthen(pcr.defined(ldd), pcr.boolean(self.endorheicLakes))
#~ 
        #~ # RvB: October, 2019: next: patch outlets and create dummy endorheic lakes
        #~ # if not defined
        #~ patch_outlets = pcr.ifthenelse((pcr.scalar(self.waterBodyOut) != \
                        #~ pcr.scalar(defaultWaterBodyOut)) & \
                            #~ (defaultWaterBodyOut != 0), pcr.scalar(1), pcr.scalar(0)) + \
                        #~ pcr.ifthenelse((pcr.scalar(self.waterBodyOut) != \
                            #~ pcr.scalar(defaultWaterBodyOut)) & \
                            #~ (self.waterBodyOut != 0), pcr.scalar(1), pcr.scalar(0))
                            #~ 
        #~ patch_outlets = (pcr.areatotal(patch_outlets, self.waterBodyIds) > 0) & \
            #~ pcr.pcrnot(self.endorheicLakes)
        #~ patch_outlets = pcr.cover(patch_outlets, 0)
        #~ # finally, patch the outlets where the mask is True
        #~ self.waterBodyOut = pcr.ifthenelse(patch_outlets, defaultWaterBodyOut, self.waterBodyOut)
        #~ 
        #~ # and add a warning to the logger for any patches!
        #~ number_patches = pcr.cellvalue(pcr.maptotal(pcr.scalar(patch_outlets)), 1)[0]
        #~ if number_patches > 0:
            #~ logger.warning("Correction on the outlet of %d water bodies made that were not identified as endorheic." % number_patches)
        #~ 
        #~ # correcting water body ids; uses the correct outlets where possible, 
        #~ # and the default ones in the case of anything else, including
        #~ # the endorheic lakes
        #~ self.waterBodyIds = pcr.ifthen(\
                            #~ pcr.scalar(self.waterBodyIds) > 0.,\
                            #~ pcr.subcatchment(ldd, \
                                #~ pcr.ifthenelse(patch_outlets, defaultWaterBodyOut, \
                                #~ pcr.ifthenelse(self.waterBodyOut != 0, \
                                #~ self.waterBodyOut, defaultWaterBodyOut))))
#~ 
        #~ # finally, cover the outlets with zeros
        #~ self.waterBodyOut = pcr.cover(self.waterBodyOut, 0)
        #~ 
        #~ # boolean map for water body outlets:   
        #~ self.waterBodyOut = pcr.ifthen(\
                            #~ pcr.scalar(self.waterBodyOut) > 0.,\
                            #~ pcr.boolean(1))
        #~ 
        #~ # RvB: October 2019: addition to remove the outlets of endorheic lakes
        #~ # first expand any endorheic lakes
        #~ self.endorheicLakes = pcr.areamaximum(pcr.scalar(self.endorheicLakes), self.waterBodyIds) == 1
#~ 
        #~ # then, expand the maps to full coverage
        #~ self.waterBodyIds = pcr.ifthen(pcr.defined(ldd), \
                            #~ pcr.cover(self.waterBodyIds, 0))
        #~ self.waterBodyOut = pcr.ifthen(pcr.defined(ldd), \
                            #~ pcr.cover(self.waterBodyOut, 0))
        #~ self.endorheicLakes   = pcr.ifthen(pcr.defined(ldd), \
                            #~ pcr.cover(self.endorheicLakes, 0))
        #~ self.waterBodyCellArea = pcr.ifthen(pcr.defined(ldd), \
                            #~ pcr.cover(self.fracWat * self.cellArea, 0))
#~ 
        #~ # next, remove the endorheic lakes from the outflow points
        #~ self.waterBodyLoc = pcr.ifthen(pcr.defined(ldd), \
                            #~ pcr.cover(self.waterBodyOut, 0))
        #~ self.waterBodyOut = self.waterBodyOut & \
                            #~ pcr.pcrnot(self.endorheicLakes)
#~ 
        #~ # this is the end of the added read on water body outlets
        #~ # with this, all outlets are updated
        #~ # RvB: October 2019: endorheic lakes included
#~ 
        #~ # RvB: february 2020: water body type read earlier than before to mask
        #~ # out zero reservoirs in the area calculation that follows
        #~ # water body types:
        #~ # - 2 = reservoirs (regulated discharge)
        #~ # - 1 = lakes (weirFormula)
        #~ # - 0 = non lakes or reservoirs (e.g. wetland)
        #~ self.waterBodyTyp = pcr.nominal(0)
        #~ 
        #~ if self.useNetCDF:
            #~ self.waterBodyTyp = vos.netcdf2PCRobjClone(self.ncFileInp,'waterBodyTyp', \
                                #~ date_used, useDoy = 'yearly',\
                                #~ cloneMapFileName = self.cloneMap)
        #~ else:
            #~ self.waterBodyTyp = vos.readPCRmapClone(
                #~ self.waterBodyTypInp+str(year_used)+".map",\
                #~ self.cloneMap,self.tmpDir,self.inputDir,False,None,True)
#~ 
        #~ # excluding wetlands (waterBodyTyp = 0) in all functions related to lakes/reservoirs 
        #~ #
        #~ self.waterBodyTyp = pcr.ifthen(\
                            #~ pcr.scalar(self.waterBodyTyp) > 0,\
                            #~ pcr.nominal(self.waterBodyTyp))    
        #~ self.waterBodyTyp = pcr.ifthen(\
                            #~ pcr.scalar(self.waterBodyIds) > 0,\
                            #~ pcr.nominal(self.waterBodyTyp))    
        #~ self.waterBodyTyp = pcr.areamajority(self.waterBodyTyp,\
                                             #~ self.waterBodyIds)     # choose only one type: either lake or reservoir                  
        #~ self.waterBodyTyp = pcr.ifthen(\
                            #~ pcr.scalar(self.waterBodyTyp) > 0,\
                            #~ pcr.nominal(self.waterBodyTyp))    
        #~ self.waterBodyTyp = pcr.ifthen(pcr.boolean(self.waterBodyIds),
                                                   #~ self.waterBodyTyp)
#~ 
        #~ # reservoir surface area (m2):
        #~ if self.useNetCDF:
            #~ resSfArea = 1000. * 1000. * \
                        #~ vos.netcdf2PCRobjClone(self.ncFileInp,'resSfAreaInp', \
                        #~ date_used, useDoy = 'yearly',\
                        #~ cloneMapFileName = self.cloneMap)
        #~ else:
            #~ resSfArea = 1000. * 1000. * vos.readPCRmapClone(
                   #~ self.resSfAreaInp+str(year_used)+".map",\
                   #~ self.cloneMap,self.tmpDir,self.inputDir)
        #~ resSfArea = pcr.ifthenelse(self.waterBodyTyp == 2, \
                    #~ pcr.areaaverage(resSfArea,self.waterBodyIds), 0)
        #~ resSfArea = pcr.cover(resSfArea,0.)                        
#~ 
        #~ # water body surface area (m2): (lakes and reservoirs)
        #~ self.waterBodyArea = pcr.cover(pcr.ifthenelse(self.waterBodyTyp == 1, \
                             #~ pcr.areatotal(self.waterBodyCellArea, self.waterBodyIds), \
                             #~ resSfArea), self.waterBodyCellArea, 0)
        #~ self.waterBodyArea = pcr.ifthen(self.waterBodyArea > 0.,\
                             #~ self.waterBodyArea)
                                #~ 
        #~ # correcting water body ids and outlets (exclude all water bodies with surfaceArea = 0)
        #~ self.waterBodyIds = pcr.ifthenelse(self.waterBodyArea > 0.,
                            #~ self.waterBodyIds, 0)               
        #~ self.waterBodyOut = pcr.ifthenelse(pcr.boolean(self.waterBodyIds),
                            #~ self.waterBodyOut, 0) 
        #~ self.waterBodyLoc = pcr.ifthenelse(pcr.boolean(self.waterBodyIds),
                            #~ self.waterBodyLoc, 0)
#~ 
        #~ # correcting lakes and reservoirs ids and outlets
        #~ self.waterBodyIds = pcr.ifthen(pcr.scalar(self.waterBodyTyp) > 0,
                                                  #~ self.waterBodyIds)               
        #~ self.waterBodyOut = pcr.ifthen(pcr.scalar(self.waterBodyIds) > 0,
                                                  #~ self.waterBodyOut)
#~ 
        #~ # reservoir maximum capacity (m3):
        #~ self.resMaxCap = pcr.scalar(0.0)
        #~ self.waterBodyCap = pcr.scalar(0.0)
#~ 
        #~ if self.useNetCDF:
            #~ self.resMaxCap = 1000. * 1000. * \
                             #~ vos.netcdf2PCRobjClone(self.ncFileInp,'resMaxCapInp', \
                             #~ date_used, useDoy = 'yearly',\
                             #~ cloneMapFileName = self.cloneMap)
        #~ else:
            #~ self.resMaxCap = 1000. * 1000. * vos.readPCRmapClone(\
                #~ self.resMaxCapInp+str(year_used)+".map", \
                #~ self.cloneMap,self.tmpDir,self.inputDir)
#~ 
        #~ self.resMaxCap = pcr.ifthen(self.resMaxCap > 0,\
                                    #~ self.resMaxCap)
        #~ self.resMaxCap = pcr.areaaverage(self.resMaxCap,\
                                         #~ self.waterBodyIds)
                                         #~ 
        #~ # water body capacity (m3): (lakes and reservoirs)
        #~ self.waterBodyCap = pcr.cover(self.resMaxCap,0.0)               # Note: Most of lakes have capacities > 0.
        #~ self.waterBodyCap = pcr.ifthen(pcr.boolean(self.waterBodyIds),
                                                   #~ self.waterBodyCap)
                                               #~ 
        #~ # correcting water body types:                                  # Reservoirs that have zero capacities will be assumed as lakes.
        #~ self.waterBodyTyp = \
                 #~ pcr.ifthen(pcr.scalar(self.waterBodyTyp) > 0.,\
                                       #~ self.waterBodyTyp) 
        #~ self.waterBodyTyp = pcr.ifthenelse(self.waterBodyCap > 0.,\
                                           #~ self.waterBodyTyp,\
                 #~ pcr.ifthenelse(pcr.scalar(self.waterBodyTyp) == 2,\
                                           #~ pcr.nominal(1),\
                                           #~ self.waterBodyTyp)) 
#~ 
        #~ # final corrections:
        #~ self.waterBodyTyp = pcr.ifthen(self.waterBodyArea > 0.,\
                                       #~ self.waterBodyTyp)                     # make sure that all lakes and/or reservoirs have surface areas
        #~ self.waterBodyTyp = \
                 #~ pcr.ifthen(pcr.scalar(self.waterBodyTyp) > 0.,\
                                       #~ self.waterBodyTyp)                     # make sure that only types 1 and 2 will be considered in lake/reservoir functions
        #~ self.waterBodyIds = pcr.ifthen(pcr.scalar(self.waterBodyTyp) > 0.,\
                            #~ self.waterBodyIds)                                # make sure that all lakes and/or reservoirs have ids
        #~ self.waterBodyOut = pcr.ifthen(pcr.scalar(self.waterBodyIds) > 0.,\
                                                  #~ self.waterBodyOut)          # make sure that all lakes and/or reservoirs have outlets
        #~ 
        #~ 
        #~ # for a natural run (self.onlyNaturalWaterBodies == True) 
        #~ # which uses only the year 1900, assume all reservoirs are lakes
        #~ if self.onlyNaturalWaterBodies == True and date_used == self.dateForNaturalCondition:
            #~ logger.info("Using only natural water bodies identified in the year 1900. All reservoirs in 1900 are assumed as lakes.")
            #~ self.waterBodyTyp = \
             #~ pcr.ifthen(pcr.scalar(self.waterBodyTyp) > 0.,\
                        #~ pcr.nominal(1))                         
        #~ 
        #~ # check that all lakes and/or reservoirs have types, ids, surface areas and outlets:
        #~ test = pcr.defined(self.waterBodyTyp) & pcr.defined(self.waterBodyArea) &\
               #~ pcr.defined(self.waterBodyIds) & pcr.boolean(pcr.areamaximum(pcr.scalar(self.waterBodyOut), self.waterBodyIds))
        #~ a,b,c = vos.getMinMaxMean(pcr.cover(pcr.scalar(test), 1.0) - pcr.scalar(1.0))
        #~ threshold = 1e-3
        #~ if abs(a) > threshold or abs(b) > threshold:
            #~ logger.warning("Missing information in some lakes and/or reservoirs.")
#~ 
        #~ # at the beginning of simulation period (timeStepPCR = 1)
        #~ # - we have to define/get the initial conditions 
        #~ #
        #~ if initial_condition_dictionary != None and currTimeStep.timeStepPCR == 1:
            #~ self.getICs(initial_condition_dictionary)
        #~ 
        #~ # For each new reservoir (introduced at the beginning of the year)
        #~ # initiating storage, average inflow and outflow
        #~ # PS: THIS IS NOT NEEDED FOR OFFLINE MODFLOW RUN! 
        #~ #
        #~ try:
            #~ self.waterBodyStorage = pcr.cover(self.waterBodyStorage,0.0)
            #~ self.avgInflow        = pcr.cover(self.avgInflow ,0.0)
            #~ self.avgOutflow       = pcr.cover(self.avgOutflow,0.0)
            #~ self.waterBodyStorage = pcr.ifthen(self.landmask, self.waterBodyStorage)
            #~ self.avgInflow        = pcr.ifthen(self.landmask, self.avgInflow       )
            #~ self.avgOutflow       = pcr.ifthen(self.landmask, self.avgOutflow      )
        #~ except:
            #~ # PS: FOR OFFLINE MODFLOW RUN!
            #~ pass
        #~ # TODO: Remove try and except    
#~ 
        #~ # cropping only in the landmask region:
        #~ self.fracWat           = pcr.ifthen(self.landmask, self.fracWat         )
        #~ self.waterBodyIds      = pcr.ifthen(self.landmask, self.waterBodyIds    ) 
        #~ self.waterBodyOut      = pcr.ifthen(self.landmask, self.waterBodyOut    )
        #~ self.waterBodyArea     = pcr.ifthen(self.landmask, self.waterBodyArea   )
        #~ self.waterBodyTyp      = pcr.ifthen(self.landmask, self.waterBodyTyp    )  
        #~ self.waterBodyCap      = pcr.ifthen(self.landmask, self.waterBodyCap    )


    def getICs(self,initial_condition):

        avgInflow  = initial_condition['avgLakeReservoirInflowShort']  
        avgOutflow = initial_condition['avgLakeReservoirOutflowLong'] 
        #
        if not isinstance(initial_condition['waterBodyStorage'],types.NoneType):
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
                           avgChannelDischarge,\
                           length_of_time_step = vos.secondsPerDay(),\
                           downstreamDemand = None):

        if self.debugWaterBalance:\
           preStorage = self.waterBodyStorage    # unit: m
     
        self.timestepsToAvgDischarge = timestepsToAvgDischarge          # TODO: include this one in "currTimeStep"     
        
        # obtain inflow (and update storage)
        self.moveFromChannelToWaterBody(\
         newStorageAtLakeAndReservoirs,\
             timestepsToAvgDischarge,\
             maxTimestepsToAvgDischargeShort,\
             length_of_time_step)
        
        # calculate outflow (and update storage)
        self.getWaterBodyOutflow(\
             maxTimestepsToAvgDischargeLong,\
             avgChannelDischarge,\
             length_of_time_step,\
             downstreamDemand)
        
        if self.debugWaterBalance:\
            vos.waterBalanceCheck( \
                [pcr.cover(self.inflow/self.waterBodyArea,0.0)],\
                [pcr.cover(self.waterBodyOutflow/self.waterBodyArea,0.0)],\
                [pcr.cover(preStorage/self.waterBodyArea,0.0)],\
                [pcr.cover(self.waterBodyStorage/self.waterBodyArea,0.0)],\
                'WaterBodyStorage (unit: m)',\
                True,\
                currTimeStep.fulldate,threshold=5e-3)

        self.waterBodyBalance = (pcr.cover(self.inflow/self.waterBodyArea, 0.0) - pcr.cover(self.waterBodyOutflow/self.waterBodyArea,0.0)) -\
                                (pcr.cover(self.waterBodyStorage/self.waterBodyArea,0.0) - pcr.cover(preStorage/self.waterBodyArea,0.0))

        # end

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

    def getWaterBodyOutflow(self,\
                            maxTimestepsToAvgDischargeLong,\
                            avgChannelDischarge,\
                            length_of_time_step = vos.secondsPerDay(),\
                            downstreamDemand = None):

        # outflow in volume from water bodies with lake type (m3): 
        lakeOutflow = self.getLakeOutflow(avgChannelDischarge,length_of_time_step)  
             
        # outflow in volume from water bodies with reservoir type (m3): 
        if isinstance(downstreamDemand, types.NoneType): downstreamDemand = pcr.scalar(0.0)
        reservoirOutflow = self.getReservoirOutflow(avgChannelDischarge,length_of_time_step,downstreamDemand)  

        # outgoing/release volume from lakes and/or reservoirs
        self.waterBodyOutflow = pcr.cover(reservoirOutflow, lakeOutflow)  
        
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
        self.waterBodyStorage = self.waterBodyStorage -\
                                self.waterBodyOutflow
        self.waterBodyStorage = pcr.max(0.0, self.waterBodyStorage)                        

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
        return (resvOutflow) # unit: m3  