# Core Django imports
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse

# Third-party lib imports
import numpy as np

# Apps imports
from apps.solutions.models import WaterUse
import service as solutions_service

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
    
    # extract & clean data
    values = WaterUse.objects.values_list("frac_date", "water_use", "horizontal_length")
    frac_date = []
    water_use = np.empty(len(values), dtype=float)
    horizontal_length = np.empty(len(values), dtype=float)
    for i in range(len(values)):
        frac_date.append(values[i][0])
        water_use[i] = float(values[i][1])
        horizontal_length[i] = float(values[i][2])
    water_use_per_foot = np.divide(water_use, horizontal_length)
    
    # polyfit & evaluation
    p = np.polyfit(horizontal_length, water_use, 1)
    yfit = np.polyval(p, horizontal_length)
    ss_total = (len(water_use) - 1) * np.var(water_use)
    ss_resid = np.dot(np.subtract(water_use, yfit), np.subtract(water_use, yfit))
    r2 = 1 - (ss_resid / ss_total)
    
    context = {"page_title": "AQUAM | Water Use Analyzer",
               "records": records,
               "frac_date": frac_date,
               "water_use": water_use,
               "horizontal_length": horizontal_length,
               "water_use_per_foot": water_use_per_foot,
               "r2": r2,
    }
    
    if request.is_ajax():
        target_template = "solutions/partial/water-use-table.html"
    else:
        target_template = "solutions/demo/water-use-analyzer.html"
    
    return render_to_response(target_template, context, context_instance=RequestContext(request))


def water_use_json(request):
    water_use = solutions_service.list_water_use()
    context = {"water_use": water_use}
    return JsonResponse(context)

def horizontal_length_json(request):
    horizontal_length = solutions_service.list_horizontal_length()
    context = {"horizontal_length": horizontal_length}
    return JsonResponse(context)