#!/bin/bash

set -x

# submit the job/sbatch script - please modify the following variables

#~ # - 2000 January
#~ MAIN_INPUT_DIRECTORY="/scratch-shared/edwin/pcrglobwb_input_ulysses_v202312XX/develop_edwin/"
#~ PCRGLOBWB_MODEL_SCRIPT_FOLDER="/home/edwin/github/edwinkost/PCR-GLOBWB_model/model/"
#~ INI_FILE="/home/edwin/github/edwinkost/PCR-GLOBWB_model/config/ulysses/develop_since_2023-12-XX/two_land_covers/global_ulysses/setup_6arcmin_ulysses_2LCs_version_2023-12-14_finalize_global.ini"
#~ MAIN_OUTPUT_DIRECTORY="/scratch-shared/edwin/pcrglobwb_ulysses_2023-12-25_global_two_landcovers/2000-01-01_to_2000-01-31/"
#~ STARTING_DATE="2000-01-01"
#~ END_DATE="2000-01-31"
#~ MAIN_INITIAL_STATE_FOLDER="/scratch-shared/edwin/pcrglobwb_input_ulysses_v202312XX/develop_edwin/initial_conditions/"
#~ DATE_FOR_INITIAL_STATES="1999-12-31"
#~ PRECIPITATION_FORCING_FILE="/projects/0/dfguu2/users/edwin/data/era5land_ulysses/version_20231206/2000/01/pre_01_2000.nc"
#~ TEMPERATURE_FORCING_FILE="/projects/0/dfguu2/users/edwin/data/era5land_ulysses/version_20231206/2000/01/tavg_01_2000.nc"
#~ REF_POT_ET_FORCING_FILE="/projects/0/dfguu2/users/edwin/data/era5land_ulysses/version_20231206/2000/01/pet_01_2000.nc
#~ sbatch --export 
#~ MAIN_INPUT_DIRECTORY=${MAIN_INPUT_DIRECTORY},PCRGLOBWB_MODEL_SCRIPT_FOLDER=${PCRGLOBWB_MODEL_SCRIPT_FOLDER},INI_FILE=${INI_FILE},MAIN_OUTPUT_DIRECTORY=${MAIN_OUTPUT_DIRECTORY},STARTING_DATE=${STARTING_DATE},END_DATE=${END_DATE},MAIN_INITIAL_STATE_FOLDER=${MAIN_INITIAL_STATE_FOLDER},DATE_FOR_INITIAL_STATES=${DATE_FOR_INITIAL_STATES},PRECIPITATION_FORCING_FILE=${PRECIPITATION_FORCING_FILE},TEMPERATURE_FORCING_FILE=${TEMPERATURE_FORCING_FILE},REF_POT_ET_FORCING_FILE=${REF_POT_ET_FORCING_FILE} job_script_sbatch_pcrglobwb_template_global_no_parallelization.sh

# - 1981 January
MAIN_INPUT_DIRECTORY="/scratch-shared/edwin/pcrglobwb_input_ulysses_v202312XX/develop_edwin/"
PCRGLOBWB_MODEL_SCRIPT_FOLDER="/home/edwin/github/edwinkost/PCR-GLOBWB_model/model/"
INI_FILE="/home/edwin/github/edwinkost/PCR-GLOBWB_model/config/ulysses/develop_since_2023-12-XX/two_land_covers/global_ulysses/setup_6arcmin_ulysses_2LCs_version_2023-12-14_finalize_global.ini"
MAIN_OUTPUT_DIRECTORY="/scratch-shared/edwin/pcrglobwb_ulysses_2023-12-25_global_two_landcovers/1981-01-01_to_1981-01-31/"
STARTING_DATE="1981-01-01"
END_DATE="1981-01-31"
# - initial conditions (note for the run for the month Jan 1981 (the first year), we use the initial conditions after the spin up)
MAIN_INITIAL_STATE_FOLDER="/scratch-shared/edwin/pcrglobwb_input_ulysses_v202312XX/develop_edwin/initial_conditions/after_spinups_with_1981/"
DATE_FOR_INITIAL_STATES="1981-12-31"
# - forcing file
PRECIPITATION_FORCING_FILE="/projects/0/dfguu2/users/edwin/data/era5land_ulysses/version_20231206/1981/01/pre_01_1981.nc"
TEMPERATURE_FORCING_FILE="/projects/0/dfguu2/users/edwin/data/era5land_ulysses/version_20231206/1981/01/tavg_01_1981.nc"
REF_POT_ET_FORCING_FILE="/projects/0/dfguu2/users/edwin/data/era5land_ulysses/version_20231206/1981/01/pet_01_1981nc
# - submit the job
sbatch --export 
MAIN_INPUT_DIRECTORY=${MAIN_INPUT_DIRECTORY},PCRGLOBWB_MODEL_SCRIPT_FOLDER=${PCRGLOBWB_MODEL_SCRIPT_FOLDER},INI_FILE=${INI_FILE},MAIN_OUTPUT_DIRECTORY=${MAIN_OUTPUT_DIRECTORY},STARTING_DATE=${STARTING_DATE},END_DATE=${END_DATE},MAIN_INITIAL_STATE_FOLDER=${MAIN_INITIAL_STATE_FOLDER},DATE_FOR_INITIAL_STATES=${DATE_FOR_INITIAL_STATES},PRECIPITATION_FORCING_FILE=${PRECIPITATION_FORCING_FILE},TEMPERATURE_FORCING_FILE=${TEMPERATURE_FORCING_FILE},REF_POT_ET_FORCING_FILE=${REF_POT_ET_FORCING_FILE} job_script_sbatch_pcrglobwb_template_global_no_parallelization.sh

set +x
