#!/bin/bash

# List of sensor reading scripts
scripts=('/root/hassio-growbox/sensors/bme280/air-temperature.py' '/root/hassio-growbox/sensors/bme280/air-humidity.py' 
    '/root/hassio-growbox/sensors/bme280/air-pressure.py' '/root/hassio-growbox/sensors/sht20/soil-temperature.py' 
    '/root/hassio-growbox/sensors/sht20/soil-humidity.py'
)

function run_sensor_scripts {
    # Schedule this function to run again in 20 seconds
    (sleep 20 && run_sensor_scripts) &

    # Loop through each script and run it
    for script in "${scripts[@]}"
    do
        /root/hassio-growbox/env/bin/python "$script"
    done
}

# Run the function once to start the loop
run_sensor_scripts
