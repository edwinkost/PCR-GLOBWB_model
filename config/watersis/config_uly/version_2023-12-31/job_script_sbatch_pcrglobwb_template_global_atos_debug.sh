#!/bin/bash

#SBATCH --qos=nf
#SBATCH --job-name=pcrglobwb_ulysses

#SBATCH --mem-per-cpu=1250MB
#SBATCH --ntasks=32
#SBATCH --cpus-per-task=1
#SBATCH --threads-per-core=2

#SBATCH --time=04:00:00

# budget account - provided by Robert Jan 2024
#SBATCH --account=c3s24101


#~ #SBATCH --output=/ec/fws4/sb/project/C3SHydroGL/edwin/tmp/pcrglobwb_slurm_output.out

#~ #SBATCH --export MAIN_INPUT_DIRECTORY="/scratch-shared/edwin/pcrglobwb_input_ulysses_v202312XX/develop_edwin/",PCRGLOBWB_MODEL_SCRIPT_FOLDER="/home/edwin/github/edwinkost/PCR-GLOBWB_model/model/",INI_FILE="/home/edwin/github/edwinkost/PCR-GLOBWB_model/config/ulysses/develop_since_2023-12-XX/two_land_covers/global_ulysses/setup_6arcmin_ulysses_2LCs_version_2023-12-14_finalize_global.ini",MAIN_OUTPUT_DIRECTORY="/scratch-shared/edwin/pcrglobwb_ulysses_2023-12-25_global_two_landcovers/2000-01-01_to_2000-01-31/",STARTING_DATE="2000-01-01",END_DATE="2000-01-31",MAIN_INITIAL_STATE_FOLDER="/scratch-shared/edwin/pcrglobwb_input_ulysses_v202312XX/develop_edwin/initial_conditions/",DATE_FOR_INITIAL_STATES="1999-12-31",PRECIPITATION_FORCING_FILE="/ec/fws4/sb/project/C3SHydroGL/c3s_hydro_reference_runs/era5land_adjust_forcing/2000/01/pre_01_2000.nc",TEMPERATURE_FORCING_FILE="/ec/fws4/sb/project/C3SHydroGL/c3s_hydro_reference_runs/era5land_adjust_forcing/2000/01/tavg_01_2000.nc",REF_POT_ET_FORCING_FILE="/ec/fws4/sb/project/C3SHydroGL/c3s_hydro_reference_runs/era5land_adjust_forcing/2000/01/pet_01_2000.nc"

# Please set the following variables (alternatively, you can also activate and use the abovementioned SBATCH --export lines/variables) 

# - pcrglobwb input folder (containing model parameters, etc)
MAIN_INPUT_DIRECTORY="/ec/fws4/sb/project/C3SHydroGL/edwin/pcrglobwb_input_ulysses_v202312XX/pcrglobwb_ulysses_input_files_v2023-12-31/"

# - the folder that contains the pcrglobwb python scripts
PCRGLOBWB_MODEL_SCRIPT_FOLDER="/home/cyes/gitlab/ulysses/ulysses_pgb_source/model/"

# - pcrglobwb configuration file
INI_FILE="/home/cyes/gitlab/ulysses/ulysses_pgb_source/config/ulysses/version_2023-12-31/setup_6arcmin_ulysses_2LCs_version_2023-12-31_finalize_global_clean.ini"

# - pcrglobwb output folder
MAIN_OUTPUT_DIRECTORY="/ec/fws4/sb/project/C3SHydroGL/edwin/pcrglobwb_ulysses_v2023-12-31_test_output/1981-01-01_to_1981-01-31/"

# - starting date and end date
#~ STARTING_DATE="1981-01-01"
#~ END_DATE="1981-01-31"
STARTING_DATE="1981-02-01"
END_DATE="1981-02-28"

# - initial conditions (note for the run for the month Jan 1981 (the first year), we use the initial conditions after the spin up)
MAIN_INITIAL_STATE_FOLDER="/ec/fws4/sb/project/C3SHydroGL/edwin/pcrglobwb_input_ulysses_v202312XX/pcrglobwb_ulysses_input_files_v2023-12-31/initial_conditions/after_spinups_with_1981/"
DATE_FOR_INITIAL_STATES="1981-12-31"


#~ PRECIPITATION_FORCING_FILE="/ec/fws4/sb/project/C3SHydroGL/c3s_hydro_reference_runs/era5land_adjust_forcing/1981/01/pre_01_1981.nc"
#~ TEMPERATURE_FORCING_FILE="/ec/fws4/sb/project/C3SHydroGL/c3s_hydro_reference_runs/era5land_adjust_forcing/1981/01/tavg_01_1981.nc"
#~ REF_POT_ET_FORCING_FILE="/ec/fws4/sb/project/C3SHydroGL/c3s_hydro_reference_runs/era5land_adjust_forcing/1981/01/pet_01_1981.nc"

PRECIPITATION_FORCING_FILE="/ec/res4/scratch/cyrs/temp_pgb/input/meteo/pre.nc"
TEMPERATURE_FORCING_FILE="/ec/res4/scratch/cyrs/temp_pgb/input/meteo/tavg.nc"
REF_POT_ET_FORCING_FILE="/ec/res4/scratch/cyrs/temp_pgb/input/meteo/pet.nc"

#~ (pcrglobwb_python3) cyes@ac6-100.bullx:/ec/res4/scratch/cyrs/temp_pgb/input/meteo$ ls -lah
#~ total 20K
#~ drwxr-xr-x 2 cyrs copext 4.0K Feb  1 15:26 .
#~ drwxr-xr-x 5 cyrs copext 4.0K Feb  1 15:26 ..
#~ lrwxrwxrwx 1 cyrs copext  115 Feb  1 15:26 pet.nc -> ../../../../../fws4/sb/project/C3SHydroGL/c3s_hydro_reference_runs/era5land_adjust_forcing_raw_files/pet_02_1981.nc
#~ lrwxrwxrwx 1 cyrs copext  128 Feb  1 15:26 pre.nc -> ../../../../../fws4/sb/project/C3SHydroGL/c3s_hydro_reference_runs/em_earth_forcing_pre_raw_files/precipitation_daily_02_1981.nc
#~ lrwxrwxrwx 1 cyrs copext  116 Feb  1 15:26 tavg.nc -> ../../../../../fws4/sb/project/C3SHydroGL/c3s_hydro_reference_runs/era5land_adjust_forcing_raw_files/tavg_02_1981.nc



set -e          # stop the shell on first error
set -u          # fail when using an undefined variable
set -x          # echo script lines as they are executed
set -o pipefail # fail if last(rightmost) command exits with a non-zero status


# load modules on atos
module load python3
module load pcraster
module load gdal

# use at least 8 workers
export PCRASTER_NR_WORKER_THREADS=32

export OMP_NUM_THREADS=32

# set the configuration file (.ini) that will be used
INI_FILE=${INI_FILE}

# set the output folder
MAIN_OUTPUT_DIRECTORY=${MAIN_OUTPUT_DIRECTORY}

# set the starting and end simulation dates
STARTING_DATE=${STARTING_DATE}
END_DATE=${END_DATE}

# set the initial conditions (folder and time stamp for the files)
MAIN_INITIAL_STATE_FOLDER=${MAIN_INITIAL_STATE_FOLDER}
DATE_FOR_INITIAL_STATES=${DATE_FOR_INITIAL_STATES}

# set the forcing files
PRECIPITATION_FORCING_FILE=${PRECIPITATION_FORCING_FILE}
TEMPERATURE_FORCING_FILE=${TEMPERATURE_FORCING_FILE}
REF_POT_ET_FORCING_FILE=${REF_POT_ET_FORCING_FILE}


# go to the folder where the pcrglobwb python scripts are stored
PCRGLOBWB_MODEL_SCRIPT_FOLDER=${PCRGLOBWB_MODEL_SCRIPT_FOLDER}
cd ${PCRGLOBWB_MODEL_SCRIPT_FOLDER}

# make the run
#~ python3 deterministic_runner_ulysses.py ${INI_FILE} no-debug \
python3 deterministic_runner_ulysses.py ${INI_FILE} debug \
-mod          ${MAIN_OUTPUT_DIRECTORY} \
-mid          ${MAIN_INPUT_DIRECTORY} \
-sd           ${STARTING_DATE} \
-ed           ${END_DATE} \
-pff          ${PRECIPITATION_FORCING_FILE} \
-tff          ${TEMPERATURE_FORCING_FILE} \
-rpetff       ${REF_POT_ET_FORCING_FILE} \
-misf         ${MAIN_INITIAL_STATE_FOLDER} \
-dfis         ${DATE_FOR_INITIAL_STATES} \

set +x

exit
