import os
import requests
import threading
import board
from adafruit_bme280 import basic as adafruit_bme280

LLA_TOKEN = os.environ["TOKEN"]

i2c = board.I2C() 
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

def sensing():
    threading.Timer(30.0, sensing).start()

    # GET & SEND AIR PRESSURE
    air_pressure = str(("%.2f" % round(bme280.pressure, 2)))
    requests.post('http://localhost:8123/api/states/sensor.air_pressure', headers={
        'Authorization': 'Bearer ' + LLA_TOKEN,
        'Content-Type': 'application/json'
    }, json={
        'state': air_pressure,
        'attributes': {
            'unit_of_measurement': '°C'
        }
    })