#!/bin/bash 

#SBATCH --qos=nf
#SBATCH --job-name=pgb_6min_global

#SBATCH --mem-per-cpu=1250MB
#SBATCH --ntasks=16
#SBATCH --cpus-per-task=1
#SBATCH --threads-per-core=2

#SBATCH --time=30:00
# A one-month global 6min run (with this configuration) should take less than 15 mins.
#~ #SBATCH --time=15:00

# load modules on Atos - the following works (and it was used by Robert UFZ), note that the other pcraster versions above the following do not work with multicore
module load python3/3.10.10-01 
module load pcraster/4.4.0-01 
module load gdal/3.6.2

# to speed up, using some cores/threads
export OMP_NUM_THREADS=16
export PCRASTER_NR_WORKER_THREADS=16

# PCR-GLOBWB configuration (.ini) file that will be used  
INI_FILE="setup_6min_global_watersis_v202609_develop.ini"
DIR_INI_FILE=$(pwd)
INI_FILE=${DIR_INI_FILE}/${INI_FILE}

# Output directory  
MAIN_OUTPUT_DIRECTORY="/lus/h2resw01/fws4/sb/project/C3SHydroGL/edwin/test_pgb_6min_202609/test/"     

# Model input directory (containing model parameters)
#~ MAIN_INPUT_DIRECTORY="/scratch/depfg/sutan101/data/pcrglobwb_input_watersis/develop/global_6min/"   
MAIN_INPUT_DIRECTORY="/home/cyes/C3SHydroGL/edwin/data/pcrglobwb_input_watersis/release/global_6min_v20260922/"   

# Starting and end date.  
STARTING_DATE="1981-01-01"             
END_DATE="1981-01-31"                  

# Number of spin up years (this should be zero, as it is assumed that warm initial conditions are provided). 
NUM_OF_YEARS_FOR_SPINUP=0   

# Initial conditions, folder and the date
#~ MAIN_INITIAL_STATE_FOLDER="/scratch/depfg/sutan101/data/pcrglobwb_input_watersis/develop/global_6min/initial_conditions/from_global_6min_run_v20260904/" 
#~ MAIN_INITIAL_STATE_FOLDER="initial_conditions/from_global_6min_run_v20260904/"
MAIN_INITIAL_STATE_FOLDER="/home/cyes/C3SHydroGL/edwin/data/pcrglobwb_input_watersis/release/global_6min_v20260922/initial_conditions/from_global_6min_run_v20260904/" 
DATE_FOR_INITIAL_STATES="1980-12-31"   


# Forcing input directory
#~ PRECIPITATION_FORCING_FILE="/scratch/depfg/sutan101/data/watersis_forcing/global/v20260813/global_pre_0p1_v20260813.nc"
#~ TEMPERATURE_FORCING_FILE="/scratch/depfg/sutan101/data/watersis_forcing/global/v20260813/global_tas_day_0p1_v20260813.nc"  
#~ REF_POT_ET_FORCING_FILE="/scratch/depfg/sutan101/data/watersis_forcing/global/v20260813/global_pet_hargreaves_samani_0p1_v20260813.nc"   
#~ PRECIPITATION_FORCING_FILE="/ec/fws4/sb/project/C3SHydroGL/phase_3/global/reanalysis/meteo/era5_em_earth/2000/01/pre_0p1.nc"
#~ TEMPERATURE_FORCING_FILE="/ec/fws4/sb/project/C3SHydroGL/phase_3/global/reanalysis/meteo/era5_em_earth/2000/01/tas_day.nc"  
#~ REF_POT_ET_FORCING_FILE="/ec/fws4/sb/project/C3SHydroGL/phase_3/global/reanalysis/meteo/era5_em_earth/2000/01/pet_hargreaves_samani_0p1.nc"  
PRECIPITATION_FORCING_FILE="/ec/fws4/sb/project/C3SHydroGL/phase_3/global/reanalysis/meteo/era5/mem_00/1981/01/pr_era5_mem_00_1981-01-01_1981-01-31_daily.nc"
TEMPERATURE_FORCING_FILE="/ec/fws4/sb/project/C3SHydroGL/phase_3/global/reanalysis/meteo/era5/mem_00/1981/01/tas_era5_mem_00_1981-01-01_1981-01-31_daily.nc"  
REF_POT_ET_FORCING_FILE="/ec/fws4/sb/project/C3SHydroGL/phase_3/global/reanalysis/meteo/era5/mem_00/1981/01/pet_era5_mem_00_1981-01-01_1981-01-31_daily.nc"  

# Directory containing the model script files
PCRGLOBWB_MODEL_SCRIPT_FOLDER="/home/cyes/github/edwinkost/PCR-GLOBWB_model/model/"

# go to the folder that contain PCR-GLOBWB model script file
cd ${PCRGLOBWB_MODEL_SCRIPT_FOLDER}

# run the model
#~ python3 deterministic_runner_ulysses.py ${INI_FILE} no-debug  \
python3 deterministic_runner_ulysses.py ${INI_FILE} debug  \
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



