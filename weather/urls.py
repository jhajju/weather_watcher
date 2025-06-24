from django.urls import path
from . import views

urlpatterns = [
    path('', views.city_list, name='city_list'),  # Root page shows the city list
    path('delete/<int:city_id>/', views.delete_city, name='delete_city'), 
]
