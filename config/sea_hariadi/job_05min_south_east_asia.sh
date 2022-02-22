#!/bin/bash

# using 32 cores in 1 thin/normal node (1 normal node consists of 128 cores)
#SBATCH -N 1
#SBATCH -n 32
#SBATCH -p thin

# wall clock time
#SBATCH -t 119:59:00

# job name
#SBATCH -J sea-demo

# mail alert at start, end and abortion of execution
#SBATCH --mail-type=ALL

# send mail to this address - DON'T FORGET TO CHANGE THIS
#SBATCH --mail-user=hsutanudjajacchms99@yahoo.com



set -x

# load all software
. /home/edwin/load_all_default.sh

#~ # test pcraster
#~ pcrcalc

# using 16 cores (optional)
export PCRASTER_NR_WORKER_THREADS=16

# configuration (.ini) file
INI_FILE=/home/edwin/github/edwinkost/PCR-GLOBWB_model/config/sea_hariadi/setup_05min_south_east_asia.ini

# go to the folder that contains your pcrglobwb model scripts
cd /home/edwin/github/edwinkost/PCR-GLOBWB_model/model/

# run 
python deterministic_runner_with_arguments.py ${INI_FILE} debug

echo "end of model runs (please check your results)"

set +x

