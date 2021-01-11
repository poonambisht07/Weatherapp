import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *
from datetime import datetime


# Create your views here.
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=56a3270c46d91192ec67911b0a20de10'
    
    context = {}
    context['date_time'] = datetime.now().strftime(" %A, %d %b %Y | %I:%M:%S %p")

    if request.method == "POST":
        new_city = request.POST.get('cname').title()
        
        exist_city = City.objects.filter(name=new_city).count()
        if exist_city == 0:
            r = requests.get(url.format(new_city)).json()
            if r['cod'] == 200:
                nr = City.objects.create(name=new_city)  
                nr.save()
                
            else:
                context['msg'] = "City does not exist in the World!"
                context['col'] = "alert-danger"
        else:
            context['msg'] = "City Already Exists."
            context['col'] = "alert-danger"
            
    cities = City.objects.all().order_by('-id')
    
    weather_data = []
    
    for city in cities:
        r = requests.get(url.format(city)).json()
          
        city_weather = {
            'id' : city.id,
            'city' : city.name,
            'temperature' : ((r['main']['temp']-32)*5//9),
            'description' : (r['weather'][0]['description']).title(),
            'icon' : r['weather'][0]['icon'],
            'sunrise' :datetime.fromtimestamp(int(r['sys']['sunrise'])).strftime('%I:%M:%S %p'),
            'sunset' :datetime.fromtimestamp(int(r['sys']['sunset'])).strftime('%I:%M:%S %p')             
        }
        
        weather_data.append(city_weather) 

    context['city_weather'] = weather_data 
    print(context)
    
    return render(request, 'index.html', context)
   

def del_city(request):
    id = request.GET.get('id')
    City.objects.filter(id=id).delete()
    return redirect ('/')