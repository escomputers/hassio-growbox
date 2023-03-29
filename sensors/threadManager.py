import os
import threading


# os.chdir('/root/hassio-growbox/sensors')

# List of sensor reading scripts
scripts = ['bme280/air-temperature.py', 'bme280/air-humidity.py', 
    'bme280/air-pressure.py', 'sht20/soil-temperature.py', 
    'sht20/soil-humidity.py'
]


def run_sensor_scripts():
    threading.Timer(45.0, run_sensor_scripts).start()

    # Loop through each script and run it while holding the lock
    for script in scripts:
        os.system('/root/hassio-growbox/env/bin/python ' + script)


run_sensor_scripts()