# Stdlib imports
import datetime
import calendar

# Third-party lib imports
from scipy import optimize
import numpy as np


class WaterUseAnalyzer():
    """
    Used to providing computed result based on Water Use Model
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
    Used to providing ARP modeling result based on Produecd Water Model
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