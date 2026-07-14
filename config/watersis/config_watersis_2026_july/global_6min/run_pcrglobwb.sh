#!/bin/bash 

#SBATCH --qos=nf
#SBATCH --job-name=pcrglobwb_ulysses

#SBATCH --mem-per-cpu=1250MB
#SBATCH --ntasks=16
#SBATCH --cpus-per-task=1
#SBATCH --threads-per-core=2

#SBATCH --time=30:00
# A one-month run (with this configuration) should take less than 15 mins.
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
INI_FILE="setup_6min_global_watersis_nopar_v20260714.ini"

# Output directory  
MAIN_OUTPUT_DIRECTORY="/lus/h2resw01/fws4/sb/project/C3SHydroGL/edwin/test_final_pcrglobwb_global_6min/with_mk_forcing_with_workers/"     

# Starting and end date.  
STARTING_DATE="2000-01-01"             
END_DATE="2000-01-31"                  

# Number of spin up years (this should be zero, as it is assumed that warm initial conditions are provided). 
NUM_OF_YEARS_FOR_SPINUP=0   

# Initial conditions, folder and the date
MAIN_INITIAL_STATE_FOLDER="initial_conditions/from_run_v20260604/" 
DATE_FOR_INITIAL_STATES="1999-12-31"   
# NOTE: Please use proper warm initial condition files. For the first year, I can also prepare them, but please make sure that the forcing files are final.

# Model input directory (containing model parameters)
MAIN_INPUT_DIRECTORY="/home/cyes/C3SHydroGL/edwin/data/pcrglobwb_input_watersis/release/global_6min_v20260710/"   

# Forcing input directory
PRECIPITATION_FORCING_FILE="/ec/fws4/sb/project/C3SHydroGL/phase_3/global/reanalysis/meteo/era5_em_earth/2000/01/pre_0p1.nc"
TEMPERATURE_FORCING_FILE="/ec/fws4/sb/project/C3SHydroGL/phase_3/global/reanalysis/meteo/era5_em_earth/2000/01/tas_day.nc"  
REF_POT_ET_FORCING_FILE="/ec/fws4/sb/project/C3SHydroGL/phase_3/global/reanalysis/meteo/era5_em_earth/2000/01/pet_hargreaves_samani_0p1.nc"  

# Directory containing the model script
PCRGLOBWB_MODEL_SCRIPT_FOLDER="/home/cyes/github/edwinkost/PCR-GLOBWB_model/model/"

# go to the folder that contain PCR-GLOBWB scripts
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

