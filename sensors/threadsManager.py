import os
import threading


def run_sensor_scripts():
    threading.Timer(20.0, run_sensor_scripts).start()

    # List of sensor reading scripts
    scripts = ['sensors/bme280/air-temperature.py', 'sensors/bme280/air-humidity.py', 
		'sensors/bme280/air-pressure.py', 'sensors/sht20/soil-temperature.py', 
		'sensors/sht20/soil-humidity.py'
	]
    
    # Loop through each script and run it while holding the lock
    for script in scripts:
        os.system('python ' + script)

run_sensor_scripts()
