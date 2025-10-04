import requests
import sys
import json
import mysql.connector
from mysql.connector import errorcode

TABLE_NAME = 'userdata'  

try: 
    cnx = mysql.connector.connect(user='root',
                                    password='password',
                                    host="localhost",
                                    database = 'templayer') # specify db
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errorcode == errorcode.ER_BAD_DB_ERROR:
        print("DB Does not exist")
    else:
        print(err)

cursor = cnx.cursor()

# response = requests.request("GET", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Storrs%2C%20CT?unitGroup=us&elements=datetime%2Ctemp%2Chumidity%2Cwindspeedmean%2Cconditions&include=days&key=KR9B77ZYFSZU8JBZJXX8BHENN&contentType=json")
# if response.status_code!=200:
#   print('Unexpected Status code: ', response.status_code)
#   sys.exit()  
# # jsonData = response.json()

# Parse the results as JSON
file = r'layer_prediction/Storrs, CT.json'
with open(file, "r") as f:
    jsonData = json.load(f)

add_new_data = (f"INSERT INTO {TABLE_NAME}"
                "(date, conditions, temp, humidity, wind_speed)"
                "VALUES (%s, %s, %s, %s, %s)")

new_data = jsonData['days']

for day in new_data:
    curr_day = day['datetime']
    curr_day_temp = day['temp']
    curr_day_humidity = day['humidity']
    curr_day_windspeedmean = day['windspeedmean']
    curr_day_conditions = day['conditions']

    # print(f"{curr_day}\n{curr_day_temp}\n{curr_day_humidity}\n{curr_day_windspeedmean}\n{curr_day_conditions}\n\n")

    data_to_insert = (curr_day, curr_day_conditions, curr_day_temp, curr_day_humidity, curr_day_windspeedmean)

    cursor.execute(add_new_data, data_to_insert)
    cnx.commit()

cursor.close()
cnx.commit()
cnx.close()

# TODO (Later): Make inserting more effieiclet



