#!/bin/bash 
#SBATCH -N 1

# on snellius, using the entire node (so that we can use the entire RAM: 336GB)
#SBATCH -n 192
#SBATCH -p genoa
#SBATCH -t 119:59:00
#~ #SBATCH -t 59:00

#SBATCH -J merging_daily_nc_files

# mail alert at start, end and abortion of execution
#SBATCH --mail-type=ALL

# send mail to this address
#SBATCH --mail-user=edwinkost@gmail.com

#SBATCH --export FORCING_NAME="ERA5",FIRST_YEAR=1981,LAST_YEAR=2019


set -x

# load the software
. /home/edwin/load_all_default.sh

MERGING_PYTHON_SCRIPT="/home/edwingwt/gits/github/edwinkost/PCR-GLOBWB_model/model/merge_netcdf_6_arcmin_ulysses.py"

FORCING_NAME="emearth"

FIRST_YEAR=1981
LAST_YEAR=2019

for YEAR in $(seq "$FIRST_YEAR" "$LAST_YEAR"); do

    #~ python merge_netcdf_6_arcmin_ulysses.py "$YEAR" &

    #~ python merge_netcdf_6_arcmin_ulysses.py /scratch-shared/edwin/pcrglobwb_ulysses_2023-12-XX_rerun_on_202609/emearth/emearth_pgb_uly_rerun_two_lcs_sqrt/begin_from_1981 /scratch-shared/edwin/pcrglobwb_ulysses_2023-12-XX_rerun_on_202609/emearth/emearth_pgb_uly_rerun_two_lcs_sqrt/merged_daily_test/ outDailyTotNC 1981-01-01 1981-12-31 ulyssesP,ulyssesET,ulyssesSWE,ulyssesQsm,ulyssesSM,ulyssesQrRunoff,ulyssesDischarge,ulyssessRefPET,ulyssessCropPET,ulyssesSnowFraction,ulyssesSMUpp,temperature,totalWaterStorageThickness NETCDF4 True 2 Global FUFZ &

    python ${MERGING_PYTHON_SCRIPT} /scratch-shared/edwin/pcrglobwb_ulysses_2023-12-XX_rerun_on_202609/${FORCING_NAME}/${FORCING_NAME}_pgb_uly_rerun_two_lcs_sqrt/begin_from_1981/ /projects/0/prjs1222/edwingwt/pcrglobwb_ulysses_2023-12-XX_rerun_on_202609/${FORCING_NAME}/${FORCING_NAME}_pgb_uly_rerun_two_lcs_sqrt/merged_daily/ outDailyTotNC ${YEAR}-01-01 ${YEAR}-12-31 ulyssesQrRunoff,ulyssesDischarge,ulyssesET NETCDF4 True 3 Global FUFZ & 

done

wait


for YEAR in $(seq "$FIRST_YEAR" "$LAST_YEAR"); do

    python ${MERGING_PYTHON_SCRIPT} /scratch-shared/edwin/pcrglobwb_ulysses_2023-12-XX_rerun_on_202609/${FORCING_NAME}/${FORCING_NAME}_pgb_uly_rerun_two_lcs_sqrt/begin_from_1981/ /projects/0/prjs1222/edwingwt/pcrglobwb_ulysses_2023-12-XX_rerun_on_202609/${FORCING_NAME}/${FORCING_NAME}_pgb_uly_rerun_two_lcs_sqrt/merged_daily/ outDailyTotNC ${YEAR}-01-01 ${YEAR}-12-31 ulyssesP,ulyssessRefPET,ulyssessCropPET,temperature,ulyssesSWE,ulyssesQsm,ulyssesSM,ulyssesSnowFraction,ulyssesSMUpp,totalWaterStorageThickness NETCDF4 True 4 Global FUFZ & 

done

wait

exit

set +x

