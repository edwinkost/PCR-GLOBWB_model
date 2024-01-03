#!/bin/bash 
#SBATCH -N 1

# on snellius
#SBATCH -n 96
#SBATCH -p genoa
#~ #SBATCH -t 119:59:00
#SBATCH -t 59:00

#SBATCH -J pgb_ulysses

#SBATCH --export MAIN_INPUT_DIRECTORY="/scratch-shared/edwin/pcrglobwb_input_ulysses_v202312XX/develop_edwin/",PCRGLOBWB_MODEL_SCRIPT_FOLDER="/home/edwin/github/edwinkost/PCR-GLOBWB_model/model/",INI_FILE="/home/edwin/github/edwinkost/PCR-GLOBWB_model/config/ulysses/develop_since_2023-12-XX/two_land_covers/global_ulysses/setup_6arcmin_ulysses_2LCs_version_2023-12-14_finalize_global.ini",MAIN_OUTPUT_DIRECTORY="/scratch-shared/edwin/pcrglobwb_ulysses_2023-12-25_global_two_landcovers/2000-01-01_to_2000-01-31/",STARTING_DATE="2000-01-01",END_DATE="2000-01-31",MAIN_INITIAL_STATE_FOLDER="/scratch-shared/edwin/pcrglobwb_input_ulysses_v202312XX/develop_edwin/initial_conditions/",DATE_FOR_INITIAL_STATES="1999-12-31",PRECIPITATION_FORCING_FILE="/projects/0/dfguu2/users/edwin/data/era5land_ulysses/version_20231206/2000/01/pre_01_2000.nc",TEMPERATURE_FORCING_FILE="/projects/0/dfguu2/users/edwin/data/era5land_ulysses/version_20231206/2000/01/tavg_01_2000.nc",REF_POT_ET_FORCING_FILE="/projects/0/dfguu2/users/edwin/data/era5land_ulysses/version_20231206/2000/01/pet_01_2000.nc"

set -x

# load modules on snellius
# - using miniconda
module load 2022
module load Miniconda3/4.12.0
# - abandon any existing PYTHONPATH (recommended, if you want to use miniconda or anaconda)
unset PYTHONPATH
# - activate conda env for pcrglobwb
source activate /home/hydrowld/.conda/envs/pcrglobwb_python3_2023-10-31
#~ # - use 48 workers
#~ export PCRASTER_NR_WORKER_THREADS=48


# set the configuration file (.ini) that will be used
INI_FILE=${INI_FILE}

# set the output folder
MAIN_OUTPUT_DIRECTORY=${MAIN_OUTPUT_DIRECTORY}

# set the starting and end simulation dates
STARTING_DATE=${STARTING_DATE}
END_DATE=${END_DATE}

# set the initial conditions (folder and time stamp for the files)
MAIN_INITIAL_STATE_FOLDER=${MAIN_INITIAL_STATE_FOLDER}
DATE_FOR_INITIAL_STATES=${DATE_FOR_INITIAL_STATES}

# set the forcing files
PRECIPITATION_FORCING_FILE=${PRECIPITATION_FORCING_FILE}
TEMPERATURE_FORCING_FILE=${TEMPERATURE_FORCING_FILE}
REF_POT_ET_FORCING_FILE=${REF_POT_ET_FORCING_FILE}


# go to the folder where the pcrglobwb python scripts are stored
PCRGLOBWB_MODEL_SCRIPT_FOLDER=${PCRGLOBWB_MODEL_SCRIPT_FOLDER}
cd ${PCRGLOBWB_MODEL_SCRIPT_FOLDER}

# make the run
python3 deterministic_runner_ulysses.py ${INI_FILE} no-debug \
-mod          ${MAIN_OUTPUT_DIRECTORY} \
-mid          ${MAIN_INPUT_DIRECTORY} \
-sd           ${STARTING_DATE} \
-ed           ${END_DATE} \
-pff          ${PRECIPITATION_FORCING_FILE} \
-tff          ${TEMPERATURE_FORCING_FILE} \
-rpetff       ${REF_POT_ET_FORCING_FILE} \
-misf         ${MAIN_INITIAL_STATE_FOLDER} \
-dfis         ${DATE_FOR_INITIAL_STATES} \

set +x

exit
