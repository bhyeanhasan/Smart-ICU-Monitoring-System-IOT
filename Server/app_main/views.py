from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from app_temperature.models import Sensors
from datetime import datetime
import csv


def calculate_spo2(ir, red):
    red_dc = sum(red) / len(red) + 1
    ir_dc = sum(ir) / len(ir) + 1
    red_ac = [value - red_dc for value in red]
    ir_ac = [value - ir_dc for value in ir]
    red_ac_rms = (sum([value ** 2 for value in red_ac]) / len(red_ac)) ** 0.5
    ir_ac_rms = (sum([value ** 2 for value in ir_ac]) / len(ir_ac)) ** 0.5
    ratio = red_ac_rms / ir_ac_rms
    spo2 = 110 - 25 * ratio
    return int(spo2)


def home(request):
    sensors = Sensors.objects.all().order_by('-id')[:200]

    temperature = []
    ecg = []
    gsr = []
    hr = []
    ir = []
    red = []
    spo2 = []

    for sensor in sensors:
        temperature.append(sensor.patient_temp)
        ecg.append(sensor.ecg)
        gsr.append(sensor.gsr)
        hr.append(sensor.hr)
        ir.append(sensor.ir)
        red.append(sensor.red)

    for i in range(0, len(ir), 10):
        ir_chunk = ir[i:i + 50]
        red_chunk = red[i:i + 50]
        spo2_val = calculate_spo2(ir_chunk, red_chunk)
        spo2.append(spo2_val)

    return render(request, 'home.html',
                  {"y": temperature[:5], "ecg": ecg[:51], "gsr": gsr[:51], "hr": hr[:5], "spo2": spo2[:5],
                   "ecg_cnt": list(range(51))})


def exportData(request):
    obj = Sensors.objects.all().order_by('-id')
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="somefilename.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(["Date and Time", "Temperature", "ECG", "GSR", "HR", "IR", "RED"])

    for index, obj in enumerate(obj):
        writer.writerow([obj.time, obj.patient_temp, obj.ecg, obj.gsr, obj.hr, obj.ir, obj.red])

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
