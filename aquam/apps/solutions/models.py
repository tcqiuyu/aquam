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

class ProducedWater(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(auto_now=False, auto_now_add=False)
    well_1 = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    well_2 = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    well_3 = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    well_4 = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    well_5 = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    well_6 = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    well_7 = models.DecimalField(max_digits=20, decimal_places=0, null=True)

class WaterQuality(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(auto_now=False, auto_now_add=False)
    wells_number = models.IntegerField()
    volume = models.DecimalField(max_digits=20, decimal_places=3, null=True)
    tds = models.DecimalField(max_digits=20, decimal_places=3, null=True)
    sodium = models.DecimalField(max_digits=20, decimal_places=3, null=True)
    chloride = models.DecimalField(max_digits=20, decimal_places=3, null=True)
    calcium = models.DecimalField(max_digits=20, decimal_places=3, null=True)
    iron = models.DecimalField(max_digits=20, decimal_places=3, null=True)

class NobleWells(models.Model):
    id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=100, null=True)
    township = models.CharField(max_length=10, null=True)
    range = models.CharField(max_length=10, null=True)
    section = models.IntegerField(null=True)
    idp = models.CharField(max_length=20, null=True)
    area = models.CharField(max_length=10, null=True)
    api = models.CharField(max_length=20, null=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=6)
    longtitude = models.DecimalField(max_digits=20, decimal_places=6)
    reservoir = models.CharField(max_length=20, null=True)
    well_trajectory = models.CharField(max_length=20, null=True)
    stages = models.IntegerField(null=True)
    frac_fluid = models.CharField(max_length=20, null=True)
    frac_date = models.DateField(auto_now=False, auto_now_add=False)
    water_use = models.DecimalField(max_digits=20, decimal_places=1)