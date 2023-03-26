import os
import requests
import threading
from sensor import SHT20
import syslog

syslog.openlog(facility=syslog.LOG_LOCAL0)

LLA_TOKEN = os.getenv("TOKEN")

sht = SHT20(1, 0x40)

def sensing():
    threading.Timer(30.0, sensing).start()

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

sensing()
