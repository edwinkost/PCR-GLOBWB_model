#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# PCR-GLOBWB (PCRaster Global Water Balance) Global Hydrological Model
#
# Copyright (C) 2016, Ludovicus P. H. (Rens) van Beek, Edwin H. Sutanudjaja, Yoshihide Wada,
# Joyce H. C. Bosmans, Niels Drost, Inge E. M. de Graaf, Kor de Jong, Patricia Lopez Lopez,
# Stefanie Pessenteiner, Oliver Schmitz, Menno W. Straatsma, Niko Wanders, Dominik Wisser,
# and Marc F. P. Bierkens,
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
import shutil
import datetime

import pcraster as pcr
from pcraster.framework import DynamicModel
from pcraster.framework import DynamicFramework

from configuration import Configuration
from currTimeStep import ModelTime
from reporting import Reporting
from spinUp import SpinUp

from pcrglobwb import PCRGlobWB

from modify_ini_file import *

import logging
logger = logging.getLogger(__name__)

import disclaimer

class DeterministicRunner(DynamicModel):

    def __init__(self, configuration, modelTime, initialState = None, system_argument = None, spinUpRun = False):
        DynamicModel.__init__(self)

        self.modelTime = modelTime        
        self.model = PCRGlobWB(configuration, modelTime, initialState, spinUpRun)
        self.reporting = Reporting(configuration, self.model, modelTime)
        
        # option to include merging processes for pcraster maps and netcdf files:
        # - default option
        self.with_merging = False
        # - set based on ini file
        if ('with_merging' in configuration.globalOptions.keys()) and (configuration.globalOptions['with_merging'] == "False"):
            self.with_merging = False
        if ('with_merging' in configuration.globalOptions.keys()) and (configuration.globalOptions['with_merging'] == "True"):
            self.with_merging = True

        # for a run with spinUp, we have to disactivate merging
        if spinUpRun == True: 
            logger.info("During spin-up runs, no merging (of pcraster maps and netcdf files) will be executed.")
            self.with_merging = False
        
        # make the configuration available for the other method/function
        self.configuration = configuration

    def initial(self): 
        pass

    def dynamic(self):

        # re-calculate current model time using current pcraster timestep value
        self.modelTime.update(self.currentTimeStep())

        # read model forcing (will pick up current model time from model time object)
        self.model.read_forcings()
        
        # update model (will pick up current model time from model time object)
        self.model.update(report_water_balance = True)
		
        # do any needed reporting for this time step        
        self.reporting.report()

        # if runs are executed with_merging, halt calculation until related merging process are ready
        if self.modelTime.isLastDayOfMonth() and self.with_merging:
            
            # wait until merged files are ready
            merged_files_are_ready = False
            self.count_check = 0
            while merged_files_are_ready == False:
                if datetime.datetime.now().second == 14 or\
                   datetime.datetime.now().second == 29 or\
                   datetime.datetime.now().second == 34 or\
                   datetime.datetime.now().second == 59:\
                   merged_files_are_ready = self.check_merging_status()

    def check_merging_status(self):

        # ~ status_file = str(self.configuration.main_output_directory) + "/global/maps/merged_files_for_"    + str(self.modelTime.fulldate) + "_are_ready.txt"

        status_file = str(self.configuration.main_output_directory) + "/../global/maps/merged_files_for_"    + str(self.modelTime.fulldate) + "_are_ready.txt"

        msg = 'Waiting for the file: ' + status_file
        if self.count_check == 1: logger.info(msg)
        if self.count_check < 7:
            logger.debug(msg)			# INACTIVATE THIS AS THIS MAKE A HUGE DEBUG (dbg) FILE
            self.count_check = self.count_check + 1
        status = os.path.exists(status_file)
        if status == False: return status	
        if status: self.count_check = 0            
        return status
 
 
def main():
    
    # print disclaimer
    disclaimer.print_disclaimer()

    # get the full path of configuration/ini file given in the system argument
    iniFileName   = os.path.abspath(sys.argv[1])
    
    # modify ini file and return it in a new location 
    if "-mod" in sys.argv:
        # replace the configuration file based on the system arguments that are given
        iniFileName   = modify_ini_file(original_ini_file = iniFileName,
                                        system_argument   = sys.argv)
    
    # debug option
    debug_mode = False
    if len(sys.argv) > 2: 
        if sys.argv[2] == "debug" or sys.argv[2] == "debug_parallel" or sys.argv[2] == "debug-parallel": debug_mode = True
    

    # parallel option
    this_run_is_part_of_a_set_of_parallel_run = False    
    if len(sys.argv) > 2: 
        if sys.argv[2] == "parallel" or sys.argv[2] == "debug_parallel" or sys.argv[2] == "debug-parallel": this_run_is_part_of_a_set_of_parallel_run = True

    # object to handle configuration/ini file
    configuration = Configuration(iniFileName = iniFileName, \
                                  debug_mode = debug_mode, \
                                  no_modification = False)      

    
    # for a parallel run (e.g. usually for 5min and 6min runs), we assign a specific directory based on the clone number/code:
    if this_run_is_part_of_a_set_of_parallel_run:
        # modfiying clone-map landmask, etc (based on the given system arguments)
        # - clone code in string
        clone_code = str(sys.argv[3])
        # - clone map
        configuration.globalOptions['cloneMap'] = configuration.globalOptions['cloneMap'] %(int(clone_code))
        # - landmask for model calculation
        if configuration.globalOptions['landmask'] != "None":
            configuration.globalOptions['landmask']   = configuration.globalOptions['landmask'] %(int(clone_code))
        # - landmask for reporting
        if configuration.reportingOptions['landmask_for_reporting'] != "None":
            configuration.reportingOptions['landmask_for_reporting'] = configuration.reportingOptions['landmask_for_reporting'] %(int(clone_code))

        # ~ # Note that output folder is set on modify_ini_file.py
        # ~ # - output folder
        # ~ output_folder_with_clone_code = "M%07i" %int(clone_code)
        # ~ configuration.globalOptions['outputDir'] += "/" + output_folder_with_clone_code 

    # set configuration
    configuration.set_configuration(system_arguments = sys.argv)
    

    # timeStep info: year, month, day, doy, hour, etc
    currTimeStep = ModelTime() 

    # object for spin_up
    spin_up = SpinUp(configuration)            
    
    # spinning-up 
    noSpinUps = int(configuration.globalOptions['maxSpinUpsInYears'])
    initial_state = None
    if noSpinUps > 0:
        
        logger.info('Spin-Up #Total Years: '+str(noSpinUps))

        spinUpRun = 0 ; has_converged = False
        while spinUpRun < noSpinUps and has_converged == False:
            spinUpRun += 1
            currTimeStep.getStartEndTimeStepsForSpinUp(
                    configuration.globalOptions['startTime'],
                    spinUpRun, noSpinUps)
            logger.info('Spin-Up Run No. '+str(spinUpRun))
            deterministic_runner = DeterministicRunner(configuration, currTimeStep, initial_state, sys.argv, spinUpRun = True)
            
            all_state_begin = deterministic_runner.model.getAllState() 
            
            dynamic_framework = DynamicFramework(deterministic_runner,currTimeStep.nrOfTimeSteps)
            dynamic_framework.setQuiet(True)
            dynamic_framework.run()
            
            all_state_end = deterministic_runner.model.getAllState() 
            
            has_converged = spin_up.checkConvergence(all_state_begin, all_state_end, spinUpRun, deterministic_runner.model.routing.cellArea)
            
            initial_state = deterministic_runner.model.getState()
            
        # TODO: for a parallel run call merging when the spinUp is done and isolate the states in a separate directory/folder

    # Running the deterministic_runner (excluding DA scheme)
    currTimeStep.getStartEndTimeSteps(configuration.globalOptions['startTime'],
                                      configuration.globalOptions['endTime'])
    
    logger.info('Transient simulation run started.')
    deterministic_runner = DeterministicRunner(configuration, currTimeStep, initial_state, sys.argv, spinUpRun = False)
    
    dynamic_framework = DynamicFramework(deterministic_runner,currTimeStep.nrOfTimeSteps)
    dynamic_framework.setQuiet(True)
    dynamic_framework.run()

if __name__ == '__main__':
    # print disclaimer
    disclaimer.print_disclaimer(with_logger = True)
    sys.exit(main())

