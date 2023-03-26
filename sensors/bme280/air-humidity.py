import os
import requests
import threading
import board
from adafruit_bme280 import basic as adafruit_bme280
import syslog

syslog.openlog(facility=syslog.LOG_LOCAL0)

LLA_TOKEN = os.environ["TOKEN"]

i2c = board.I2C() 
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

def sensing():
    threading.Timer(30.0, sensing).start()

    # GET & SEND AIR HUMIDITY
    air_humidity = str(("%.2f" % round(bme280.humidity, 2)))
    try:
        response = requests.post('http://localhost:8123/api/states/sensor.air_humidity', headers={
            'Authorization': 'Bearer ' + LLA_TOKEN,
            'Content-Type': 'application/json'
        }, json={
            'state': air_humidity,
            'attributes': {
                'unit_of_measurement': '%'
            }
        })
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        syslog.syslog(syslog.LOG_WARNING, str(e))

sensing()
