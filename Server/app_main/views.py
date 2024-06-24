import json

from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from app_temperature.models import Temperature
from asgiref.sync import sync_to_async


def home(request):
    temperatures = Temperature.objects.all().order_by('-id')[:10]
    x =[]
    y =[]
    for index,temp in enumerate(temperatures):
        x.append(index)
        y.append(temp.patient_temp)

    return render(request, 'home.html',{"x":x,"y":y})


def dashboardData(request):
    objects = Temperature.objects.all()
    cnt = 0
    y = []
    x = []
    for object in objects:
        cnt += 1
        y.append(int(object.patient_temp))
        x.append(cnt)

    return JsonResponse({'x': x, 'y': y})
