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
            return Q0 / (1 + D * x) ** (1 / b)
        
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
        result = {"data": data, "Q0": Q0, "D": D, "b": b}
        return result
    
    def get_arp_prediction(self, start_date, end_date, wells_num_per_month):
        pass