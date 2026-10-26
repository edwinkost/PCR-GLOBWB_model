#!/bin/bash

GCMNAME=$1

JOBNAME="pgb_6min"
JOBNAME=${GCMNAME}

set -x

MAIN_OUTPUT_DIR="/scratch-shared/edwin/watersis_v202609_for_gcm_spinups_runs_on_20261026/"${JOBNAME}"/"

PCRGLOBWB_MODEL_SCRIPT_FOLDER="/home/edwin/gits/github/edwinkost/PCR-GLOBWB_model_for_watersis_gcm_spinups/model/"

SPINUP_RUN_INI="/home/edwin/gits/github/edwinkost/PCR-GLOBWB_model_for_watersis_gcm_spinups/config/watersis/global_run_parallel_202609XX/setup_6min_global_watersis_develop_since_oct_2026.ini"
WARMED_RUN_INI="/home/edwin/gits/github/edwinkost/PCR-GLOBWB_model_for_watersis_gcm_spinups/config/watersis/global_run_parallel_202609XX/setup_6min_global_watersis_develop_since_oct_2026.ini" 

#~ MAIN_INPUT_DIRECTORY="/scratch/depfg/sutan101_new/pcrglobwb_input_watersis/develop/global_6min/"   
MAIN_INPUT_DIRECTORY="/scratch-shared/edwin/data/pcrglobwb_input_watersis/release/global_6min_v20260922/"   

#~ PRECIPITATION_FORCING_FILE="/scratch/depfg/sutan101/data/watersis_forcing/global/v20260813/global_pre_0p1_v20260813.nc"
#~ TEMPERATURE_FORCING_FILE="/scratch/depfg/sutan101/data/watersis_forcing/global/v20260813/global_tas_day_0p1_v20260813.nc"  
#~ REF_POT_ET_FORCING_FILE="/scratch/depfg/sutan101/data/watersis_forcing/global/v20260813/global_pet_hargreaves_samani_0p1_v20260813.nc"   

PRECIPITATION_FORCING_FILE="/scratch-shared/edwin/data/watersis_historical_gcms/global/v20261026_only1951/"${GCMNAME}"/pr_"${GCMNAME}"_1951_daily.nc"
TEMPERATURE_FORCING_FILE="/scratch-shared/edwin/data/watersis_historical_gcms/global/v20261026_only1951/"${GCMNAME}"/tas_"${GCMNAME}"_1951_daily.nc"  
REF_POT_ET_FORCING_FILE="/scratch-shared/edwin/data/watersis_historical_gcms/global/v20261026_only1951/"${GCMNAME}"/pet_"${GCMNAME}"_1951_daily.nc"   

#~ edwin@tcn530.local.snellius.surf.nl:/scratch-shared/edwin/data/watersis_historical_gcms/global/v20261026_only1951$ ls -lah ACCESS_CM2/
#~ total 21G
#~ drwxr-xr-x+  2 edwin edwin 4.0K Oct 26 13:29 .
#~ drwxr-xr-x+ 16 edwin edwin 4.0K Oct 26 13:14 ..
#~ -rw-r--r--.  1 edwin edwin 6.9G Oct 26 13:20 pet_ACCESS_CM2_1951_daily.nc
#~ -rw-r--r--.  1 edwin edwin 6.9G Oct 26 13:25 pr_ACCESS_CM2_1951_daily.nc
#~ -rw-r--r--.  1 edwin edwin 6.9G Oct 26 13:29 tas_ACCESS_CM2_1951_daily.nc


# spin up run
NUM_OF_YEARS_FOR_SPINUP="25"
SUB_JOBNAME=${JOBNAME}_spinup_with_1951
SUB_INIFILE=${SPINUP_RUN_INI}
STA_DATE="1951-01-01"
END_DATE="1951-12-31"
#~ INITIAL_FOLD="dummy_initial_conditions/"
INITIAL_FOLD="/scratch-shared/edwin/data/watersis_initial_conditions_for_spinup_historical_gcms/v20261026/"
INITIAL_DATE="2019-12-31"
SUB_OUT_DIR=${MAIN_OUTPUT_DIR}/_spinup/with_1951/

#~ # - for testing
#~ NUM_OF_YEARS_FOR_SPINUP="0"
#~ STA_DATE="1970-12-29"

#~ # - for testing with 5 year spinup
#~ NUM_OF_YEARS_FOR_SPINUP="5"
#~ STA_DATE="1970-01-01"

# - start the run
SPINUP=$(sbatch -J "${SUB_JOBNAME}" --export INI_FILE="${SUB_INIFILE}",MAIN_OUTPUT_DIR="${SUB_OUT_DIR}",STARTING_DATE="${STA_DATE}",END_DATE="${END_DATE}",MAIN_INITIAL_STATE_FOLDER="${INITIAL_FOLD}",DATE_FOR_INITIAL_STATES="${INITIAL_DATE}",NUM_OF_YEARS_FOR_SPINUP="${NUM_OF_YEARS_FOR_SPINUP}",MAIN_INPUT_DIRECTORY="${MAIN_INPUT_DIRECTORY}",PRECIPITATION_FORCING_FILE=${PRECIPITATION_FORCING_FILE},TEMPERATURE_FORCING_FILE=${TEMPERATURE_FORCING_FILE},REF_POT_ET_FORCING_FILE=${REF_POT_ET_FORCING_FILE},PCRGLOBWB_MODEL_SCRIPT_FOLDER=${PCRGLOBWB_MODEL_SCRIPT_FOLDER} job_script_sbatch_pcrglobwb_template.sh | sed 's/Submitted batch job //')


# run for the period 1951 only
NUM_OF_YEARS_FOR_SPINUP="0"
SUB_JOBNAME=${JOBNAME}_1951
SUB_INIFILE=${WARMED_RUN_INI}
STA_DATE="1951-01-01"
END_DATE="1951-12-31"
INITIAL_FOLD=${SUB_OUT_DIR}/global/states/
INITIAL_DATE="1951-12-31"
SUB_OUT_DIR=${MAIN_OUTPUT_DIR}/begin_from_1951/
# - start the run
FIRST=$(sbatch --dependency=afterany:${SPINUP} -J "${SUB_JOBNAME}" --export INI_FILE="${SUB_INIFILE}",MAIN_OUTPUT_DIR="${SUB_OUT_DIR}",STARTING_DATE="${STA_DATE}",END_DATE="${END_DATE}",MAIN_INITIAL_STATE_FOLDER="${INITIAL_FOLD}",DATE_FOR_INITIAL_STATES="${INITIAL_DATE}",NUM_OF_YEARS_FOR_SPINUP="${NUM_OF_YEARS_FOR_SPINUP}",MAIN_INPUT_DIRECTORY="${MAIN_INPUT_DIRECTORY}",PRECIPITATION_FORCING_FILE=${PRECIPITATION_FORCING_FILE},TEMPERATURE_FORCING_FILE=${TEMPERATURE_FORCING_FILE},REF_POT_ET_FORCING_FILE=${REF_POT_ET_FORCING_FILE},PCRGLOBWB_MODEL_SCRIPT_FOLDER=${PCRGLOBWB_MODEL_SCRIPT_FOLDER} job_script_sbatch_pcrglobwb_template.sh | sed 's/Submitted batch job //')
set +x


echo $SPINUP
echo $FIRST

sleep 3
squeue
squeue -u edwin




