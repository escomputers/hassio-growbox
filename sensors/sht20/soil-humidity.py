import os
import requests
import fcntl
from sensor import SHT20
import syslog


syslog.openlog(facility=syslog.LOG_LOCAL0)

LLA_TOKEN = os.environ.get('TOKEN')

sht = SHT20(1, 0x40)

# Create a lock file
lock_file = open('../lockfile.lock', 'w')


def sensing():
    # Acquire a lock on the lock file
    fcntl.flock(lock_file, fcntl.LOCK_EX)

    # GET & SEND SOIL HUMIDITY
    h = sht.humidity()
    soil_humidity = str(("%.2f" % round(h.RH, 2)))
    try:
        response = requests.post('http://localhost:8123/api/states/sensor.soil_humidity', headers={
            'Authorization': 'Bearer ' + LLA_TOKEN,
            'Content-Type': 'application/json'
        }, json={
            'state': soil_humidity,
            'attributes': {
                'unit_of_measurement': '%'
            }
        })
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        syslog.syslog(syslog.LOG_WARNING, str(e))
    finally:
        # Release the lock on the lock file
        fcntl.flock(lock_file, fcntl.LOCK_UN)

sensing()
