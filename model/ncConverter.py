#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

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
import sys
import datetime
import time
import re
import glob
import subprocess
import netCDF4 as nc
import numpy as np

# ~ import pcraster as pcr
# ~ import luepcr as pcr
# ~ print("LUE is USED.")
try:
    import luepcr as pcr
    print("LUE is USED.")
except:
    import pcraster as pcr		

import virtualOS as vos

# TODO: defined the dictionary (e.g. filecache = dict()) to avoid open and closing files

class PCR2netCDF():
    
    def __init__(self,iniItems,specificAttributeDictionary=None):
                
        # cloneMap
        pcr.setclone(iniItems.cloneMap)
        # ~ cloneMap = pcr.boolean(1.0)
        
        # ~ # latitudes and longitudes
        # ~ self.latitudes  = np.unique(pcr.pcr2numpy(pcr.ycoordinate(cloneMap), vos.MV))[::-1]
        # ~ self.longitudes = np.unique(pcr.pcr2numpy(pcr.xcoordinate(cloneMap), vos.MV))
        
        #~ # latitudes and longitudes
        #~ self.longitudes, self.latitudes, cellSizeInArcMin = self.set_latlon_based_on_cloneMapFileName(iniItems.cloneMap)

        # latitudes and longitudes
        self.longitudes, self.latitudes, cellSizeInArcMin = self.set_latlon_based_on_cloneMapFileName_using_mapattr(iniItems.cloneMap)

        # ~ # Let users decide what their preference regarding latitude order. 
        # ~ self.netcdf_y_orientation_follow_cf_convention = False
        # ~ if 'netcdf_y_orientation_follow_cf_convention' in list(iniItems.reportingOptions.keys()) and\
            # ~ iniItems.reportingOptions['netcdf_y_orientation_follow_cf_convention'] == "True":
            # ~ msg = "Latitude (y) orientation for output netcdf files start from the bottom to top."
            # ~ self.netcdf_y_orientation_follow_cf_convention = True
            # ~ self.latitudes  = np.unique(pcr.pcr2numpy(pcr.ycoordinate(cloneMap), vos.MV))
        
        # set the general netcdf attributes (based on the information given in the ini/configuration file) 
        self.set_general_netcdf_attributes(iniItems, specificAttributeDictionary)
        
        # netcdf format and zlib setup 
        self.format = 'NETCDF3_CLASSIC'
        self.zlib = False
        if "formatNetCDF" in list(iniItems.reportingOptions.keys()):
            self.format = str(iniItems.reportingOptions['formatNetCDF'])
        if "zlib" in list(iniItems.reportingOptions.keys()):
            if iniItems.reportingOptions['zlib'] == "True": self.zlib = True
        

        # if given in the ini file, use the netcdf as given in the section 'specific_attributes_for_netcdf_output_files'
        if 'specific_attributes_for_netcdf_output_files' in iniItems.allSections:
            for key in list(iniItems.specific_attributes_for_netcdf_output_files.keys()):

                self.attributeDictionary[key] = iniItems.specific_attributes_for_netcdf_output_files[key]
                
                if self.attributeDictionary[key] == "None": self.attributeDictionary[key] = ""

                if key == "history" and self.attributeDictionary[key] == "Default":
                    self.attributeDictionary[key] = \
                                    'created on ' + datetime.datetime.today().isoformat(' ')
                if self.attributeDictionary[key] == "Default" and\
                  (key == "date_created" or key == "date_issued"):
                    self.attributeDictionary[key] = datetime.datetime.today().isoformat(' ')
 

    def set_latlon_based_on_cloneMapFileName_using_mapattr(self, cloneMapFileName):

        clone_map_attributes = vos.getMapAttributesALL(cloneMapFileName)
        
        # properties of the clone maps
        # - numbers of rows and colums
        rows = clone_map_attributes['rows']
        cols = clone_map_attributes['cols']

        # - cell size in arc minutes rounded to one value behind the decimal
        cellSizeInArcMin = round(clone_map_attributes['cellsize'] * 60.0, 1) 
        # - cell sizes in ar degrees for longitude and langitude direction 
        deltaLon = cellSizeInArcMin / 60.
        deltaLat = deltaLon
        # - coordinates of the upper left corner - rounded to two values behind the decimal in order to avoid rounding errors during (future) resampling process
        x_min = round(clone_map_attributes['xUL'], 2)
        y_max = round(clone_map_attributes['yUL'], 2)
        # - coordinates of the lower right corner - rounded to two values behind the decimal in order to avoid rounding errors during (future) resampling process
        x_max = round(x_min + cols*deltaLon, 2) 
        y_min = round(y_max - rows*deltaLat, 2) 
        
        # cell centres coordinates
        longitudes = np.arange(x_min + deltaLon/2., x_max, deltaLon)
        latitudes  = np.arange(y_max - deltaLat/2., y_min,-deltaLat)

        #~ # cell centres coordinates
        #~ longitudes = np.linspace(x_min + deltaLon/2., x_max - deltaLon/2., cols)
        #~ latitudes  = np.linspace(y_max - deltaLat/2., y_min + deltaLat/2., rows)
        
        #~ # cell centres coordinates (latitudes and longitudes, directly from the clone maps)
        #~ longitudes = np.unique(pcr.pcr2numpy(pcr.xcoordinate(cloneMap), vos.MV))
        #~ latitudes  = np.unique(pcr.pcr2numpy(pcr.ycoordinate(cloneMap), vos.MV))[::-1]

        return longitudes, latitudes, cellSizeInArcMin  

    def set_latlon_based_on_cloneMapFileName(self, cloneMapFileName):

        # cloneMap
        cloneMap = pcr.boolean(pcr.readmap(cloneMapFileName))
        cloneMap = pcr.boolean(pcr.scalar(1.0))
        
        # properties of the clone maps
        # - numbers of rows and colums
        rows = pcr.clone().nrRows() 
        cols = pcr.clone().nrCols()
        # - cell size in arc minutes rounded to one value behind the decimal
        cellSizeInArcMin = round(pcr.clone().cellSize() * 60.0, 1) 
        # - cell sizes in ar degrees for longitude and langitude direction 
        deltaLon = cellSizeInArcMin / 60.
        deltaLat = deltaLon
        # - coordinates of the upper left corner - rounded to two values behind the decimal in order to avoid rounding errors during (future) resampling process
        x_min = round(pcr.clone().west(), 2)
        y_max = round(pcr.clone().north(), 2)
        # - coordinates of the lower right corner - rounded to two values behind the decimal in order to avoid rounding errors during (future) resampling process
        x_max = round(x_min + cols*deltaLon, 2) 
        y_min = round(y_max - rows*deltaLat, 2) 
        
        # cell centres coordinates
        longitudes = np.arange(x_min + deltaLon/2., x_max, deltaLon)
        latitudes  = np.arange(y_max - deltaLat/2., y_min,-deltaLat)

        #~ # cell centres coordinates
        #~ longitudes = np.linspace(x_min + deltaLon/2., x_max - deltaLon/2., cols)
        #~ latitudes  = np.linspace(y_max - deltaLat/2., y_min + deltaLat/2., rows)
        
        #~ # cell centres coordinates (latitudes and longitudes, directly from the clone maps)
        #~ longitudes = np.unique(pcr.pcr2numpy(pcr.xcoordinate(cloneMap), vos.MV))
        #~ latitudes  = np.unique(pcr.pcr2numpy(pcr.ycoordinate(cloneMap), vos.MV))[::-1]

        return longitudes, latitudes, cellSizeInArcMin  
                    
    def set_general_netcdf_attributes(self,iniItems,specificAttributeDictionary=None):

        # netCDF attributes (based on the configuration file or specificAttributeDictionary):
        self.attributeDictionary = {}
        if specificAttributeDictionary == None:
            self.attributeDictionary['institution'] = iniItems.globalOptions['institution']
            self.attributeDictionary['title'      ] = iniItems.globalOptions['title'      ]
            self.attributeDictionary['description'] = iniItems.globalOptions['description']
        else:
            for ncAttributeKey, ncAttribute in list(specificAttributeDictionary.items()):
                print(ncAttributeKey, ncAttribute)
                self.attributeDictionary[ncAttributeKey]= ncAttribute

    def createNetCDF(self, ncFileName, varName, varUnits, longName = None, standardName= None):

        rootgrp = nc.Dataset(ncFileName,'w',format= self.format)

        #-create dimensions - time is unlimited, others are fixed
        rootgrp.createDimension('time',None)
        rootgrp.createDimension('lat',len(self.latitudes))
        rootgrp.createDimension('lon',len(self.longitudes))

        date_time = rootgrp.createVariable('time','f4',('time',))
        date_time.standard_name = 'time'
        date_time.long_name = 'Days since 1901-01-01'

        #~ date_time.units = 'Days since 1901-01-01' 
        # - fixing for ulysses
        date_time.units    = 'days since 1901-01-01'

        date_time.calendar = 'standard'

        lat= rootgrp.createVariable('lat','f4',('lat',))
        lat.long_name = 'latitude'
        lat.units = 'degrees_north'
        lat.standard_name = 'latitude'

        lon= rootgrp.createVariable('lon','f4',('lon',))
        lon.standard_name = 'longitude'
        lon.long_name = 'longitude'
        lon.units = 'degrees_east'

        lat[:]= self.latitudes
        lon[:]= self.longitudes

        shortVarName = varName
        longVarName  = varName
        standardVarName = varName
        if longName != None: longVarName = longName
        if standardName != None: standardVarName = standardName

        var = rootgrp.createVariable(shortVarName,'f4',('time','lat','lon',) ,fill_value=vos.MV,zlib=self.zlib)
        var.standard_name = standardVarName
        var.long_name = longVarName
        var.units = varUnits

        attributeDictionary = self.attributeDictionary
        for k, v in list(attributeDictionary.items()): setattr(rootgrp,k,v)

        rootgrp.sync()
        rootgrp.close()

    def changeAtrribute(self, ncFileName, attributeDictionary):

        rootgrp = nc.Dataset(ncFileName,'a')

        for k, v in list(attributeDictionary.items()): setattr(rootgrp,k,v)

        rootgrp.sync()
        rootgrp.close()

    def addNewVariable(self, ncFileName, varName, varUnits, longName = None):

        rootgrp = nc.Dataset(ncFileName,'a')

        shortVarName = varName
        longVarName  = varName
        if longName != None: longVarName = longName

        var = rootgrp.createVariable(shortVarName,'f4',('time','lat','lon',) ,fill_value=vos.MV,zlib=self.zlib)
        var.standard_name = varName
        var.long_name = longVarName
        var.units = varUnits

        rootgrp.sync()
        rootgrp.close()

    def data2NetCDF(self, ncFileName, shortVarName, varField, timeStamp, posCnt = None):

        rootgrp = nc.Dataset(ncFileName,'a')

        date_time = rootgrp.variables['time']
        if posCnt == None: posCnt = len(date_time)
        date_time[posCnt] = nc.date2num(timeStamp,date_time.units,date_time.calendar)

        # flip variable if necessary (to follow cf_convention)
        if self.netcdf_y_orientation_follow_cf_convention: varField = np.flipud(varField)
        
        rootgrp.variables[shortVarName][posCnt,:,:] = varField

        rootgrp.sync()
        rootgrp.close()

    def dataList2NetCDF(self, ncFileName, shortVarNameList, varFieldList, timeStamp, posCnt = None):

        rootgrp = nc.Dataset(ncFileName,'a')

        date_time = rootgrp.variables['time']
        if posCnt == None: posCnt = len(date_time)

        for shortVarName in shortVarNameList:
            
            date_time[posCnt] = nc.date2num(timeStamp,date_time.units,date_time.calendar)
            varField = varFieldList[shortVarName]
            
            # flip variable if necessary (to follow cf_convention)
            if self.netcdf_y_orientation_follow_cf_convention: varField = np.flipud(varField)
            
            rootgrp.variables[shortVarName][posCnt,:,:] = varField

        rootgrp.sync()
        rootgrp.close()

    def close(self, ncFileName):

        rootgrp = nc.Dataset(ncFileName,'w')

        # closing the file 
        rootgrp.close()
