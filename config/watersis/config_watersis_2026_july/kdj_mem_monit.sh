command="my_command"
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
