# Stdlib imports
import json
import datetime

# Core Django imports
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Apps imports
from apps.solutions.models import WaterUse, ProducedWater, WaterQuality, WaterTreatment
from apps.solutions.tools import WaterUseAnalyzer, ProducedWaterModeler, WaterQualityAnalyzer, WaterTreatmentAnalyzer


# Water Use Analyzer VIEWS & JSON APIs
def water_use_analyzer(request):
    objs = WaterUse.objects.all()
    paginator = Paginator(objs, 10)  # show 10 rows per page
    page = request.GET.get("page")
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
        target_template = "solutions/water-use-analyzer.html"
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

# Produced Water Modeler Views & JSON APIs
def produced_water_modeler(request):
    objs = ProducedWater.objects.all()
    paginator = Paginator(objs, 10)  # show 10 rows per page
    page = request.GET.get("page")
    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        records = paginator.page(1)
    except EmptyPage:
        records = paginator.page(paginator.num_pages)
    context = {"page_title": "AQUAM | Produced Water Modeler", "records": records,}
    if request.is_ajax():
        target_template = "solutions/partial/produced-water-table.html"
    else:
        target_template = "solutions/produced-water-modeler.html"
    return render_to_response(target_template, context, context_instance=RequestContext(request))

def get_arp_model(request):
    modeler = ProducedWaterModeler(ProducedWater)
    result = modeler.get_arp_model()
    return JsonResponse(result)
    
def get_arp_prediction(request):
    modeler = ProducedWaterModeler(ProducedWater)
    # get the parameters from request later
    start_date = datetime.date(2014,3, 1)
    end_date = datetime.date(2014, 6, 1)
    wells_num_per_month = 5
    arp_model = {"Q0": 549.7142, "b": 0.9380, "D": 0.1299}
    result = modeler.get_arp_prediction(arp_model, start_date, end_date, wells_num_per_month)
    return JsonResponse(result)
    
# Water Quality Analyzer Views & JSON APIs
def water_quality_analyzer(request):
    analyzer = WaterQualityAnalyzer(WaterQuality)
    location = "Greeley Crescent"
    #analyzer.set_database(location)
    context = {"page_title": "AQUAM | Water Quality Analyzer"}
    return render_to_response("solutions/water-quality-analyzer.html", context, context_instance=RequestContext(request))

def get_water_quality_values(request):
    analyzer = WaterQualityAnalyzer(WaterQuality)
    result = analyzer.get_water_quality_values()
    return HttpResponse(json.dumps(result), content_type="application/json")

def water_treatment_analyzer(request):
    analyzer = WaterTreatmentAnalyzer(WaterTreatment)
    location_name = "Core"
    constituent_name = "TDS"
    end_day = 1000
    stages = 20
    coefficients = analyzer.coefficients
    methods = analyzer.methods
    constants = analyzer.constants
    parameters = analyzer.parameters
    percent = 1.0
    #analyzer.set_database_result(end_day, coefficients, methods, constants, parameters, stages, location_name, constituent_name, percent)
    context = {"page_title": "AQUAM | Water Treatment Analyzer"}
    return render_to_response("solutions/water-treatment-analyzer.html", context, context_instance=RequestContext(request))

def get_treatment_iteration_result(request):
    analyzer = WaterTreatmentAnalyzer(WaterTreatment)
    location_name = "Core"
    constituent_name = "TDS"
    end_day = 1000
    stages = 20
    coefficients = analyzer.coefficients
    methods = analyzer.methods
    constants = analyzer.constants
    parameters = analyzer.parameters
    percent = 1.0
    result = analyzer.get_treatment_iteration_result(end_day, coefficients, methods, constants, parameters, stages, location_name, constituent_name, percent)
    return HttpResponse(json.dumps(result), content_type="application/json")