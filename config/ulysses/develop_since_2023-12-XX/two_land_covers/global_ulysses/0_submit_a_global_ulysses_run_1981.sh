#!/bin/bash

set -x

# submit the job/sbatch script - please modify the variables

MAIN_INPUT_DIRECTORY="/scratch-shared/edwin/pcrglobwb_input_ulysses_v202312XX/develop_edwin/"
PCRGLOBWB_MODEL_SCRIPT_FOLDER="/home/edwin/github/edwinkost/PCR-GLOBWB_model/model/"
INI_FILE="/home/edwin/github/edwinkost/PCR-GLOBWB_model/config/ulysses/develop_since_2023-12-XX/two_land_covers/global_ulysses/setup_6arcmin_ulysses_2LCs_version_2023-12-14_finalize_global.ini"
FORCING_FOLDER="/projects/0/dfguu2/users/edwin/data/era5land_ulysses/version_20231206/"

MAIN_OUTPUT_FOLDER="/scratch-shared/edwin/pcrglobwb_ulysses_2023-12-25_global_two_landcovers_final_test/"

YEAR="1981"
END_DATE_FOR_FEBRUARY="28"

# - month 01 (January)
MONTH="01"
# - initial conditions (note for the run for the month Jan 1981 (the first year), we use the initial conditions after the spin up)
MAIN_INITIAL_STATE_FOLDER="/scratch-shared/edwin/pcrglobwb_input_ulysses_v202312XX/develop_edwin/initial_conditions/after_spinups_with_1981/"
DATE_FOR_INITIAL_STATES="1981-12-31"
# - starting and end dates
STARTING_DATE=${YEAR}"-"${MONTH}"-01"
END_DATE="31"
END_DATE=${YEAR}"-"${MONTH}"-"${END_DATE}
# - output directory
MAIN_OUTPUT_DIRECTORY=${MAIN_OUTPUT_FOLDER}"/"${STARTING_DATE}"_to"_${END_DATE}"/"
# - forcing files
PRECIPITATION_FORCING_FILE=${FORCING_FOLDER}"/"${YEAR}"/"${MONTH}"/pre_"${MONTH}"_"${YEAR}".nc"
TEMPERATURE_FORCING_FILE=${FORCING_FOLDER}"/"${YEAR}"/"${MONTH}"/tavg_"${MONTH}"_"${YEAR}".nc"
REF_POT_ET_FORCING_FILE=${FORCING_FOLDER}"/"${YEAR}"/"${MONTH}"/pet_"${MONTH}"_"${YEAR}".nc"
# - job name
JOB_NAME=${YEAR}"-"${MONTH}"_pgb-uly"
# - submit the job
sbatch -J ${JOB_NAME} --export MAIN_INPUT_DIRECTORY=${MAIN_INPUT_DIRECTORY},PCRGLOBWB_MODEL_SCRIPT_FOLDER=${PCRGLOBWB_MODEL_SCRIPT_FOLDER},INI_FILE=${INI_FILE},MAIN_OUTPUT_DIRECTORY=${MAIN_OUTPUT_DIRECTORY},STARTING_DATE=${STARTING_DATE},END_DATE=${END_DATE},MAIN_INITIAL_STATE_FOLDER=${MAIN_INITIAL_STATE_FOLDER},DATE_FOR_INITIAL_STATES=${DATE_FOR_INITIAL_STATES},PRECIPITATION_FORCING_FILE=${PRECIPITATION_FORCING_FILE},TEMPERATURE_FORCING_FILE=${TEMPERATURE_FORCING_FILE},REF_POT_ET_FORCING_FILE=${REF_POT_ET_FORCING_FILE} job_script_sbatch_pcrglobwb_template_global_no_parallelization.sh


# - month 02 (February)
MONTH="02"
# - initial conditions (from the previous job)
MAIN_INITIAL_STATE_FOLDER=${MAIN_OUTPUT_DIRECTORY}"/states/"
DATE_FOR_INITIAL_STATES=${END_DATE}
# - starting and end dates
STARTING_DATE=${YEAR}"-"${MONTH}"-01"
END_DATE=${END_DATE_FOR_FEBRUARY}
END_DATE=${YEAR}"-"${MONTH}"-"${END_DATE}
# - output directory
MAIN_OUTPUT_DIRECTORY=${MAIN_OUTPUT_FOLDER}"/"${STARTING_DATE}"_to"_${END_DATE}"/"
# - forcing files
PRECIPITATION_FORCING_FILE=${FORCING_FOLDER}"/"${YEAR}"/"${MONTH}"/pre_"${MONTH}"_"${YEAR}".nc"
TEMPERATURE_FORCING_FILE=${FORCING_FOLDER}"/"${YEAR}"/"${MONTH}"/tavg_"${MONTH}"_"${YEAR}".nc"
REF_POT_ET_FORCING_FILE=${FORCING_FOLDER}"/"${YEAR}"/"${MONTH}"/pet_"${MONTH}"_"${YEAR}".nc"
# - previous job name
PREV_JOB_NAME=${JOB_NAME}
# - job name
JOB_NAME=${YEAR}"-"${MONTH}"_pgb-uly"
# - submit the job
sbatch --dependency=afterany:$(squeue --noheader --format %i --name ${PREV_JOB_NAME}) -J ${JOB_NAME} --export MAIN_INPUT_DIRECTORY=${MAIN_INPUT_DIRECTORY},PCRGLOBWB_MODEL_SCRIPT_FOLDER=${PCRGLOBWB_MODEL_SCRIPT_FOLDER},INI_FILE=${INI_FILE},MAIN_OUTPUT_DIRECTORY=${MAIN_OUTPUT_DIRECTORY},STARTING_DATE=${STARTING_DATE},END_DATE=${END_DATE},MAIN_INITIAL_STATE_FOLDER=${MAIN_INITIAL_STATE_FOLDER},DATE_FOR_INITIAL_STATES=${DATE_FOR_INITIAL_STATES},PRECIPITATION_FORCING_FILE=${PRECIPITATION_FORCING_FILE},TEMPERATURE_FORCING_FILE=${TEMPERATURE_FORCING_FILE},REF_POT_ET_FORCING_FILE=${REF_POT_ET_FORCING_FILE} job_script_sbatch_pcrglobwb_template_global_no_parallelization.sh


# - months 3 to 12
for I_MONTH in {3..12..1}

do
MONTH=${I_MONTH}
if [$MONTH -lt 10]
then
     MONTH="0"${I_MONTH}
fi

# - initial conditions (from the previous job)
MAIN_INITIAL_STATE_FOLDER=${MAIN_OUTPUT_DIRECTORY}"/states/"
DATE_FOR_INITIAL_STATES=${END_DATE}

# - starting and end dates
STARTING_DATE=${YEAR}"-"${MONTH}"-01"

if [$MONTH -eq 3]
then
END_DATE=31
fi
if [$MONTH -eq 4]
then
END_DATE=31
fi
if [$MONTH -eq 5]
then
END_DATE=31
fi
if [$MONTH -eq 6]
then
END_DATE=30
fi
if [$MONTH -eq 7]
then
END_DATE=31
fi
if [$MONTH -eq 8]
then
END_DATE=31
fi
if [$MONTH -eq 9]
then
END_DATE=30
fi
if [$MONTH -eq 10]
then
END_DATE=31
fi
if [$MONTH -eq 11]
then
END_DATE=30
fi
if [$MONTH -eq 12]
then
END_DATE=31
fi


END_DATE=${YEAR}"-"${MONTH}"-"${END_DATE}

# - output directory
MAIN_OUTPUT_DIRECTORY=${MAIN_OUTPUT_FOLDER}"/"${STARTING_DATE}"_to"_${END_DATE}"/"

# - forcing files
PRECIPITATION_FORCING_FILE=${FORCING_FOLDER}"/"${YEAR}"/"${MONTH}"/pre_"${MONTH}"_"${YEAR}".nc"
TEMPERATURE_FORCING_FILE=${FORCING_FOLDER}"/"${YEAR}"/"${MONTH}"/tavg_"${MONTH}"_"${YEAR}".nc"
REF_POT_ET_FORCING_FILE=${FORCING_FOLDER}"/"${YEAR}"/"${MONTH}"/pet_"${MONTH}"_"${YEAR}".nc"

# - previous job name
PREV_JOB_NAME=${JOB_NAME}

# - job name
JOB_NAME=${YEAR}"-"${MONTH}"_pgb-uly"

# - submit the job
sbatch --dependency=afterany:$(squeue --noheader --format %i --name ${PREV_JOB_NAME}) -J ${JOB_NAME} --export MAIN_INPUT_DIRECTORY=${MAIN_INPUT_DIRECTORY},PCRGLOBWB_MODEL_SCRIPT_FOLDER=${PCRGLOBWB_MODEL_SCRIPT_FOLDER},INI_FILE=${INI_FILE},MAIN_OUTPUT_DIRECTORY=${MAIN_OUTPUT_DIRECTORY},STARTING_DATE=${STARTING_DATE},END_DATE=${END_DATE},MAIN_INITIAL_STATE_FOLDER=${MAIN_INITIAL_STATE_FOLDER},DATE_FOR_INITIAL_STATES=${DATE_FOR_INITIAL_STATES},PRECIPITATION_FORCING_FILE=${PRECIPITATION_FORCING_FILE},TEMPERATURE_FORCING_FILE=${TEMPERATURE_FORCING_FILE},REF_POT_ET_FORCING_FILE=${REF_POT_ET_FORCING_FILE} job_script_sbatch_pcrglobwb_template_global_no_parallelization.sh


done

set +x

