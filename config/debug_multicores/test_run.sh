
module load foss2025a
module load PCRaster/4.4.3-foss-2025a

PCRGLOBWB_RUNNER="../../../model/deterministic_runner_ulysses.py"
PCRGLOBWB_CONFIG="setup_rhine_meuse_30min_using_input_example.ini"
PCRGLOBWB_OUTPUT_FOLDER="/scratch/sutan101/test_debug_multicores/"

export PCRASTER_NR_WORKER_THREADS=4
python ${PCRGLOBWB_RUNNER} ${PCRGLOBWB_CONFIG} debug -mod ${PCRGLOBWB_OUTPUT_FOLDER}
