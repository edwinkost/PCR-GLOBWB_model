#~ [globalOptions]

# -- on Snellius
inputDir="/projects/0/dfguu/users/edwin/data/pcrglobwb_input_arise/develop/"

ln -s ${inputDir}/africa_30sec/cloneMaps/version_2020-XX-XX clone_maps



#~ [meteoOptions]

#~ precipitationNC             = /tank/edwin/data/isimip_forcing/w5e5_version_2.0_downscaled_with_chirps/pr_W5E5v2.0_1981-2019_mm_per_day_africa_downscaled_with_chirps.nc 
#~ temperatureNC               = /tank/edwin/data/meteo_arise/era5land_africa/africa_merged/1981-2019/daily/africa_era5-land_daily_t2m-average_rempacon-150-arcsec_daily.nc
#~ wind_speed_10m              = /tank/edwin/data/meteo_arise/era5land_africa/africa_merged/1981-2019/daily/africa_era5-land_daily_wind10m-avg_rempacon-150-arcsec_daily.nc
#~ atmospheric_pressure        = /tank/edwin/data/meteo_arise/era5land_africa/africa_merged/1981-2019/daily/africa_era5-land_daily_spressu-avg_rempacon-150-arcsec_daily.nc
#~ surface_net_solar_radiation = /tank/edwin/data/meteo_arise/era5land_africa/africa_merged/1981-2019/daily/africa_era5-land_daily_total-ssrad_rempacon-150-arcsec_daily.nc
#~ albedo                      = /tank/edwin/data/meteo_arise/era5land_africa/africa_merged/1981-2019/daily/africa_era5-land_daily_fal-average_rempacon-150-arcsec_daily.nc
#~ dewpoint_temperature_avg    = /tank/edwin/data/meteo_arise/era5land_africa/africa_merged/1981-2019/daily/africa_era5-land_daily_d2m-average_rempacon-150-arcsec_daily.nc


ln -s ${inputDir}/global_30sec/landSurface/topography/merit_dem_processed/version_2021-02-XX/maps_covered_with_zero/dem_average_topography_parameters_30sec_february_2021_global_covered_with_zero.nc

ln -s ${inputDir}/global_30sec/meteo/unique_ids/unique_ids_150_arcsec_correct_lats.nc

ln -s ${inputDir}/global_05min_from_gmd_paper_input/meteo/downscaling_from_30min/temperature_slope.nc                                                                     
ln -s ${inputDir}/global_05min_from_gmd_paper_input/meteo/downscaling_from_30min/precipitation_slope.nc                                                                   
                                                                                                                                                                 
ln -s ${inputDir}/global_05min_from_gmd_paper_input/meteo/downscaling_from_30min/temperature_correl.nc                                                                     
ln -s ${inputDir}//global_05min_from_gmd_paper_input/meteo/downscaling_from_30min/precipitation_correl.nc                                                                   

ln -s ${inputDir}/global_30sec/landSurface/topography/merit_dem_processed/version_2021-02-XX/maps_covered_with_zero/topography_parameters_30sec_february_2021_global_covered_with_zero.nc

ln -s ${inputDir}/africa_30sec/landSurface/soil/soilgrids/version_2021-02-XX/layerDepth_average_1_africa_30sec.nc
ln -s ${inputDir}/africa_30sec/landSurface/soil/soilgrids/version_2021-02-XX/layerDepth_average_2_africa_30sec.nc
ln -s ${inputDir}/africa_30sec/landSurface/soil/soilgrids/version_2021-02-XX/WHC_average_1_africa_30sec.nc
ln -s ${inputDir}/africa_30sec/landSurface/soil/soilgrids/version_2021-02-XX/WHC_average_2_africa_30sec.nc
ln -s ${inputDir}/africa_30sec/landSurface/soil/soilgrids/version_2021-02-XX/psiAir_average_1_africa_30sec.nc
ln -s ${inputDir}/africa_30sec/landSurface/soil/soilgrids/version_2021-02-XX/psiAir_average_2_africa_30sec.nc
ln -s ${inputDir}/africa_30sec/landSurface/soil/soilgrids/version_2021-02-XX/BCH_average_1_africa_30sec.nc
ln -s ${inputDir}/africa_30sec/landSurface/soil/soilgrids/version_2021-02-XX/BCH_average_2_africa_30sec.nc
ln -s ${inputDir}/africa_30sec/landSurface/soil/soilgrids/version_2021-02-XX/vmcRes_average_1_africa_30sec.nc
ln -s ${inputDir}/africa_30sec/landSurface/soil/soilgrids/version_2021-02-XX/vmcRes_average_2_africa_30sec.nc
ln -s ${inputDir}/africa_30sec/landSurface/soil/soilgrids/version_2021-02-XX/vmcSat_average_1_africa_30sec.nc
ln -s ${inputDir}/africa_30sec/landSurface/soil/soilgrids/version_2021-02-XX/vmcSat_average_2_africa_30sec.nc
ln -s ${inputDir}/africa_30sec/landSurface/soil/soilgrids/version_2021-02-XX/kSat_average_1_africa_30sec.nc
ln -s ${inputDir}/africa_30sec/landSurface/soil/soilgrids/version_2021-02-XX/kSat_average_2_africa_30sec.nc
ln -s ${inputDir}/global_30sec/landSurface/soil/impeded_drainage/global_30sec_impeded_drainage_permafrost_dsmw_correct_lats.nc


ln -s ${inputDir}/global_30min_from_gmd_paper_input/waterUse/irrigation/irrigation_efficiency/efficiency.nc

#~ # OLD WATER DEMAN FILES domestic, industrial and livestock water demand data (unit must be in m.day-1)
#~ domesticWaterDemandFile  = global_05min_from_gmd_paper_input/waterUse/waterDemand/domestic/domestic_water_demand_version_april_2015.nc
#~ industryWaterDemandFile  = global_05min_from_gmd_paper_input/waterUse/waterDemand/industry/industry_water_demand_version_april_2015.nc
#~ livestockWaterDemandFile = global_05min_from_gmd_paper_input/waterUse/waterDemand/livestock/livestock_water_demand_version_april_2015.nc


# - the following water demand files were used for the Aqueduct runs
ln -s ${inputDir}/global_05min/waterUse/waterDemand/version_2021-09-13/domestic_water_demand_historical_1960-2019.nc
ln -s ${inputDir}/global_05min/waterUse/waterDemand/version_2021-09-13/domestic_water_demand_ssp1_2000-2100.nc
ln -s ${inputDir}/global_05min/waterUse/waterDemand/version_2021-09-13/domestic_water_demand_ssp2_2000-2100.nc
ln -s ${inputDir}/global_05min/waterUse/waterDemand/version_2021-09-13/domestic_water_demand_ssp3_2000-2100.nc
ln -s ${inputDir}/global_05min/waterUse/waterDemand/version_2021-09-13/domestic_water_demand_ssp5_2000-2100.nc
ln -s ${inputDir}/global_05min/waterUse/waterDemand/version_2021-09-13/industry_water_demand_historical_1960-2019.nc
ln -s ${inputDir}/global_05min/waterUse/waterDemand/version_2021-09-13/industry_water_demand_ssp1_2000-2100.nc
ln -s ${inputDir}/global_05min/waterUse/waterDemand/version_2021-09-13/industry_water_demand_ssp2_2000-2100.nc
ln -s ${inputDir}/global_05min/waterUse/waterDemand/version_2021-09-13/industry_water_demand_ssp3_2000-2100.nc
ln -s ${inputDir}/global_05min/waterUse/waterDemand/version_2021-09-13/industry_water_demand_ssp5_2000-2100.nc
ln -s ${inputDir}/global_05min/waterUse/waterDemand/version_2021-09-13/livestock_water_demand_05min.nc


ln -s ${inputDir}/global_05min_from_gmd_paper_input/waterUse/desalination/desalination_water_version_april_2015.nc

ln -s ${inputDir}/global_05min_from_gmd_paper_input/waterUse/abstraction_zones/abstraction_zones_60min_05min.nc

ln -s ${inputDir}/global_05min_from_gmd_paper_input/waterUse/source_partitioning/surface_water_fraction_for_irrigation/AEI_SWFRAC.nc
ln -s ${inputDir}/global_05min_from_gmd_paper_input/waterUse/source_partitioning/surface_water_fraction_for_irrigation/AEI_QUAL.nc

ln -s ${inputDir}/global_30min_from_gmd_paper_input/waterUse/source_partitioning/surface_water_fraction_for_non_irrigation/max_city_sw_fraction.nc


ln -s ${inputDir}/africa_30sec/landSurface/landCover/naturalVegetationAndRainFedCrops/version_2020-12-XX/composite-short-n-tall_crop_coefficient.nc
ln -s ${inputDir}/africa_30sec/landSurface/landCover/naturalVegetationAndRainFedCrops/version_2020-12-XX/composite-short-n-tall_intercept_capacity.nc
ln -s ${inputDir}/africa_30sec/landSurface/landCover/naturalVegetationAndRainFedCrops/version_2020-12-XX/composite-short-n-tall_cover_fraction.nc

ln -s ${inputDir}/africa_30sec/landSurface/landCover/naturalVegetationAndRainFedCrops/version_2020-12-XX/rfrac1_all.nc
ln -s ${inputDir}/africa_30sec/landSurface/landCover/naturalVegetationAndRainFedCrops/version_2020-12-XX/rfrac2_all.nc	
ln -s ${inputDir}/africa_30sec/landSurface/landCover/naturalVegetationAndRainFedCrops/version_2020-12-XX/meanrootdepth_all.nc

ln -s ${inputDir}/global_30sec/landSurface/landCover/irrigated_fractions/global_estimate_irrigation_paddy_fraction_30sec.nc
ln -s ${inputDir}/global_30min_from_gmd_paper_input/landSurface/landCover/irrPaddy/rfrac1_paddy.nc
ln -s ${inputDir}/global_30min_from_gmd_paper_input/landSurface/landCover/irrPaddy/rfrac2_paddy.nc

ln -s ${inputDir}/global_30min_from_gmd_paper_input/landSurface/landCover/irrPaddy/Global_CropCoefficientKc-IrrPaddy_30min.nc


ln -s ${inputDir}/global_30sec/landSurface/landCover/irrigated_fractions/global_estimate_irrigation_non_paddy_fraction_30sec.nc
ln -s ${inputDir}/global_30min_from_gmd_paper_input/landSurface/landCover/irrNonPaddy/rfrac1_nonpaddy.nc
ln -s ${inputDir}/global_30min_from_gmd_paper_input/landSurface/landCover/irrNonPaddy/rfrac2_nonpaddy.nc
maxRootDepth     = 1.0
#
# Parameters for the Arno's scheme:
arnoBeta = None
# If arnoBeta is defined, the soil water capacity distribution is based on this.
# If arnoBeta is NOT defined, maxSoilDepthFrac must be defined such that arnoBeta will be calculated based on maxSoilDepthFrac and minSoilDepthFrac.
#
# other paramater values
minTopWaterLayer = 0.0
minCropKC        = 0.2
cropDeplFactor   = 0.5
minInterceptCap  = 0.0002

cropCoefficientNC = global_30min_from_gmd_paper_input/landSurface/landCover/irrNonPaddy/Global_CropCoefficientKc-IrrNonPaddy_30min.nc

# initial conditions:

interceptStorIni = /tank/edwin/pcrglobwb_output_africa/version_2021-07-XX/tanzania_30sec/1999-2001/states/interceptStor_irrNonPaddy_1999-12-31.map
snowCoverSWEIni  = /tank/edwin/pcrglobwb_output_africa/version_2021-07-XX/tanzania_30sec/1999-2001/states/snowCoverSWE_irrNonPaddy_1999-12-31.map
snowFreeWaterIni = /tank/edwin/pcrglobwb_output_africa/version_2021-07-XX/tanzania_30sec/1999-2001/states/snowFreeWater_irrNonPaddy_1999-12-31.map
topWaterLayerIni = /tank/edwin/pcrglobwb_output_africa/version_2021-07-XX/tanzania_30sec/1999-2001/states/topWaterLayer_irrNonPaddy_1999-12-31.map
storUppIni       = /tank/edwin/pcrglobwb_output_africa/version_2021-07-XX/tanzania_30sec/1999-2001/states/storUpp_irrNonPaddy_1999-12-31.map
storLowIni       = /tank/edwin/pcrglobwb_output_africa/version_2021-07-XX/tanzania_30sec/1999-2001/states/storLow_irrNonPaddy_1999-12-31.map
interflowIni     = /tank/edwin/pcrglobwb_output_africa/version_2021-07-XX/tanzania_30sec/1999-2001/states/interflow_irrNonPaddy_1999-12-31.map

noParameterExtrapolation = True


[groundwaterOptions]

debugWaterBalance = True

#~ groundwaterPropertiesNC = global_05min/groundwater/properties/groundwaterProperties5ArcMin.nc
groundwaterPropertiesNC    = None
#
recessionCoeff = global_30sec/groundwater/properties/version_202102XX/recession_coefficient_30sec.nc
kSatAquifer    = global_30sec/groundwater/properties/version_202102XX/k_conductivity_aquifer_filled_30sec.nc
specificYield  = global_30sec/groundwater/properties/version_202102XX/specific_yield_aquifer_filled_30sec.nc
#
# minimum value for groundwater recession coefficient (day-1) 
# - about 11 years
minRecessionCoeff = 0.00025
#~ # - about 27 years
#~ minRecessionCoeff = 1.0e-4

#~ (pcrglobwb_python3) sutan101@gpu038.cluster:/scratch/depfg/sutan101/data/pcrglobwb_input_arise/develop/global_30sec/groundwater/properties/version_202102XX$ ls -lah *.nc
#~ -rw-r--r-- 1 sutan101 depfg 3.5G Mar  1 16:32 k_conductivity_aquifer_filled_30sec.nc
#~ -rw-r--r-- 1 sutan101 depfg 3.5G Mar  1 16:32 recession_coefficient_30sec.nc
#~ -rw-r--r-- 1 sutan101 depfg 3.5G Mar  1 16:33 specific_yield_aquifer_filled_30sec.nc

# some options for constraining groundwater abstraction
limitFossilGroundWaterAbstraction      = True
estimateOfRenewableGroundwaterCapacity = 0.0
estimateOfTotalGroundwaterThickness    = global_30sec/groundwater/aquifer_thickness_estimate/version_2020-09-XX/thickness_05min_remapbil_to_30sec_filled_with_pcr_correct_lat.nc
# minimum and maximum total groundwater thickness 
minimumTotalGroundwaterThickness       = 100.
maximumTotalGroundwaterThickness       = None

#~ (pcrglobwb_python3) sutan101@gpu038.cluster:/scratch/depfg/sutan101/data/pcrglobwb_input_arise/develop/global_30sec/groundwater/aquifer_thickness_estimate/version_2020-09-XX$ ls -lah *.nc
#~ -rw-r--r-- 1 sutan101 depfg 3.5G Jan 28 17:49 diff.nc
#~ -rw-r--r-- 1 sutan101 depfg 3.5G Jan 28 17:52 thickness_05min_remapbil_to_30sec_filled.nc
#~ -rw-r--r-- 1 sutan101 depfg 3.5G Jan 28 17:54 thickness_05min_remapbil_to_30sec_filled_with_pcr_correct_lat.nc
#~ -rw-r--r-- 1 sutan101 depfg 3.5G Jan 28 17:53 thickness_05min_remapbil_to_30sec_filled_with_pcr.map.nc
#~ -rw-r--r-- 1 sutan101 depfg 3.5G Jan 28 17:51 thickness_05min_remapbil_to_30sec.nc

doNotExtrapolateThickness = True
noParameterExtrapolation  = True

# annual pumping capacity for each region (unit: billion cubic meter per year), should be given in a netcdf file
pumpingCapacityNC    = global_30min_from_gmd_paper_input/waterUse/groundwater_pumping_capacity/regional_abstraction_limit.nc

# zonal IDs (scale) at which zonal allocation of groundwater is performed  
allocationSegmentsForGroundwater    = global_05min_from_gmd_paper_input/waterUse/abstraction_zones/abstraction_zones_30min_05min.nc
#~ allocationSegmentsForGroundwater = False




# initial conditions:
storGroundwaterIni                           = /tank/edwin/pcrglobwb_output_africa/version_2021-07-XX/tanzania_30sec/1999-2001/states/storGroundwater_1999-12-31.map
#~ storGroundwaterIni                        = ESTIMATE_FROM_GROUNDWATER_RECHARGE_RATE

storGroundwaterFossilIni                     = /tank/edwin/pcrglobwb_output_africa/version_2021-07-XX/tanzania_30sec/1999-2001/states/storGroundwaterFossil_1999-12-31.map
#~ storGroundwaterFossilIni                  = Maximum

avgNonFossilGroundwaterAllocationLongIni     = /tank/edwin/pcrglobwb_output_africa/version_2021-07-XX/tanzania_30sec/1999-2001/states/avgNonFossilGroundwaterAllocationLong_1999-12-31.map
avgNonFossilGroundwaterAllocationShortIni    = /tank/edwin/pcrglobwb_output_africa/version_2021-07-XX/tanzania_30sec/1999-2001/states/avgNonFossilGroundwaterAllocationShort_1999-12-31.map
avgTotalGroundwaterAbstractionIni            = /tank/edwin/pcrglobwb_output_africa/version_2021-07-XX/tanzania_30sec/1999-2001/states/avgTotalGroundwaterAbstraction_1999-12-31.map
avgTotalGroundwaterAllocationLongIni         = /tank/edwin/pcrglobwb_output_africa/version_2021-07-XX/tanzania_30sec/1999-2001/states/avgTotalGroundwaterAllocationLong_1999-12-31.map
avgTotalGroundwaterAllocationShortIni        = /tank/edwin/pcrglobwb_output_africa/version_2021-07-XX/tanzania_30sec/1999-2001/states/avgTotalGroundwaterAllocationShort_1999-12-31.map
relativeGroundwaterHeadIni                   = /tank/edwin/pcrglobwb_output_africa/version_2021-07-XX/tanzania_30sec/1999-2001/states/relativeGroundwaterHead_1999-12-31.map
baseflowIni                                  = /tank/edwin/pcrglobwb_output_africa/version_2021-07-XX/tanzania_30sec/1999-2001/states/baseflow_1999-12-31.map

# we need avgStorGroundwater for a non linear groundwater reservoir
avgStorGroundwaterIni                        = /tank/edwin/pcrglobwb_output_africa/version_2021-07-XX/tanzania_30sec/1999-2001/states/avgStorGroundwater_1999-12-31.map


# option to start with the maximum value for storGroundwaterFossilIni (this will set/lead to storGroundwaterFossilIni = Maximum ; overwrite/overrule existing storGroundwaterFossilIni)
#~ useMaximumStorGroundwaterFossilIni        = True
#~ useMaximumStorGroundwaterFossilIni        = False
useMaximumStorGroundwaterFossilIni           = USE_MAXIMUM_STOR_GROUNDWATER_FOSSIL_INI


# option to start with the value of storGroundwaterIni estimated from groundwater recharge (this will set/lead to storGroundwaterIni = ESTIMATE_FROM_GROUNDWATER_RECHARGE_RATE)
#~ estimateStorGroundwaterIniFromRecharge    = True
#~ estimateStorGroundwaterIniFromRecharge    = False
estimateStorGroundwaterIniFromRecharge       = ESTIMATE_STOR_GROUNDWATER_INI_FROM_RECHARGE
dailyGroundwaterRechargeIni                  = DAILY_GROUNDWATER_RECHARGE_INI


[routingOptions]

debugWaterBalance = True

# drainage direction map
lddMap      = global_30sec/routing/surface_water_bodies/version_2020-05-XX/lddsound_30sec_version_202005XX_correct_lat.nc

# cell area (unit: m2)
cellAreaMap = global_30sec/routing/cell_area/cdo_grid_area_30sec_map_correct_lat.nc

# routing method:
routingMethod = accuTravelTime

# manning coefficient
manningsN   = 0.04

# Option for flood plain simulation
dynamicFloodPlain = True

# manning coefficient for floodplain
floodplainManningsN = 0.07


#~ pcrglobwb_python3) sutan101@gpu038.cluster:/scratch/depfg/sutan101/data/pcrglobwb_input_arise/develop/global_30sec/routing/channel_properties/version_2021-02-XX/maps_covered_with_zero$ ls -lah *.nc
#~ -rw-r--r-- 1 sutan101 depfg 25G Mar  1 15:52 channel_parameters_30sec_february_2021_global_covered_with_zero.nc

# channel gradient
gradient             = global_30sec/routing/channel_properties/version_2021-02-XX/maps_covered_with_zero/channel_gradient_channel_parameters_30sec_february_2021_global_covered_with_zero.nc

# constant channel depth 
constantChannelDepth = global_30sec/routing/channel_properties/version_2021-02-XX/maps_covered_with_zero/bankfull_depth_channel_parameters_30sec_february_2021_global_covered_with_zero.nc

# constant channel width (optional)
constantChannelWidth = global_30sec/routing/channel_properties/version_2021-02-XX/maps_covered_with_zero/bankfull_width_channel_parameters_30sec_february_2021_global_covered_with_zero.nc

# minimum channel width (optional)
minimumChannelWidth  = global_30sec/routing/channel_properties/version_2021-02-XX/maps_covered_with_zero/bankfull_width_channel_parameters_30sec_february_2021_global_covered_with_zero.nc

# channel properties for flooding
bankfullCapacity     = None
# - If None, it will be estimated from (bankfull) channel depth (m) and width (m) 

# files for relative elevation (above minimum dem) 
relativeElevationFiles  = global_30sec/landSurface/topography/merit_dem_processed/version_2021-02-XX/maps_covered_with_zero/dzRel%04d_topography_parameters_30sec_february_2021_global_covered_with_zero.nc
relativeElevationLevels = 0.0, 0.01, 0.05, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00


# composite crop factors for WaterBodies: 
cropCoefficientWaterNC = global_30min_from_gmd_paper_input/routing/kc_surface_water/cropCoefficientForOpenWater.nc
minCropWaterKC         = 1.00

#~ (pcrglobwb_python3) sutan101@gpu038.cluster:/scratch/depfg/sutan101/data/pcrglobwb_input_arise/develop/global_30sec/routing/surface_water_bodies/version_2020-05-XX$ ls -lah *.nc
#~ -r--r--r-- 1 sutan101 depfg 209G Jan 28 19:05 lakes_and_reservoirs_30sec_global_2010_to_2019_version_202005XX.nc
#~ -r--r--r-- 1 sutan101 depfg  21G Jan 28 19:09 lakes_and_reservoirs_30sec_global_2019_version_202005XX.nc
#~ -r--r--r-- 1 sutan101 depfg 1.8G Jan 28 19:10 lddsound_30sec_version_202005XX_correct_lat.nc
#~ -r--r--r-- 1 sutan101 depfg 891M Jan 28 19:10 lddsound_30sec_version_202005XX.nc

# lake and reservoir parameters
includeWaterBodies        = True
#~ waterBodyInputNC       = africa_30sec/routing/surface_water_bodies/version_20200525/lakes_and_reservoirs_30sec_africa_version_may_2020.nc
waterBodyInputNC          = global_30sec/routing/surface_water_bodies/version_2020-05-XX/lakes_and_reservoirs_30sec_global_2019_version_202005XX.nc
#~ fracWaterInp           = None
#~ waterBodyIds           = None
#~ waterBodyTyp           = None
#~ resMaxCapInp           = None
#~ resSfAreaInp           = None
onlyNaturalWaterBodies    = False


# initial conditions:
waterBodyStorageIni            = /tank/edwin/pcrglobwb_output_africa/version_2021-07-XX/tanzania_30sec/1999-2001/states/waterBodyStorage_1999-12-31.map
channelStorageIni              = /tank/edwin/pcrglobwb_output_africa/version_2021-07-XX/tanzania_30sec/1999-2001/states/channelStorage_1999-12-31.map
readAvlChannelStorageIni       = /tank/edwin/pcrglobwb_output_africa/version_2021-07-XX/tanzania_30sec/1999-2001/states/readAvlChannelStorage_1999-12-31.map
avgDischargeLongIni            = /tank/edwin/pcrglobwb_output_africa/version_2021-07-XX/tanzania_30sec/1999-2001/states/avgDischargeLong_1999-12-31.map
avgDischargeShortIni           = /tank/edwin/pcrglobwb_output_africa/version_2021-07-XX/tanzania_30sec/1999-2001/states/avgDischargeShort_1999-12-31.map
m2tDischargeLongIni            = /tank/edwin/pcrglobwb_output_africa/version_2021-07-XX/tanzania_30sec/1999-2001/states/m2tDischargeLong_1999-12-31.map
avgBaseflowLongIni             = /tank/edwin/pcrglobwb_output_africa/version_2021-07-XX/tanzania_30sec/1999-2001/states/avgBaseflowLong_1999-12-31.map
riverbedExchangeIni            = /tank/edwin/pcrglobwb_output_africa/version_2021-07-XX/tanzania_30sec/1999-2001/states/riverbedExchange_1999-12-31.map
subDischargeIni                = /tank/edwin/pcrglobwb_output_africa/version_2021-07-XX/tanzania_30sec/1999-2001/states/subDischarge_1999-12-31.map
avgLakeReservoirInflowShortIni = /tank/edwin/pcrglobwb_output_africa/version_2021-07-XX/tanzania_30sec/1999-2001/states/avgLakeReservoirInflowShort_1999-12-31.map
avgLakeReservoirOutflowLongIni = /tank/edwin/pcrglobwb_output_africa/version_2021-07-XX/tanzania_30sec/1999-2001/states/avgLakeReservoirOutflowLong_1999-12-31.map
timestepsToAvgDischargeIni     = /tank/edwin/pcrglobwb_output_africa/version_2021-07-XX/tanzania_30sec/1999-2001/states/timestepsToAvgDischarge_1999-12-31.map


[reportingOptions]

# landmask for reporting
landmask_for_reporting = None

# output files that will be written in the disk in netcdf files:
# - daily resolution
outDailyTotNC    = discharge,totalRunoff,gwRecharge,totalGroundwaterAbstraction,surfaceWaterStorage,temperature,precipitation,referencePotET,satDegUpp,satDegLow,satDegTotal,totalEvaporation,channelStorage,dynamicFracWat,floodVolume,floodDepth,surfaceWaterLevel
#~ outDailyTotNC = discharge,totalRunoff
# - monthly resolution
outMonthTotNC = actualET,irrPaddyWaterWithdrawal,irrNonPaddyWaterWithdrawal,domesticWaterWithdrawal,industryWaterWithdrawal,livestockWaterWithdrawal,runoff,totalRunoff,baseflow,directRunoff,interflowTotal,totalGroundwaterAbstraction,desalinationAbstraction,surfaceWaterAbstraction,nonFossilGroundwaterAbstraction,fossilGroundwaterAbstraction,irrGrossDemand,nonIrrGrossDemand,totalGrossDemand,nonIrrWaterConsumption,nonIrrReturnFlow,precipitation,gwRecharge,surfaceWaterInf,referencePotET,totalEvaporation,totalPotentialEvaporation,totLandSurfaceActuaET,totalLandSurfacePotET,waterBodyActEvaporation,waterBodyPotEvaporation
outMonthAvgNC = discharge,temperature,dynamicFracWat,surfaceWaterStorage,interceptStor,snowFreeWater,snowCoverSWE,topWaterLayer,storUppTotal,storLowTotal,storGroundwater,storGroundwaterFossil,totalActiveStorageThickness,totalWaterStorageThickness,satDegUpp,satDegLow,channelStorage,waterBodyStorage
outMonthEndNC = storGroundwater,storGroundwaterFossil,waterBodyStorage,channelStorage,totalWaterStorageThickness,totalActiveStorageThickness
# - annual resolution
outAnnuaTotNC = totalEvaporation,precipitation,gwRecharge,totalRunoff,baseflow,desalinationAbstraction,surfaceWaterAbstraction,nonFossilGroundwaterAbstraction,fossilGroundwaterAbstraction,totalGroundwaterAbstraction,totalAbstraction,irrGrossDemand,nonIrrGrossDemand,totalGrossDemand,nonIrrWaterConsumption,nonIrrReturnFlow,runoff,actualET,irrPaddyWaterWithdrawal,irrNonPaddyWaterWithdrawal,irrigationWaterWithdrawal,domesticWaterWithdrawal,industryWaterWithdrawal,livestockWaterWithdrawal,precipitation_at_irrigation,netLqWaterToSoil_at_irrigation,evaporation_from_irrigation,transpiration_from_irrigation,referencePotET
outAnnuaAvgNC = temperature,discharge,surfaceWaterStorage,waterBodyStorage,interceptStor,snowFreeWater,snowCoverSWE,topWaterLayer,storUppTotal,storLowTotal,storGroundwater,storGroundwaterFossil,totalWaterStorageThickness,satDegUpp,satDegLow,channelStorage,waterBodyStorage,fractionWaterBodyEvaporation,fractionTotalEvaporation,fracSurfaceWaterAllocation,fracDesalinatedWaterAllocation,gwRecharge
outAnnuaEndNC = surfaceWaterStorage,interceptStor,snowFreeWater,snowCoverSWE,topWaterLayer,storUppTotal,storLowTotal,storGroundwater,storGroundwaterFossil,totalWaterStorageThickness
# - monthly and annual maxima
outMonthMaxNC = channelStorage,dynamicFracWat,floodVolume,floodDepth,surfaceWaterLevel,discharge,totalRunoff
outAnnuaMaxNC = channelStorage,dynamicFracWat,floodVolume,floodDepth,surfaceWaterLevel,discharge,totalRunoff

#~ # netcdf format and zlib setup
#~ formatNetCDF = NETCDF4
#~ zlib = True

