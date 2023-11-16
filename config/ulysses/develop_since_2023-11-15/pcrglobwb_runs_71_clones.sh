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
MAIN_INITIAL_STATE_FOLDER=$5         
DATE_FOR_INITIAL_STATES=$6           
PRECIPITATION_FORCING_FILE=$7        
TEMPERATURE_FORCING_FILE=$8          
REF_POT_ET_FORCING_FILE=$9           
BASEFLOW_EXPONENT=${10}              
LOG_10_MULTIPLIER_FOR_KSAT=${11}     
NUM_OF_YEARS_FOR_SPINUP=${12}        

PCRGLOBWB_MODEL_SCRIPT_FOLDER="/home/edwin/github/edwinkost/PCR-GLOBWB_model/model/"

#~ # load modules on cca (or ccb)
#~ module load python3/3.6.10-01
#~ module load pcraster/4.3.0
#~ module load gdal/3.0.4
#~ # - use 4 working threads
#~ export PCRASTER_NR_WORKER_THREADS=4


#~ # load modules on eejit
#~ . /quanta1/home/sutan101/load_my_miniconda_and_my_default_env.sh
#~ # - unset pcraster working threads
#~ unset PCRASTER_NR_WORKER_THREADS


# load modules on snellius
. /home/edwin/load_all_default.sh
# - unset pcraster working threads
unset PCRASTER_NR_WORKER_THREADS



# go to the folder that contain PCR-GLOBWB scripts
cd ${PCRGLOBWB_MODEL_SCRIPT_FOLDER}


# run the model for all clones, from 1 to 71

#~ for i in {1..71}

# - for testing
for i in {2..3}


do

CLONE_CODE=${i}
python3 deterministic_runner_ulysses.py ${INI_FILE} debug_parallel ${CLONE_CODE} \
-mod         ${MAIN_OUTPUT_DIRECTORY} \
-sd          ${STARTING_DATE} \
-ed          ${END_DATE} \
-noyfsu      ${NUM_OF_YEARS_FOR_SPINUP} \
-pff         ${PRECIPITATION_FORCING_FILE} \
-tff         ${TEMPERATURE_FORCING_FILE} \
-rpetff      ${REF_POT_ET_FORCING_FILE} \
-misf        ${MAIN_INITIAL_STATE_FOLDER} \
-dfis        ${DATE_FOR_INITIAL_STATES} \
-bfexp       ${BASEFLOW_EXP} \
-log10mfksat ${LOG_10_MULTIPLIER_FOR_KSAT} \
&

done


# merging process
python3 dynamic_file_merging_ulysses.py ${INI_FILE} \
-mod         ${MAIN_OUTPUT_DIRECTORY} \
-sd          ${STARTING_DATE} \
-ed          ${END_DATE} \
-noyfsu      ${NUM_OF_YEARS_FOR_SPINUP} \
-pff         ${PRECIPITATION_FORCING_FILE} \
-tff         ${TEMPERATURE_FORCING_FILE} \
-rpetff      ${REF_POT_ET_FORCING_FILE} \
-misf        ${MAIN_INITIAL_STATE_FOLDER} \
-dfis        ${DATE_FOR_INITIAL_STATES} \
-bfexp       ${BASEFLOW_EXP} \
-log10mfksat ${LOG_10_MULTIPLIER_FOR_KSAT} \
&

wait

