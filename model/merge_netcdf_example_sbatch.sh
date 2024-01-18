#!/bin/bash 
#SBATCH -N 1

# on snellius
#SBATCH -n 32
#SBATCH -p genoa
#SBATCH -t 119:59:00
#~ #SBATCH -t 59:00

#SBATCH -J dynqual_merging

# mail alert at start, end and abortion of execution
#SBATCH --mail-type=ALL

# send mail to this address
#SBATCH --mail-user=edwinkost@gmail.com

#SBATCH --export START_YEAR=1981,END_YEAR=1990

set -x

# load modules on snellius
. /home/edwin/load_all_default.sh


START_YEAR=${START_YEAR}
END_YEAR=${END_YEAR}

INPUT_DIR="/gpfs/work4/0/einf6448/users/dgraham/DynQual_DO_GFDL_SSP3RCP7/${START_YEAR}-${END_YEAR}/"

OUTPUT_DIR="/scratch-shared/edwinoxy/dynqual_dgraham/ssp370/${START_YEAR}-${END_YEAR}/"

mkdir -p ${OUTPUT_DIR}

for i in {${START_YEAR}..${END_YEAR}}

do

YEAR=${i}

python merge_netcdf.py ${INPUT_DIR} ${OUTPUT_DIR} outDailyTotNC ${YEAR}-01-01 ${YEAR}-12-31 discharge,waterTemp NETCDF4 True 2 Global53ExceptM28M29 &

#~ edwinoxy@tcn531.local.snellius.surf.nl:/gpfs/work4/0/einf6448/users/dgraham/DynQual_DO_GFDL_SSP3RCP7/2091-2100$ ls -lah M53/netcdf/
#~ total 5.8G
#~ drwxr-s--- 2 dgraham prjs0584 4.0K Dec 15 10:50 .
#~ drwxr-s--- 9 dgraham prjs0584 4.0K Dec 15 10:50 ..
#~ -rw-r----- 1 dgraham prjs0584 971M Dec 17 03:50 BOD_concentration_dailyTot_output.nc
#~ -rw-r----- 1 dgraham prjs0584 971M Dec 17 03:50 discharge_dailyTot_output.nc
#~ -rw-r----- 1 dgraham prjs0584  32M Dec 17 03:50 discharge_monthAvg_output.nc
#~ -rw-r----- 1 dgraham prjs0584 971M Dec 17 03:50 k1_dailyTot_output.nc
#~ -rw-r----- 1 dgraham prjs0584 971M Dec 17 03:50 oxygen_dailyTot_output.nc
#~ -rw-r----- 1 dgraham prjs0584 971M Dec 17 03:50 saturation_dailyTot_output.nc
#~ -rw-r----- 1 dgraham prjs0584 971M Dec 17 03:50 waterTemp_dailyTot_output.nc
#~ -rw-r----- 1 dgraham prjs0584  32M Dec 17 03:50 waterTemp_monthAvg_output.nc

done

# wait until all above processes done
wait

set +x
