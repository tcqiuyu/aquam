from django.db import models

# Create your models here.

class WaterUse(models.Model):
    id = models.AutoField(primary_key=True)
    api = models.CharField(max_length=20, null=True)
    frac_date = models.DateField(auto_now=False, auto_now_add=False)
    state = models.CharField(max_length=20, null=True)
    county = models.CharField(max_length=20, null=True)
    operator = models.CharField(max_length=100, null=True)
    well_name = models.CharField(max_length=50, null=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=6)
    longtitude = models.DecimalField(max_digits=20, decimal_places=6)
    datum = models.CharField(max_length=20, null=True)
    well_trajectory = models.CharField(max_length=20, null=True)
    horizontal_length = models.DecimalField(max_digits=20, decimal_places=0)
    water_use = models.DecimalField(max_digits=20, decimal_places=3)
