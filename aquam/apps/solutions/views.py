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
    context = {"page_title": "AQUAM | Water Use Analyzer", "records": records, }
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
    context = {"page_title": "AQUAM | Produced Water Modeler", "records": records, }
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
    input = request.__str__().split("get-arp-prediction/")[1].split("/")
    wells_num_per_month = int(input[0])
    # start_date = datetime.date(2014, 3, 1)
    # end_date = datetime.date(2014, 6, 1)
    start_date_str = input[1].split("-")
    end_date_str = input[2].split("'")[0].split("-")
    start_date=datetime.date(int(start_date_str[1]), int(start_date_str[0]), 1)
    end_date=datetime.date(int(end_date_str[1]), int(end_date_str[0]), 1)
    arp_model = {"Q0": 549.7142, "b": 0.9380, "D": 0.1299}
    result = modeler.get_arp_prediction(arp_model, start_date, end_date, wells_num_per_month)
    return JsonResponse(result)


# Water Quality Analyzer Views & JSON APIs
def water_quality_analyzer(request):
    #analyzer.set_database(location)
    context = {"page_title": "AQUAM | Water Quality Analyzer"}
    return render_to_response("solutions/water-quality-analyzer.html", context, context_instance=RequestContext(request))


def get_water_quality_settings(request):
    analyzer = WaterQualityAnalyzer(WaterQuality)
    result = analyzer.get_water_quality_settings()
    return HttpResponse(json.dumps(result), content_type="application/json")

def get_water_quality_result(request):
    location = request.__str__().split("/")[4].split("'")[0]
    location_name = location.replace("%20", " ")
    analyzer = WaterQualityAnalyzer(WaterQuality)
    # location_name = "Greeley Crescent"
    parameter = analyzer.parameters[location_name]
    coefficient = analyzer.coefficients[location_name]
    result = analyzer.get_water_quality_result(parameter, coefficient, location_name)
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
    # analyzer.set_database_result(end_day, coefficients, methods, constants, parameters, stages, location_name, constituent_name, percent)
    context = {"page_title": "AQUAM | Water Treatment Analyzer"}
    return render_to_response("solutions/water-treatment-analyzer.html", context,
                              context_instance=RequestContext(request))

def get_water_treatment_general_settings(request):
    analyzer = WaterTreatmentAnalyzer(request)
    settings = analyzer.get_water_treatment_general_settings()
    return HttpResponse(json.dumps(settings), content_type="application/json")

def get_water_treatment_location_settings(request):
    analyzer = WaterTreatmentAnalyzer(request)
    settings = analyzer.get_water_treatment_location_settings()
    return HttpResponse(json.dumps(settings), content_type="application/json")

def get_treatment_iteration_result(request):
    analyzer = WaterTreatmentAnalyzer(WaterTreatment)
    input = request.__str__().split("get-water-treatment-iteration-result/")[1]
    input = input.split("/")
    location_name = input[0]
    constitutent_name = input[1]
    end_day = int(input[2])
    stages = int(input[3])
    percent = float(input[4].split("'")[0])
    coefficients = analyzer.coefficients
    methods = analyzer.methods
    constants = analyzer.constants
    parameters = analyzer.parameters
    result = analyzer.get_treatment_iteration_result(end_day, coefficients, methods, constants, parameters, stages,
                                                     location_name, constitutent_name, percent)
    return HttpResponse(json.dumps(result), content_type="application/json")