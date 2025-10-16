
set -eu


#~ # on snellius
#~ module load 2024 
#~ module load PCRaster/4.4.2-foss-2024a
#~ module load netcdf4-python/1.7.1.post2-foss-2024a
#~ module load LUE/development-foss-2024a

# on eejit
export MODULEPATH=/depfg/easybuild/foss2024a/modules/all/
module load PCRaster/development-foss-2024a
module load netcdf4-python
module load LUE/development-foss-2024a


# Run this script with LUE package in environment. This should work:
# python -c "import lue"

libtcmalloc=$(find $EBROOTGPERFTOOLS -name libtcmalloc_minimal.so.4)

LD_PRELOAD=$libtcmalloc \
LUE_PCRASTER_PROVIDER_NAME=lue \
LUE_PARTITION_SHAPE="9000,8520" \
     python /eejit/home/sutan101/github/edwinkost/PCR-GLOBWB_model/model/deterministic_runner.py /eejit/home/sutan101/github/edwinkost/PCR-GLOBWB_model/config/lue/30sec_africa_test.ini debug \
         --hpx:threads=16
         
