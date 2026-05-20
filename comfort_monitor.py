#!/usr/bin/env python3
## Room Comfort Monitor - Release 1: Basic Sensor Reading
from sense_hat import SenseHat
import time
import json
from datetime import datetime

sense = SenseHat()
sense.clear()

# Comfort thresholds
TEMP_IDEAL_LOW = 18
TEMP_IDEAL_HIGH = 22
HUMIDITY_IDEAL_LOW = 30
HUMIDITY_IDEAL_HIGH = 60

## Calculate comfort level based on temperature and humidity
def calculate_comfort(temp, humidity):
    if temp < TEMP_IDEAL_LOW:
        temp_status = "Too Cold"
        temp_color = "Blue"
    elif temp > TEMP_IDEAL_HIGH:
        temp_status = "Too Hot"
        temp_color = "Red"
    else:
        temp_status = "Good"
        temp_color = "Green"
    
    if humidity < HUMIDITY_IDEAL_LOW:
        humidity_status = "Too Dry"
    elif humidity > HUMIDITY_IDEAL_HIGH:
        humidity_status = "Too Humid"
    else:
        humidity_status = "Good"
    
    if temp_status == "Good" and humidity_status == "Good":
        overall = "Excellent"
    elif temp_status == "Good" or humidity_status == "Good":
        overall = "Fair"
    else:
        overall = "Poor"
    
    return {
        "temp_status": temp_status,
        "temp_color": temp_color,
        "humidity_status": humidity_status,
        "overall": overall
    }

## Set Sense HAT LED color based on overall comfort
def set_led_color(overall):
    if overall == "Excellent":
        sense.clear(0, 255, 0)  # Green
    elif overall == "Fair":
        sense.clear(255, 255, 0)  # Yellow
    else:
        sense.clear(255, 0, 0)  # Red

print("Room Comfort Monitor - Release 1")
print("=" * 40)

try:
    while True:
        temp = round(sense.get_temperature(), 1)
        humidity = round(sense.get_humidity(), 1)
        comfort = calculate_comfort(temp, humidity)
        set_led_color(comfort["overall"])
        
        # Console output - need more explanation on this.
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}]")
        print(f"Temperature: {temp}°C ({comfort['temp_status']})")
        print(f"Humidity: {humidity}% ({comfort['humidity_status']})")
        print(f"Overall Comfort: {comfort['overall']}")
        
        time.sleep(5)
        
except KeyboardInterrupt:
    print("\nShutting down...")
    sense.clear()
