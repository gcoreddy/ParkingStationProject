from __future__ import unicode_literals
from django.db import models as m
from django.utils import timezone

class TariffPlan(m.Model):
	plan = m.CharField(max_length=10,primary_key=True)
	cost = m.CharField(max_length=100, default=10)
	freetime = m.CharField(max_length=100,default=15)
	
class carDataDetails(m.Model):
    carno = m.CharField(max_length=100,primary_key=True)
    tariff_plan = m.CharField(max_length=100,default="Hourly")
    inTime = m.CharField(max_length=100,default="")
    location = m.CharField(max_length=100,default="")
    outTime = m.CharField(max_length=100,default="")
	
class ParkingLevel(m.Model):
    level_num = m.CharField(max_length=50,primary_key=True)
    total_spots   = m.CharField(max_length=50)
    free_spots    = m.TextField(null=True)
    occupied_spots = m.TextField(null=True)