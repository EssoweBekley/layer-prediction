# https://www.visualcrossing.com/weather-api

import requests
import sys
import csv
import os
import json
import shutil
from dotenv import load_dotenv


load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
API_KEY = os.getenv('api_key')
API_URL = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Hartford/monthtodate?unitGroup=us&elements=datetime%2Ctemp%2Chumidity%2Cwindspeedmean%2Cconditions&key={API_KEY}&contentType=json'
CSV_FILENAME = 'weather_data.csv'
CSV2_FILENAME = 'weather_data2.csv'
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

CSV_PATH = os.path.join(SCRIPT_DIR, 'data', CSV_FILENAME)
CSV2_PATH = os.path.join(SCRIPT_DIR, 'data', CSV2_FILENAME)

response = requests.get(API_URL)
if response.status_code != 200:
    print('Unexpected Status code:', response.status_code)
    sys.exit()

data = response.json()

with open("./jsonData.json", "a") as jsonfile:
    json.dump(data, jsonfile, indent=4)

new_days = data['days'] 

existing_dates = set()
if os.path.exists(CSV_PATH):
    with open(CSV_PATH, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing_dates.add(row['date'])
      
print(f"Writing to CSV at: {CSV_PATH}")
 

with open(CSV_PATH, 'a', newline='') as f:
    fieldnames = ['date', 'conditions','temp', 'humidity', 'wind_speed', 'layer_count', 'layer_types']
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    # Write headers if file is empty
    if os.stat(CSV_PATH).st_size == 0:
        writer.writeheader()

    for day in data['days']:
        date = day['datetime']
        if date not in existing_dates:
            writer.writerow({
                'date': date,
                'temp': day.get('temp', ''),
                'humidity': day.get('humidity', ''),
                'wind_speed': day.get('windspeedmean', ''),
                'layer_count': '',
                'layer_types': '',
                'conditions': day.get('conditions', '')
            })


# copy to new file
shutil.copy(CSV_PATH, CSV2_PATH)
print('Done')