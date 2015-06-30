# Stdlib imports
import json

# Core Django imports
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Third-party lib imports
import numpy as np

# Apps imports
from apps.solutions.models import WaterUse
from apps.solutions.service import WaterUseAnalyzer

# Create your views here.
def water_use_analyzer_demo(request):
    # Pagination
    objs = WaterUse.objects.all()
    paginator = Paginator(objs, 10)  # show 10 rows per page
    page = request.GET.get('page')
    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        records = paginator.page(1)
    except EmptyPage:
        records = paginator.page(paginator.num_pages)
    
    context = {"page_title": "AQUAM | Water Use Analyzer", "records": records,}
    
    if request.is_ajax():
        target_template = "solutions/partial/water-use-table.html"
    else:
        target_template = "solutions/demo/water-use-analyzer.html"
    
    return render_to_response(target_template, context, context_instance=RequestContext(request))


def get_water_use(request):
    analyzer = WaterUseAnalyzer(WaterUse)
    result = analyzer.get_water_use()
    return JsonResponse(result)

def get_horizontal_length(request):
    analyzer = WaterUseAnalyzer(WaterUse)
    result = analyzer.get_horizontal_length()
    return JsonResponse(result)

def get_water_use_per_horizontal_foot(request):
    analyzer = WaterUseAnalyzer(WaterUse)
    result = analyzer.get_water_use_per_horizontal_foot()
    return JsonResponse(result)

def get_annual_water_use(request):
    analyzer = WaterUseAnalyzer(WaterUse)
    result = analyzer.get_annual_water_use()
    return HttpResponse(json.dumps(result), content_type="application/json")

def get_annual_horizontal_feet_drilled(request):
    analyzer = WaterUseAnalyzer(WaterUse)
    result = analyzer.get_annual_horizontal_feet_drilled()
    return HttpResponse(json.dumps(result), content_type="application/json")

def get_annual_bbls_ft_metric(request):
    analyzer = WaterUseAnalyzer(WaterUse)
    result = analyzer.get_annual_bbls_ft_metric()
    return HttpResponse(json.dumps(result), content_type="application/json")

def get_linear_fitting(request):
    analyzer = WaterUseAnalyzer(WaterUse)
    result = analyzer.get_quadratic_fitting()
    return JsonResponse(result)

def get_quadratic_fitting(request):
    analyzer = WaterUseAnalyzer(WaterUse)
    result = analyzer.get_cubic_fitting()
    return JsonResponse(result)

def get_cubic_fitting(request):
    analyzer = WaterUseAnalyzer(WaterUse)
    result = analyzer.get_linear_fitting()
    return JsonResponse(result)