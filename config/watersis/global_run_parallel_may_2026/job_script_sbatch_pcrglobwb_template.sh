#!/bin/bash 
#SBATCH -N 1

#~ # on snellius
#~ #SBATCH -n 96
#~ #SBATCH -p genoa
#~ #SBATCH -t 119:59:00
#~ #SBATCH -t 59:00

# on eejit
#SBATCH -n 96
#SBATCH -p defq
#SBATCH --exclusive

#SBATCH -J pgb_watersis_spinup_and_actual_runs

# mail alert at start, end and abortion of execution
#SBATCH --mail-type=ALL

# send mail to this address
#SBATCH --mail-user=edwinkost@gmail.com

#~ #SBATCH --export INI_FILE=setup_6arcmin.ini,MAIN_OUTPUT_DIR="/scratch/pcrglobwb_ulysses_reference_runs/test/",STARTING_DATE="1981-01-01",END_DATE="2000-12-31",MAIN_INITIAL_STATE_FOLDER="/scratch/spinup/global/states/",DATE_FOR_INITIAL_STATES="1981-12-31",BASEFLOW_EXPONENT="1.0",LOG_10_MULTIPLIER_FOR_KSAT="0.0",LOG_10_MULTIPLIER_FOR_RECESSION_COEFF=0.0,NUM_OF_YEARS_FOR_SPINUP="0.0"

#SBATCH --export INI_FOLDER="config"INI_FILE="setup_6arcmin.ini",MAIN_OUTPUT_DIR="/scratch/pcrglobwb_ulysses_reference_runs/test/",STARTING_DATE="1981-01-01",END_DATE="2000-12-31",MAIN_INITIAL_STATE_FOLDER="/scratch/spinup/global/states/",DATE_FOR_INITIAL_STATES="1981-12-31",NUM_OF_YEARS_FOR_SPINUP="0.0",MAIN_INPUT_DIRECTORY="/INPUT_FOLDER/",PRECIPITATION_FORCING_FILE="/pre.nc",TEMPERATURE_FORCING_FILE="/tavg.nc",REF_POT_ET_FORCING_FILE="/pet0.nc",PCRGLOBWB_MODEL_SCRIPT_FOLDER


set -x

# set the configuration file (*.ini)=
INI_FILE=${INI_FILE}

# set the output folder
MAIN_OUTPUT_DIR=${MAIN_OUTPUT_DIR}

# set the input folder
MAIN_INPUT_DIRECTORY=${MAIN_INPUT_DIRECTORY}

# set the starting and end simulation dates
STARTING_DATE=${STARTING_DATE}
END_DATE=${END_DATE}

# set the initial conditions (folder and time stamp for the files)
MAIN_INITIAL_STATE_FOLDER=${MAIN_INITIAL_STATE_FOLDER}
DATE_FOR_INITIAL_STATES=${DATE_FOR_INITIAL_STATES}

# set the forcing files
#~ PRECIPITATION_FORCING_FILE="NONE"
#~ TEMPERATURE_FORCING_FILE="NONE"
#~ REF_POT_ET_FORCING_FILE="NONE"
PRECIPITATION_FORCING_FILE="${PRECIPITATION_FORCING_FILE}"
TEMPERATURE_FORCING_FILE="${TEMPERATURE_FORCING_FILE}"
REF_POT_ET_FORCING_FILE="${REF_POT_ET_FORCING_FILE}"

#~ # go to the folder that contain the bash script that will be submitted using aprun
#~ # - using the folder that contain this job script 
#~ cd ${PBS_O_WORKDIR}
#~ cd ${SLURM_SUBMIT_DIR}
#~ cd ${INI_FOLDER}

# make the run for every clone 
bash pcrglobwb_runs_71_clones.sh ${INI_FILE} ${MAIN_OUTPUT_DIR} ${STARTING_DATE} ${END_DATE} ${NUM_OF_YEARS_FOR_SPINUP} ${MAIN_INITIAL_STATE_FOLDER} ${DATE_FOR_INITIAL_STATES} ${MAIN_INPUT_DIRECTORY} ${PRECIPITATION_FORCING_FILE} ${TEMPERATURE_FORCING_FILE} ${REF_POT_ET_FORCING_FILE} 

# wait for 30 sec 
sleep 30

set +x

exit
