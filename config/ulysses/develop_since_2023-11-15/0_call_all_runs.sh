#!/bin/bash

set -x

bash complete_job_scripts_for_a_run_simplified_recessionCoef.sh "reccf5.00" "0.69897000433"
bash complete_job_scripts_for_a_run_simplified_recessionCoef.sh "reccf10.0" "1.0"
bash complete_job_scripts_for_a_run_simplified_recessionCoef.sh "reccf50.0" "1.69897000434"
bash complete_job_scripts_for_a_run_simplified_recessionCoef.sh "reccfsqrt" "SQUARE_ROOT"

set +x
