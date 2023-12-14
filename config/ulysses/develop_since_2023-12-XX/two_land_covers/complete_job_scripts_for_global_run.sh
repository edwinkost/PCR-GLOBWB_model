#!/bin/bash

JOBNAME="two_lcs"
LOGRECF="SQUARE_ROOT"

#~ JOBNAME=$1
#~ LOGRECF=$2

BFEXPON="1.50"
LOG_10_MULTIPLIER_FOR_KSAT="0.0"

SPINUP_RUN_INI="setup_6arcmin_ulysses_2LCs_version_2023-12-14.ini"
WARMED_RUN_INI="setup_6arcmin_ulysses_2LCs_version_2023-12-14.ini" 

MAIN_OUTPUT_DIR="/scratch/depfg/sutan1010/pcrglobwb_ulysses_2023-12-XX/"${JOBNAME}

set -x

# spin up run
NUM_OF_YEARS_FOR_SPINUP="25"
SUB_JOBNAME=${JOBNAME}_spinup_with_1981
SUB_INIFILE=${SPINUP_RUN_INI}
STA_DATE="1981-01-01"
END_DATE="1981-12-31"
INITIAL_FOLD="/scratch/depfg/sutan101/data/pcrglobwb_input_ulysses/initial_conditions/from_runs_created_in_january_2021/"
INITIAL_DATE="1981-12-31"
SUB_OUT_DIR=${MAIN_OUTPUT_DIR}/_spinup/with_1981/

#~ # - for testing
#~ NUM_OF_YEARS_FOR_SPINUP="0"
#~ STA_DATE="1981-12-29"

#~ # - for testing with 5 year spinup
#~ NUM_OF_YEARS_FOR_SPINUP="5"
#~ STA_DATE="1981-01-01"

# - start the run
SPINUP=$(sbatch -J "${SUB_JOBNAME}" --export INI_FILE="${SUB_INIFILE}",MAIN_OUTPUT_DIR="${SUB_OUT_DIR}",STARTING_DATE="${STA_DATE}",END_DATE="${END_DATE}",MAIN_INITIAL_STATE_FOLDER="${INITIAL_FOLD}",DATE_FOR_INITIAL_STATES="${INITIAL_DATE}",BASEFLOW_EXPONENT="${BFEXPON}",LOG_10_MULTIPLIER_FOR_KSAT="${LOG_10_MULTIPLIER_FOR_KSAT}",LOG_10_MULTIPLIER_FOR_RECESSION_COEFF="${LOGRECF}",NUM_OF_YEARS_FOR_SPINUP="${NUM_OF_YEARS_FOR_SPINUP}" job_script_sbatch_pcrglobwb_template.sh | sed 's/Submitted batch job //')


# run for the period 1981-2022
SUB_JOBNAME=${JOBNAME}_1981-2022
SUB_INIFILE=${WARMED_RUN_INI}
STA_DATE="1981-01-01"
END_DATE="2022-12-31"
INITIAL_FOLD=${SUB_OUT_DIR}/global/states/
INITIAL_DATE="1981-12-31"
SUB_OUT_DIR=${MAIN_OUTPUT_DIR}/begin_from_1981/
# - start the run
FIRST=$(sbatch --dependency=afterany:${SPINUP} -J "${SUB_JOBNAME}" --export INI_FILE="${SUB_INIFILE}",MAIN_OUTPUT_DIR="${SUB_OUT_DIR}",STARTING_DATE="${STA_DATE}",END_DATE="${END_DATE}",MAIN_INITIAL_STATE_FOLDER="${INITIAL_FOLD}",DATE_FOR_INITIAL_STATES="${INITIAL_DATE}",BASEFLOW_EXPONENT="${BFEXPON}",LOG_10_MULTIPLIER_FOR_KSAT="${LOG_10_MULTIPLIER_FOR_KSAT}",LOG_10_MULTIPLIER_FOR_RECESSION_COEFF="${LOGRECF}",NUM_OF_YEARS_FOR_SPINUP="0" job_script_sbatch_pcrglobwb_template.sh | sed 's/Submitted batch job //')



set +x

echo $SPINUP
echo $FIRST

sleep 3
squeue
squeue -u sutan101

