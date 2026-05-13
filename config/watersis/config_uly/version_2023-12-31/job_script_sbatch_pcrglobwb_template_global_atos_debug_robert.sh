#!/bin/bash

#SBATCH --qos=nf
#SBATCH --job-name=pcrglobwb_ulysses

#SBATCH --mem-per-cpu=1250MB
#SBATCH --ntasks=32
#SBATCH --cpus-per-task=1
#SBATCH --threads-per-core=2

#SBATCH --time=04:00:00

# budget account - provided by Robert Jan 2024
#SBATCH --account=c3s24101


module load python3/3.10.10-01 
module load pcraster/4.4.0-01 
module load gdal/3.6.2

export OMP_NUM_THREADS=32
export PCRASTER_NR_WORKER_THREADS=32

MAIN_OUTPUT_DIRECTORY="/ec/fws4/sb/project/C3SHydroGL/edwin/pcrglobwb_ulysses_v2023-12-31_test_output/debug_robert/"

python3 /home/cyes/gitlab/ulysses/ulysses_pgb_source/model/deterministic_runner_ulysses.py /home/cyes/gitlab/ulysses/ulysses_pgb_source/config/ulysses/version_2023-12-31/pgb_config_robert.ini debug -mod ${MAIN_OUTPUT_DIRECTORY}
