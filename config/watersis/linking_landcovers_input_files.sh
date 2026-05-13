
TARGET_DIR="/scratch/depfg/sutan101/pcrglobwb_input_watersis/develop/global_6min/landcovers_v2023-11-XX/"
cd ${TARGET_DIR}

SOURCE_DIR="/scratch/depfg/sutan101/pcrglobwb_input_ulysses_v202312XX/develop_edwin/"

ln -s ${SOURCE_DIR}/tall_crop_coefficient.nc
ln -s ${SOURCE_DIR}/tall_cover_fraction.nc
ln -s ${SOURCE_DIR}/tall_intercept_capacity.nc
ln -s ${SOURCE_DIR}/vegf_tall.map
ln -s ${SOURCE_DIR}/minf_tall.map
ln -s ${SOURCE_DIR}/maxf_tall.map
ln -s ${SOURCE_DIR}/rfrac1_tall.map
ln -s ${SOURCE_DIR}/rfrac2_tall.map
#~ ln -s ${SOURCE_DIR}/maxrootdepth_tall.map
ln -s ${SOURCE_DIR}/short_crop_coefficient.nc
ln -s ${SOURCE_DIR}/short_cover_fraction.nc
ln -s ${SOURCE_DIR}/short_intercept_capacity.nc
ln -s ${SOURCE_DIR}/vegf_short.map
ln -s ${SOURCE_DIR}/minf_short.map
ln -s ${SOURCE_DIR}/maxf_short.map
ln -s ${SOURCE_DIR}/rfrac1_short.map
ln -s ${SOURCE_DIR}/rfrac2_short.map
#~ ln -s ${SOURCE_DIR}/maxrootdepth_short.map


#~ fracVegCover      = landcovers_v2023-11-XX/
#~ minSoilDepthFrac  = landcovers_v2023-11-XX/
#~ maxSoilDepthFrac  = landcovers_v2023-11-XX/
#~ rootFraction1     = landcovers_v2023-11-XX/
#~ rootFraction2     = landcovers_v2023-11-XX/
#~ maxRootDepth      = 0.5

#~ cropCoefficientNC = landcovers_v2023-11-XX/
#~ coverFractionNC   = landcovers_v2023-11-XX/
#~ interceptCapNC    = landcovers_v2023-11-XX/
