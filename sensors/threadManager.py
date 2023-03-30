import os
import threading


# List of sensor reading scripts
scripts = ['bme280.py', 'sht20.py']


def run_sensor_scripts():
    threading.Timer(45.0, run_sensor_scripts).start()

    # Loop through each script and run it while holding the lock
    for script in scripts:
        os.system('/root/hassio-growbox/env/bin/python ' + script)


run_sensor_scripts()
