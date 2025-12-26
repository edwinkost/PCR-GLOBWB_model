set -eu

# on snellius
export MODULEPATH=/home/edwin/.local/easybuild/RHEL9/2024/modulefiles/all/:$MODULEPATH
module load 2024 
module load PCRaster/4.4.2-foss-2024a
module load netcdf4-python/1.7.1.post2-foss-2024a
module load LUE/development-foss-2024a

# Run this script with LUE package in environment. This should work:
# python -c "import lue"

libtcmalloc=$(find $EBROOTGPERFTOOLS -name libtcmalloc_minimal.so.4)

#~ LD_PRELOAD=$libtcmalloc \
#~ LUE_PCRASTER_PROVIDER_NAME=lue \
#~ LUE_PARTITION_SHAPE="600,600" \
     #~ python /home/hydrowld/github/edwinkost/PCR-GLOBWB_model/model/deterministic_runner.py /home/hydrowld/github/edwinkost/PCR-GLOBWB_model/config/lue/30sec_africa_vdevelop.ini debug \
         #~ --hpx:threads=96

LD_PRELOAD=$libtcmalloc \
LUE_PCRASTER_PROVIDER_NAME=lue \
LUE_PARTITION_SHAPE="600,600" \
     python /home/hydrowld/github/edwinkost/PCR-GLOBWB_model/model/deterministic_runner.py /home/hydrowld/github/edwinkost/PCR-GLOBWB_model/config/lue/30sec_africa_vdevelop.ini \
         --hpx:threads=96
