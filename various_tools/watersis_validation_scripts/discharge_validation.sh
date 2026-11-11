#!/bin/bash
  
#SBATCH --job-name=validate
#SBATCH --qos=nf
##SBATCH --account=     # adjust
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem-per-cpu=15G
#SBATCH --time=06:00:00
#SBATCH --output=%x.%j.out
#SBATCH --error=%x.%j.err

set -x

#~ MODEL_OUTPUT_DIR=YOUR_PATH #/lus/h1resw01/project/C3SHydroGL.addendum/europe/reanalysis/experiment/era5_v4/ecland/output/mem_00/
#~ EVALUATION_OUTPUT_DIR=/scratch/$USER/validation_europe/discharge2
#~ START_YEAR=1980 # 1985 if you want to skip the first 5 years of spinup
#~ EVALUATION_OUTPUT_DIR=/scratch/$USER/validation_europe/discharge/

MODEL_OUTPUT_DIR="/scratch/cyes/c3s_hydro_reanalysis_run_europe/final_output/reanalysis/experiment/era5_v0/pcr_globwb/output/mem_00/"
EVALUATION_OUTPUT_DIR=/scratch/cyes/validation_europe/discharge/

START_YEAR=1990

NCPUS=8

cd $MODEL_OUTPUT_DIR
ml python3
export PYTHONPATH=/lus/h2resw01/fws4/sb/project/C3SHydroGL/phase_3/global/exchange/model_validation_scripts/mhm_tools_env_eval/src/
time python3 -m mhm_tools._cli evaluation discharge-evaluation --observed-data-path /lus/h2resw01/fws4/sb/project/C3SHydroGL/phase_3/global/validation_data/streamflow/grdc/grdc_daily_1970_2025.nc --model-data-path .  --output-dir $EVALUATION_OUTPUT_DIR --model-file-name  rdis_ecland_era5_mem_00*.nc --gauge-coordinate-file /lus/h1resw01/project/C3SHydroGL.addendum/europe/exchange/model_validation_scripts/scc_gauges_epsg3035.nc --gauge-optimization-method nearest --ncpus=$NCPUS --start-date $START_YEAR --shape-dir /lus/h2resw01/fws4/sb/project/C3SHydroGL/phase_3/global/exchange/model_validation_scripts/shapefiles_merit_burek2023 

# flag for hydrograph --hydrograph-plots

echo "Done!"
