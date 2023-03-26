import os
import requests
import threading
import board
from adafruit_bme280 import basic as adafruit_bme280
import syslog
import datetime

syslog.openlog(facility=syslog.LOG_LOCAL0)

LLA_TOKEN = os.environ["TOKEN"]

i2c = board.I2C() 
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

def sensing():
    threading.Timer(30.0, sensing).start()

    # GET & SEND AIR TEMPERATURE
    air_temperature = str(("%.2f" % round(bme280.temperature, 2)))
    try:
        requests.post('http://localhost:8123/api/states/sensor.air_temperature', headers={
            'Authorization': 'Bearer ' + LLA_TOKEN,
            'Content-Type': 'application/json'
        }, json={
            'state': air_temperature,
            'attributes': {
                'unit_of_measurement': '°C'
            }
        })
    except ConnectionError:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        syslog.syslog(syslog.LOG_WARNING, '[' + timestamp + ']' + '[WARNING HASSIO REST API for BME280-AIRTEMP] Cannot send sensor data to Home Assistant REST endpoint.')

sensing()
