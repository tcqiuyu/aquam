# Stdlib imports
import datetime
import calendar
import math

# Third-party lib imports
from scipy import optimize
import numpy as np


class WaterUseAnalyzer():
    """
    Used for providing the results computed on the base of Water Use Model
    """
    def __init__(self, model):
        self.model = model
    
    def get_water_use(self):
        values_list = self.model.objects.values_list("water_use")
        water_use = np.empty(len(values_list), dtype=float)
        for i in range(len(values_list)):
            water_use[i] = values_list[i][0]
        mean = round(np.mean(water_use), 3)
        std = round(np.std(water_use), 3)
        result = {"water_use": water_use.tolist(), "water_use_mean": mean, "water_use_std": std}
        return result
    
    def get_horizontal_length(self):
        values_list = self.model.objects.values_list("horizontal_length")
        horizontal_length = np.empty(len(values_list), dtype=int)
        for i in range(len(values_list)):
            horizontal_length[i] = int(values_list[i][0])
        mean = round(np.mean(horizontal_length), 3)
        std = round(np.std(horizontal_length), 3)
        result = {"horizontal_length": horizontal_length.tolist(), "horizontal_length_mean": mean, "horizontal_length_std": std}
        return result
    
    def get_water_use_per_horizontal_foot(self):
        values_list = self.model.objects.values_list("water_use", "horizontal_length")
        water_use = np.empty(len(values_list), dtype=float)
        horizontal_length = np.empty(len(values_list), dtype=float)
        for i in range(len(values_list)):
            water_use[i] = values_list[i][0]
            horizontal_length[i] = values_list[i][1]
        water_use_per_horizontal_foot = np.divide(water_use, horizontal_length)
        mean = round(np.mean(water_use_per_horizontal_foot), 3)
        std = round(np.std(water_use_per_horizontal_foot), 3)
        result = {"water_use_per_horizontal_foot": water_use_per_horizontal_foot.tolist(), "water_use_per_horizontal_foot_mean": mean, "water_use_per_horizontal_foot_std": std}
        return result
    
    def get_annual_water_use(self):
        values_list = self.model.objects.values_list("frac_date", "water_use")
        frac_years = np.empty(len(values_list), dtype=int)
        water_use = np.empty(len(values_list), dtype=float)
        for i in range(len(values_list)):
            frac_date = values_list[i][0]
            frac_years[i] = frac_date.year
            water_use[i] = values_list[i][1]
        years = np.unique(frac_years)
        annual_water_use = []
        for year in years:
            indx = np.where(frac_years == year, 1, 0)
            values = [x for x in np.multiply(water_use, indx) if x]
            annual_water_use.append((np.mean(values), np.std(values)))
        result = []
        for a, b in zip(years, annual_water_use):
            obj = {"year": a, "mean": round(b[0], 3), "std": round(b[1], 3)}
            result.append(obj)
        return result
    
    def get_annual_horizontal_feet_drilled(self):
        values_list = self.model.objects.values_list("frac_date", "water_use")
        frac_years = np.empty(len(values_list), dtype=int)
        horizontal_length = np.empty(len(values_list), dtype=float)
        for i in range(len(values_list)):
            frac_date = values_list[i][0]
            frac_years[i] = frac_date.year
            horizontal_length[i] = values_list[i][1]
        years = np.unique(frac_years)
        annual_horizontal_feet_drilled = []
        for year in years:
            indx = np.where(frac_years == year, 1, 0)
            values = [x for x in np.multiply(horizontal_length, indx) if x]
            annual_horizontal_feet_drilled.append((np.mean(values), np.std(values)))
        result = []
        for a, b in zip(years, annual_horizontal_feet_drilled):
            obj = {"year": a, "mean": round(b[0], 3), "std": round(b[1], 3)}
            result.append(obj)
        return result
    
    def get_annual_bbls_ft_metric(self):
        values_list = self.model.objects.values_list("frac_date", "water_use", "horizontal_length")
        frac_years = np.empty(len(values_list), dtype=int)
        water_use = np.empty(len(values_list), dtype=float)
        horizontal_length = np.empty(len(values_list), dtype=float)
        for i in range(len(values_list)):
            frac_date = values_list[i][0]
            frac_years[i] = frac_date.year
            water_use[i] = values_list[i][1]
            horizontal_length[i] = values_list[i][2]
        water_use_per_horizontal_foot = np.divide(water_use, horizontal_length)
        years = np.unique(frac_years)
        annual_bbls_ft_metric = []
        for year in years:
            indx = np.where(frac_years == year, 1, 0)
            values = [x for x in np.multiply(water_use_per_horizontal_foot, indx) if x]
            annual_bbls_ft_metric.append((np.mean(values), np.std(values)))
        result = []
        for a, b in zip(years, annual_bbls_ft_metric):
            obj = {"year": a, "mean": round(b[0], 3), "std": round(b[1], 3)}
            result.append(obj)
        return result
    
    def get_linear_fitting(self):
        values_list = self.model.objects.values_list("water_use", "horizontal_length")
        water_use = np.empty(len(values_list), dtype=float)
        horizontal_length = np.empty(len(values_list), dtype=float)
        for i in range(len(values_list)):
            water_use[i] = values_list[i][0]
            horizontal_length[i] = values_list[i][1]
        p = np.polyfit(horizontal_length, water_use, 1)
        yfit = np.polyval(p, horizontal_length)
        ss_total = (len(water_use) - 1) * np.var(water_use)
        ss_resid = np.dot(np.subtract(water_use, yfit), np.subtract(water_use, yfit))
        r2 = 1 - (ss_resid / ss_total)
        data = []
        for x, y, z in zip(horizontal_length, water_use, yfit):
            obj = {"horizontal_length": x, "water_use": y, "fitted_water_use": z}
            data.append(obj)
        result = {"data": data, "r2": round(r2, 4)}
        return result
    
    def get_quadratic_fitting(self):
        values_list = self.model.objects.values_list("water_use", "horizontal_length")
        water_use = np.empty(len(values_list), dtype=float)
        horizontal_length = np.empty(len(values_list), dtype=float)
        for i in range(len(values_list)):
            water_use[i] = values_list[i][0]
            horizontal_length[i] = values_list[i][1]
        p = np.polyfit(horizontal_length, water_use, 2)
        yfit = np.polyval(p, horizontal_length)
        ss_total = (len(water_use) - 1) * np.var(water_use)
        ss_resid = np.dot(np.subtract(water_use, yfit), np.subtract(water_use, yfit))
        r2 = 1 - (ss_resid / ss_total)
        data = []
        for x, y, z in zip(horizontal_length, water_use, yfit):
            obj = {"horizontal_length": x, "water_use": y, "fitted_water_use": z}
            data.append(obj)
        result = {"data": data, "r2": round(r2, 4)}
        return result
    
    def get_cubic_fitting(self):
        values_list = self.model.objects.values_list("water_use", "horizontal_length")
        water_use = np.empty(len(values_list), dtype=float)
        horizontal_length = np.empty(len(values_list), dtype=float)
        for i in range(len(values_list)):
            water_use[i] = values_list[i][0]
            horizontal_length[i] = values_list[i][1]
        p = np.polyfit(horizontal_length, water_use, 3)
        yfit = np.polyval(p, horizontal_length)
        ss_total = (len(water_use) - 1) * np.var(water_use)
        ss_resid = np.dot(np.subtract(water_use, yfit), np.subtract(water_use, yfit))
        r2 = 1 - (ss_resid / ss_total)
        data = []
        for x, y, z in zip(horizontal_length, water_use, yfit):
            obj = {"horizontal_length": x, "water_use": y, "fitted_water_use": z}
            data.append(obj)
        result = {"data": data, "r2": round(r2, 4)}
        return result


class ProducedWaterModeler():
    """
    Used for providing the ARP modeling results computed on the base of Produecd Water Model
    """
    def __init__(self, model):
        self.model = model
     
    def get_arp_model(self):
        # arp model
        def arp(x, D, b):
            return Q0 / (1 + D * x)**(1/b)
        # fitting
        values_list = self.model.objects.values_list("days", "well_1", "well_2", "well_3", "well_4", "well_5", "well_6", "well_7")
        days = []
        produced_water = np.zeros(len(values_list))
        for i in range(len(values_list)):
            days.append(values_list[i][0])
            values = [float(x) for x in values_list[i][1:] if x > 0]
            if values:
                produced_water[i] = np.mean(values)
            else:
                produced_water[i] = produced_water[i-1]
        Q0 = produced_water[0]
        params = optimize.curve_fit(arp, days, produced_water)
        D, b = params[0]
        yfit = [arp(x, D, b) for x in days ]
        # results
        data = []
        for x, y, z in zip(days, produced_water, yfit):
            obj = {"day": x, "produced_water": y, "fitted_produced_water": z}
            data.append(obj)
        result = {"data": data, "Q0": round(Q0,3), "D": round(D,3), "b": round(b, 3)}
        return result
    
    def get_arp_prediction(self, arp_model, start_date, end_date, wells_num_per_month):
        # day arrays
        start_year = start_date.year
        start_month = start_date.month
        end_year = end_date.year
        end_month = end_date.month
        year_range = end_year - start_year
        month_range = 0
        if year_range == 0:
            month_range = end_month - start_month + 1
        if year_range > 0:
            month_range = 12*(year_range-1) + (12-start_month+1) + end_month
        end_day = calendar.monthrange(end_year, end_month)[1]
        day_range = (datetime.date(end_year, end_month, end_day) - datetime.date(start_year, start_month, 1)).days + 1
        days = 0
        n = 0
        days_arr = np.zeros([day_range, month_range], dtype=int)
        for year in range(start_year, start_year+year_range+1):
            m = 1
            if year == start_year:
                m = start_month
            for month in range(m, 13):
                if datetime.date(year, month, 1) <= datetime.date(end_year, end_month, 1):
                    end_day = calendar.monthrange(end_year, end_month)[1]
                    days = (datetime.date(end_year, end_month, end_day) - datetime.date(year, month, 1)).days + 1
                    for i in range(days):
                        if n < month_range:
                            days_arr[day_range-i-1][n] = days - i
                    n = n + 1
        
        # arp model
        Q0 = arp_model["Q0"]
        b = arp_model["b"]
        D = arp_model["D"]
        
        # produced water arrays
        produced_water_arr = np.zeros([day_range, month_range], dtype=float)
        for j in range(month_range):
            for i in range(day_range):
                t = days_arr[i][j]
                q = 0
                if t > 0:
                    q = Q0 / (1 + D * t)**(1/b)
                produced_water_arr[i][j] = round(q, 3)
        
        # prediction
        day_volume = np.zeros(day_range, dtype=float)
        for i in range(day_range):
            day_volume[i] = np.sum(produced_water_arr[i])
        total_volume = np.sum(day_volume)
        result = {"total_volume": round(total_volume, 3)}
        return result


class WaterQualityAnalyzer():
    """
    Used for providing the water quality results computed based on Water Quality Model
    """
    def __init__(self, model):
        self.model = model
    
    def get_constituents(self):
        constituents = ["TDS", "Sodium", "Chloride", "Calcium", "Iron"]
        return constituents
    
    def get_locations(self):
        locations = ['Undifined', 'Core', 'Mustang', 'Greeley Crescent', 'East Pony', 'West Pony', 'Wells Ranch', 'Commins']
        return locations
    
    def get_fit_equation_coefficients(self):
        coefficients = {"Undifined": {"TDS": "", "Sodium": "", "Chloride": "", "Calcium": "", "Iron": ""}, 
            "Core": {"TDS": (2982.1, 4312.1), "Sodium": (927.91, 1804.4), "Chloride": (1971.8, 1177.2), "Calcium": (61.173, -22.745), "Iron": (0, 53.46)}, 
            "Mustang": {"TDS": (2282.5, 10691), "Sodium": (1601.8, -262.57), "Chloride": (2293, 10729), "Calcium": (52.016, 0.5952), "Iron": (0, 29.75)}, 
            "Greeley Crescent": {"TDS": (2322.1, 6992.7), "Sodium": (787.65, 2556.2), "Chloride": (1512.6, 3583.6), "Calcium": (68.964, -20.551), "Iron": (0, 66.40)}, 
            "East Pony": {"TDS": (4636.6, 1614.5), "Sodium": (2062.2, -928.59), "Chloride": (3000, -361.24), "Calcium": (30.791, -2.6108), "Iron": (0, 32.55)}, 
            "West Pony": {"TDS": (6129.5, 1551.8), "Sodium": (2344.5, 105.16), "Chloride": (4007.2, -961.57), "Calcium": (56.77, -9.5692), "Iron": (0, 76.68)}, 
            "Wells Ranch": {"TDS": (4028.5, 4924.5), "Sodium": (1292.2, 2649), "Chloride": (2084.4, 3499.4), "Calcium": (51.705, 63.865), "Iron": (0, 106.11)}, 
            "Commins": {"TDS": (3244, 16778), "Sodium": (1161.8, 6270.1), "Chloride": (2033.8, 9192), "Calcium": (22.732, 340.34), "Iron": (0, 71.45)}
        }
        return coefficients
    
    def get_arp_model_parameters(self):
        parameters = {"Undifined": {"Fracturing Flowback": {"Q0":0.0, "D":0.0, "b":0.0}, "Transition": {"Q0":0.0, "D":0.0, "b":0.0}, "Produced Water": {"Q0":0.0, "D":0.0, "b":0.0}},
            "Core": {"Fracturing Flowback": {"Q0":1043.04, "D":0.721, "b":0.0}, "Transition": {"Q0":90, "D":0.0529, "b":1.3}, "Produced Water": {"Q0":19.4084, "D":0.00715, "b":1.7}},
            "Mustang": {"Fracturing Flowback": {"Q0":1157.61, "D":0.725, "b":0.0}, "Transition": {"Q0":98.49, "D":0.0693, "b":1.533742331}, "Produced Water": {"Q0":22.99, "D":0.00119, "b":1.46627566}},
            "Greeley Crescent": {"Fracturing Flowback": {"Q0":1406.48, "D":0.863, "b":0.0}, "Transition": {"Q0":74.65, "D":0.011, "b":0.480076812}, "Produced Water": {"Q0":12.93, "D":0.0039, "b":1.6}},
            "East Pony": {"Fracturing Flowback": {"Q0":1590, "D":0.2492, "b":0.947867299}, "Transition": {"Q0":165.92, "D":0.057, "b":1.346982759}, "Produced Water": {"Q0":33.62, "D":0.00837, "b":1.200480192}},
            "West Pony": {"Fracturing Flowback": {"Q0":0.0, "D":0.0, "b":0.0}, "Transition": {"Q0":0.0, "D":0.0, "b":0.0}, "Produced Water": {"Q0":0.0, "D":0.0, "b":0.0}},
            "Wells Ranch": {"Fracturing Flowback": {"Q0":1516, "D":0.0614, "b":0.478011472}, "Transition": {"Q0":176.33, "D":0.0347, "b":1.006}, "Produced Water": {"Q0":29.39, "D":0.0034, "b":0.899280576}},
            "Commins": {"Fracturing Flowback": {"Q0":0.0, "D":0.0, "b":0.0}, "Transition": {"Q0":0.0, "D":0.0, "b":0.0}, "Produced Water": {"Q0":0.0, "D":0.0, "b":0.0}}
        }
        return parameters
    
    def set_fitted_constituent_values(self, location):
        
        def fit_equation(x, alpha, beta):
            return alpha * math.log(x) + beta
        
        values_list = self.model.objects.values_list("date")
        start_date = values_list[0][0]
        coefficients = self.get_fit_equation_coefficients()
        constituents = self.get_constituents()
        objs = self.model.objects.all()
        for obj in objs:
            day = (obj.date - start_date).days + 1
            for constituent in constituents:
                coeff = coefficients[location][constituent]
                alpha = coeff[0]
                beta = coeff[1]
                if constituent == "TDS":
                    val = fit_equation(day, alpha, beta)
                    if val < 0:
                        obj.tds = abs(val)
                    else:
                        obj.tds = val
                elif constituent == "Sodium":
                    val = fit_equation(day, alpha, beta)
                    if val < 0:
                        obj.sodium = abs(val)
                    else:
                        obj.sodium = val
                elif constituent == "Chloride":
                    val = fit_equation(day, alpha, beta)
                    if val < 0:
                        obj.chloride = abs(val)
                    else:
                        obj.chloride = val
                elif constituent == "Calcium":
                    val = fit_equation(day, alpha, beta)
                    if val < 0:
                        obj.calcium = abs(val)
                    else:
                        obj.calcium = val
                elif constituent == "Iron":
                    obj.iron = fit_equation(day, alpha, beta)
            obj.save()
    
    def get_arp_model_values(self, location):
        
        def arp_model(x, Q0, D, b):
            if b > 0.0:
                return Q0 / ((1 + D * x)**(1/b))
            elif b == 0.0:
                k = D
                return Q0 * (x**k)
            else:
                return 0.0
        
        values_list = self.model.objects.values_list("date")
        start_date = values_list[0][0]
        end_date = values_list[len(values_list)-1][0]
        ndays = (end_date - start_date).days + 1
        param = self.get_arp_model_parameters()[location]
        constituents = self.get_constituents()
        result = {}
        for constituent in constituents:
            values = []
            for day in range(1, ndays+1):
                if 0 < day <= 30:
                    Q0 = param["Fracturing Flowback"]["Q0"]
                    D = param["Fracturing Flowback"]["D"]
                    b = param["Fracturing Flowback"]["b"]
                    values.append(arp_model(day, Q0, D, b))
                elif 30 < day <= 150:
                    Q0 = param["Transition"]["Q0"]
                    D = param["Transition"]["D"]
                    b = param["Transition"]["b"]
                    values.append(arp_model(day-30, Q0, D, b))
                elif day > 150:
                    Q0 = param["Produced Water"]["Q0"]
                    D = param["Produced Water"]["D"]
                    b = param["Produced Water"]["b"]
                    values.append(arp_model(day-150, Q0, D, b))
                else:
                    return 0.0
            result[constituent] = values
        return result
        