
module load foss2025a
module load PCRaster/4.4.3-foss-2025a
module load netcdf4-python/1.7.2-foss-2025a

#~ . /home/sutan101/load_all_default.sh


PCRGLOBWB_RUNNER="/scratch/sutan101/debug_multicores/PCR-GLOBWB_model/model/deterministic_runner_ulysses.py"

# Configuration file
# - Rhine Meuse 50km
#~ PCRGLOBWB_CONFIG="/scratch/sutan101/debug_multicores/PCR-GLOBWB_model/config/debug_multicores/setup_rhine_meuse_30min_using_input_example.ini"
# - Global 10km
PCRGLOBWB_CONFIG="/scratch/sutan101/debug_multicores/PCR-GLOBWB_model/config/debug_multicores/setup_05min.ini"


# Please make sure that you have the write permission to the following folder.
PCRGLOBWB_OUTPUT_FOLDER="/scratch/sutan101/test_debug_multicores/"


export PCRASTER_NR_WORKER_THREADS=4
python ${PCRGLOBWB_RUNNER} ${PCRGLOBWB_CONFIG} debug -mod ${PCRGLOBWB_OUTPUT_FOLDER}
