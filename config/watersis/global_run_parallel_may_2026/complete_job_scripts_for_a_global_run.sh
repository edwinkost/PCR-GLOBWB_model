#!/bin/bash


JOBNAME="pgb_6min"
#~ JOBNAME=$1

set -x

MAIN_OUTPUT_DIR="/scratch/depfg/sutan101/watersis_runs_may_2026/global_6min_with_watersis_forcing_with_parallel_v20260604/"${JOBNAME}"/"

PCRGLOBWB_MODEL_SCRIPT_FOLDER="/eejit/home/sutan101/github/edwinkost/PCR-GLOBWB_model/model/"

SPINUP_RUN_INI="/eejit/home/sutan101/github/edwinkost/PCR-GLOBWB_model/config/watersis/global_run_parallel_may_2026/setup_6min_global_watersis_develop.ini"
WARMED_RUN_INI="/eejit/home/sutan101/github/edwinkost/PCR-GLOBWB_model/config/watersis/global_run_parallel_may_2026/setup_6min_global_watersis_develop.ini" 

MAIN_INPUT_DIRECTORY="/scratch/depfg/sutan101_new/pcrglobwb_input_watersis/develop/global_6min/"   
PRECIPITATION_FORCING_FILE="/scratch/depfg/sutan101/data/watersis_forcing/global/v20260514/global_pre_0p1_v20260514.nc"
TEMPERATURE_FORCING_FILE="/scratch/depfg/sutan101/data/watersis_forcing/global/v20260514/global_tas_day_0p1_v20260514.nc"  
REF_POT_ET_FORCING_FILE="/scratch/depfg/sutan101/data/watersis_forcing/global/v20260514/global_pet_hargreaves_samani_0p1_v20260514.nc"   

#~ STARTING_DATE="1970-01-01"             
#~ END_DATE="2019-12-31"                  
#~ NUM_OF_YEARS_FOR_SPINUP=1   
#~ MAIN_INITIAL_STATE_FOLDER="dummy_initial_conditions/" 
#~ DATE_FOR_INITIAL_STATES="1999-12-31"   


# spin up run
NUM_OF_YEARS_FOR_SPINUP="25"
SUB_JOBNAME=${JOBNAME}_spinup_with_1970
SUB_INIFILE=${SPINUP_RUN_INI}
STA_DATE="1970-01-01"
END_DATE="1970-12-31"
INITIAL_FOLD="dummy_initial_conditions/"
INITIAL_DATE="1999-12-31"
SUB_OUT_DIR=${MAIN_OUTPUT_DIR}/_spinup/with_1970/

#~ # - for testing
#~ NUM_OF_YEARS_FOR_SPINUP="0"
#~ STA_DATE="1970-12-29"

#~ # - for testing with 5 year spinup
#~ NUM_OF_YEARS_FOR_SPINUP="5"
#~ STA_DATE="1970-01-01"

# - start the run
SPINUP=$(sbatch -J "${SUB_JOBNAME}" --export INI_FILE="${SUB_INIFILE}",MAIN_OUTPUT_DIR="${SUB_OUT_DIR}",STARTING_DATE="${STA_DATE}",END_DATE="${END_DATE}",MAIN_INITIAL_STATE_FOLDER="${INITIAL_FOLD}",DATE_FOR_INITIAL_STATES="${INITIAL_DATE}",NUM_OF_YEARS_FOR_SPINUP="${NUM_OF_YEARS_FOR_SPINUP}",MAIN_INPUT_DIRECTORY="${MAIN_INPUT_DIRECTORY}",PRECIPITATION_FORCING_FILE=${PRECIPITATION_FORCING_FILE},TEMPERATURE_FORCING_FILE=${TEMPERATURE_FORCING_FILE},REF_POT_ET_FORCING_FILE=${REF_POT_ET_FORCING_FILE},PCRGLOBWB_MODEL_SCRIPT_FOLDER=${PCRGLOBWB_MODEL_SCRIPT_FOLDER} job_script_sbatch_pcrglobwb_template.sh | sed 's/Submitted batch job //')


# run for the period 1970-2019
SUB_JOBNAME=${JOBNAME}_1970-2019
SUB_INIFILE=${WARMED_RUN_INI}
STA_DATE="1970-01-01"
END_DATE="2019-12-31"
INITIAL_FOLD=${SUB_OUT_DIR}/global/states/
INITIAL_DATE="1970-12-31"
SUB_OUT_DIR=${MAIN_OUTPUT_DIR}/begin_from_1970/
# - start the run
FIRST=$(sbatch --dependency=afterany:${SPINUP} -J "${SUB_JOBNAME}" --export INI_FILE="${SUB_INIFILE}",MAIN_OUTPUT_DIR="${SUB_OUT_DIR}",STARTING_DATE="${STA_DATE}",END_DATE="${END_DATE}",MAIN_INITIAL_STATE_FOLDER="${INITIAL_FOLD}",DATE_FOR_INITIAL_STATES="${INITIAL_DATE}",NUM_OF_YEARS_FOR_SPINUP="${NUM_OF_YEARS_FOR_SPINUP}",MAIN_INPUT_DIRECTORY="${MAIN_INPUT_DIRECTORY}",PRECIPITATION_FORCING_FILE=${PRECIPITATION_FORCING_FILE},TEMPERATURE_FORCING_FILE=${TEMPERATURE_FORCING_FILE},REF_POT_ET_FORCING_FILE=${REF_POT_ET_FORCING_FILE},PCRGLOBWB_MODEL_SCRIPT_FOLDER=${PCRGLOBWB_MODEL_SCRIPT_FOLDER} job_script_sbatch_pcrglobwb_template.sh | sed 's/Submitted batch job //')
set +x


echo $SPINUP
echo $FIRST

sleep 3
squeue
squeue -u sutan101



