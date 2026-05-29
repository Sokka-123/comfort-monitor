# Overview

**Room Comfort Monitor:** It's an IoT solution that monitors temperature and humidity in real-time, calculates a comfort index, and provides visual feedback through LED colors. Data is sent to both Blynk (for live dashboard) and ThingSpeak (for historical logging).

**Why this project?** Many people don't notice when their indoor environment becomes uncomfortable, leading to poor sleep, reduced productivity, and/or some health issues. This system makes comfort visible and trackable.

## Features

- Temperature Sensing: Reads temperature from Sense HAT with calibration to compensate for Pi CPU heat 
- Humidity Sensing: Monitors relative humidity levels
- Comfort Calculation: Combines temperature and humidity to determine comfort level
- LED Feedback: Color-coded LED matrix (Green=Excellent, Yellow=Fair, Red=Poor)
- Live Dashboard: Real-time data display on Blynk web dashboard
- Historical Logging: Storage and charts on ThingSpeak
- Automatic Updates: Sends data every 60 seconds to both cloud services

## Architecture
Sensor -> MQTT Broker -> Web Dashboard -> ThingSpeak Cloud

## Hardware Required
- Raspberry Pi (4B or newer): Main processing unit
- Sense HAT: Temperature, humidity sensors + LED matrix 
- Power Supply: 5V/3A USB-C for Pi

## Software Required
- Raspberry Pi OS (64-bit)
- Python
- Sense HAT library
- Requests library

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Sokka-123/comfort-monitor.git
cd comfort-monitor
```

### 2. Install Dependencies

sudo apt update
sudo apt install sense-hat
pip install requests

### 3. Configure Cloud Services

#### 3.1 Blynk Setup

1. Create a free account at https://blynk.cloud/
2. Create a new Template (Raspberry Pi)
3. Add Datastreams:
- V0: Temperature (Double, 0-50°C)
- V1: Humidity (Double, 0-100%)
- V2: Comfort Status (String)
4. Create a Device using the template
5. Copy your Auth Token from Device Info

#### 3.2 ThingSpeak Setup

1. Create a free account at https://thingspeak.com/
2. Create a New Channel:
- Field 1: Temperature (°C)
- Field 2: Humidity (%)
3. Navigate to the API Keys tab
4. Copy your Write API Key

### 4. Update the Script

Edit comfort_monitor_blynk_http.py and update:

TOKEN = "YOUR_BLYNK_AUTH_TOKEN"
THINGSPEAK_KEY = "YOUR_THINGSPEAK_WRITE_KEY"

### 5. Run the Script

python comfort_monitor_blynk_http.py

Example Terminal Output:

==================================================
Room Comfort Monitor
Sending data every minute...
==================================================

14:30:05
Temperature: 22.6°C
Humidity: 34.5%
Comfort: Too Hot / Good - Fair :)
Data sent to Blynk
Sent to ThingSpeak (entry: 1234567)

## Sense HAT LED Colors:
Color	        Comfort Level	     Temperature	  Humidity

Green	        Excellent	     18-22°C              30-60%

Yellow	        Fair	             One ideal, one not	  One ideal, one not

Red	        Poor	             Outside ideal range  Outside ideal range

## Blynk Dashboard
- Live temperature and humidity gauges
- Real-time comfort status text
- Updates every 60 seconds

## ThingSpeak Channel
- Historical temperature chart
- Historical humidity chart
- Data export to CSV
- View by hour, day, week, or month

## System Test
Test					Expected Result

Run script with Pi at room temperature	LEDs change based on readings

Warm the Raspberyy Pi with your hand	Temperature increases, comfort may change to "Too Hot"

Check Blynk dashboard			Values update within 60 seconds

Check ThingSpeak			Data points appear on charts

## Troubleshooting
Issue				Solution

Blynk connection fails		Verify token and internet connection

ThingSpeak error		Check API key and rate limits (15 sec minimum)

Temperature reading too high	Calibration subtracts 10°C; adjust if needed

LED not changing		Check Sense HAT connection and orientation

## Future Improvements
- Mobile push notifications for poor comfort alerts
- Email reports (daily/weekly summaries)
- Multiple sensor locations
- Integration with smart home (turn on fan/heater)

## Author
- David Treacy
- GitHub: https://github.com/Sokka-123
- Project repository: https://github.com/Sokka-123/comfort-monitor
- Project demonstation: https://youtu.be/L2lr4qngqZo

## Student Number
- 20119117
