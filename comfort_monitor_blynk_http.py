#!/usr/bin/env python3
import time
import requests
from sense_hat import SenseHat

# Blynk Configuration
TOKEN = "nblBXZWfDnRMlJeGRbagJH-EsWWg-im0"

# Thingspeak Configuration
THINGSPEAK_KEY = "OT18E4861YEN08NG"

# Blynk HTTP API URLs (created due to issues connecting to Blynk)
BLYNK_TEMP_URL = f"https://blynk.cloud/external/api/update?token={TOKEN}&v0="
BLYNK_HUM_URL = f"https://blynk.cloud/external/api/update?token={TOKEN}&v1="
BLYNK_COMFORT_URL = f"https://blynk.cloud/external/api/update?token={TOKEN}&v2="

# Thingspeak URL
THINGSPEAK_URL = "https://api.thingspeak.com/update"

# Room comfort thresholds
TEMP_LOW = 18
TEMP_HIGH = 22
HUM_LOW = 30
HUM_HIGH = 60

# Initialize Sense HAT
sense = SenseHat()
sense.clear()

def get_calibrated_temp(): # Compensate for Pi CPU Heat
    raw_temp = sense.get_temperature()
    calibrated = raw_temp - 11.5  # Subtract 11.5°C to compensate
    return round(calibrated, 1)

def calculate_comfort(temp, humidity):
    # Temperature assessment
    if temp < TEMP_LOW:
        temp_status = "Too Cold"
    elif temp > TEMP_HIGH:
        temp_status = "Too Hot"
    else:
        temp_status = "Good"

    # Humidity assessment
    if humidity < HUM_LOW:
        hum_status = "Too Dry"
    elif humidity > HUM_HIGH:
        hum_status = "Too Humid"
    else:
        hum_status = "Good"

    # Overall comfort
    if temp_status == "Good" and hum_status == "Good":
        overall = "Excellent :D"
        led_color = (0, 255, 0)  # Green
    elif temp_status == "Good" or hum_status == "Good":
        overall = "Fair :)"
        led_color = (255, 255, 0)  # Yellow
    else:
        overall = "Poor :("
        led_color = (255, 0, 0)  # Red

    status = f"{temp_status} / {hum_status}"
    return status, overall, led_color

def set_led_color(color): # Calls function that changes the Sense HAT LED colours.
    sense.clear(color[0], color[1], color[2])

def send_to_blynk(temp, humidity, comfort_text):
    try:
        # Send temperature to Virtual Pin V0
        response1 = requests.get(f"{BLYNK_TEMP_URL}{temp}", timeout=5)
        # Send humidity to Virtual Pin V1
        response2 = requests.get(f"{BLYNK_HUM_URL}{humidity}", timeout=5)
        # Send comfort status to Virtual Pin V2
        response3 = requests.get(f"{BLYNK_COMFORT_URL}{comfort_text}", timeout=5)
        
        if response1.status_code == 200:
            print("Data sent to Blynk")
            return True
        else:
            print(f"Blynk error: {response1.status_code}")
            return False
    except Exception as e:
        print(f"Connection error: {e}")
        return False

def send_to_thingspeak(temp, humidity):
    try:
        payload = {
            'api_key': THINGSPEAK_KEY,
            'field1': temp,
            'field2': humidity
        }
        response = requests.get(THINGSPEAK_URL, params=payload, timeout=5)
        if response.status_code == 200:
            print(f"Sent to ThingSpeak (entry: {response.text})")
            return True
        else:
            print(f"ThingSpeak error: {response.status_code}")
            return False
        # Error handling (catches the error and prints it)
    except Exception as e:
            print(f"ThingSpeak error: {e}")
            return False

print("=" * 50)
print("Room Comfort Monitor")
print("Sending data every minute...")
print("=" * 50)

try:
    while True:
        # Read sensors
        temp = get_calibrated_temp()
        humidity = round(sense.get_humidity(), 1)

        # Calculate comfort
        status, overall, led_color = calculate_comfort(temp, humidity)
        comfort_text = f"{status} - {overall}"

        # Update Sense HAT LEDs
        set_led_color(led_color)

        # Send to Blynk
        print(f"\n{time.strftime('%H:%M:%S')}")
        print(f"Temperature: {temp}°C")
        print(f"Humidity: {humidity}%")
        print(f"Comfort: {comfort_text}")

        # Send to Blynk & ThingSpeak
        send_to_blynk(temp, humidity, comfort_text)
        send_to_thingspeak(temp, humidity)

        time.sleep(60)  # Send every minute

except KeyboardInterrupt:
    print("\nShutting down...")
    sense.clear()
    print("Goodbye!")
