# Third-party lib imports
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from scipy import optimize
import numpy as np

# Apps imports
from models import WaterUse


# json service for Water Use Analyzer
@api_view(["GET"])
class WaterUseSerializer(serializers.ModelSerializer):
    water_use_per_horizontal_foot = serializers.SerializerMethodField("get_water_use_per_horizontal_foot")
    
    class Meta:
        model = WaterUse
        fields = ("water_use", "horizontal_length", "water_use_per_horizontal_foot")
    
    def get_water_use_per_horizontal_foot(self, obj):
        return obj.water_use / obj.horizontal_length
    

class AnnualWaterUseSerializer():
    annual_average_water_use = serializers.SerializerMethodField("get_annual_water_use")
    
    class Meta:
        model = WaterUse
        fields = ("annual_average_water_use")
    
    def get_annual_water_use(self, obj):
        pass
    
    def get_annual_average_horizontal_feet(self, obj):
        pass
    
    def get_annual_bbls_ft_metric(self, obj):
        pass


def annual_averge_water_use(frac_date, water_use):
    frac_years = np.array([dt.year for dt in frac_date])
    unique_years = np.unique(frac_years)
    avg_water_use = []
    std_water_use = []
    for year in unique_years:
        indx = np.where(frac_years == year, 1, 0)
        temp = [x for x in np.multiply(water_use, indx) if x]
        avg_water_use.append(np.mean(temp))
        std_water_use.append(np.std(temp))
    return unique_years, avg_water_use, std_water_use
    
    
def annual_averge_horizontal_length(frac_date, horizontal_length):
    frac_years = np.array([dt.year for dt in frac_date])
    unique_years = np.unique(frac_years)
    avg_horizontal_length = []
    std_horizontal_length = []
    for year in unique_years:
        indx = np.where(frac_years == year, 1, 0)
        temp = [x for x in np.multiply(horizontal_length, indx) if x]
        avg_horizontal_length.append(np.mean(temp))
        std_horizontal_length.append(np.std(temp))
    return unique_years, avg_horizontal_length, std_horizontal_length


def annual_averge_water_use_per_foot(frac_date, water_use_per_foot):
    frac_years = np.array([dt.year for dt in frac_date])
    unique_years = np.unique(frac_years)
    avg_water_use_per_foot = []
    std_water_use_per_foot = []
    for year in unique_years:
        indx = np.where(frac_years == year, 1, 0)
        temp = [x for x in np.multiply(water_use_per_foot, indx) if x]
        avg_water_use_per_foot.append(np.mean(temp))
        std_water_use_per_foot.append(np.std(temp))
    return unique_years, avg_water_use_per_foot, std_water_use_per_foot


def model_parameters(values, wells_number):
    record_date = []
    raw_produced_water = np.zeros([wells_number, len(values)])
    for i in range(len(values)):
        record_date.append(values[i][1])
        for j in range(wells_number):
            if values[i][j + 2] is not None:
                raw_produced_water[j][i] = float(values[i][j + 2])
    produced_water = np.zeros([wells_number, len(values)])
    for j in range(wells_number):
        loc = 0
        for i in range(len(values)):
            if raw_produced_water[j][i] != 0:
                loc = i;
                break;
        for i in range(len(values) - loc):
            produced_water[j][i] = raw_produced_water[j][i + loc]
    
    # build the Arp model
    avg_produced_water = np.zeros(len(values))
    for i in range(len(values)):
        produced_water_transpose = np.transpose(produced_water)
        temp_list = [x for x in produced_water_transpose[i] if x != 0]
        if temp_list:
            avg_produced_water[i] = np.mean(temp_list)
        else:
            avg_produced_water[i] = 0
    Q0 = avg_produced_water[0]
    def arp(x, D, b):
        return Q0 / (1 + D * x) ** (1 / b)
    days = np.array([x for x in range(1, len(values) + 1)])
    params = optimize.curve_fit(arp, days, avg_produced_water)
    D, b = params[0]
    yfit = arp(days, D, b)
    return days, avg_produced_water, D, b, yfit
