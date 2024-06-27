from datetime import datetime

from django.db import models


# Create your models here.

class Sensors(models.Model):
    patient_temp = models.FloatField(null=True, blank=True)
    ecg = models.FloatField(null=True, blank=True)
    time = models.DateTimeField(default=datetime.now())
