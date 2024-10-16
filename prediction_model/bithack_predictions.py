# -*- coding: utf-8 -*-
"""bithack_predictions.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1b1JU9CaqpF7iHJEJ-fSndQWfRP3o0AL_
"""

!pip install geojson
!pip install requests
!pip install joblib
!pip install pandas
!pip install json
!pip install sklearn

import geojson
import requests
import joblib
import pandas as pd
import json
from datetime import datetime, timedelta
from collections import OrderedDict

csv_file = '/content/mean_values_hourly.csv'

df_csv = pd.read_csv(csv_file)

df_csv['Date'] = pd.to_datetime(df_csv['Date'])

df_csv['Měsíc'] = df_csv['Date'].dt.month
df_csv['Den'] = df_csv['Date'].dt.day

df_csv.head()

# Funkce pro výběr hodnot z CSV na základě měsíce, dne a hodiny
def get_csv_values_for_hour(df_csv, future_time):
    """
    Vybere relevantní hodnoty z CSV pro konkrétní hodinu na základě měsíce, dne a hodiny.
    Ignoruje rok a vrací hodnoty mean_ na základě historie.
    """
    # Získání měsíce, dne a hodiny z future_time
    month = future_time.month
    day = future_time.day
    hour = future_time.hour

    # Filtrovat hodnoty na základě měsíce, dne a hodiny (ignorujeme rok)
    filtered_rows = df_csv[(df_csv['Měsíc'] == month) & (df_csv['Den'] == day) & (df_csv['Hodina'] == hour)]

    if not filtered_rows.empty:
        # Vezmeme průměrné hodnoty z nalezených řádků
        return {
            'mean_teplota_max': filtered_rows['Mean_Teplota_Max'].mean(),
            'mean_teplota_min': filtered_rows['Mean_Teplota_Min'].mean(),
            'mean_abonenti': filtered_rows['Mean_Abonenti'].mean(),
            'mean_verejnost': filtered_rows['Mean_Verejnost'].mean(),
            'mean_rychlost_vetru': filtered_rows['Mean_Rychlost_Vetru'].mean(),
            'mean_tlak_vzduchu': filtered_rows['Mean_Tlak_Vzduchu'].mean(),
            'mean_uhrn_srazek': filtered_rows['Mean_Uhrn_Srazek'].mean()
        }
    else:
        # Pokud nejsou data pro konkrétní měsíc, den a hodinu dostupná
        print(f"No data available for month {month}, day {day}, hour {hour}. Using overall averages.")
        return {
            'mean_teplota_max': df_csv['Mean_Teplota_Max'].mean(),
            'mean_teplota_min': df_csv['Mean_Teplota_Min'].mean(),
            'mean_abonenti': df_csv['Mean_Abonenti'].mean(),
            'mean_verejnost': df_csv['Mean_Verejnost'].mean(),
            'mean_rychlost_vetru': df_csv['Mean_Rychlost_Vetru'].mean(),
            'mean_tlak_vzduchu': df_csv['Mean_Tlak_Vzduchu'].mean(),
            'mean_uhrn_srazek': df_csv['Mean_Uhrn_Srazek'].mean()
        }

"""# Loading data from APIs"""

def fetch_starez_data():
    # URL GeoJSON API
    url_starez = "https://services6.arcgis.com/fUWVlHWZNxUvTUh8/arcgis/rest/services/starez1/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

    # Provedení GET požadavku
    response = requests.get(url_starez)

    # Kontrola úspěšnosti požadavku
    if response.status_code == 200:
        # Uložení dat
        data_starez = response.json()  # GeoJSON data ve formátu JSON
        #print(geojson.dumps(data_starez, indent=2))  # Výpis s formátováním
        return data_starez
    else:
        print(f"Error: {response.status_code}")
        return None

# Example usage:
starez_data = fetch_starez_data()

def get_weather_data():
    # WEATHER DATA API

    # URL API
    url = "https://api.met.no/weatherapi/locationforecast/2.0/compact"

    # Souřadnice pro požadavek (input lat, lon)
    # Brno - Tuřany
    params = {
        'lat': 49.1597,  # Zeměpisná šířka
        'lon': 16.6956   # Zeměpisná délka
    }

    # Hlavičky požadavku
    headers = {
        'User-Agent': 'TeamHackson/1.0 (david.chocholaty12@gmail.com)'
    }

    # Provedení GET požadavku
    response = requests.get(url, headers=headers, params=params)

    # Zpracování odpovědi
    if response.status_code == 200:
        data_weather = response.json()  # Pokud je odpověď úspěšná, převést na JSON
        #print("Weather data retrieved successfully.")
        return data_weather
    else:
        print(f"Error: {response.status_code}")
        return None

weather_data = get_weather_data()
#weather_data

def extract_temperature(weather_data, future_time):
    """
    Získá teplotu z weather_data pro danou hodinu (future_time).
    """
    # Projdi načtené časové série z weather API
    for entry in weather_data['properties']['timeseries']:
        time_str = entry['time']
        # Pokud čas v API odpovídá hledanému času
        if future_time.isoformat() + 'Z' == time_str:
            return entry['data']['instant']['details']['air_temperature']
    # Pokud nenajdeme odpovídající čas
    return None

def get_today_weather_data(weather_data):
    """
    Filtruje a vrací data o počasí pouze pro dnešní den ve formátu seznamu s časem, teplotou,
    tlakem, vlhkostí, rychlostí větru a srážkami za 1 hodinu.
    """
    # Definuj aktuální datum (dnesní den)
    current_date = datetime.utcnow().date()

    # Filtruj data, která jsou pouze do konce aktuálního dne
    weather_filtered_data = [
        {
            'time': entry["time"],
            'temperature': entry["data"]["instant"]["details"].get("air_temperature"),
            'air_pressure': entry["data"]["instant"]["details"].get("air_pressure_at_sea_level"),
            'humidity': entry["data"]["instant"]["details"].get("relative_humidity"),
            'wind_speed': entry["data"]["instant"]["details"].get("wind_speed"),
            'precipitation_1h': entry.get("data", {}).get("next_1_hours", {}).get("details", {}).get("precipitation_amount")
        }
        for entry in weather_data["properties"]["timeseries"]
        if datetime.strptime(entry["time"], "%Y-%m-%dT%H:%M:%SZ").date() == current_date
    ]

    return weather_filtered_data

weather_data = get_weather_data()
if weather_data:
    today_weather = get_today_weather_data(weather_data)
    for entry in today_weather:
        print(f"Time: {entry['time']}, Temperature: {entry['temperature']}°C, Pressure: {entry['air_pressure']} hPa, "
              f"Humidity: {entry['humidity']}%, Wind: {entry['wind_speed']} m/s, "
              f"Precipitation (1h): {entry['precipitation_1h']} mm")

import json

def parse_starez_geojson(data_starez):
    """
    Zpracuje GeoJSON data, přidá ID k jednotlivým záznamům a vrátí je ve formátu JSON.
    """
    features = data_starez.get("features", [])
    parsed_data = []

    # Projdeme každou položku (feature)
    for index, feature in enumerate(features):
        properties = feature.get("properties", {})
        geometry = feature.get("geometry", {})

        # Získání vlastností
        name = properties.get("Name")
        capacity = properties.get("Capacity")
        count = properties.get("Count_")
        day_count = properties.get("Day_Count")
        address = properties.get("Address")
        latitude = properties.get("Latitude")
        longitude = properties.get("Longitude")

        # Získání souřadnic z geometrie
        coordinates = geometry.get("coordinates", [])

        # Uložíme vyparsovaná data jako slovník do seznamu
        parsed_data.append({
            'id': index + 1,  # Přidání ID (založeno na indexu, začíná od 1)
            'name': name,
            'capacity': capacity,
            'count': count,
            'day_count': day_count,
            'address': address,
            'latitude': latitude,
            'longitude': longitude,
            'coordinates': coordinates
        })

    # Vrátíme data jako JSON
    return json.dumps(parsed_data, ensure_ascii=False, indent=4)

# Příklad volání funkce s GeoJSON daty
starez_data_json = parse_starez_geojson(starez_data)

# Výstup
print(starez_data_json)

def predict_for_hour(loaded_model, future_time, df_csv, weather_data, selected_place):
    """
    Vrací predikci pro danou hodinu (future_time) pomocí modelu, hodnot z CSV a weather API.
    Parametr selected_place určuje místo, pro které chceme provést predikci.
    """
    # Mapa míst (klíče odpovídají hodnotám pro Zkratka_* v datasetu)
    places = {
        'Bazény Lužánky': 'Zkratka_Bazény Lužánky',
        'Bruslení za Lužánkami': 'Zkratka_Bruslení za Lužánkami',
        'Kluziště Vodova': 'Zkratka_Kluziště Vodova',
        'Koupaliště Riviéra': 'Zkratka_Koupaliště Riviéra',
        'Koupaliště Riviéra Automat': 'Zkratka_Koupaliště Riviéra Automat',
        'Koupaliště Zábrdovice': 'Zkratka_Koupaliště Zábrdovice',
        'Krytý plavecký bazén Ponávka': 'Zkratka_Krytý plavecký bazén Ponávka',
        'Lázně Rašínova Bazén': 'Zkratka_Lázně Rašínova Bazén',
        'Lázně Rašínova Posilovna': 'Zkratka_Lázně Rašínova Posilovna'
    }

    # Inicializuj místa s nulovými hodnotami
    future_data = OrderedDict([
        ('Měsíc', [future_time.month]),
        ('Den', [future_time.day]),
        ('Hodina', [future_time.hour]),
        ('teplota prumerna_value', [0]),  # Bude přepsáno později
        ('day_of_week', [future_time.weekday()]),
        ('mean_abonenti', [0]),  # Bude přepsáno později
        ('mean_verejnost', [0]),  # Bude přepsáno později
        ('mean_rychlost_vetru', [0]),  # Bude přepsáno později
        ('mean_tlak_vzduchu', [0]),  # Bude přepsáno později
        ('mean_uhrn_srazek', [0]),  # Bude přepsáno později
        ('Zkratka_Bazény Lužánky', [0]),
        ('Zkratka_Bruslení za Lužánkami', [0]),
        ('Zkratka_Kluziště Vodova', [0]),
        ('Zkratka_Koupaliště Riviéra', [0]),
        ('Zkratka_Koupaliště Riviéra Automat', [0]),
        ('Zkratka_Koupaliště Zábrdovice', [0]),
        ('Zkratka_Krytý plavecký bazén Ponávka', [0]),
        ('Zkratka_Lázně Rašínova Bazén', [0]),
        ('Zkratka_Lázně Rašínova Posilovna', [0])
    ])

    # Nastav vybrané místo na 1
    if selected_place in places:
        future_data[places[selected_place]] = [1]
    else:
        raise ValueError(f"Unknown place: {selected_place}")

    # Získání teploty z API
    temperature = extract_temperature(weather_data, future_time)

    # Pokud není teplota dostupná, použij historickou průměrnou teplotu
    if temperature is None:
        print(f"Unable to fetch temperature for {future_time}. Using historical average.")
        temperature = df_csv['Mean_Teplota_Max'].mean()  # Náhradní hodnota

    # Získat další hodnoty z CSV na základě měsíce, dne a hodiny
    csv_values = get_csv_values_for_hour(df_csv, future_time)

    # Aktualizace predikčních dat
    future_data['teplota prumerna_value'] = [temperature]
    future_data['mean_abonenti'] = [csv_values['mean_abonenti']]
    future_data['mean_verejnost'] = [csv_values['mean_verejnost']]
    future_data['mean_rychlost_vetru'] = [csv_values['mean_rychlost_vetru']]
    future_data['mean_tlak_vzduchu'] = [csv_values['mean_tlak_vzduchu']]
    future_data['mean_uhrn_srazek'] = [csv_values['mean_uhrn_srazek']]

    # Převést na DataFrame
    input_df = pd.DataFrame(future_data)

    # Proveď predikci
    prediction = loaded_model.predict(input_df)
    return prediction[0]  # Vrátí predikovanou hodnotu

def predict_until_end_of_day(loaded_model, df_csv, weather_data, selected_place):
    """
    Vrací seznam predikcí pro všechny hodiny do konce dne ve formátu JSON.
    """
    current_time = datetime.utcnow()
    next_hour_time = (current_time + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    end_of_day = current_time.replace(hour=23, minute=0, second=0, microsecond=0)

    predictions = []
    future_time = next_hour_time

    while future_time <= end_of_day:
        predicted_value = predict_for_hour(loaded_model, future_time, df_csv, weather_data, selected_place)
        predictions.append({
            "time": future_time.strftime('%Y-%m-%d %H:%M'),
            "predicted_people": predicted_value
        })
        future_time += timedelta(hours=1)

    return json.dumps(predictions)

# Load the model
loaded_model = joblib.load('random_forest_model_final.pkl')

df_csv['Date'] = pd.to_datetime(df_csv['Date'])
df_csv['Měsíc'] = df_csv['Date'].dt.month
df_csv['Den'] = df_csv['Date'].dt.day

selected_place = 'Bazény Lužánky'

# Zavolej predikce na následující hodiny do konce dne
json_predictions = predict_until_end_of_day(loaded_model, df_csv, weather_data, selected_place)

# Výstup predikcí v JSON formátu
print(json_predictions)

