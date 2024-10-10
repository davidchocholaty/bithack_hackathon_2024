from django.shortcuts import render

# Create your views here.
def main_page(request):
    facilities = [
        {'name':'Facility 1',
         'capacity':100,
         'count':23,
         'day_count':980,
         'address':'Address 1',
        },
        {'name':'Facility 2',
         'capacity':102,
         'count':40,
         'day_count':750,
         'address':'Address 2',
        },
        {'name':'Facility 3',
         'capacity':60,
         'count':60,
         'day_count':1000,
         'address':'Address 3',
        },
    ]
    
    
    # Calculate occupancy percentage for each facility
    for facility in facilities:
        facility['occupancy_percentage'] = (facility['count'] / facility['capacity']) * 100

    
    context = {
        'facilities' : facilities
    }
    return render(request, "base.html", context)
