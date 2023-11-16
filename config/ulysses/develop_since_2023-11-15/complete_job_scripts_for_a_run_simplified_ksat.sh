#!/bin/bash

JOBNAME="ksat_0.50"
LOGKSAT="-0.30102999566"

JOBNAME=$1
LOGKSAT=$2

BFEXPON="1.50"


SPINUP_RUN_INI="setup_6arcmin_ulysses_develop_since_2023-11.ini"
WARMED_RUN_INI="setup_6arcmin_ulysses_develop_since_2023-11.ini" 

MAIN_OUTPUT_DIR="/scratch-shared/edwin/pcrglobwb_ulysses_test_ksat_november_2023/"${JOBNAME}

set -x

# spin up run
NUM_OF_YEARS_FOR_SPINUP="25"
SUB_JOBNAME=${JOBNAME}_spinup_with_1981
SUB_INIFILE=${SPINUP_RUN_INI}
STA_DATE="1981-01-01"
END_DATE="1981-12-31"
INITIAL_FOLD="/projects/0/dfguu/users/edwin/data/pcrglobwb_input_ulysses/initial_conditions/from_runs_created_in_january_2021/"
INITIAL_DATE="1981-12-31"
SUB_OUT_DIR=${MAIN_OUTPUT_DIR}/_spinup/with_1981/

# - for testing
NUM_OF_YEARS_FOR_SPINUP="25"
STA_DATE="1981-12-29"

# - start the run
SPINUP=$(sbatch -J "${SUB_JOBNAME}" --export INI_FILE="${SUB_INIFILE}",MAIN_OUTPUT_DIR="${SUB_OUT_DIR}",STARTING_DATE="${STA_DATE}",END_DATE="${END_DATE}",MAIN_INITIAL_STATE_FOLDER="${INITIAL_FOLD}",DATE_FOR_INITIAL_STATES="${INITIAL_DATE}",BASEFLOW_EXPONENT="${BFEXPON}",LOG_10_MULTIPLIER_FOR_KSAT="${LOGKSAT}",NUM_OF_YEARS_FOR_SPINUP="${NUM_OF_YEARS_FOR_SPINUP}" job_script_sbatch_pcrglobwb_template.sh | sed 's/Submitted batch job //')


# run for the period 1981-2019
SUB_JOBNAME=${JOBNAME}_1981-2019
SUB_INIFILE=${WARMED_RUN_INI}
STA_DATE="1981-01-01"
END_DATE="2019-12-31"
INITIAL_FOLD=${SUB_OUT_DIR}/global/states/
INITIAL_DATE="1981-12-31"
SUB_OUT_DIR=${MAIN_OUTPUT_DIR}/begin_from_1981/
# - start the run
FIRST=$(sbatch ---dependency=afterany:${SPINUP} -J "${SUB_JOBNAME}" --export INI_FILE="${SUB_INIFILE}",MAIN_OUTPUT_DIR="${SUB_OUT_DIR}",STARTING_DATE="${STA_DATE}",END_DATE="${END_DATE}",MAIN_INITIAL_STATE_FOLDER="${INITIAL_FOLD}",DATE_FOR_INITIAL_STATES="${INITIAL_DATE}",BASEFLOW_EXPONENT="${BFEXPON}",LOG_10_MULTIPLIER_FOR_KSAT="${LOGKSAT}",NUM_OF_YEARS_FOR_SPINUP="0" job_script_sbatch_pcrglobwb_template.sh | sed 's/Submitted batch job //')



set +x

echo $SPINUP
echo $FIRST

sleep 3
squeue

