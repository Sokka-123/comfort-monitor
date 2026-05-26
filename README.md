# Room Comfort Monitor

A Raspberry Pi-based system that monitors temperature and humidity to calculate a comfort index within a room in my apartment.

## Features
- Real-time temperature and humidity sensing using Sense HAT
- Comfort index calculation i.e. goldilocks zone (too hot, too cold, just right)
- Live web dashboard with color-coded status
- MQTT for real-time updates
- Historical data logging to ThingSpeak

## Architecture
Sensor -> MQTT Broker -> Web Dashboard -> ThingSpeak Cloud

## Hardware Required
- Raspberry Pi 4 Model B
- Sense HAT

## Author
David Treacy

## Student Number
20119117
