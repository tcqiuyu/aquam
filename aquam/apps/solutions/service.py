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
        real = []
        for x, y in zip(horizontal_length, water_use):
            obj = {"horizontal_length": x, "water_use": y}
            real.append(obj)
        fitting = []
        for x, y in zip(horizontal_length, yfit):
            obj = {"horizontal_length": x, "fitted_water_use": y}
            fitting.append(obj)
        result = {"real": real, "fitting": fitting, "r2": round(r2, 4)}
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
        real = []
        for x, y in zip(horizontal_length, water_use):
            obj = {"horizontal_length": x, "water_use": y}
            real.append(obj)
        fitting = []
        for x, y in zip(horizontal_length, yfit):
            obj = {"horizontal_length": x, "fitted_water_use": y}
            fitting.append(obj)
        result = {"real": real, "fitting": fitting, "r2": round(r2, 4)}
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
        real = []
        for x, y in zip(horizontal_length, water_use):
            obj = {"horizontal_length": x, "water_use": y}
            real.append(obj)
        fitting = []
        for x, y in zip(horizontal_length, yfit):
            obj = {"horizontal_length": x, "fitted_water_use": y}
            fitting.append(obj)
        result = {"real": real, "fitting": fitting, "r2": round(r2, 4)}
        return result


# class ProducedWaterModeler():
#     """
#     Used to providing ARP modeling result based on Produecd Water Model
#     """
#     def __init__(self, model):
#         self.model = model
#     
#     def get_arp_model(self):
#         record_date = []
#         raw_produced_water = np.zeros([wells_number, len(values)])
#         for i in range(len(values)):
#             record_date.append(values[i][1])
#             for j in range(wells_number):
#                 if values[i][j + 2] is not None:
#                     raw_produced_water[j][i] = float(values[i][j + 2])
#         produced_water = np.zeros([wells_number, len(values)])
#         for j in range(wells_number):
#             loc = 0
#             for i in range(len(values)):
#                 if raw_produced_water[j][i] != 0:
#                     loc = i;
#                     break;
#             for i in range(len(values) - loc):
#                 produced_water[j][i] = raw_produced_water[j][i + loc]
#         
#         # build the Arp model
#         avg_produced_water = np.zeros(len(values))
#         for i in range(len(values)):
#             produced_water_transpose = np.transpose(produced_water)
#             temp_list = [x for x in produced_water_transpose[i] if x != 0]
#             if temp_list:
#                 avg_produced_water[i] = np.mean(temp_list)
#             else:
#                 avg_produced_water[i] = 0
#         Q0 = avg_produced_water[0]
#         def arp(x, D, b):
#             return Q0 / (1 + D * x) ** (1 / b)
#         days = np.array([x for x in range(1, len(values) + 1)])
#         params = optimize.curve_fit(arp, days, avg_produced_water)
#         D, b = params[0]
#         yfit = arp(days, D, b)
#         return days, avg_produced_water, D, b, yfit