#!/bin/bash

set -x

PGB_OUTPUT_DIR_UNMERGED="/scratch-shared/edwin/pcrglobwb_wmo_run/v20250417/"
PGB_OUTPUT_DIR_MERGED="/scratch-shared/edwindan/pcrglobwb_wmo_run_merged_test/v20250417/global/netcdf/"

python merge_netcdf_5_arcmin_wmo_run.py ${MAIN_OUTPUT_DIR} ${MAIN_OUTPUT_DIR}/global/netcdf outDailyTotNC 1981-01-01 1981-12-31 discharge NETCDF4 False 1 Global_M0000053 all_lats

set +x
