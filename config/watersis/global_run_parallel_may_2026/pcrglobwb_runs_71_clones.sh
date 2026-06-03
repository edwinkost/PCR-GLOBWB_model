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
=MAIN_INITIAL_STATE_FOLDER=$6         
DATE_FOR_INITIAL_STATES=$7           
MAIN_INPUT_DIRECTORY=$8
PRECIPITATION_FORCING_FILE=$8        
TEMPERATURE_FORCING_FILE=$9          
REF_POT_ET_FORCING_FILE=${10}           

#~ # on snellius
#~ PCRGLOBWB_MODEL_SCRIPT_FOLDER="/home/edwin/github/edwinkost/PCR-GLOBWB_model/model/"

# on eejit
PCRGLOBWB_MODEL_SCRIPT_FOLDER="/eejit/home/sutan101/github/edwinkost/PCR-GLOBWB_model/model/"

# load modules on eejit
. /eejit/home/sutan10/load_default.sh

#~ # load modules on snellius
#~ . /home/edwin/load_all_default.sh

# - unset pcraster working threads
unset PCRASTER_NR_WORKER_THREADS

#~ # - you may have to activate the following
#~ export OPENBLAS_NUM_THREADS=1

# go to the folder that contain PCR-GLOBWB scripts
cd ${PCRGLOBWB_MODEL_SCRIPT_FOLDER}


# run the model for all clones, from 1 to 71

for i in {1..71}

#~ # - for testing
#~ for i in {2..2}


do

CLONE_CODE=${i}
python3 deterministic_runner_ulysses.py ${INI_FILE} debug_parallel ${CLONE_CODE} \
-mod          ${MAIN_OUTPUT_DIRECTORY} \
-sd           ${STARTING_DATE} \
-ed           ${END_DATE} \
-noyfsu       ${NUM_OF_YEARS_FOR_SPINUP} \
-pff          ${PRECIPITATION_FORCING_FILE} \
-tff          ${TEMPERATURE_FORCING_FILE} \
-rpetff       ${REF_POT_ET_FORCING_FILE} \
-misf         ${MAIN_INITIAL_STATE_FOLDER} \
-dfis         ${DATE_FOR_INITIAL_STATES} \
-bfexp        ${BASEFLOW_EXPONENT} \
-log10mfksat  ${LOG_10_MULTIPLIER_FOR_KSAT} \
-log10mfreccf ${LOG_10_MULTIPLIER_FOR_RECESSION_COEFF} \
&

done


# merging process
python3 dynamic_file_merging_ulysses.py ${INI_FILE} \
-mod          ${MAIN_OUTPUT_DIRECTORY} \
-sd           ${STARTING_DATE} \
-ed           ${END_DATE} \
-noyfsu       ${NUM_OF_YEARS_FOR_SPINUP} \
-pff          ${PRECIPITATION_FORCING_FILE} \
-tff          ${TEMPERATURE_FORCING_FILE} \
-rpetff       ${REF_POT_ET_FORCING_FILE} \
-misf         ${MAIN_INITIAL_STATE_FOLDER} \
-dfis         ${DATE_FOR_INITIAL_STATES} \
-bfexp        ${BASEFLOW_EXPONENT} \
-log10mfksat  ${LOG_10_MULTIPLIER_FOR_KSAT} \
-log10mfreccf ${LOG_10_MULTIPLIER_FOR_RECESSION_COEFF} \
&

wait

exit
