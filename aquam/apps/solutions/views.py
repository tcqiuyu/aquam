# Std lib imports
import json

# Core Django imports
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Third-party lib imports
import numpy as np

# Apps imports
from apps.solutions.models import WaterUse


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
    
    # histogram for per well
    water_use_count, water_use_bins = np.histogram(water_use, bins=10)
    water_use_mean = np.mean(water_use)
    water_use_std = np.std(water_use)
    horizontal_length_count, horizontal_length_bins = np.histogram(horizontal_length, bins=10)
    horizontal_length_mean = np.mean(horizontal_length)
    horizontal_length_std = np.std(horizontal_length)
    water_use_per_foot_count, water_use_per_foot_bins = np.histogram(water_use_per_foot, bins=10)
    water_use_per_foot_mean = np.mean(water_use_per_foot)
    water_use_per_foot_std = np.mean(water_use_per_foot)
    
    # histogram for annual average
    # unique_years, avg_water_use, std_water_use = compute.annual_averge_water_use(frac_date, water_use)
    # unique_years, avg_horizontal_length, std_horizontal_length = compute.annual_averge_horizontal_length(frac_date, horizontal_length)
    # unique_years, avg_water_use_per_foot, std_water_use_per_foot = compute.annual_averge_water_use_per_foot(frac_date, water_use_per_foot)
    
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
