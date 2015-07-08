from django.db import models


# Create your models here.
class WaterUse(models.Model):
    id = models.AutoField(primary_key=True)
    api = models.CharField(max_length=20, null=False)
    frac_date = models.DateField(auto_now=False, auto_now_add=False)
    state = models.CharField(max_length=20, null=True)
    county = models.CharField(max_length=20, null=True)
    well_name = models.CharField(max_length=100, null=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=6)
    longtitude = models.DecimalField(max_digits=20, decimal_places=6)
    horizontal_length = models.DecimalField(max_digits=20, decimal_places=3)
    water_use = models.DecimalField(max_digits=20, decimal_places=3)
    
    class Meta:
        ordering = ["api"]
    
    
class ProducedWater(models.Model):
    id = models.AutoField(primary_key=True)
    days = models.PositiveIntegerField(null=False)
    well_1 = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    well_2 = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    well_3 = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    well_4 = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    well_5 = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    well_6 = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    well_7 = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    
    class Meta:
        ordering = ["days"]
    
    
class WaterQuality(models.Model):
    id = models.AutoField(primary_key = True)
    location = models.CharField(max_length=50, null=False)
    date = models.DateField(auto_now=False, auto_now_add=False, null=False)
    wells_number = models.PositiveIntegerField(null=False)
    tds = models.DecimalField(max_digits=20, decimal_places=3, null=True)
    chloride = models.DecimalField(max_digits=20, decimal_places=3, null=True)
    sodium = models.DecimalField(max_digits=20, decimal_places=3, null=True)
    calcium = models.DecimalField(max_digits=20, decimal_places=3, null=True)
    iron = models.DecimalField(max_digits=20, decimal_places=3, null=True)
    volume = models.DecimalField(max_digits=20, decimal_places=3, null=True)
    
    class Meta:
        ordering = ["id"]
    

class WaterTreatment(models.Model):
    id = models.AutoField(primary_key = True)
    location = models.CharField(max_length=50, null=False)
    days = models.PositiveIntegerField(null=False)
    stages = models.PositiveIntegerField(null=False)
    constituent = models.CharField(max_length=20, null=False)
    quality = models.DecimalField(max_digits=20, decimal_places=3, null=True)
    vfrac = models.DecimalField(max_digits=20, decimal_places=3, null=True)
    wqfrac_cf = models.DecimalField(max_digits=20, decimal_places=3, null=True)
    wqfrac_sc = models.DecimalField(max_digits=20, decimal_places=3, null=True)
    wqfrac_ro = models.DecimalField(max_digits=20, decimal_places=3, null=True)
    vfresh_cf = models.DecimalField(max_digits=20, decimal_places=3, null=True)
    vfresh_sc = models.DecimalField(max_digits=20, decimal_places=3, null=True)
    vfresh_ro = models.DecimalField(max_digits=20, decimal_places=3, null=True)
    vfresh_vrec_cf = models.DecimalField(max_digits=20, decimal_places=3, null=True)
    vfresh_vrec_sc = models.DecimalField(max_digits=20, decimal_places=3, null=True)
    vfresh_vrec_ro = models.DecimalField(max_digits=20, decimal_places=3, null=True)
    
    class Meta:
        ordering = ["id"]