from django.urls import path
from . import views


urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('facility/<int:facility_id>/', views.get_facility_data, name='get_facility_data'),
]