#!/bin/bash 
#SBATCH -N 1

# on snellius
#SBATCH -n 24
#SBATCH -p genoa
#SBATCH -t 119:59:00
#~ #SBATCH -t 59:00

#SBATCH -J archiv

# mail alert at start, end and abortion of execution
#SBATCH --mail-type=ALL

# send mail to this address
#SBATCH --mail-user=edwinkost@gmail.com

#SBATCH --export FORCING_NAME="ERA5"

MAIN_FOLDER="/projects/0/prjs1222/edwingwt/pcrglobwb_ulysses_2023-12-XX_rerun_on_202609_to_archive/"
cd ${MAIN_FOLDER}

FORCING_NAME=${FORCING_NAME}

OUTPUT_FOLDER=${FORCING_NAME}_pgb_uly_rerun_two_lcs_sqrt
mkdir ${OUTPUT_FOLDER}
cd ${OUTPUT_FOLDER}

ln -s /projects/0/prjs1222/edwingwt/pcrglobwb_ulysses_2023-12-XX_rerun_on_202609/${FORCING_NAME}/${FORCING_NAME}_pgb_uly_rerun_two_lcs_sqrt/merged_daily begin_from_1981_global_netcdf_daily

7za a _spinup.7z                /scratch-shared/edwin/pcrglobwb_ulysses_2023-12-XX_rerun_on_202609/${FORCING_NAME}/${FORCING_NAME}_pgb_uly_rerun_two_lcs_sqrt/_spinup/ 
7za a begin_from_1981_global.7z /scratch-shared/edwin/pcrglobwb_ulysses_2023-12-XX_rerun_on_202609/${FORCING_NAME}/${FORCING_NAME}_pgb_uly_rerun_two_lcs_sqrt/begin_from_1981/global/
7za a begin_from_1981.7z        /scratch-shared/edwin/pcrglobwb_ulysses_2023-12-XX_rerun_on_202609/${FORCING_NAME}/${FORCING_NAME}_pgb_uly_rerun_two_lcs_sqrt/begin_from_1981/
7za a analysis.7z               /scratch-shared/edwin/pcrglobwb_ulysses_2023-12-XX_rerun_on_202609/${FORCING_NAME}/${FORCING_NAME}_pgb_uly_rerun_two_lcs_sqrt/analysis/

7za l _spinup.7z > 7za_l_spinup.7z.txt
7za l begin_from_1981_global.7z > 7za_l_begin_from_1981_global.7z.txt
7za l begin_from_1981.7z > 7za_l_begin_from_1981.7z.txt
7za l analysis.7z > 7za_l_analysis.7z.txt

tree > tree.txt

exit

