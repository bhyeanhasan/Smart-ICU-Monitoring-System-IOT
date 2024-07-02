from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from app_temperature.models import Sensors
from datetime import datetime
import csv


def home(request):
    temperatures = Sensors.objects.all().order_by('-id')[:5]
    x = []
    y = []
    z = []
    for index, temp in enumerate(temperatures):
        x.append(index)
        y.append(temp.patient_temp)
        z.append(temp.time)

    ecg_obj = Sensors.objects.all().order_by('-id')[:50]
    ecg = []
    ecg_cnt = []
    for index, obj in enumerate(ecg_obj):
        ecg.append(obj.ecg)
        ecg_cnt.append(index)

    print(ecg)
    print(ecg_cnt)

    return render(request, 'home.html', {"x": x, "y": y, "z": z, "ecg": ecg, "ecg_cnt": ecg_cnt})


def exportData(request):
    obj = Sensors.objects.all().order_by('-id')
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="somefilename.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(["Date and Time", "Temperature", "ECG"])

    for index, obj in enumerate(obj):
        writer.writerow([obj.time, obj.patient_temp, obj.ecg])

    return response


def dashboardData(request):
    objects = Sensors.objects.all()
    cnt = 0
    y = []
    x = []
    for object in objects:
        cnt += 1
        y.append(int(object.patient_temp))
        x.append(cnt)

    return JsonResponse({'x': x, 'y': y})
