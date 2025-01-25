Home Assistant as growbox controller, using several different devices and sensors, connected via D1 Mini/ESP8266-12-e

## Home Assistant setup

### Install
1. Install Home Assistant Core

```bash
# Install system requirements
sudo apt update && sudo apt install python3-dev python3-venv python3-pip bluez libffi-dev libssl-dev libjpeg-dev zlib1g-dev autoconf build-essential libopenjp2-7 libtiff6 libturbojpeg0-dev tzdata ffmpeg liblapack3 liblapack-dev libatlas-base-dev cmake -y

# Required only when using a MySQL database
sudo apt install default-libmysqlclient-dev pkg-config -y

# Required only when using a MariaDB database
sudo apt install libmariadbclient-dev-compat -y

# Optional: install a specific Python version (script works only on Unix-like hosts)
sudo bash utils/install-python.sh 3.11.0

# Create homeassistant system account along with its own home directory
sudo useradd -rm homeassistant

# Create Python environment
sudo mkdir /srv/homeassistant
sudo chown homeassistant:homeassistant /srv/homeassistant
sudo chown -R homeassistant:homeassistant /home/homeassistant
sudo -u homeassistant -H -s  # change to homeassistant user
python -m venv /srv/homeassistant
source /srv/homeassistant/bin/activate
python -m pip install wheel

# Required only when using a MySQL/MariaDB database
python -m pip install mysqlclient pymysql

# Install HomeAssistant
python -m pip install git+https://github.com/home-assistant/core.git

# Run as system service
sudo cp ha@homeassistant.service /etc/systemd/system/
sudo systemctl enable ha@homeassistant.service
sudo systemctl daemon-reload
sudo systemctl start ha@homeassistant.service
```

### Restore backup (optional)

1. Copy the backup .tar file to the target host, uncompress it and copy it to HomeAssistant configuration directory
```bash
tar xf backupfile.tar && tar xf homeassistant.tar.gz
sudo rsync -a data/ /home/homeassistant/.homeassistant/
```

2. Connect esp8266 to your PC using USB cable (buy one with serial converter integrated) and install ESPHome Device builder:

- https://esphome.io/guides/getting_started_command_line#bonus-esphome-device-builder
- https://esphome.io/guides/getting_started_hassio.html#installing-esphome-device-builder

3. Install the ESPHome integration


### Configure
[homeassistant-configuration directory](homeassistant-configuration/configuration.yaml) contains configuration for controlling USB relay board, using [RESTful Binary Sensor](https://www.home-assistant.io/integrations/binary_sensor.rest).\
To get it working, an API service must be started within raspbian OS and it allows you to install Home Assistant into a different host.\
Link to the repo: [usbAPI](https://github.com/escomputers/usbAPI)\
If you don't want to use a USB relay board, you could use a WIFI relay board like [this](https://denkovi.com/wifi-16-relay-board-modBus-tcp) and thus you can skip all the steps related to USB-API relay board management.

Here's the [example scripts.yaml file](homeassistant-configuration/scripts.yaml) containing the scripts used for controlling relay board via API


Here's the [example YAML](homeassistant-configuration/.storage/lovelace) for dashboard setup (cards and tiles)

---

## ESPHome installation
1. Install ESPHome into your virtual environment

```bash
python -m pip -r requirements.txt
```

2. Connect esp8266 to your PC using USB cable (buy esp8266 with serial converter integrated)

3. Edit esphome-configuration/secrets.yaml to reflect your current wifi network

4. Move esphome-configuration/secrets.yaml and esphome-configuration/sht20.h (only if you use it, otherwise it's not required) to .esphome directory

```
mv esphome-configuration/secrets.yaml esphome-configuration/sht20.h .esphome
```

5. The first time you connect to esp8266 (via usb to serial cable), you need to tell esphome some information about
your esp8266 device. Right after that, it will validate the configuration, create a binary, upload it, and start logs

```bash
cd .esphome && esphome wizard esphome-config.yaml
```

Next time you need to configure it, just connect to the same esp8266 network and launch commands over the air:

```bash
esphome run esphome-configuration/esphome-config.yaml
```

6. Read all the output and check for sensors errors, if clear come back to Home Assistant installation steps

---

## DEVICES

### Main controller
[D1 Mini](https://www.az-delivery.de/en/products/d1-mini) - [pinout](https://m.media-amazon.com/images/I/71b9yM7dFlL.jpg)\
[USB to serial converter](https://www.az-delivery.de/en/products/usb-auf-seriell-adapter-mit-ch340)

### Relay Board
[Denkovi USB 8 Channel](https://denkovi.com/usb-eight-channel-relay-board-for-automation) - [wiring](https://github.com/escomputers/hassio-growbox/blob/325ab9b5c127c14f19560fe0ca1c8efceda2f83e/wirings/12V-USB-8CH-relay-board-wiring.pdf)

| DEVICE     | RPI4 |
| ----------- | ---------- |
| USB-B       | USB           |

### PWM Controller
[Universal AC MAINS Dimmer - MPDMv4.1](https://www.tindie.com/products/next_evo1/universal-ac-mains-dimmer-mpdmv41/)\
used for controlling 5 fans (4 oscillating + 1 inline)
| PWM board   | ESP8266 |
| ----------- | ---------- |
| VCC         | 3V3        |
| GND         | GND        |
| VCNT        | GPIO15/D8        |


## Sensors
[D1-MINI/ESP8266 sensors wiring](https://github.com/escomputers/hassio-growbox/blob/325ab9b5c127c14f19560fe0ca1c8efceda2f83e/wirings/d1mini-esp8266-sensors-wiring.pdf)

### Air

[BME280](https://www.adafruit.com/product/2652) Temperature + Humidity + Pressure (i2c bus)
| SENSOR      | ESP8266 |
| ----------- | ---------- |
| VIN         | 3V3        |
| GND         | GND        |
| SCK         | SCL/GPIO5/D1        |
| SDO         | SDA/GPIO4/D2        |


### Soil

[SHT20](https://www.makerfabs.com/soil-temperature-and-humidity-sensor-sht20.html) Temperature + Humidity (i2c bus)
| SENSOR      | ESP8266 |
| ----------- | ---------- |
| RED         | 3V3        |
| BLACK       | GND        |
| GREEN       | SDA/GPIO4/D2        |
| YELLOW      | SCL/GPIO5/D1         |


### CO2

[MH-Z19C NDIR](https://www.winsen-sensor.com/product/mh-z19c.html) (UART bus - 7pin terminal connection version)
| SENSOR      | ESP8266 |
| ----------- | ---------- |
| PIN4 VIN    | 5V        |
| PIN3 GND    | GND        |
| PIN5 RX     | TX/GPIO1/D10        |
| PIN6 TX     | RX/GPIO3/D9        |

---

## POWER

| DEVICE     | REQUIRED POWER SOURCES |
| ----------- | ---------- |
| Denkovi USB 8CH relay board       | 12V 1A + 220V|
| Esp8266                           | 5V/3.3V 1A |
| Raspberry Pi 4                    | 5V 2A|
| Raspberry Pi 4 Fan                | 9V 1A|
| Power sockets                     | 220V 16A (1,5mm<sup>2</sup> cables)|


---

## 3D CASES

Take a look at [3D directory](3D/)\
References:
- Raspberry Pi 4 case (40mm fan) by John_Sinclair on [Thingiverse](https://www.thingiverse.com/thing:3723481)
- 12V USB 8 Channel relay board by polysquare on [Thingverse](https://www.thingiverse.com/thing:2306082)
- BME280 case by leptitnicolas on [Thingverse](https://www.thingiverse.com/thing:3809818)
- Arduino nano + 2 channel arduino relay + voltage stepdown box by flying_ginger on [Thingverse](https://www.thingiverse.com/thing:3162083). Used for housing ESP8266 (by making a drawer/slot manually since screw holes aren't available on the board), MH-Z19, cables and as attach surface for placing BME280 externally.

---
