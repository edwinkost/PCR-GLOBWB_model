#!/bin/bash 

#~ # load modules on Atos - the following works (and it was used by Robert UFZ)
#~ module load python3/3.10.10-01 
#~ module load pcraster/4.4.0-01 
#~ module load gdal/3.6.2

# load software on eejit (somehow pcraster we have to use pcraster 4.3 if we want to use multicore)
conda activate /eejit/home/hydrowld/opt/miniconda3/envs/pcrglobwb_python3_pcraster43_v2024-08-30

# to speed up, using some cores/threads
export OMP_NUM_THREADS=16
export PCRASTER_NR_WORKER_THREADS=16

# PCR-GLOBWB configuration (.ini) file that will be used  
INI_FILE="setup_6min_global_watersis_v202609_develop.ini"
DIR_INI_FILE=$(pwd)
INI_FILE=${DIR_INI_FILE}/${INI_FILE}

# Output directory  
MAIN_OUTPUT_DIRECTORY="/scratch/depfg/sutan101/test_pgb_6min_202609/test/"     

# Starting and end date.  
STARTING_DATE="1981-01-01"             
END_DATE="1981-01-31"                  

# Number of spin up years (this should be zero, as it is assumed that warm initial conditions are provided). 
NUM_OF_YEARS_FOR_SPINUP=0   

# Initial conditions, folder and the date
MAIN_INITIAL_STATE_FOLDER="/scratch/depfg/sutan101/data/pcrglobwb_input_watersis/develop/global_6min/initial_conditions/from_global_6min_run_v20260904/" 
DATE_FOR_INITIAL_STATES="1980-12-31"   

# Model input directory (containing model parameters)
MAIN_INPUT_DIRECTORY="/scratch/depfg/sutan101/data/pcrglobwb_input_watersis/develop/global_6min/"   

# Forcing input directory
#~ PRECIPITATION_FORCING_FILE="/ec/fws4/sb/project/C3SHydroGL/phase_3/global/reanalysis/meteo/era5_em_earth/2000/01/pre_0p1.nc"
#~ TEMPERATURE_FORCING_FILE="/ec/fws4/sb/project/C3SHydroGL/phase_3/global/reanalysis/meteo/era5_em_earth/2000/01/tas_day.nc"  
#~ REF_POT_ET_FORCING_FILE="/ec/fws4/sb/project/C3SHydroGL/phase_3/global/reanalysis/meteo/era5_em_earth/2000/01/pet_hargreaves_samani_0p1.nc"  
PRECIPITATION_FORCING_FILE="/scratch/depfg/sutan101/data/watersis_forcing/global/v20260813/global_pre_0p1_v20260813.nc"
TEMPERATURE_FORCING_FILE="/scratch/depfg/sutan101/data/watersis_forcing/global/v20260813/global_tas_day_0p1_v20260813.nc"  
REF_POT_ET_FORCING_FILE="/scratch/depfg/sutan101/data/watersis_forcing/global/v20260813/global_pet_hargreaves_samani_0p1_v20260813.nc"   

# Directory containing the model script files
#~ PCRGLOBWB_MODEL_SCRIPT_FOLDER="/home/cyes/github/edwinkost/PCR-GLOBWB_model/model/"
PCRGLOBWB_MODEL_SCRIPT_FOLDER="/eejit/home/sutan101/gits/github/edwinkost/PCR-GLOBWB_model/model/"

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



