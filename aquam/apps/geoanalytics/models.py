from django.contrib.gis.db import models

# Create your models here.
class GeoWaterUse(models.Model):
    id = models.AutoField(primary_key=True)
    geometry = models.PointField()
    api = models.CharField(max_length=20, null=False)
    well_name = models.CharField(max_length=100, null=True)
    frac_date = models.DateField(auto_now=False, auto_now_add=False)
    state = models.CharField(max_length=20, null=True)
    county = models.CharField(max_length=20, null=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=6)
    longitude = models.DecimalField(max_digits=20, decimal_places=6)
    horizontal_length = models.DecimalField(max_digits=20, decimal_places=3)
    water_use = models.DecimalField(max_digits=20, decimal_places=3)
    objects = models.GeoManager()
    
    class Meta:
        ordering = ["api"]
        

class GeoProducedWater(models.Model):
    id = models.AutoField(primary_key=True)
    geometry = models.PointField()
    api = models.CharField(max_length=20, null=False)
    well_name = models.CharField(max_length=100, null=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=6)
    longitude = models.DecimalField(max_digits=20, decimal_places=6)
    volume_date = models.DateField(auto_now=False, auto_now_add=False)
    h2o_volume = models.DecimalField(max_digits=10, decimal_places=2)
    days_on = models.PositiveIntegerField()
    is_prediction = models.BooleanField()
    objects = models.GeoManager()
    
    class Meta:
        ordering = ["api"]