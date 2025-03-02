Home Assistant as growbox controller, using several different devices and sensors, connected via D1 Mini/ESP8266-12-e

## Home Assistant setup

### Install
1. Install Home Assistant as container (for Core installation check the "core" branch out)

```bash
docker compose up -d
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

[Best PINs to use on ESP8266](https://espeasy.readthedocs.io/en/latest/Reference/GPIO.html#best-pins-to-use-on-esp8266)

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


### Water Flow meter
[YF-S402B](https://robu.in/wp-content/uploads/2021/07/NB178.pdf)

WARNING: enable option "Allow the device to perform Home Assistant actions" in Settings/Devices&Services/ESPHome/configure

<ins>Installation</ins>

- Straight Pipe Section Before and After the Sensor

  - Upstream (Inlet):
  Ensure there is a sufficient length of straight pipe (typically 10–15 times the pipe diameter) before the sensor. This helps in creating a uniform, laminar flow profile and minimizes turbulence before the water reaches the sensor.

  - Downstream (Outlet):
  Similarly, maintain a straight run after the sensor (at least 5–10 pipe diameters) if possible. This prevents any backflow or turbulent eddies from affecting the sensor’s operation.

- Avoid installing the sensor in positions where gravity or buoyancy effects could cause bubbles or sediment accumulation.

- Avoiding Vibrations and Mechanical Interference

  - Mount the sensor securely using proper fittings to prevent vibrations. Excessive vibration can introduce noise into the measurement. Ensure that the sensor is not subjected to mechanical stress or movement, as this can affect the pulse signal.

- Minimize Air Entrapment and Bubbles

  - Install the sensor in a part of the piping system where air is unlikely to be trapped. Air bubbles can cause the turbine to rotate erratically, leading to inaccurate readings.

- Stable Electrical Connections

  - Use good quality wiring and, if possible, shielded cables to reduce electrical noise, which might cause false triggering or counting errors.
  Enable the internal pull-up resistor to maintain a stable digital signal.

| YF-S402B    | ESP8266    |
| ----------- | ---------- |
| RED         | 5V         |
| BLACK       | GND        |
| YELLOW      | GPIO12/D6  |

<ins>Calculate calibration constant</ins>

1. Measure the quantity of water running through the sensor in a specific time interval

2. Count the pulses over time to calculate the exact flow rate frequency

3. Adjust the default calibration constant based on observed data to improve precision

For example:\
If you collected 1,6 liters in 60 seconds:\
Flow Rate (Q) = 1,6 Liters per minute

Calibration Constant (K) = Pulses/minute (P) : Flow Rate (Q)\
1.596,35635625 = 2.554,17017 (median of all pulses measurements) : 1,6

Volume (L) = Pulses : K\
1,6 = 2.554,17017 : 1.596,35635625

## POWER

| DEVICE     | REQUIRED POWER SOURCES |
| ----------- | ---------- |
| Denkovi USB 8CH relay board       | 12V 1A + 220V|
| Esp8266                           | 5V/3.3V 1A |
| Raspberry Pi 4                    | 5V 2A|
| Raspberry Pi 4 Fan                | 9V 1A|
| Power sockets                     | 220V 16A (1,5mm<sup>2</sup> cables)|


## 3D CASES

Take a look at [3D directory](3D/)\
References:
- Raspberry Pi 4 case (40mm fan) by John_Sinclair on [Thingiverse](https://www.thingiverse.com/thing:3723481)
- 12V USB 8 Channel relay board by polysquare on [Thingverse](https://www.thingiverse.com/thing:2306082)
- BME280 case by leptitnicolas on [Thingverse](https://www.thingiverse.com/thing:3809818)
- Arduino nano + 2 channel arduino relay + voltage stepdown box by flying_ginger on [Thingverse](https://www.thingiverse.com/thing:3162083). Used for housing ESP8266 (by making a drawer/slot manually since screw holes aren't available on the board), MH-Z19, cables and as attach surface for placing BME280 externally.

---
