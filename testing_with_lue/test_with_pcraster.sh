#~ Hi Edwin,

#~ Here are the two scripts I use to run the model with either PCRaster or
#~ LUE. You can use them as inspiration for your own runs.

#~ Setting LD_PRELOAD is required, otherwise a LUE model will likely crash
#~ upon exit. I asked Oliver to see whether loading the LUE EasyBuild
#~ module could set the variable as a side-effect. Once that is done, we
#~ don't have to set it anymore. You can test this by "echo $LD_PRELOAD".

#~ Here's what I would do if I where you:
#~ 1. Look at the changes which I made so you know what the differences are
#~ 2. Run the model with PCRaster. Store the results in a directory.
#~ 3. Run the model with LUE. Store the results in another directory.
#~ 4. Look at the differences between the LUE and PCRaster outputs. Figure
#~ out why some rasters are different. I will fix any issue with LUE of course.

#~ I will send you a script which I used to compare results between
#~ PCRaster and LUE outputs.

#~ Let me know if things don't work and I will fix 'm.

#~ Kor



set -eu

# Run this script with PCRaster package in environment. This should work:
# python -c "import pcraster, lue.framework.pcraster_provider"

output_dir="/scratch/sutan101/pgb_test_with_lue/pcraster/"
ini_in="../config/lue/setup_30min_on_velocity_for_lue.ini"

rm -fr $output_dir

LUE_PCRASTER_PROVIDER_NAME=pcraster \
     python ../model/deterministic_runner.py $ini_in

