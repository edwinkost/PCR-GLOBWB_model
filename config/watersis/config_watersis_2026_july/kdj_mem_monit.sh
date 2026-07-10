
command="my_command"

command="python3 deterministic_runner_ulysses.py ../config/watersis/config_watersis_2026_july/setup_6min_global_watersis_nopar_develop.ini debug -mod /lus/h2resw01/fws4/sb/project/C3SHydroGL/edwin/test_global_6min/ -mid /ec/fws4/sb/project/C3SHydroGL/edwin/data/pcrglobwb_input_watersis/develop/global_6min/ -sd 2000-01-01 -ed 2000-01-31 -noyfsu 1 -pff /ec/fws4/sb/project/C3SHydroGL/edwin/data/watersis_forcing/global/v20260514/global_pre_0p1_v20260514.nc -tff /ec/fws4/sb/project/C3SHydroGL/edwin/data/watersis_forcing/global/v20260514/global_tas_day_0p1_v20260514.nc -rpetff /ec/fws4/sb/project/C3SHydroGL/edwin/data/watersis_forcing/global/v20260514/global_pet_hargreaves_samani_0p1_v20260514.nc -misf dummy_initial_conditions/ -dfis 1999-12-31 -end"

command="bash pcrglobwb_run_test.sh"

sleep_duration=5 # Seconds

while true; do
    if process_id=$(pgrep -u "$USER" -f "$command"); then
        duration=$SECONDS
        time_stamp=$duration

        # power: 0 -> kibibyte
        # power: 1 -> mebibyte
        # power: 2 -> gibibyte
        power=2
        memory_usage=$(grep -e '^Pss' "/proc/$process_id/smaps" | awk "{sum += \$2} END {print sum / 1024**${power}}")

        # Time in seconds, usage in kibibytes / 1024**$power bytes
        echo "$time_stamp $memory_usage"
    else
        SECONDS=0
    fi
    sleep $sleep_duration                                                                                                                                                                                       
done                
