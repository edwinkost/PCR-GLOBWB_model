#!/bin/bash

#SBATCH -p sen2agri*

#SBATCH -A crpmdl
# #SBATCH --qos=m100_qos_dbg

#SBATCH --job-name=pcrglobwb_Arise

#SBATCH --output="%x_%j.out"
#SBATCH --error="%x_%j.err"

#SBATCH --nodes=1
#SBATCH --ntasks=12

#SBATCH --time=480:00:00



# load conda, etc
# - abandon any existing PYTHONPATH (recommended, if you want to use miniconda or anaconda)
unset PYTHONPATH
# - activate my default conda env
source activate /home/edwinsutanudjaja/opt/miniconda3/envs/pcrglobwb_python3


# unset PCRASTER_NR_WORKER_THREADS (this should be the same as --ntasks)
export PCRASTER_NR_WORKER_THREADS=12


# set the folder that contain PCR-GLOBWB model scripts (note that this is not always the latest version)
PCRGLOBWB_MODEL_SCRIPT_FOLDER="/tank/edwin/github/PCR-GLOBWB_model/model/"
# - go there
cd ${PCRGLOBWB_MODEL_SCRIPT_FOLDER} 


# set the configuration file that we want to run
PCRGLOBWB_CONFIG_FILE="/tank/edwin/github/PCR-GLOBWB_model/config/30sec_african_countries/arise_2023/setup_30sec_agmip_clone_01_version_2021-10-20_on_poly-server.ini"


# running pcrglobwb
python deterministic_runner.py ${PCRGLOBWB_CONFIG_FILE}
