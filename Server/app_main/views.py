import json

from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from app_temperature.models import Temperature
from asgiref.sync import sync_to_async


def home(request):
    return render(request, 'home.html')


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
