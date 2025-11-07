import requests
import sqlite3
import time  # For scheduling daily execution

def create_weather_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY,
            city_id INTEGER,
            date TEXT NOT NULL,
            temperature REAL NOT NULL,
            humidity INTEGER NOT NULL,
            description TEXT NOT NULL
        )
    ''')
def insert_weather_record(cursor, city_id, date, temperature, humidity, description):
    cursor.execute('''
        INSERT INTO weather (city_id, date, temperature, humidity, description)
        VALUES (?, ?, ?, ?, ?)
    ''', (city_id, date, temperature, humidity, description))
    conn.commit()

def get_weather_records(cursor, city_id):
    cursor.execute('''
        SELECT * FROM weather WHERE city_id = ?
    ''', (city_id,))
    return cursor.fetchall()

API_KEY = '72082b1ac3782f2d6f45a2ff89a4d5d0'

def get_weather(city_name):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data

def store_weather_data(cursor, weather_data):
    # Your code to insert data into the WeatherRecords table
    city_id = 1  # You can get this from your city mapping table
    date = time.strftime('%Y-%m-%d')
    temperature = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']
    description = weather_data['weather'][0]['description']
    insert_weather_record(cursor, city_id, date, temperature, humidity, description)

conn = sqlite3.connect('weather_data.db')
cursor = conn.cursor()
create_weather_table(cursor)
city_name = 'New York'
weather_data = get_weather(city_name)
store_weather_data(cursor, weather_data)
records = get_weather_records(cursor, 1)
for record in records:
    print(record)
conn.close()