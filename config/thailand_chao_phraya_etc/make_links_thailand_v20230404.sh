
mkdir /scratch/depfg/sutan101/data/pcrglobwb_input_arise/input_for_thailand_30sec_v20240404/
cd    /scratch/depfg/sutan101/data/pcrglobwb_input_arise/input_for_thailand_30sec_v20240404/

INPUT_DIR="/scratch/depfg/sutan101/data/pcrglobwb_input_arise/develop/"

# clone maps
ln -s ${INPUT_DIR}/thailand_30sec/cloneMaps

# meteo
ln -s /scratch/depfg/sutan101/data/isimip_forcing/isimip3a_version_2021-09-XX/copied_on_2021-09-XX/GSWP3-W5E5/merged/w5e5_1979-2019_with_climatology_on_1978 meteo_w5e5/

# initial conditions:
ln -s ${INPUT_DIR}/thailand_30sec/initialConditions

ln -s ${INPUT_DIR}/global_30sec/landSurface/topography/merit_dem_processed/version_2021-02-XX/maps_covered_with_zero/dem_average_topography_parameters_30sec_february_2021_global_covered_with_zero.nc

ln -s ${INPUT_DIR}/global_05min_from_gmd_paper_input/meteo/downscaling_from_30min/uniqueIds_30min.nc
ln -s ${INPUT_DIR}/global_05min_from_gmd_paper_input/meteo/downscaling_from_30min/temperature_slope.nc                                                                     
ln -s ${INPUT_DIR}/global_05min_from_gmd_paper_input/meteo/downscaling_from_30min/precipitation_slope.nc                                                                   
ln -s ${INPUT_DIR}/global_05min_from_gmd_paper_input/meteo/downscaling_from_30min/temperature_correl.nc                                                                     
ln -s ${INPUT_DIR}/global_05min_from_gmd_paper_input/meteo/downscaling_from_30min/precipitation_correl.nc                                                                   
ln -s ${INPUT_DIR}/global_30sec/landSurface/topography/merit_dem_processed/version_2021-02-XX/maps_covered_with_zero/topography_parameters_30sec_february_2021_global_covered_with_zero.nc

ln -s ${INPUT_DIR}/thailand_30sec/landSurface/soil/soilgrids_30sec_v202303XX_sea_india/WHC_average_1_south_east_asian_and_india_etc_30sec.nc
ln -s ${INPUT_DIR}/thailand_30sec/landSurface/soil/soilgrids_30sec_v202303XX_sea_india/WHC_average_2_south_east_asian_and_india_etc_30sec.nc
ln -s ${INPUT_DIR}/thailand_30sec/landSurface/soil/soilgrids_30sec_v202303XX_sea_india/psiAir_average_1_south_east_asian_and_india_etc_30sec.nc
ln -s ${INPUT_DIR}/thailand_30sec/landSurface/soil/soilgrids_30sec_v202303XX_sea_india/psiAir_average_2_south_east_asian_and_india_etc_30sec.nc
ln -s ${INPUT_DIR}/thailand_30sec/landSurface/soil/soilgrids_30sec_v202303XX_sea_india/BCH_average_1_south_east_asian_and_india_etc_30sec.nc
ln -s ${INPUT_DIR}/thailand_30sec/landSurface/soil/soilgrids_30sec_v202303XX_sea_india/BCH_average_2_south_east_asian_and_india_etc_30sec.nc
ln -s ${INPUT_DIR}/thailand_30sec/landSurface/soil/soilgrids_30sec_v202303XX_sea_india/vmcSat_average_1_south_east_asian_and_india_etc_30sec.nc
ln -s ${INPUT_DIR}/thailand_30sec/landSurface/soil/soilgrids_30sec_v202303XX_sea_india/vmcSat_average_2_south_east_asian_and_india_etc_30sec.nc
ln -s ${INPUT_DIR}/thailand_30sec/landSurface/soil/soilgrids_30sec_v202303XX_sea_india/kSat_average_1_south_east_asian_and_india_etc_30sec.nc
ln -s ${INPUT_DIR}/thailand_30sec/landSurface/soil/soilgrids_30sec_v202303XX_sea_india/kSat_average_2_south_east_asian_and_india_etc_30sec.nc

ln -s ${INPUT_DIR}/global_30sec/landSurface/soil/impeded_drainage/global_30sec_impeded_drainage_permafrost_dsmw_correct_lats.nc

ln -s ${INPUT_DIR}/global_30min_from_gmd_paper_input/waterUse/irrigation/irrigation_efficiency/efficiency.nc

ln -s ${INPUT_DIR}/global_05min_from_gmd_paper_input/waterUse/waterDemand/domestic/domestic_water_demand_version_april_2015.nc
ln -s ${INPUT_DIR}/global_05min_from_gmd_paper_input/waterUse/waterDemand/industry/industry_water_demand_version_april_2015.nc
ln -s ${INPUT_DIR}/global_05min_from_gmd_paper_input/waterUse/waterDemand/livestock/livestock_water_demand_version_april_2015.nc

ln -s ${INPUT_DIR}/global_05min_from_gmd_paper_input/waterUse/desalination/desalination_water_version_april_2015.nc

ln -s ${INPUT_DIR}/global_05min_from_gmd_paper_input/waterUse/abstraction_zones/abstraction_zones_60min_05min.nc

ln -s ${INPUT_DIR}/global_05min_from_gmd_paper_input/waterUse/source_partitioning/surface_water_fraction_for_irrigation/AEI_SWFRAC.nc
ln -s ${INPUT_DIR}/global_05min_from_gmd_paper_input/waterUse/source_partitioning/surface_water_fraction_for_irrigation/AEI_QUAL.nc
ln -s ${INPUT_DIR}/global_30min_from_gmd_paper_input/waterUse/source_partitioning/surface_water_fraction_for_non_irrigation/max_city_sw_fraction.nc

ln -s ${INPUT_DIR}/global_30sec/landSurface/landCover/naturalVegetationAndRainFedCrops_version_2021-02-XX/composite-short-n-tall_crop_coefficient.nc
ln -s ${INPUT_DIR}/global_30sec/landSurface/landCover/naturalVegetationAndRainFedCrops_version_2021-02-XX/composite-short-n-tall_intercept_capacity.nc
ln -s ${INPUT_DIR}/global_30sec/landSurface/landCover/naturalVegetationAndRainFedCrops_version_2021-02-XX/composite-short-n-tall_cover_fraction.nc
ln -s ${INPUT_DIR}/global_30sec/landSurface/landCover/naturalVegetationAndRainFedCrops_version_2021-02-XX/rfrac1_all.nc
ln -s ${INPUT_DIR}/global_30sec/landSurface/landCover/naturalVegetationAndRainFedCrops_version_2021-02-XX/rfrac2_all.nc	
ln -s ${INPUT_DIR}/global_30sec/landSurface/landCover/naturalVegetationAndRainFedCrops_version_2021-02-XX/meanrootdepth_all.nc
ln -s ${INPUT_DIR}/global_30sec/landSurface/landCover/irrigated_fractions/global_estimate_irrigation_paddy_fraction_30sec.nc
ln -s ${INPUT_DIR}/global_30min_from_gmd_paper_input/landSurface/landCover/irrPaddy/rfrac1_paddy.nc
ln -s ${INPUT_DIR}/global_30min_from_gmd_paper_input/landSurface/landCover/irrPaddy/rfrac2_paddy.nc
ln -s ${INPUT_DIR}/global_30min_from_gmd_paper_input/landSurface/landCover/irrPaddy/Global_CropCoefficientKc-IrrPaddy_30min.nc
ln -s ${INPUT_DIR}/global_30sec/landSurface/landCover/irrigated_fractions/global_estimate_irrigation_non_paddy_fraction_30sec.nc
ln -s ${INPUT_DIR}/global_30min_from_gmd_paper_input/landSurface/landCover/irrNonPaddy/rfrac1_nonpaddy.nc
ln -s ${INPUT_DIR}/global_30min_from_gmd_paper_input/landSurface/landCover/irrNonPaddy/rfrac2_nonpaddy.nc
ln -s ${INPUT_DIR}/global_30min_from_gmd_paper_input/landSurface/landCover/irrNonPaddy/Global_CropCoefficientKc-IrrNonPaddy_30min.nc
ln -s ${INPUT_DIR}/global_30sec/groundwater/properties/version_202102XX/recession_coefficient_30sec.nc
ln -s ${INPUT_DIR}/global_30sec/groundwater/properties/version_202102XX/k_conductivity_aquifer_filled_30sec.nc
ln -s ${INPUT_DIR}/global_30sec/groundwater/properties/version_202102XX/specific_yield_aquifer_filled_30sec.nc
ln -s ${INPUT_DIR}/global_30sec/groundwater/aquifer_thickness_estimate/version_2020-09-XX/thickness_05min_remapbil_to_30sec_filled_with_pcr_correct_lat.nc
ln -s ${INPUT_DIR}/global_30min_from_gmd_paper_input/waterUse/groundwater_pumping_capacity/regional_abstraction_limit.nc
ln -s ${INPUT_DIR}/global_05min_from_gmd_paper_input/waterUse/abstraction_zones/abstraction_zones_30min_05min.nc
ln -s ${INPUT_DIR}/global_30sec/routing/surface_water_bodies/version_2020-05-XX/lddsound_30sec_version_202005XX_correct_lat.nc
ln -s ${INPUT_DIR}/global_30sec/routing/cell_area/cdo_grid_area_30sec_map_correct_lat.nc
ln -s ${INPUT_DIR}/global_30sec/routing/channel_properties/version_2021-02-XX/maps_covered_with_zero/channel_gradient_channel_parameters_30sec_february_2021_global_covered_with_zero.nc
ln -s ${INPUT_DIR}/global_30sec/routing/channel_properties/version_2021-02-XX/maps_covered_with_zero/bankfull_depth_channel_parameters_30sec_february_2021_global_covered_with_zero.nc
ln -s ${INPUT_DIR}/global_30sec/routing/channel_properties/version_2021-02-XX/maps_covered_with_zero/bankfull_width_channel_parameters_30sec_february_2021_global_covered_with_zero.nc
ln -s ${INPUT_DIR}/global_30sec/routing/channel_properties/version_2021-02-XX/maps_covered_with_zero/bankfull_width_channel_parameters_30sec_february_2021_global_covered_with_zero.nc
ln -s ${INPUT_DIR}/global_30min_from_gmd_paper_input/routing/kc_surface_water/cropCoefficientForOpenWater.nc
ln -s ${INPUT_DIR}/thailand_30sec/routing/surface_water_bodies/south-east-asia_india_version_2023-03-23/lakes_and_reservoirs_30sec_sea_india_version_20230323.nc

#~ global_30sec/landSurface/topography/merit_dem_processed/version_2021-02-XX/maps_covered_with_zero/dzRel%04d_topography_parameters_30sec_february_2021_global_covered_with_zero.nc
DZREL_FOLDER=${INPUT_DIR}/"/global_30sec/landSurface/topography/merit_dem_processed/version_2021-02-XX/maps_covered_with_zero/"
ln -s ${DZREL_FOLDER}/dzRel0000_topography_parameters_30sec_february_2021_global_covered_with_zero.nc
ln -s ${DZREL_FOLDER}/dzRel0001_topography_parameters_30sec_february_2021_global_covered_with_zero.nc
ln -s ${DZREL_FOLDER}/dzRel0005_topography_parameters_30sec_february_2021_global_covered_with_zero.nc
ln -s ${DZREL_FOLDER}/dzRel0010_topography_parameters_30sec_february_2021_global_covered_with_zero.nc
ln -s ${DZREL_FOLDER}/dzRel0020_topography_parameters_30sec_february_2021_global_covered_with_zero.nc
ln -s ${DZREL_FOLDER}/dzRel0030_topography_parameters_30sec_february_2021_global_covered_with_zero.nc
ln -s ${DZREL_FOLDER}/dzRel0040_topography_parameters_30sec_february_2021_global_covered_with_zero.nc
ln -s ${DZREL_FOLDER}/dzRel0050_topography_parameters_30sec_february_2021_global_covered_with_zero.nc
ln -s ${DZREL_FOLDER}/dzRel0060_topography_parameters_30sec_february_2021_global_covered_with_zero.nc
ln -s ${DZREL_FOLDER}/dzRel0070_topography_parameters_30sec_february_2021_global_covered_with_zero.nc
ln -s ${DZREL_FOLDER}/dzRel0080_topography_parameters_30sec_february_2021_global_covered_with_zero.nc
ln -s ${DZREL_FOLDER}/dzRel0090_topography_parameters_30sec_february_2021_global_covered_with_zero.nc
ln -s ${DZREL_FOLDER}/dzRel0100_topography_parameters_30sec_february_2021_global_covered_with_zero.nc


