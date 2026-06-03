

INI_FILE="../config/watersis/global_run_parallel_may_2026/setup_6min_global_watersis_develop.ini"

MAIN_OUTPUT_DIRECTORY="/scratch/depfg/sutan101/watersis_runs_may_2026/test_global_6min_with_watersis_forcing_with_parallel/test_single_clone/"     
MAIN_INPUT_DIRECTORY="/scratch/depfg/sutan101_new/pcrglobwb_input_watersis/develop/global_6min/"   
STARTING_DATE="1970-01-01"             
END_DATE="2019-12-31"                  
NUM_OF_YEARS_FOR_SPINUP=1   
PRECIPITATION_FORCING_FILE="/scratch/depfg/sutan101/data/watersis_forcing/global/v20260514/global_pre_0p1_v20260514.nc"
TEMPERATURE_FORCING_FILE="/scratch/depfg/sutan101/data/watersis_forcing/global/v20260514/global_tas_day_0p1_v20260514.nc"  
REF_POT_ET_FORCING_FILE="/scratch/depfg/sutan101/data/watersis_forcing/global/v20260514/global_pet_hargreaves_samani_0p1_v20260514.nc"   
MAIN_INITIAL_STATE_FOLDER="dummy_initial_conditions/" 
DATE_FOR_INITIAL_STATES="1999-12-31"   


set -x

# go to the script folder
cd /eejit/home/sutan101/github/edwinkost/PCR-GLOBWB_model/model/

CLONE_CODE="2"

python3 deterministic_runner_ulysses.py ${INI_FILE} debug_parallel ${CLONE_CODE} \
#~ python3 deterministic_runner_ulysses.py ${INI_FILE} debug \
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
-end_of_arguments

set +x
