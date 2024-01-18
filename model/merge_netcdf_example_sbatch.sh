#!/bin/bash

set -x

INPUT_DIR="/gpfs/work4/0/einf6448/users/dgraham/DynQual_DO_GFDL_SSP3RCP7/2091-2100"

OUTPUT_DIR="/scratch-shared/edwinoxy/test_merging/"

python merge_netcdf_files.py ${INPUT_DIR} ${OUTPUT_DIR} outDailyTotNC 1981-01-01 1981-12-31 discharge,waterTemp NETCDF4 True 1 Global53ExceptM28M29 defined -180 180 -90 90 0.083333333333333333333333

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

set +x
