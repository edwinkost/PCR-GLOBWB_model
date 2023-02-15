#!/bin/bash

#SBATCH -p debug

#SBATCH -A crpmdl
# #SBATCH --qos=m100_qos_dbg

#SBATCH --job-name=pcrglobwb_Arise

#SBATCH --output="%x_%j.out"
#SBATCH --error="%x_%j.err"

#SBATCH --nodes=1
#SBATCH --ntasks=12

#SBATCH --time=480:00:00



# load conda, etc
conda activate XXX

# unset PCRASTER_NR_WORKER_THREADS (this should be the same as --ntasks)
export PCRASTER_NR_WORKER_THREADS=12

# set the folder that contain PCR-GLOBWB model scripts (note that this is not always the latest version)
PCRGLOBWB_MODEL_SCRIPT_FOLDER="/tank/edwin/pcrglobwb_model/model/"
# - go there
cd ${PCRGLOBWB_MODEL_SCRIPT_FOLDER} 

# set the configuration file that we want to run
PCRGLOBWB_CONFIG_FILE=""

# running pcrglobbw
python deterministic_runner.py ${PCRGLOBWB_CONFIG_FILE}
