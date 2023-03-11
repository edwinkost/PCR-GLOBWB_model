#!/bin/bash 


set -x


# folder containing .ini file
# - with bash
INI_FOLDER=$(pwd)


# configuration (.ini) file
INI_FILE=${INI_FOLDER}/"setup_05min_thailand_develop.ini"


# starting and end dates
# - historical
STARTING_DATE="1978-01-01"
END_DATE="2019-12-31"
# - PS: for continuing runs (including the transition from the historical to SSP runs), plese use the output files from previous model runs.


# location/folder, where you will store output files of your 
MAIN_OUTPUT_DIR="/scratch/depfg/sutan101/thailand_05min/version_20230311_accutraveltime/"


# meteorological forcing files

# - historical reference - gswp3-w5e5
RELATIVE_HUMIDITY_FORCING_FILE="/scratch/depfg/sutan101/data/isimip_forcing/isimip3a_version_2021-09-XX/copied_on_2021-09-XX/GSWP3-W5E5/merged/w5e5_1979-2019_with_climatology_on_1978/gswp3-w5e5_obsclim_hurs_global_daily_1979-2019_version_2021-09-XX_with_climatology_on_1978.nc"
PRECIPITATION_FORCING_FILE="/scratch/depfg/sutan101/data/isimip_forcing/isimip3a_version_2021-09-XX/copied_on_2021-09-XX/GSWP3-W5E5/merged/w5e5_1979-2019_with_climatology_on_1978/gswp3-w5e5_obsclim_pr_global_daily_1979-2019_version_2021-09-XX_with_climatology_on_1978.nc"
PRESSURE_FORCING_FILE="/scratch/depfg/sutan101/data/isimip_forcing/isimip3a_version_2021-09-XX/copied_on_2021-09-XX/GSWP3-W5E5/merged/w5e5_1979-2019_with_climatology_on_1978/gswp3-w5e5_obsclim_ps_global_daily_1979-2019_version_2021-09-XX_with_climatology_on_1978.nc"
SHORTWAVE_RADIATION_FORCING_FILE="/scratch/depfg/sutan101/data/isimip_forcing/isimip3a_version_2021-09-XX/copied_on_2021-09-XX/GSWP3-W5E5/merged/w5e5_1979-2019_with_climatology_on_1978/gswp3-w5e5_obsclim_rsds_global_daily_1979-2019_version_2021-09-XX_with_climatology_on_1978.nc"
WIND_FORCING_FILE="/scratch/depfg/sutan101/data/isimip_forcing/isimip3a_version_2021-09-XX/copied_on_2021-09-XX/GSWP3-W5E5/merged/w5e5_1979-2019_with_climatology_on_1978/gswp3-w5e5_obsclim_sfcwind_global_daily_1979-2019_version_2021-09-XX_with_climatology_on_1978.nc"
TEMPERATURE_FORCING_FILE="/scratch/depfg/sutan101/data/isimip_forcing/isimip3a_version_2021-09-XX/copied_on_2021-09-XX/GSWP3-W5E5/merged/w5e5_1979-2019_with_climatology_on_1978/gswp3-w5e5_obsclim_tas_global_daily_1979-2019_version_2021-09-XX_with_climatology_on_1978.nc"


# initial conditions
MAIN_INITIAL_STATE_FOLDER="/depfg/sutan101/pcrglobwb_wri_aqueduct_2021/pcrglobwb_aqueduct_2021_states_files_selected/version_2021-09-16/gswp3-w5e5/historical-reference/begin_from_1960/global/states/"
DATE_FOR_INITIAL_STATES="1978-12-31"


# number of spinup years
NUMBER_OF_SPINUP_YEARS="25"
#~ # - PS: For continuing runs, please set it to zero
#~ NUMBER_OF_SPINUP_YEARS="0"


# location of your pcrglobwb model scripts
PCRGLOBWB_MODEL_SCRIPT_FOLDER=~/github/edwinkost/PCR-GLOBWB_model/model/


#~ # load the conda enviroment on azure
#~ source activate pcrglobwb_python3

#~ # unset pcraster working threads (due to a limited number of cores on the Azure VM)
#~ unset PCRASTER_NR_WORKER_THREADS


# test pcraster
pcrcalc


# go to the folder that contain PCR-GLOBWB scripts
cd ${PCRGLOBWB_MODEL_SCRIPT_FOLDER}
pwd


CLONE_CODE="00"
python deterministic_runner_with_arguments.py ${INI_FILE} debug ${CLONE_CODE} -mod ${MAIN_OUTPUT_DIR} -sd ${STARTING_DATE} -ed ${END_DATE} -pff ${PRECIPITATION_FORCING_FILE} -tff ${TEMPERATURE_FORCING_FILE} -presff ${PRESSURE_FORCING_FILE} -windff ${WIND_FORCING_FILE} -swradff ${SHORTWAVE_RADIATION_FORCING_FILE} -relhumff ${RELATIVE_HUMIDITY_FORCING_FILE} -misd ${MAIN_INITIAL_STATE_FOLDER} -dfis ${DATE_FOR_INITIAL_STATES} -num_of_sp_years ${NUMBER_OF_SPINUP_YEARS}



echo "end of model runs (please check your results)"

