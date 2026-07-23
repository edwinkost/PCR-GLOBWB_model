#!/bin/bash 

#~ echo "Arg 0: $0"
#~ echo "Arg 1: $1"
#~ echo "Arg 2: $2"
#~ 
#~ for arg in "$@"
#~ do
    #~ echo "$arg"
#~ done


set -x

# get the aguments
INI_FILE=$1                          
MAIN_OUTPUT_DIRECTORY=$2             
STARTING_DATE=$3                     
END_DATE=$4                          
NUM_OF_YEARS_FOR_SPINUP=$5        
MAIN_INITIAL_STATE_FOLDER=$6         
DATE_FOR_INITIAL_STATES=$7           
MAIN_INPUT_DIRECTORY=$8
PRECIPITATION_FORCING_FILE=$9        
TEMPERATURE_FORCING_FILE=${10}          
REF_POT_ET_FORCING_FILE=${11}           
PCRGLOBWB_MODEL_SCRIPT_FOLDER=${12}

#~ # example of input arguments
#~ INI_FILE="../config/watersis/global_run_parallel_may_2026/setup_6min_global_watersis_develop.ini"
#~ MAIN_OUTPUT_DIRECTORY="/scratch/depfg/sutan101/watersis_runs_may_2026/test_global_6min_with_watersis_forcing_with_parallel/test_multiple_clones/"     
#~ STARTING_DATE="1970-01-01"             
#~ END_DATE="2019-12-31"                  
#~ NUM_OF_YEARS_FOR_SPINUP=1   
#~ MAIN_INITIAL_STATE_FOLDER="dummy_initial_conditions/" 
#~ DATE_FOR_INITIAL_STATES="1999-12-31"   
#~ MAIN_INPUT_DIRECTORY="/scratch/depfg/sutan101_new/pcrglobwb_input_watersis/develop/global_6min/"   
#~ PRECIPITATION_FORCING_FILE="/scratch/depfg/sutan101/data/watersis_forcing/global/v20260514/global_pre_0p1_v20260514.nc"
#~ TEMPERATURE_FORCING_FILE="/scratch/depfg/sutan101/data/watersis_forcing/global/v20260514/global_tas_day_0p1_v20260514.nc"  
#~ REF_POT_ET_FORCING_FILE="/scratch/depfg/sutan101/data/watersis_forcing/global/v20260514/global_pet_hargreaves_samani_0p1_v20260514.nc"   
#~ PCRGLOBWB_MODEL_SCRIPT_FOLDER="/eejit/home/sutan101/github/edwinkost/PCR-GLOBWB_model/model/"



# load modules on eejit
. /eejit/home/sutan101/load_default.sh

#~ # load modules on snellius
#~ . /home/edwin/load_all_default.sh

# - unset pcraster working threads
unset PCRASTER_NR_WORKER_THREADS

# - you may have to activate the following
export OPENBLAS_NUM_THREADS=1

# go to the folder that contain PCR-GLOBWB scripts
cd ${PCRGLOBWB_MODEL_SCRIPT_FOLDER}


# run the model for all clones, from 1 to 71

for i in {1..71}

#~ # - for testing
#~ for i in {2..2}


do

CLONE_CODE=${i}
python3 deterministic_runner_ulysses.py ${INI_FILE} debug_parallel ${CLONE_CODE} \
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
&

done


# merging process
python3 dynamic_file_merging_ulysses.py ${INI_FILE} \
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
&

wait

exit
