
from django.core.serializers import serialize


class WaterUseGeoanalyzer():
    """
    Used for providing the results computed on the base of Geo Water Use Model
    """
    def __init__(self, model):
        self.model = model
    
    def get_geo_water_use(self):
        objs = self.model.objects.all()
        result = serialize("geojson", objs)
        return result