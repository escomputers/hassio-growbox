import os
import requests
import fcntl
import board
from adafruit_bme280 import basic as adafruit_bme280
import syslog
import time

syslog.openlog(facility=syslog.LOG_LOCAL0)

LLA_TOKEN = os.getenv('TOKEN')

i2c = board.I2C() 
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

# Create a lock file
lock_file = open('../lockfile.lock', 'w')


def sensing():
    # Acquire a lock on the lock file
    fcntl.flock(lock_file, fcntl.LOCK_EX)

    # GET VALUES
    air_temperature = str(round(bme280.temperature, 2))
    air_humidity = str(round(bme280.humidity, 2))
    air_pressure = str(round(bme280.pressure, 2))

    # SEND VALUES
    header = {'Authorization': 'Bearer ' + LLA_TOKEN, 'Content-Type': 'application/json'}
    try:
        requests.post('http://localhost:8123/api/states/sensor.air_temperature', headers=header, json={
            'state': air_temperature,
            'attributes': {
                'unit_of_measurement': '°C'
            }
        })
        time.sleep(5)
        requests.post('http://localhost:8123/api/states/sensor.air_humidity', headers=header, json={
            'state': air_humidity,
            'attributes': {
                'unit_of_measurement': '%'
            }
        })
        time.sleep(5)
        requests.post('http://localhost:8123/api/states/sensor.air_pressure', headers=header, json={
            'state': air_pressure,
            'attributes': {
                'unit_of_measurement': 'mbar'
            }
        })
        #response.raise_for_status()
    except requests.exceptions.RequestException as e:
        syslog.syslog(syslog.LOG_WARNING, str(e))
    finally:
        # Release the lock on the lock file
        fcntl.flock(lock_file, fcntl.LOCK_UN)


sensing()
