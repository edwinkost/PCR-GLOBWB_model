#!/bin/bash 

#SBATCH --qos=nf
#SBATCH --job-name=pgb_5km_europe

#SBATCH --mem-per-cpu=1250MB
#SBATCH --ntasks=16
#SBATCH --cpus-per-task=1
#SBATCH --threads-per-core=2

#SBATCH --time=30:00
# A one-month europe 5km run (with this configuration) should take less than XX mins.
#~ #SBATCH --time=15:00


set -x

# load modules on Atos - the following works (and it was used by Robert UFZ)
module load python3/3.10.10-01 
module load pcraster/4.4.0-01 
module load gdal/3.6.2

# to speed up, using some cores/threads
export OMP_NUM_THREADS=8
export PCRASTER_NR_WORKER_THREADS=8

#~ # activate the following for using a single core/thread (lo
#~ # - unset pcraster working threads
#~ unset PCRASTER_NR_WORKER_THREADS
#~ # - you also may have to activate the following
#~ export OPENBLAS_NUM_THREADS=1

# PCR-GLOBWB configuration (.ini) file that will be used  
INI_FILE="setup_5km_europe_watersis_v20260715.ini"
DIR_INI_FILE=$(pwd)
INI_FILE=${DIR_INI_FILE}/${INI_FILE}

# Output directory  
MAIN_OUTPUT_DIRECTORY="/lus/h2resw01/fws4/sb/project/C3SHydroGL/edwin/test_pcrglobwb_europe_5km/with_mk_forcing_with_workers/"     

# Starting and end date.  
STARTING_DATE="2000-01-01"             
END_DATE="2000-01-31"                  

# Number of spin up years (this should be zero, as it is assumed that warm initial conditions are provided). 
NUM_OF_YEARS_FOR_SPINUP=0   

# Initial conditions, folder and the date
MAIN_INITIAL_STATE_FOLDER="/lus/h2resw01/fws4/sb/project/C3SHydroGL/edwin/data/pcrglobwb_input_watersis/release/europe_5km_v20260715/dummy_initial_conditions/from_a_run_on_20260312/" 
DATE_FOR_INITIAL_STATES="1981-12-31"   
# NOTE: Please consider the above initial condition files as dummy. Please use proper warm initial condition files. For the first year, Edwin can also prepare them, but please make sure that the forcing and landmask files are final.

# Model input directory (containing model parameters)
MAIN_INPUT_DIRECTORY="/lus/h2resw01/fws4/sb/project/C3SHydroGL/edwin/data/pcrglobwb_input_watersis/release/europe_5km_v20260715/"   

# Forcing input directory
PRECIPITATION_FORCING_FILE="/ec/fws4/sb/project/C3SHydroGL/phase_3/europe/reanalysis/meteo/emo_era5/2000/01/pr_0p05.nc"
TEMPERATURE_FORCING_FILE="/ec/fws4/sb/project/C3SHydroGL/phase_3/europe/reanalysis/meteo/emo_era5/2000/01/tas_0p05.nc"
REF_POT_ET_FORCING_FILE="/ec/fws4/sb/project/C3SHydroGL/phase_3/europe/reanalysis/meteo/emo_era5/2000/01/pet_hargreaves_samani_0p05.nc" 

# Directory containing the model script files
PCRGLOBWB_MODEL_SCRIPT_FOLDER="/home/cyes/github/edwinkost/PCR-GLOBWB_model/model/"

# go to the folder that contain PCR-GLOBWB model script file
cd ${PCRGLOBWB_MODEL_SCRIPT_FOLDER}

# run the model
python3 deterministic_runner_ulysses.py ${INI_FILE} no-debug  \
-mod     ${MAIN_OUTPUT_DIRECTORY}      \
-mid     ${MAIN_INPUT_DIRECTORY}       \
-sd      ${STARTING_DATE}              \
-ed      ${END_DATE}                   \
-noyfsu  ${NUM_OF_YEARS_FOR_SPINUP}    \
-pff     ${PRECIPITATION_FORCING_FILE} \
-tff     ${TEMPERATURE_FORCING_FILE}   \
-rpetff  ${REF_POT_ET_FORCING_FILE}    \
-misf    ${MAIN_INITIAL_STATE_FOLDER}  \
-dfis    ${DATE_FOR_INITIAL_STATES}    \
-end

set +x

exit

