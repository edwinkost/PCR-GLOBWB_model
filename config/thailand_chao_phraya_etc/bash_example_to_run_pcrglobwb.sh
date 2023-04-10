
# activate the correct conda envinroment
# - to setup this conda environment, please follow the instruction given on the PCR-GLOBWB github site, see e.g. https://github.com/edwinkost/PCR-GLOBWB_model/blob/thailand_30sec_v20230409/README.md#how-to-install
conda activate pcrglobwb_python3

# set the PCR-GLOBWB configuration (.ini) file
# - do not forget to adjust the settings, e.g. inputDir, outputDir, cloneMap, etc. 
CONFIG_INI_FILE="/home/edwin/github/edwinkost/PCR-GLOBWB_model/config/thailand_chao_phraya_etc/setup_30sec_thailand_v20230409.ini

# go to the folder that contains PCR-GLOBWB scripts
cd /home/edwin/github/edwinkost/PCR-GLOBWB_model/model/

# run the model
python deterministic_runner.py ${CONFIG_INI_FILE} debug

