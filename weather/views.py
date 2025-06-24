import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import City
from .forms import CityForm
from django.contrib.auth.decorators import login_required
from django.conf import settings  # To access API key


@login_required
def city_list(request):
    form = CityForm()

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.save(commit=False)
            city.user = request.user
            city.save()
            return redirect('city_list')

    cities = City.objects.filter(user=request.user)
    weather_data = []

    for city in cities:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city.name}&appid={settings.OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather = {
                'id': city.id,
                'name': city.name,
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
            }
            weather_data.append(weather)
        else:
            # If the city name is invalid, skip it
            weather_data.append({
                'id': city.id,
                'name': city.name,
                'temperature': 'N/A',
                'description': 'City not found',
                'icon': '01d',
            })

    return render(request, 'weather/city_list.html', {
        'form': form,
        'weather_data': weather_data
    })


@login_required
def delete_city(request, city_id):
    city = get_object_or_404(City, id=city_id, user=request.user)
    city.delete()
    return redirect('city_list')
