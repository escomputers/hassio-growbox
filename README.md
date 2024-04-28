Home Assistant as growbox controller, using several different devices and sensors, connected via D1 Mini/ESP8266-12-e

## Home Assistant setup

1. Install Home Assistant as container

```
docker compose up -d
```

If you need Docker run for RaspiOS:

```
sudo bash utils/install-docker.sh
```

2. Run the steps for ESPHome installation, when completed run step 3

3. Install the ESPHome integration and in the "host" field, put your esp8266 ip address

---

## ESPHome installation

1. Install Python (Linux hosts only), you can install a specific version by running:

```
sudo bash utils/install-python.sh 3.11.0
```

2. Install pip and venv

```
sudo apt-get install python3-pip python3-venv -y
```

3. Clone repository and activate virtual environment
```
mkdir -p env
python -m venv env/
```

4. Install ESPHome and other requirements

```
python -m pip -r requirements.txt
```

5. Connect esp8266 to your PC using USB cable (buy esp8266 with serial converter integrated)

6. Edit esphome-configuration/secrets.yaml to reflect your current wifi network

7. Move esphome-configuration/secrets.yaml and esphome-configuration/sht20.h (only if you use it, otherwise it's not required) to .esphome directory

```
mv esphome-configuration/secrets.yaml esphome-configuration/sht20.h .esphome
```

8. The first time you connect to esp8266 (via usb to serial cable), you need to tell esphome some information about
your esp8266 device. Right after that, it will validate the configuration, create a binary, upload it, and start logs

```
cd .esphome && esphome wizard esphome-config.yaml
```

Next time you need to configure it, just connect to the same esp8266 network and launch commands over the air:

```
esphome run esphome-configuration/esphome-config.yaml
```

9. Read all the output and check for sensors errors, if clear come back to Home Assistant installation steps

---

## HOME ASSISTANT CONFIGURATION

[homeassistant-configuration directory](homeassistant-configuration/configuration.yaml) contains configuration for controlling USB relay board, using [RESTful Binary Sensor](https://www.home-assistant.io/integrations/binary_sensor.rest).\
To get it working, an API service must be started within raspbian OS and it allows you to install Home Assistant into a different host.\
Link to the repo: [usbAPI](https://github.com/escomputers/usbAPI)

Here's the [example scripts.yaml file](homeassistant-configuration/scripts.yaml) containing the scripts used for controlling relay board via API


Here's the [example YAML](homeassistant-configuration/.storage/lovelace) for dashboard setup (cards and tiles)

---

## DEVICES

### Main controller
[D1 Mini](https://www.az-delivery.de/en/products/d1-mini) - [pinout](https://m.media-amazon.com/images/I/71b9yM7dFlL.jpg)
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

