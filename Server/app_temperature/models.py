from datetime import datetime

from django.db import models


# Create your models here.

class Sensors(models.Model):
    patient_temp = models.FloatField(null=True, blank=True)
    ecg = models.FloatField(null=True, blank=True)
    gsr = models.FloatField(null=True, blank=True)
    hr = models.FloatField(null=True, blank=True)
    ir = models.FloatField(null=True, blank=True,default=0)
    red = models.FloatField(null=True, blank=True,default=0)
    time = models.DateTimeField(default=datetime.now())
