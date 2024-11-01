# Raspberry Pi Weather Station

A real-time environmental monitoring system using Raspberry Pi, DHT11 sensor, and I2C LCD display.

## Features

- Temperature and humidity monitoring using DHT11 sensor
- Real-time display on 16x2 I2C LCD screen
- Data logging with timestamp
- JSON file storage organized by date
- Automatic data collection every 5 minutes

## Hardware Requirements

- Raspberry Pi (any model)
- DHT11 Temperature and Humidity Sensor
- 16x2 LCD Display with I2C backpack (PCF8574)
- Jumper wires (female-to-female)
- Breadboard (optional)

## Wiring Instructions

### DHT11 Sensor Connection:
1. VCC (Power) → 3.3V (Pin 1)
2. GND (Ground) → Ground (Pin 6)
3. DATA → GPIO4 (Pin 7)

### I2C LCD Connection:
1. VCC → 5V (Pin 2)
2. GND → Ground (Pin 6)
3. SDA → GPIO2/SDA (Pin 3)
4. SCL → GPIO3/SCL (Pin 5)

## Software Setup

1. Enable I2C interface on Raspberry Pi:
```bash
sudo raspi-config
# Navigate to Interface Options → I2C → Enable
```

2. Install required system packages:
```bash
sudo apt-get update
sudo apt-get install python3-pip git python3-smbus i2c-tools
```

3. Verify I2C LCD connection:
```bash
sudo i2cdetect -y 1
```
You should see the LCD address (usually 0x27) in the output.

4. Clone this repository:
```bash
git clone https://github.com/yourusername/room-weather-station.git
cd room-weather-station
```

5. Install Python dependencies:
```bash
pip3 install -r requirements.txt
```

6. Run the weather station:
```bash
python3 weather_station.py
```

## Auto-start on Boot

1. Copy the service file to systemd:
```bash
sudo cp weather-station.service /etc/systemd/system/
```

2. Enable and start the service:
```bash
sudo systemctl enable weather-station
sudo systemctl start weather-station
```

## Data Storage

Data is stored in JSON format in the `data` directory. Files are organized by date (e.g., `weather_data_2024-01-20.json`).

Each reading contains:
- Timestamp
- Temperature (°C)
- Humidity (%)

## LCD Display

The 16x2 LCD display shows:
- Line 1: Current temperature in Celsius
- Line 2: Current humidity percentage

The display updates every 5 minutes along with data logging.

## Monitoring the Service

Check service status:
```bash
sudo systemctl status weather-station
```

View logs:
```bash
journalctl -u weather-station
```

## Troubleshooting

1. If the LCD doesn't display:
   - Check I2C address using `sudo i2cdetect -y 1`
   - Verify wiring connections
   - Ensure I2C is enabled in raspi-config

2. If sensor readings fail:
   - Check DHT11 wiring
   - Verify GPIO pin number in code matches your connection
   - Ensure proper power supply to Raspberry Pi

