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