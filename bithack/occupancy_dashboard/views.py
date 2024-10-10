import requests
from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd
import json
from datetime import datetime
import logging

# Load and preprocess your data (adjust the file path)
data = pd.read_excel('occupancy_dashboard/data/Starez.xlsx', sheet_name='Data')
data = data.drop(columns=['Veřejnost', 'Abonenti'])
data.columns = ['Facility', 'Year', 'Month', 'Day', 'Hour', 'Total']
data = data.dropna()

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


# New view to get facility details
def get_facility_data(request, facility_id):
    facilities = [
        {
            "id": 1,
            "name": "Facility 1",
            "capacity": 100,
            "count": 23,
            "day_count": 980,
            "address": "Address 1",
        },
        {
            "id": 2,
            "name": "Facility 2",
            "capacity": 102,
            "count": 40,
            "day_count": 750,
            "address": "Address 2",
        },
        {
            "id": 3,
            "name": "Facility 3",
            "capacity": 60,
            "count": 60,
            "day_count": 1000,
            "address": "Address 3",
        },
    ]
    
    facilities = json.loads(parse_starez_geojson(fetch_starez_data()))

    # Find the facility by id
    facility = next((f for f in facilities if f["id"] == facility_id), None)

    print(facility)
    
      #facility_name = default_facility.get("name", "")
    facility_names = {
        1: "",
        2: "",
        3: "",
        4: "",
        5: "",
        6: "",
        7: "",
        8: "",
        9: "",
        10: "",
        11: "",
        12: "",
    }
    facility_data = data[data['Facility'] == "MPS Lužánky"]

    current_weekday = datetime.now().strftime('%A')
    facility_data.loc[:, 'Weekday'] = pd.to_datetime(facility_data[['Year', 'Month', 'Day']]).dt.day_name()
    current_day_data = facility_data[facility_data['Weekday'] == current_weekday]

    # Prepare data for Chart.js
    median_occupancy_per_hour = current_day_data.groupby('Hour')['Total'].median().reindex(range(24), fill_value=0)
    labels = list(median_occupancy_per_hour.index)  # Hours of the day (0-23)
    values = list(median_occupancy_per_hour.values)  # Median occupancy per hour

    # Convert data to JSON to pass to the template
    chart_data = {
        'labels': labels,
        'values': values,
    }
    
    if facility:
        facility["occupancy_percentage"] = (
            facility["count"] / facility["capacity"]
        ) * 100
        return JsonResponse(facility)
    else:
        return JsonResponse({"error": "Facility not found"}, status=404)


# Create your views here.
def main_page(request):
    facilities = [
        {
            "id": 1,
            "name": "Facility 1",
            "capacity": 100,
            "count": 23,
            "day_count": 980,
            "address": "Address 1",
        },
        {
            "id": 2,
            "name": "Facility 2",
            "capacity": 102,
            "count": 40,
            "day_count": 750,
            "address": "Address 2",
        },
        {
            "id": 3,
            "name": "Facility 3",
            "capacity": 60,
            "count": 60,
            "day_count": 1000,
            "address": "Address 3",
        },
    ]
    facilities = json.loads(parse_starez_geojson(fetch_starez_data()))
    # Calculate occupancy percentage for each facility
    # Calculate occupancy percentage and add to each facility
    for facility in facilities:
        if facility['capacity'] > 0:  # Prevent division by zero
            facility['occupancy_percentage'] = (facility['count'] / facility['capacity']) * 100
        else:
            facility['occupancy_percentage'] = 0  # Set to 0 if capacity is 0
    # Choose a default facility to display (e.g., the first one)
    default_facility = facilities[0] if facilities else {}
     #facility_name = default_facility.get("name", "")
    facility_data = data[data['Facility'] == "KLU Kluziště"]

    current_weekday = datetime.now().strftime('%A')
    facility_data.loc[:, 'Weekday'] = pd.to_datetime(facility_data[['Year', 'Month', 'Day']]).dt.day_name()
    current_day_data = facility_data[facility_data['Weekday'] == current_weekday]

    # Prepare data for Chart.js
    median_occupancy_per_hour = current_day_data.groupby('Hour')['Total'].median().reindex(range(24), fill_value=0)
    labels = list(median_occupancy_per_hour.index)  # Hours of the day (0-23)
    values = list(median_occupancy_per_hour.values)  # Median occupancy per hour

    # Convert data to JSON to pass to the template
    chart_data = {
        'labels': labels,
        'values': values,
    }

    # Log the chart_data for debugging
    logging.info("Chart data: %s", json.dumps(chart_data))

    context = {
        "facilities": facilities,
        "default_facility": default_facility,
        "chart_data": json.dumps(chart_data),
    }

    return render(request, "base.html", context)
