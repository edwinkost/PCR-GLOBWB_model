#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
import sys
import datetime
import glob
import shutil

from six.moves.configparser import RawConfigParser as ConfigParser

import disclaimer

def modify_ini_file(original_ini_file,
                    system_argument): 

    # created by Edwin H. Sutanudjaja on August 2020 for the Ulysses project
    
    # parse the configuration (.ini) file and check whether there is a section "modificationBasedOnSystemArgumentOptions" 
    config = ConfigParser()
    config.optionxform = str
    config.read(original_ini_file)
    # all sections provided in the configuration/ini file
    allSections = config.sections()

    if "modificationBasedOnSystemArgumentOptions" not in allSections: return original_ini_file


    if "modificationBasedOnSystemArgumentOptions" in allSections:

        # a dictionary containing the system argument codes (e.g. -xyz, -abc) and their variable names (e.g. DEFGH and OPQRSTU)
        ini_variables = {}

        options = config.options("modificationBasedOnSystemArgumentOptions")
        for opt in options:
            val = config.get("modificationBasedOnSystemArgumentOptions", opt)  # value defined in every option 
            ini_variables[opt] = val                                           # example: ini_variables["-mod"] = "OUTPUT_FOLDER"
        
        # open and read the configuration (.ini) file
        file_ini = open(original_ini_file, "rt")
        # - content of the configuration file
        file_ini_content = file_ini.read()
        file_ini.close()
        

        for var in ini_variables.keys():
             
             assigned_string = system_argument[system_argument.index(var) + 1]
	    
             # for the output directory
             if var == "-mod":
	    		 
                 output_dir = assigned_string
                 
                 # parallel option
                 this_run_is_part_of_a_set_of_parallel_run = False    
                 if system_argument[2] == "parallel" or system_argument[2] == "debug_parallel": this_run_is_part_of_a_set_of_parallel_run = True
                 
                 # for a parallel run (usually at the resolutions of 6 or 5 arcmins, or higher), we assign the following based on the clone number/code:
                 if this_run_is_part_of_a_set_of_parallel_run:

                     # set the output directory for every clone
                     clone_code = "M%07i" %int(str(sys.argv[3])) 
                     assigned_string = assigned_string + "/" + clone_code + "/"

                     output_dir      = assigned_string
	    
             file_ini_content = file_ini_content.replace(ini_variables[var], assigned_string)
             msg = "The string " + str(ini_variables[var]) + " in the given configuration file is replaced with the one given after the system argument " +  str(var) + ": "  + assigned_string + "."
	    
             print(msg)
	    
	    
        # folder for saving original and modified ini files
        folder_for_ini_files = os.path.join(output_dir, "ini_files")
        # - create folder
        if os.path.exists(folder_for_ini_files): shutil.rmtree(folder_for_ini_files)
        os.makedirs(folder_for_ini_files)
        
        # save/copy the original ini file
        shutil.copy(original_ini_file, os.path.join(folder_for_ini_files, os.path.basename(original_ini_file) + ".original"))
	    
        # save the new ini file
        new_ini_file_name = os.path.join(folder_for_ini_files, os.path.basename(original_ini_file) + ".modified_and_used")
        new_ini_file = open(new_ini_file_name, "w")
        new_ini_file.write(file_ini_content)
        new_ini_file.close()
                
        return new_ini_file_name
