from django.http import JsonResponse
from django.shortcuts import render


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

    # Find the facility by id
    facility = next((f for f in facilities if f["id"] == facility_id), None)

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

    # Calculate occupancy percentage for each facility
    for facility in facilities:
        facility["occupancy_percentage"] = (
            facility["count"] / facility["capacity"]
        ) * 100
    # Choose a default facility to display (e.g., the first one)
    default_facility = facilities[0] if facilities else {}

    context = {"facilities": facilities, "default_facility": default_facility}
    return render(request, "base.html", context)
