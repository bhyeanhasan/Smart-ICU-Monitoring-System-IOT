from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from app_temperature.models import Sensors
from datetime import datetime
import csv


def calculate_spo2(ir, red):
	# Calculate the DC and AC components of the signals
	red_dc = sum(red) / len(red) + 1
	ir_dc = sum(ir) / len(ir) + 1
	red_ac = [value - red_dc for value in red]
	ir_ac = [value - ir_dc for value in ir]

	# Calculate RMS of AC components
	red_ac_rms = (sum([value ** 2 for value in red_ac]) / len(red_ac)) ** 0.5
	ir_ac_rms = (sum([value ** 2 for value in ir_ac]) / len(ir_ac)) ** 0.5

	# Calculate ratio of AC components
	ratio = red_ac_rms / ir_ac_rms

	# Apply a calibration equation to calculate SpO2
	spo2 = 110 - 25 * ratio  # This is a simplification; calibration is usually more complex

	return int(spo2)


def home(request):
	temperatures = Sensors.objects.all().order_by('-id')[:5]
	x = []
	y = []
	z = []
	hr = []
	for index, temp in enumerate(temperatures):
		x.append(index)
		y.append(temp.patient_temp)
		hr.append(temp.hr)
		z.append(temp.time)

	ecg_obj = Sensors.objects.all().order_by('-id')[:50]
	ecg = []
	ecg_cnt = []
	gsr = []

	for index, obj in enumerate(ecg_obj):
		ecg.append(obj.ecg)
		gsr.append(obj.gsr)
		ecg_cnt.append(index)

	ir = []
	red = []

	spo2_lst = []

	spdata = Sensors.objects.all()
	for ob in spdata:
		ir.append(ob.ir)
		red.append(ob.red)

	for i in range(0, len(ir), 50):
		ir_chunk = ir[i:i + 50]
		red_chunk = red[i:i + 50]
		spo2 = calculate_spo2(ir_chunk, red_chunk)
		spo2_lst.append(spo2)

	# spo2_lst = [93,92,94,93,96,97,94]
	# hr = [77,78,80,78,81,82,76]
	# y = [90,91,93,95,93,90,96]


	return render(request, 'home.html',
				  {"x": x, "y": y, "z": z, "ecg": ecg, "ecg_cnt": ecg_cnt, "gsr": gsr, "hr": hr, "spo2": spo2_lst})


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
