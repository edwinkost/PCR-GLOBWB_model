#!/usr/bin/env bash
#SBATCH --partition=genoa
#SBATCH -N 1
#SBATCH -n 192
#~ #SBATCH -n 1
#~ #SBATCH -c 192
#~ #SBATCH --time=24:00:00
#SBATCH --time=59:00
#SBATCH --job-name test_lue
#~ #SBATCH -o %x_out.txt
#~ #SBATCH -e %x_err.txt

# on snellius

#~ # - if you are not "edwin" you have to set the MODULEPATH as the following (so that you will load LUE etc compiled by "edwin")
#~ export MODULEPATH=/home/edwin/.local/easybuild/RHEL9/2025/modulefiles/all/:$MODULEPATH

#~ # - load NEW LUE etc
#~ module load 2025 
#~ module load PCRaster/development-foss-2025a
#~ module load netcdf4-python/1.7.2-foss-2025a
#~ module load LUE/development-foss-2025a

# - load OLD LUE etc
module load 2024 
module load PCRaster/4.4.2-foss-2024a
module load netcdf4-python/1.7.1.post2-foss-2024a
module load LUE/development-foss-2024a


#~ # Run this script with LUE package in environment. This should work:
#~ python -c "import lue"

libtcmalloc=$(find $EBROOTGPERFTOOLS -name libtcmalloc_minimal.so.4)

LD_PRELOAD=$libtcmalloc \
LUE_PCRASTER_PROVIDER_NAME=lue \
LUE_PARTITION_SHAPE="600,600" \
     python /home/edwin/github/edwinkost/PCR-GLOBWB_model/model/deterministic_runner.py /home/edwin/github/edwinkost/PCR-GLOBWB_model/config/lue/30sec_africa_v2026develop.ini debug \
         --hpx:threads=48

         #~ --hpx:threads=48 \
         #~ --hpx:threads=24 \
         #~ --end

       
