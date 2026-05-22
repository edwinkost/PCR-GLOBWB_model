#!/bin/bash

JOBNAME="test"
#~ JOBNAME=$1

SPINUP_RUN_INI="setup_6min_global_watersis_develop.ini"
WARMED_RUN_INI="setup_6min_global_watersis_develop.ini" 

MAIN_OUTPUT_DIR="/scratch/depfg/sutan101/watersis_runs_may_2026/test_global_6min/"${JOBNAME}"/"

set -x

# main input folder
MAIN_INPUT_DIRECTORY="/scratch/depfg/sutan101/pcrglobwb_input_watersis/develop/global_6min/"

# spin up run
NUM_OF_YEARS_FOR_SPINUP="25"
SUB_JOBNAME=${JOBNAME}_spinup_with_1981
SUB_INIFILE=${SPINUP_RUN_INI}
STA_DATE="1981-01-01"
END_DATE="1981-12-31"
INITIAL_FOLD="/scratch/depfg/sutan101/pcrglobwb_input_watersis/develop/global_6min/dummy_initial_conditions/after_spinups_with_1981/"
INITIAL_DATE="1981-12-31"
SUB_OUT_DIR=${MAIN_OUTPUT_DIR}/_spinup/with_1981/

# - for testing
NUM_OF_YEARS_FOR_SPINUP="0"
STA_DATE="1981-12-29"

#~ # - for testing with 5 year spinup
#~ NUM_OF_YEARS_FOR_SPINUP="5"
#~ STA_DATE="1981-01-01"

# - start the run
SPINUP=$(sbatch -J "${SUB_JOBNAME}" --export INI_FILE="${SUB_INIFILE}",MAIN_OUTPUT_DIR="${SUB_OUT_DIR}",STARTING_DATE="${STA_DATE}",END_DATE="${END_DATE}",MAIN_INITIAL_STATE_FOLDER="${INITIAL_FOLD}",DATE_FOR_INITIAL_STATES="${INITIAL_DATE}",NUM_OF_YEARS_FOR_SPINUP="${NUM_OF_YEARS_FOR_SPINUP}",MAIN_INPUT_DIRECTORY="${MAIN_INPUT_DIRECTORY}" job_script_sbatch_pcrglobwb_template.sh | sed 's/Submitted batch job //')


# run for the period 1981-2019
SUB_JOBNAME=${JOBNAME}_1981-2019
SUB_INIFILE=${WARMED_RUN_INI}
STA_DATE="1981-01-01"
END_DATE="2019-12-31"
INITIAL_FOLD=${SUB_OUT_DIR}/global/states/
INITIAL_DATE="1981-12-31"
SUB_OUT_DIR=${MAIN_OUTPUT_DIR}/begin_from_1981/
# - start the run
FIRST=$(sbatch --dependency=afterany:${SPINUP} -J "${SUB_JOBNAME}" --export INI_FILE="${SUB_INIFILE}",MAIN_OUTPUT_DIR="${SUB_OUT_DIR}",STARTING_DATE="${STA_DATE}",END_DATE="${END_DATE}",MAIN_INITIAL_STATE_FOLDER="${INITIAL_FOLD}",DATE_FOR_INITIAL_STATES="${INITIAL_DATE}",NUM_OF_YEARS_FOR_SPINUP="0",MAIN_INPUT_DIRECTORY="${MAIN_INPUT_DIRECTORY}" job_script_sbatch_pcrglobwb_template.sh | sed 's/Submitted batch job //')

set +x

echo $SPINUP
echo $FIRST

sleep 3
squeue
squeue -u sutan101

