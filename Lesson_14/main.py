import pynmea2
from geopy.distance import geodesic
from twilio.rest import Client
import json

# Load configuration
with open("config.json") as f:
    config = json.load(f)

center = (config["geofence"]["lat"], config["geofence"]["lon"])
radius = config["geofence"]["radius_m"]

# Read NMEA data from external file
with open("nmea_data.txt") as f:  # Change 'nmea_data.txt' to your actual file name
    for line in f:
        line = line.strip()
        if line.startswith("$GPGGA") or line.startswith("$GPRMC"):
            try:
                msg = pynmea2.parse(line)
                lat = msg.latitude
                lon = msg.longitude
                point = (lat, lon)
                dist = geodesic(center, point).meters
                if dist > radius:
                    tw = config["twilio"]
                    Client(tw["account_sid"], tw["auth_token"]).messages.create(
                        body=f"Device is outside geofence ({dist:.2f} m)",
                        from_=tw["from_number"],
                        to=tw["to_number"]
                    )
            except Exception as e:
                print(f"Failed to parse line: {line}\nError: {e}")
