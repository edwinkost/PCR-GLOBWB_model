#!/bin/bash

#SBATCH -p genoa

#SBATCH -N 1
## you reserve one node

#SBATCH -n 96

#SBATCH -t 119:59:00
## this is the time, maximum 120:00:00 hours

#SBATCH -J wmo_run
## this is the job name


# mail alert at start, end and abortion of execution
#SBATCH --mail-type=ALL
#~ #~
# send mail to this address
#SBATCH --mail-user=edwinkost@gmail.com


accinfo


set -x


# folder containing .ini file
#~ INI_FOLDER=$(pwd)
INI_FOLDER="/home/edwin/github/edwinkost/PCR-GLOBWB_model_branch_wmo_2024_run/config/wmo_run_2024/"

$(pwd)

# configuration (.ini) file
INI_FILE=${INI_FOLDER}/"setup_05min_wmo_run.ini"


# starting and end dates
STARTING_DATE="1981-01-01"
END_DATE="2024-12-31"


# location/folder, where you will store output files of your 
MAIN_OUTPUT_DIR="/scratch-shared/edwin/pcrglobwb_wmo_run/version20250417"


# meteorological forcing files - DEFINED IN THE CONFIGURATION FILE


# initial conditions
MAIN_INITIAL_STATE_FOLDER="/projects/0/dfguu/users/edwin/data/pcrglobwb_input_aqueduct/version_2021-09-16/initial_conditions/"
DATE_FOR_INITIAL_STATES="2019-12-31"


# number of spinup years
NUMBER_OF_SPINUP_YEARS="25"
#~ # - PS: For continuing runs, please set it to zero
#~ NUMBER_OF_SPINUP_YEARS="0"


# location of your pcrglobwb model scripts
PCRGLOBWB_MODEL_SCRIPT_FOLDER="/home/edwin/github/edwinkost/PCR-GLOBWB_model_branch_wmo_2024_run/"


# load the conda enviroment and other things
. /home/edwin/load_all_default.sh


# unset pcraster working threads (due to a limited number of cores on the Azure VM)
unset PCRASTER_NR_WORKER_THREADS


# test pcraster
pcrcalc


# go to the folder that contain PCR-GLOBWB scripts
cd ${PCRGLOBWB_MODEL_SCRIPT_FOLDER}
pwd


# run the model for all clones, from 1 to 53

#~ # - for testing
#~ for i in {2..2}

# - loop through all clones
for i in {1..53}

do

CLONE_CODE=${i}
python3 deterministic_runner_with_arguments.py ${INI_FILE} debug_parallel ${CLONE_CODE} -mod ${MAIN_OUTPUT_DIR} -sd ${STARTING_DATE} -ed ${END_DATE} -misd ${MAIN_INITIAL_STATE_FOLDER} -dfis ${DATE_FOR_INITIAL_STATES} -num_of_sp_years ${NUMBER_OF_SPINUP_YEARS} &


done


# process for merging files at the global extent
python3 deterministic_runner_merging_with_arguments.py ${INI_FILE} parallel -mod ${MAIN_OUTPUT_DIR} -sd ${STARTING_DATE} -ed ${END_DATE} &


# wait until process is finished
wait


echo "end of model runs (please check your results)"

