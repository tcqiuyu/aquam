# Stdlib imports
import json

# Django imports
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, JsonResponse

# Apps imports
from apps.geoanalytics.models import GeoWaterUse
from apps.geoanalytics.tools import WaterUseGeoanalyzer, WaterUseHeatmapper


# Create your views here.
def water_use_geoanalyzer(request):
    context = {"page_title": "AQUAM | Water Use Geoanalyzer"}
    return render_to_response("geoanalytics/water-use-geoanalyzer.html", context, context_instance=RequestContext(request))

def get_geo_water_use(request):
    analyzer = WaterUseGeoanalyzer(GeoWaterUse)
    result = analyzer.get_geo_water_use()
    return HttpResponse(json.dumps(result), content_type="application/json")


def water_use_heatmapper(request):
    context = {"page_title": "AQUAM | Water Use Heatmapper"}
    return render_to_response("geoanalytics/water-use-heatmapper.html", context, context_instance=RequestContext(request))

def get_heat_water_use(request):
    heatmapper = WaterUseHeatmapper(GeoWaterUse)
    result = heatmapper.get_heat_water_use()
    return HttpResponse(json.dumps(result), content_type="application/json")
    