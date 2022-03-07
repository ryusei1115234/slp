
from django.db import models
from django.utils import timezone


class Employee(models.Model):
    name = models.CharField(max_length=100)
    regist_date = models.DateTimeField(default=timezone.now)
    status =models.CharField(max_length=100,default=True)
    time_restraint_day =models.CharField(max_length=100,default=True)
    time_rest_day =models.CharField(max_length=100,default=0)
    

class basic_inf(models.Model):
    name = models.CharField(max_length=100)
    regist_date = models.DateTimeField(default=timezone.now)
    actual_working_hour =models.CharField(max_length=100,default=0)
    transportation_expenses =models.CharField(max_length=100,default=0)
    hourly_wage =models.CharField(max_length=100,default=1000)
    sum_pay =models.CharField(max_length=100,default=0)

   