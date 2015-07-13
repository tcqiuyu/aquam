
# Django imports
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, JsonResponse

# Apps imports
from apps.geoanalytics.models import GeoWaterUse


# Create your views here.
def water_use_geoanalyzer(request):
    objs = GeoWaterUse.objects.filter(county="Karnes")
    context = {"page_title": "AQUAM | Water Use Geoanalyzer", "objs": objs}
    return render_to_response("geoanalytics/water-use-geoanalyzer.html", context, context_instance=RequestContext(request))