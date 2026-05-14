#!/bin/bash
#SBATCH --output=/perm/cyrs/suites/ulysses_cyrs/ecflow_home/mswep_reference_runs_update_restart1981_1_1/update_restart_1981_01_01/m01/pgb/pgb_run/pgb_run.1
#SBATCH --qos=nf
#SBATCH --job-name=mswep_reference_runs_update_restart1981_1_1
#SBATCH --mem-per-cpu=1250MB
#SBATCH --time=04:00:00
#SBATCH --ntasks=32
#SBATCH --cpus-per-task=1
#SBATCH --threads-per-core=2
#SBATCH --account=c3s432l3
#-------------------------------
#-------------------------------
set -e          # stop the shell on first error
set -u          # fail when using an undefined variable
set -x          # echo script lines as they are executed
set -o pipefail # fail if last(rightmost) command exits with a non-zero status
# Defines the variables that are needed for any communication with ECF
export ECF_FILES=/perm/cyrs/suites/ulysses_cyrs/ecflow_home/mswep_reference_runs_update_restart1981_1_1/files     # The server port number
export ECF_INCLUDE=/perm/cyrs/suites/ulysses_cyrs/ecflow_home/mswep_reference_runs_update_restart1981_1_1/incld # The server port number
export ECF_PORT=3141       # The server port number
export ECF_HOST=ecflow-gen-cyrs-001       # The host name where the server is running
export ECF_NAME=/mswep_reference_runs_update_restart1981_1_1/update_restart_1981_01_01/m01/pgb/pgb_run/pgb_run       # The name of this current task
export ECF_PASS=uIgMsbTm       # A unique password
export ECF_TRYNO=1     # Current try number of the task
export ECF_RID=$$            # record the process id

# Define the path where to find ecflow_client
# make sure client and server use the *same* version.
# Important when there are multiple versions of ecFlow
export PATH=/usr/local/apps/ecflow/5.8.1/bin:$PATH
# Tell ecFlow we have started
ecflow_client --init=$$
# Define a error handler
ERROR() {
   set +e                      # Clear -e flag, so we don not fail,
   wait                        # wait for background process to stop
   ecflow_client --abort=trap  # Notify ecFlow that something went wrong
   trap 0                      # Remove the trap
   exit 0                      # End the script
}
# Trap any calls to exit and errors caught by the -e flag
trap ERROR 0
# Trap any signal that may cause the script to fail
trap '{ echo "Killed by a signal"; ERROR ; }' 1 2 3 4 5 6 7 8 10 12 13 
set -e          # stop the shell on first error
set -u          # fail when using an undefined variable
set -x          # echo script lines as they are executed
set -o pipefail # fail if last(rightmost) command exits with a non-zero status
# Defines the variables that are needed for any communication with ECF
export ECF_FILES=/perm/cyrs/suites/ulysses_cyrs/ecflow_home/mswep_reference_runs_update_restart1981_1_1/files     # The server port number
export ECF_INCLUDE=/perm/cyrs/suites/ulysses_cyrs/ecflow_home/mswep_reference_runs_update_restart1981_1_1/incld # The server port number
export ECF_PORT=3141       # The server port number
export ECF_HOST=ecflow-gen-cyrs-001       # The host name where the server is running
export ECF_NAME=/mswep_reference_runs_update_restart1981_1_1/update_restart_1981_01_01/m01/pgb/pgb_run/pgb_run       # The name of this current task
export ECF_PASS=uIgMsbTm       # A unique password
export ECF_TRYNO=1     # Current try number of the task
export ECF_RID=$$            # record the process id

# Define the path where to find ecflow_client
# make sure client and server use the *same* version.
# Important when there are multiple versions of ecFlow
export PATH=/usr/local/apps/ecflow/5.8.1/bin:$PATH
# Tell ecFlow we have started
ecflow_client --init=$$
# Define a error handler
ERROR() {
   set +e                      # Clear -e flag, so we don not fail,
   wait                        # wait for background process to stop
   ecflow_client --abort=trap  # Notify ecFlow that something went wrong
   trap 0                      # Remove the trap
   exit 0                      # End the script
}
# Trap any calls to exit and errors caught by the -e flag
trap ERROR 0
# Trap any signal that may cause the script to fail
trap '{ echo "Killed by a signal"; ERROR ; }' 1 2 3 4 5 6 7 8 10 12 13 

ecflow_client --label="info" "prepare ..."
set -x

# load modules
module load python3
module load pcraster
module load gdal

export PYTHONPATH=${PYTHONPATH}:/ec/fws4/sb/project/C3SHydroGL/suites/ulysses_cyrs/ecflow_work/mswep_reference_runs_update_restart1981_1_1/progs/PGB_PY/model

# use at least 8 workers
export PCRASTER_NR_WORKER_THREADS=32

#  -- create workdir -------------------------------
mkdir -p /ec/fws4/sb/project/C3SHydroGL/suites/ulysses_cyrs/ecflow_work/mswep_reference_runs_update_restart1981_1_1/update_restart_1981_01_01/m01/pgb

restartdir="/ec/fws4/sb/project/C3SHydroGL/c3s_hydro_reference_runs/era5land-mswep_restart_files/pgb/$(date -d "20171201"  +%Y%m)"
restartdate=$(date -d "20171201 -1 day" +%Y-%m-%d)

for nn in $(seq 1); do
    dd=$(date -d "20171201 ${nn} months -1 day"  +%Y%m%d)
    yy=${dd:0:4}
    mm=${dd:4:2}
    dend=${dd:6:2}
    ii=${dd:0:6}
    sdate=${yy}-${mm}-01
    edate=${yy}-${mm}-${dend}
    #  -- make workdir ---------------------------------
    mkdir -p /ec/fws4/sb/project/C3SHydroGL/suites/ulysses_cyrs/ecflow_work/mswep_reference_runs_update_restart1981_1_1/update_restart_1981_01_01/m01/pgb/${ii}
    cd /ec/fws4/sb/project/C3SHydroGL/suites/ulysses_cyrs/ecflow_work/mswep_reference_runs_update_restart1981_1_1/update_restart_1981_01_01/m01/pgb/${ii}

    #  -- write pgb conf file --------------------------
    cat > /ec/fws4/sb/project/C3SHydroGL/suites/ulysses_cyrs/ecflow_work/mswep_reference_runs_update_restart1981_1_1/update_restart_1981_01_01/m01/pgb/${ii}/pgb_config.ini << EOF
[globalOptions]
outputDir = MAIN_OUTPUT_DIR
inputDir = /ec/fws4/sb/project/C3SHydroGL/suites/ulysses_cyrs/ecflow_work/mswep_reference_runs_update_restart1981_1_1/data/pgb
cloneMap = land_mask_only.map
landmask = land_mask_only.map
institution = Department of Physical Geography, Utrecht University
title = PCR-GLOBWB output (not coupled to MODFLOW), development version for Ulysses
description = by Edwin H. Sutanudjaja (contact: e.h.sutanudjaja@uu.nl)
startTime = ${sdate}
endTime = ${edate}
maxSpinUpsInYears = 0
minConvForSoilSto = 0.0
minConvForGwatSto = 0.0
minConvForChanSto = 0.0
minConvForTotlSto = 0.0

[meteoOptions]
referenceETPotMethod = Input
precipitationNC = /ec/fws4/sb/project/C3SHydroGL/suites/ulysses_cyrs/ecflow_work/mswep_reference_runs_update_restart1981_1_1/update_restart_1981_01_01/m01/adjust_forcing/%04i/%02i/pre_%02i_%04i.nc
temperatureNC = /ec/fws4/sb/project/C3SHydroGL/suites/ulysses_cyrs/ecflow_work/mswep_reference_runs_update_restart1981_1_1/update_restart_1981_01_01/m01/adjust_forcing/%04i/%02i/tavg_%02i_%04i.nc
refETPotFileNC = /ec/fws4/sb/project/C3SHydroGL/suites/ulysses_cyrs/ecflow_work/mswep_reference_runs_update_restart1981_1_1/update_restart_1981_01_01/m01/adjust_forcing/%04i/%02i/pet_%02i_%04i.nc
precipitation_file_per_month = True
temperature_file_per_month = True
refETPotFileNC_file_per_month = True
precipitationVariableName = pre
temperatureVariableName = tavg
referenceEPotVariableName = pet
precipitationConstant = 0.0
precipitationFactor = 0.001
temperatureConstant = 0.0
temperatureFactor = 1.0
referenceEPotConstant = 0.0
referenceEPotFactor = 0.001
rounddownPrecipitation = False

[landSurfaceOptions]
debugWaterBalance = True
numberOfUpperSoilLayers = 2
topographyNC = pcrglobwb_topography_parameters_06min_22_july_2020.nc
soilPropertiesNC = soilgrids_properties_ulysses_6arcmin_filled.nc
noParameterExtrapolation = True
landCoverTypes = forest,grassland,crop,urban
noLandCoverFractionCorrection = False

[forestOptions]
name = forest
debugWaterBalance = True
snowModuleType = Simple
freezingT = 0.0
degreeDayFactor = 0.0055
snowWaterHoldingCap = 0.1
refreezingCoeff = 0.05
minTopWaterLayer = 0.0
minCropKC = 0.2
cropCoefficientNC = tall_natural_cropcoefficient_06min.nc
interceptCapNC = tall_natural_interceptioncapacity_06min.nc
coverFractionNC = tall_natural_groundcover_06min.nc
landCoverMapsNC = None
fracVegCover = fraction_tall_natural_06arcmin.map
minSoilDepthFrac = tall_natural_min_rootdepth_fraction_06min.map
maxSoilDepthFrac = tall_natural_max_rootdepth_fraction_06min.map
rootFraction1 = tall_natural_rootfraction_z1_06min.map
rootFraction2 = tall_natural_rootfraction_z2_06min.map
maxRootDepth = tall_natural_max_rootdepth_06min.map
arnoBeta = None
interceptStorIni = MAIN_INITIAL_STATE_FOLDER/interceptStor_forest_DATE_FOR_INITIAL_STATES.map
snowCoverSWEIni = MAIN_INITIAL_STATE_FOLDER/snowCoverSWE_forest_DATE_FOR_INITIAL_STATES.map
snowFreeWaterIni = MAIN_INITIAL_STATE_FOLDER/snowFreeWater_forest_DATE_FOR_INITIAL_STATES.map
topWaterLayerIni = MAIN_INITIAL_STATE_FOLDER/topWaterLayer_forest_DATE_FOR_INITIAL_STATES.map
storUppIni = MAIN_INITIAL_STATE_FOLDER/storUpp_forest_DATE_FOR_INITIAL_STATES.map
storLowIni = MAIN_INITIAL_STATE_FOLDER/storLow_forest_DATE_FOR_INITIAL_STATES.map
interflowIni = MAIN_INITIAL_STATE_FOLDER/interflow_forest_DATE_FOR_INITIAL_STATES.map

[grasslandOptions]
name = grassland
debugWaterBalance = True
snowModuleType = Simple
freezingT = 0.0
degreeDayFactor = 0.0055
snowWaterHoldingCap = 0.1
refreezingCoeff = 0.05
minTopWaterLayer = 0.0
minCropKC = 0.2
cropCoefficientNC = short_cropcoefficient_06min.nc
interceptCapNC = short_interceptioncapacity_06min.nc
coverFractionNC = short_groundcover_06min.nc
landCoverMapsNC = None
fracVegCover = fraction_short_natural_06arcmin.map
minSoilDepthFrac = short_min_rootdepth_fraction_06min.map
maxSoilDepthFrac = short_max_rootdepth_fraction_06min.map
rootFraction1 = short_rootfraction_z1_06min.map
rootFraction2 = short_rootfraction_z2_06min.map
maxRootDepth = short_max_rootdepth_06min.map
arnoBeta = None
interceptStorIni = MAIN_INITIAL_STATE_FOLDER/interceptStor_grassland_DATE_FOR_INITIAL_STATES.map
snowCoverSWEIni = MAIN_INITIAL_STATE_FOLDER/snowCoverSWE_grassland_DATE_FOR_INITIAL_STATES.map
snowFreeWaterIni = MAIN_INITIAL_STATE_FOLDER/snowFreeWater_grassland_DATE_FOR_INITIAL_STATES.map
topWaterLayerIni = MAIN_INITIAL_STATE_FOLDER/topWaterLayer_grassland_DATE_FOR_INITIAL_STATES.map
storUppIni = MAIN_INITIAL_STATE_FOLDER/storUpp_grassland_DATE_FOR_INITIAL_STATES.map
storLowIni = MAIN_INITIAL_STATE_FOLDER/storLow_grassland_DATE_FOR_INITIAL_STATES.map
interflowIni = MAIN_INITIAL_STATE_FOLDER/interflow_grassland_DATE_FOR_INITIAL_STATES.map

[urbanOptions]
name = urban
debugWaterBalance = True
snowModuleType = Simple
freezingT = 0.0
degreeDayFactor = 0.0055
snowWaterHoldingCap = 0.1
refreezingCoeff = 0.05
minTopWaterLayer = 0.0
minCropKC = 0.2
cropCoefficientNC = urban_cropcoefficient_06min.nc
interceptCapNC = urban_interceptioncapacity_06min.nc
coverFractionNC = urban_groundcover_06min.nc
landCoverMapsNC = None
fracVegCover = fraction_urban_06arcmin.map
minSoilDepthFrac = urban_min_rootdepth_fraction_06min.map
maxSoilDepthFrac = urban_max_rootdepth_fraction_06min.map
rootFraction1 = urban_rootfraction_z1_06min.map
rootFraction2 = urban_rootfraction_z2_06min.map
maxRootDepth = urban_max_rootdepth_06min.map
arnoBeta = None
interceptStorIni = MAIN_INITIAL_STATE_FOLDER/interceptStor_urban_DATE_FOR_INITIAL_STATES.map
snowCoverSWEIni = MAIN_INITIAL_STATE_FOLDER/snowCoverSWE_urban_DATE_FOR_INITIAL_STATES.map
snowFreeWaterIni = MAIN_INITIAL_STATE_FOLDER/snowFreeWater_urban_DATE_FOR_INITIAL_STATES.map
topWaterLayerIni = MAIN_INITIAL_STATE_FOLDER/topWaterLayer_urban_DATE_FOR_INITIAL_STATES.map
storUppIni = MAIN_INITIAL_STATE_FOLDER/storUpp_urban_DATE_FOR_INITIAL_STATES.map
storLowIni = MAIN_INITIAL_STATE_FOLDER/storLow_urban_DATE_FOR_INITIAL_STATES.map
interflowIni = MAIN_INITIAL_STATE_FOLDER/interflow_urban_DATE_FOR_INITIAL_STATES.map

[cropOptions]
name = crop
debugWaterBalance = True
snowModuleType = Simple
freezingT = 0.0
degreeDayFactor = 0.0055
snowWaterHoldingCap = 0.1
refreezingCoeff = 0.05
minTopWaterLayer = 0.0
minCropKC = 0.2
cropCoefficientNC = crops_cropcoefficient_06min.nc
interceptCapNC = crops_interceptioncapacity_06min.nc
coverFractionNC = crops_groundcover_06min.nc
landCoverMapsNC = None
fracVegCover = fraction_cropland_06arcmin.map
minSoilDepthFrac = crops_min_rootdepth_fraction_06min.map
maxSoilDepthFrac = crops_max_rootdepth_fraction_06min.map
rootFraction1 = crops_rootfraction_z1_06min.map
rootFraction2 = crops_rootfraction_z2_06min.map
maxRootDepth = crops_max_rootdepth_06min.map
arnoBeta = None
interceptStorIni = MAIN_INITIAL_STATE_FOLDER/interceptStor_crop_DATE_FOR_INITIAL_STATES.map
snowCoverSWEIni = MAIN_INITIAL_STATE_FOLDER/snowCoverSWE_crop_DATE_FOR_INITIAL_STATES.map
snowFreeWaterIni = MAIN_INITIAL_STATE_FOLDER/snowFreeWater_crop_DATE_FOR_INITIAL_STATES.map
topWaterLayerIni = MAIN_INITIAL_STATE_FOLDER/topWaterLayer_crop_DATE_FOR_INITIAL_STATES.map
storUppIni = MAIN_INITIAL_STATE_FOLDER/storUpp_crop_DATE_FOR_INITIAL_STATES.map
storLowIni = MAIN_INITIAL_STATE_FOLDER/storLow_crop_DATE_FOR_INITIAL_STATES.map
interflowIni = MAIN_INITIAL_STATE_FOLDER/interflow_crop_DATE_FOR_INITIAL_STATES.map

[groundwaterOptions]
debugWaterBalance = True
groundwaterPropertiesNC = groundwaterProperties5ArcMin.nc
minRecessionCoeff = 0.00025
baseflow_exponent = 1.5
doNotExtrapolateThickness = True
storGroundwaterIni = MAIN_INITIAL_STATE_FOLDER/storGroundwater_DATE_FOR_INITIAL_STATES.map
avgStorGroundwaterIni = MAIN_INITIAL_STATE_FOLDER/avgStorGroundwater_DATE_FOR_INITIAL_STATES.map
storGroundwaterFossilIni = 0.0
avgNonFossilGroundwaterAllocationLongIni = 0.0
avgNonFossilGroundwaterAllocationShortIni = 0.0
avgTotalGroundwaterAbstractionIni = 0.0
avgTotalGroundwaterAllocationLongIni = 0.0
avgTotalGroundwaterAllocationShortIni = 0.0
relativeGroundwaterHeadIni = MAIN_INITIAL_STATE_FOLDER/relativeGroundwaterHead_DATE_FOR_INITIAL_STATES.map
baseflowIni = MAIN_INITIAL_STATE_FOLDER/baseflow_DATE_FOR_INITIAL_STATES.map

[routingOptions]
debugWaterBalance = True
lddMap = lddsound_06min_version_202007XX_for_ulysses.map
cellAreaMap = cellarea.map
routingMethod = accuTravelTime
manningsN = 0.04
dynamicFloodPlain = False
gradient = channel_gradient.map
constantChannelDepth = bankfull_depth.map
constantChannelWidth = bankfull_width.map
minimumChannelWidth = bankfull_width.map
bankfullCapacity = None
cropCoefficientWaterNC = cropCoefficientForOpenWater.nc
minCropWaterKC = 1.00
includeWaterBodies = True
waterBodyInputNC = lakes_and_reservoirs_06min_global_version_july_2020_for_ulysses.nc
onlyNaturalWaterBodies = False
waterBodyStorageIni = MAIN_INITIAL_STATE_FOLDER/waterBodyStorage_DATE_FOR_INITIAL_STATES.map
channelStorageIni = MAIN_INITIAL_STATE_FOLDER/channelStorage_DATE_FOR_INITIAL_STATES.map
readAvlChannelStorageIni = MAIN_INITIAL_STATE_FOLDER/readAvlChannelStorage_DATE_FOR_INITIAL_STATES.map
avgDischargeLongIni = MAIN_INITIAL_STATE_FOLDER/avgDischargeLong_DATE_FOR_INITIAL_STATES.map
avgDischargeShortIni = MAIN_INITIAL_STATE_FOLDER/avgDischargeShort_DATE_FOR_INITIAL_STATES.map
m2tDischargeLongIni = MAIN_INITIAL_STATE_FOLDER/m2tDischargeLong_DATE_FOR_INITIAL_STATES.map
avgBaseflowLongIni = MAIN_INITIAL_STATE_FOLDER/avgBaseflowLong_DATE_FOR_INITIAL_STATES.map
riverbedExchangeIni = MAIN_INITIAL_STATE_FOLDER/riverbedExchange_DATE_FOR_INITIAL_STATES.map
subDischargeIni = MAIN_INITIAL_STATE_FOLDER/subDischarge_DATE_FOR_INITIAL_STATES.map
avgLakeReservoirInflowShortIni = MAIN_INITIAL_STATE_FOLDER/avgLakeReservoirInflowShort_DATE_FOR_INITIAL_STATES.map
avgLakeReservoirOutflowLongIni = MAIN_INITIAL_STATE_FOLDER/avgLakeReservoirOutflowLong_DATE_FOR_INITIAL_STATES.map
timestepsToAvgDischargeIni = MAIN_INITIAL_STATE_FOLDER/timestepsToAvgDischarge_DATE_FOR_INITIAL_STATES.map

[reportingOptions]
landmask_for_reporting = land_mask_only.map
outDailyTotNC = ulyssesP,ulyssesET,ulyssesSWE,ulyssesQsm,ulyssesSM,ulyssesQrRunoff,ulyssesSMUpp,ulyssesSMLow,discharge
outMonthTotNC = None
outMonthAvgNC = None
outMonthEndNC = None
outAnnuaTotNC = None
outAnnuaAvgNC = None
outAnnuaEndNC = None
outMonthMaxNC = None
outAnnuaMaxNC = None
formatNetCDF = NETCDF4
zlib = True
save_monthly_end_states = True

EOF

    #  -- link files -----------------------------------
    # run the model
    ecflow_client --label="info" "${ii}: running ..."
    python3 /ec/fws4/sb/project/C3SHydroGL/suites/ulysses_cyrs/ecflow_work/mswep_reference_runs_update_restart1981_1_1/progs/PGB_PY/model/deterministic_runner_parallel_for_ulysses.py pgb_config.ini debug global -mod /ec/fws4/sb/project/C3SHydroGL/suites/ulysses_cyrs/ecflow_work/mswep_reference_runs_update_restart1981_1_1/update_restart_1981_01_01/m01/pgb/${ii} -misd ${restartdir} -dfis ${restartdate}
    #  -- store ii for next iteration --------------
    restartdir=/ec/fws4/sb/project/C3SHydroGL/suites/ulysses_cyrs/ecflow_work/mswep_reference_runs_update_restart1981_1_1/update_restart_1981_01_01/m01/pgb/${ii}/states
    restartdate=${edate}
done
set +x
ecflow_client --label="info" "done!"
        
wait                      # wait for background process to stop
ecflow_client --complete  # Notify ecFlow of a normal end
trap 0                    # Remove all traps
exit 0                    # End the shell
