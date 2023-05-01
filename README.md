## Home Assistant setup

1. Install Home Assistant as container

```
docker compose up -d
```

If you need Docker run for Raspbian/Debian/Ubuntu distros:

```
sudo bash utils/install-docker.sh
```

2. Run the steps for ESPHome installation, when completed run step 3

3. Install the ESPHome integration and in the "host" field, put your esp8266 ip address


## ESPHome installation

1. Install Python on your PC, you can install a specific version by running:

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

8. The first time you flash esp8266, you need to tell esphome some information about
your esp8266 device. Right after that, it will validate the configuration, create a binary, upload it, and start logs

```
cd .esphome && esphome wizard esphome-config.yaml
```

Next time you'll flash it, you just need to run:

```
esphome run esphome-configuration/esphome-config.yaml
```

9. Take note of the ip address printed out in the logs after you run previous command
Read all the output and check for sensors errors, if clear come back to Home Assistant installation steps


## Sensors

### Air

BME280 Temperature + Humidity + Pressure (i2c bus)
| SENSOR      | ESP8266 |
| ----------- | ---------- |
| VIN         | 3V3        |
| GND         | GND        |
| SCK         | SCL        |
| SDD         | SDA        |


### Soil

SHT20 Temperature + Humidity (i2c bus)
| SENSOR      | ESP8266 |
| ----------- | ---------- |
| RED         | 3V3        |
| BLACK       | GND        |
| GREEN       | SDA        |
| YELLOW      | SCL        |


### CO2

MH-Z19C NDIR (uart bus - 7pin terminal connection version)
| SENSOR      | ESP8266 |
| ----------- | ---------- |
| PIN4 VIN    | 5V        |
| PIN3 GND    | GND        |
| PIN5 RX     | TX        |
| PIN6 TX     | RX        |

## DEVICES

Denkovi USB 8CH relay board
| DEVICE     | RPI4 |
| ----------- | ---------- |
| USB-B       | USB           |

Home Assistant `configuration.yaml` contains configuration for controlling USB relay board, 
using [RESTful Binary Sensor](https://www.home-assistant.io/integrations/binary_sensor.rest).
To get it working, an API service must be started within raspbian OS.
Here's the repo: [usbAPI](https://github.com/escomputers/usbAPI)
In this case, the relay board is controlled by a jar file but it can be adapted to any other board by editing the commands to run.

## POWER

| DEVICE     | REQUIRED POWER SOURCES |
| ----------- | ---------- |
| Denkovi USB 8CH relay board       | 12V 1A + 220V|
| Esp8266                           | 5V 2A |
| Raspberry Pi 4                    | 5V 2A|
| Raspberry Pi 4 Fan                | 9V 1A|
| Power sockets                     | 220V 16A (1,5mm<sup>2</sup> cables)|

## WIRINGS
[USB 8CH RELAY BOARD](https://github.com/escomputers/hassio-growbox/blob/c1292adcfdd527b001ce2a75a09739360a721af4/3D/usb-8ch-relay-board/12V-USB-8CH-RELAY-BOARD-WIRING.pdf)

## 3D CASES

Take a look at 3D directory, references:
- Raspberry Pi 4 case (40mm fan) by John_Sinclair on [Thingiverse](https://www.thingiverse.com/thing:3723481)
- 12V USB 8 Channel relay board by polysquare on [Thingverse](https://www.thingiverse.com/thing:2306082)
- BME280 case by leptitnicolas on [Thingverse](https://www.thingiverse.com/thing:3809818)
- Arduino nano + 2 channel arduino relay + voltage stepdown box by flying_ginger on [Thingverse](https://www.thingiverse.com/thing:3162083). Used for housing ESP8266 (by making a drawer/slot manually since screw holes aren't available on the board), MH-Z19, cables and as attach surface for placing BME280 externally.