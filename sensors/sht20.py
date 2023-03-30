import os
import requests
import fcntl
from sensor import SHT20
import syslog
import time

syslog.openlog(facility=syslog.LOG_LOCAL0)

LLA_TOKEN = os.getenv('TOKEN')

sht = SHT20(1, 0x40)

# Create a lock file
lock_file = open('../lockfile.lock', 'w')


def sensing():
    # Acquire a lock on the lock file
    fcntl.flock(lock_file, fcntl.LOCK_EX)

    # GET VALUES
    t = sht.temperature()
    soil_temperature = str(round(t.C, 2))

    h = sht.humidity()
    soil_humidity = str(round(h.RH, 2))

    # SEND VALUES
    header = {'Authorization': 'Bearer ' + LLA_TOKEN, 'Content-Type': 'application/json'}
    try:
        requests.post('http://localhost:8123/api/states/sensor.soil_temperature', headers=header, json={
            'state': soil_temperature,
            'attributes': {
                'unit_of_measurement': '°C'
            }
        })
        time.sleep(5)
        requests.post('http://localhost:8123/api/states/sensor.soil_humidity', headers=header, json={
            'state': soil_humidity,
            'attributes': {
                'unit_of_measurement': '%'
            }
        })
        #response.raise_for_status()
    except requests.exceptions.RequestException as e:
        syslog.syslog(syslog.LOG_WARNING, str(e))
    finally:
        # Release the lock on the lock file
        fcntl.flock(lock_file, fcntl.LOCK_UN)


sensing()
