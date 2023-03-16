
set -x

mkdir /scratch/depfg/sutan101/data/pcrglobwb_input_arise/version_2023-03-16_africa-30sec_links
cd /scratch/depfg/sutan101/data/pcrglobwb_input_arise/version_2023-03-16_africa-30sec_links

# -- on eejit
inputDir="/scratch/depfg/sutan101/data/pcrglobwb_input_arise/develop/"


ln -s ${inputDir}/africa_30sec/cloneMaps/version_2020-XX-XX clone_maps

ln -s ${inputDir}/global_30sec/landSurface/topography/merit_dem_processed/version_2021-02-XX/maps_covered_with_zero/dem_average_topography_parameters_30sec_february_2021_global_covered_with_zero.nc

ln -s ${inputDir}/global_30sec/meteo/unique_ids/unique_ids_150_arcsec_correct_lats.nc
ln -s ${inputDir}/global_05min_from_gmd_paper_input/meteo/downscaling_from_30min/uniqueIds_30min.nc

ln -s ${inputDir}/global_05min_from_gmd_paper_input/meteo/downscaling_from_30min/temperature_slope.nc                                                                     
ln -s ${inputDir}/global_05min_from_gmd_paper_input/meteo/downscaling_from_30min/precipitation_slope.nc                                                                   
                                                                                                                                                                 
ln -s ${inputDir}/global_05min_from_gmd_paper_input/meteo/downscaling_from_30min/temperature_correl.nc                                                                     
ln -s ${inputDir}/global_05min_from_gmd_paper_input/meteo/downscaling_from_30min/precipitation_correl.nc                                                                   

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

# OLD WATER DEMAN FILES domestic, industrial and livestock water demand data (unit must be in m.day-1)
ln -s ${inputDir}/global_05min_from_gmd_paper_input/waterUse/waterDemand/domestic/domestic_water_demand_version_april_2015.nc
ln -s ${inputDir}/global_05min_from_gmd_paper_input/waterUse/waterDemand/industry/industry_water_demand_version_april_2015.nc
ln -s ${inputDir}/global_05min_from_gmd_paper_input/waterUse/waterDemand/livestock/livestock_water_demand_version_april_2015.nc

# - the following water demand files were used for the Aqueduct runs
ln -s ${inputDir}/global_05min/waterUse/waterDemand/version_2021-09-13/domestic_water_demands/domestic_water_demand_historical_1960-2019.nc
ln -s ${inputDir}/global_05min/waterUse/waterDemand/version_2021-09-13/domestic_water_demands/domestic_water_demand_ssp1_2000-2100.nc
ln -s ${inputDir}/global_05min/waterUse/waterDemand/version_2021-09-13/domestic_water_demands/domestic_water_demand_ssp2_2000-2100.nc
ln -s ${inputDir}/global_05min/waterUse/waterDemand/version_2021-09-13/domestic_water_demands/domestic_water_demand_ssp3_2000-2100.nc
ln -s ${inputDir}/global_05min/waterUse/waterDemand/version_2021-09-13/domestic_water_demands/domestic_water_demand_ssp5_2000-2100.nc
ln -s ${inputDir}/global_05min/waterUse/waterDemand/version_2021-09-13/industry_water_demands/industry_water_demand_historical_1960-2019.nc
ln -s ${inputDir}/global_05min/waterUse/waterDemand/version_2021-09-13/industry_water_demands/industry_water_demand_ssp1_2000-2100.nc
ln -s ${inputDir}/global_05min/waterUse/waterDemand/version_2021-09-13/industry_water_demands/industry_water_demand_ssp2_2000-2100.nc
ln -s ${inputDir}/global_05min/waterUse/waterDemand/version_2021-09-13/industry_water_demands/industry_water_demand_ssp3_2000-2100.nc
ln -s ${inputDir}/global_05min/waterUse/waterDemand/version_2021-09-13/industry_water_demands/industry_water_demand_ssp5_2000-2100.nc
ln -s ${inputDir}/global_05min/waterUse/waterDemand/version_2021-09-13/livestock_water_demands/livestock_water_demand_05min.nc


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

ln -s ${inputDir}/global_30min_from_gmd_paper_input/landSurface/landCover/irrNonPaddy/Global_CropCoefficientKc-IrrNonPaddy_30min.nc

ln -s ${inputDir}/global_30sec/groundwater/properties/version_202102XX/recession_coefficient_30sec.nc
ln -s ${inputDir}/global_30sec/groundwater/properties/version_202102XX/k_conductivity_aquifer_filled_30sec.nc
ln -s ${inputDir}/global_30sec/groundwater/properties/version_202102XX/specific_yield_aquifer_filled_30sec.nc

ln -s ${inputDir}/global_30sec/groundwater/aquifer_thickness_estimate/version_2020-09-XX/thickness_05min_remapbil_to_30sec_filled_with_pcr_correct_lat.nc

ln -s ${inputDir}/global_30min_from_gmd_paper_input/waterUse/groundwater_pumping_capacity/regional_abstraction_limit.nc

ln -s ${inputDir}/global_05min_from_gmd_paper_input/waterUse/abstraction_zones/abstraction_zones_30min_05min.nc

ln -s ${inputDir}/global_30sec/routing/surface_water_bodies/version_2020-05-XX/lddsound_30sec_version_202005XX_correct_lat.nc

ln -s ${inputDir}/global_30sec/routing/cell_area/cdo_grid_area_30sec_map_correct_lat.nc

ln -s ${inputDir}/global_30sec/routing/channel_properties/version_2021-02-XX/maps_covered_with_zero/channel_gradient_channel_parameters_30sec_february_2021_global_covered_with_zero.nc

ln -s ${inputDir}/global_30sec/routing/channel_properties/version_2021-02-XX/maps_covered_with_zero/bankfull_depth_channel_parameters_30sec_february_2021_global_covered_with_zero.nc
ln -s ${inputDir}/global_30sec/routing/channel_properties/version_2021-02-XX/maps_covered_with_zero/bankfull_width_channel_parameters_30sec_february_2021_global_covered_with_zero.nc

ln -s ${inputDir}/global_30sec/landSurface/topography/merit_dem_processed/version_2021-02-XX/maps_covered_with_zero/dzRel%04d_topography_parameters_30sec_february_2021_global_covered_with_zero.nc

ln -s ${inputDir}/global_30sec/landSurface/topography/merit_dem_processed/version_2021-02-XX/maps_covered_with_zero/dzRel0000_topography_parameters_30sec_february_2021_global_covered_with_zero.nc
ln -s ${inputDir}/global_30sec/landSurface/topography/merit_dem_processed/version_2021-02-XX/maps_covered_with_zero/dzRel0001_topography_parameters_30sec_february_2021_global_covered_with_zero.nc
ln -s ${inputDir}/global_30sec/landSurface/topography/merit_dem_processed/version_2021-02-XX/maps_covered_with_zero/dzRel0005_topography_parameters_30sec_february_2021_global_covered_with_zero.nc
ln -s ${inputDir}/global_30sec/landSurface/topography/merit_dem_processed/version_2021-02-XX/maps_covered_with_zero/dzRel0010_topography_parameters_30sec_february_2021_global_covered_with_zero.nc
ln -s ${inputDir}/global_30sec/landSurface/topography/merit_dem_processed/version_2021-02-XX/maps_covered_with_zero/dzRel0020_topography_parameters_30sec_february_2021_global_covered_with_zero.nc
ln -s ${inputDir}/global_30sec/landSurface/topography/merit_dem_processed/version_2021-02-XX/maps_covered_with_zero/dzRel0030_topography_parameters_30sec_february_2021_global_covered_with_zero.nc
ln -s ${inputDir}/global_30sec/landSurface/topography/merit_dem_processed/version_2021-02-XX/maps_covered_with_zero/dzRel0040_topography_parameters_30sec_february_2021_global_covered_with_zero.nc
ln -s ${inputDir}/global_30sec/landSurface/topography/merit_dem_processed/version_2021-02-XX/maps_covered_with_zero/dzRel0050_topography_parameters_30sec_february_2021_global_covered_with_zero.nc
ln -s ${inputDir}/global_30sec/landSurface/topography/merit_dem_processed/version_2021-02-XX/maps_covered_with_zero/dzRel0060_topography_parameters_30sec_february_2021_global_covered_with_zero.nc
ln -s ${inputDir}/global_30sec/landSurface/topography/merit_dem_processed/version_2021-02-XX/maps_covered_with_zero/dzRel0070_topography_parameters_30sec_february_2021_global_covered_with_zero.nc
ln -s ${inputDir}/global_30sec/landSurface/topography/merit_dem_processed/version_2021-02-XX/maps_covered_with_zero/dzRel0080_topography_parameters_30sec_february_2021_global_covered_with_zero.nc
ln -s ${inputDir}/global_30sec/landSurface/topography/merit_dem_processed/version_2021-02-XX/maps_covered_with_zero/dzRel0090_topography_parameters_30sec_february_2021_global_covered_with_zero.nc
ln -s ${inputDir}/global_30sec/landSurface/topography/merit_dem_processed/version_2021-02-XX/maps_covered_with_zero/dzRel0100_topography_parameters_30sec_february_2021_global_covered_with_zero.nc

ln -s ${inputDir}/global_30min_from_gmd_paper_input/routing/kc_surface_water/cropCoefficientForOpenWater.nc

ln -s ${inputDir}/africa_30sec/routing/surface_water_bodies/version_20200525/lakes_and_reservoirs_30sec_africa_version_may_2020.nc

set +x
