set -eu

# on snellius

# - if you are not "edwin" you have to set the MODULEPATH as the following (so that you will load LUE etc compiled by "edwin")
export MODULEPATH=/home/edwin/.local/easybuild/RHEL9/2025/modulefiles/all/:$MODULEPATH

# - load LUE etc
module load 2025 
module load PCRaster/development-foss-2025a
module load netcdf4-python/1.7.2-foss-2025a
module load LUE/development-foss-2025a

# Run this script with LUE package in environment. This should work:
python -c "import lue"

libtcmalloc=$(find $EBROOTGPERFTOOLS -name libtcmalloc_minimal.so.4)

LD_PRELOAD=$libtcmalloc \
LUE_PCRASTER_PROVIDER_NAME=lue \
LUE_PARTITION_SHAPE="600,600" \
     python /home/edwin/github/edwinkost/PCR-GLOBWB_model/model/deterministic_runner.py /home/edwin/github/edwinkost/PCR-GLOBWB_model/config/lue/30sec_africa_v2026develop.ini debug \
         --hpx:threads=16
