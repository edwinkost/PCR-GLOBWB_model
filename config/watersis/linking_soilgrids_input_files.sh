
TARGET_DIR="/scratch/depfg/sutan101/pcrglobwb_input_watersis/develop/global_6min/soilgrids_6min_ulysses_v202311XX/"
cd ${TARGET_DIR}

SOURCE_DIR="/scratch/depfg/sutan101/pcrglobwb_input_ulysses_v202312XX/develop_edwin/"

#~ ln -s ${SOURCE_DIR}/layerDepth_average_1_global_06min.nc
#~ ln -s ${SOURCE_DIR}/layerDepth_average_2_global_06min.nc
ln -s ${SOURCE_DIR}/WHC_average_1_global_06min.nc
ln -s ${SOURCE_DIR}/WHC_average_2_global_06min.nc
#~ ln -s ${SOURCE_DIR}/psiAir_average_1_global_06min.nc
#~ ln -s ${SOURCE_DIR}/psiAir_average_2_global_06min.nc
ln -s ${SOURCE_DIR}/BCH_average_1_global_06min.nc
ln -s ${SOURCE_DIR}/BCH_average_2_global_06min.nc
#~ ln -s ${SOURCE_DIR}/vmcRes_average_1_global_06min.nc
#~ ln -s ${SOURCE_DIR}/vmcRes_average_2_global_06min.nc
ln -s ${SOURCE_DIR}/vmcSat_average_1_global_06min.nc
ln -s ${SOURCE_DIR}/vmcSat_average_2_global_06min.nc
ln -s ${SOURCE_DIR}/kSat_average_1_global_06min.nc
ln -s ${SOURCE_DIR}/kSat_average_2_global_06min.nc

