#!/bin/bash 
#PBS -N PCR-GLOBWB
#PBS -q np
#PBS -l EC_nodes=1
#PBS -l EC_total_tasks=72
#PBS -l EC_hyperthreads=2
#PBS -l EC_billing_account=c3s432l3

#~ #PBS -l walltime=48:00:00
#~ #PBS -l walltime=8:00
#~ #PBS -l walltime=1:00:00
#~ #PBS -l walltime=12:00:00
#PBS -l walltime=6:00:00

set -x

# set the folder that contain PCR-GLOBWB model scripts (note that this is not always the latest version)
PCRGLOBWB_MODEL_SCRIPT_FOLDER="/perm/mo/nest/ulysses/src/edwin/ulysses_pgb_source/model/"
#~ PCRGLOBWB_MODEL_SCRIPT_FOLDER="/home/ms/copext/cyes/github/edwinkost/PCR-GLOBWB_model_edwin-private-development/model/"

# set the configuration file (*.ini) that will be used (assumption: the .ini file is located within the same directory as this job, i.e. ${PBS_O_WORKDIR})
INI_FILE=${PBS_O_WORKDIR}/"setup_6arcmin_version_2020-08-XX.ini"
#~ INI_FILE="setup_6arcmin_version_2020-08-XX.ini"

# set the starting and end simulation dates
STARTING_DATE=1996-01-01
END_DATE=1996-01-31
# - for testing
STARTING_DATE=1996-01-29
END_DATE=1996-01-31

# set the output folder
#~ MAIN_OUTPUT_DIR="/scratch/ms/copext/cyes/monthly_pcrglobwb_example_version_2020-08-XX/"
MAIN_OUTPUT_DIR="/scratch/ms/copext/cyes/monthly_pcrglobwb_example_version_2020-08-XX/"${STARTING_DATE}_to_${END_DATE}/

# set the initial conditions (folder and time stamp for the files)
MAIN_INITIAL_STATE_FOLDER="/scratch/ms/copext/cyes/pcrglobwb_output_version_2020-08-14/begin_from_1981/global/states/"
DATE_FOR_INITIAL_STATES=1995-12-31

# set the forcing files
PRECIPITATION_FORCING_FILE="/scratch/mo/nest/ulysses/data/meteo/era5land/1996/01/precipitation_daily_01_1996.nc"
TEMPERATURE_FORCING_FILE="/scratch/mo/nest/ulysses/data/meteo/era5land/1996/01/tavg_01_1996.nc"
REF_POT_ET_FORCING_FILE="/scratch/mo/nest/ulysses/data/meteo/era5land/1996/01/pet_01_1996.nc"




################# PCR-GLOBWB RUNS ######################################

# go to the folder that contain the bash script that will be submitted using aprun
# - using the folder that contain this pbs job script 
cd ${PBS_O_WORKDIR}

# make the run for every clone using aprun
aprun -N $EC_tasks_per_node -n $EC_total_tasks -j $EC_hyperthreads bash pcrglobwb_runs.sh ${INI_FILE} ${MAIN_OUTPUT_DIR} ${STARTING_DATE} ${END_DATE} ${MAIN_INITIAL_STATE_FOLDER} ${DATE_FOR_INITIAL_STATES} ${PRECIPITATION_FORCING_FILE} ${TEMPERATURE_FORCING_FILE} ${REF_POT_ET_FORCING_FILE} ${PCRGLOBWB_MODEL_SCRIPT_FOLDER}

############### end of pcr-globwb runs #################################





################# MERGING ##############################################

# merging netcdf and state files (TODO: Shall we put the following in a separate job and called it with qsub?)
# - load modules on cca (or ccb)
module load python3/3.6.10-01
module load pcraster/4.3.0
module load gdal/3.0.4
# - go to the folder that contain the scripts
cd ${PCRGLOBWB_MODEL_SCRIPT_FOLDER}
# - merging state files
python3 merge_pcraster_maps_6_arcmin_ulysses.py ${END_DATE} ${MAIN_OUTPUT_DIR} states 2 Global 54 False
# - merging netcdf files
python3 merge_netcdf_6_arcmin_ulysses.py ${MAIN_OUTPUT_DIR} ${MAIN_OUTPUT_DIR}/global/netcdf outDailyTotNC ${STARTING_DATE} ${END_DATE} ulyssesP,ulyssesET,ulyssesSWE,ulyssesQsm,ulyssesSM,ulyssesQrRunoff,ulyssesDischarge NETCDF4 False 2 Global

############### end of merging #########################################


set +x