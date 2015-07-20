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
        result = {"horizontal_length": horizontal_length.tolist(), "horizontal_length_mean": mean,
                  "horizontal_length_std": std}
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
        result = {"water_use_per_horizontal_foot": water_use_per_horizontal_foot.tolist(),
                  "water_use_per_horizontal_foot_mean": mean, "water_use_per_horizontal_foot_std": std}
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
        values_list = self.model.objects.values_list("frac_date", "horizontal_length")
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
            return Q0 / (1 + D * x) ** (1 / b)

        # fitting
        values_list = self.model.objects.values_list("days", "well_1", "well_2", "well_3", "well_4", "well_5", "well_6",
                                                     "well_7")
        days = []
        produced_water = np.zeros(len(values_list))
        for i in range(len(values_list)):
            days.append(values_list[i][0])
            values = [float(x) for x in values_list[i][1:] if x > 0]
            if values:
                produced_water[i] = np.mean(values)
            else:
                produced_water[i] = produced_water[i - 1]
        Q0 = produced_water[0]
        params = optimize.curve_fit(arp, days, produced_water)
        D, b = params[0]
        yfit = [arp(x, D, b) for x in days]

        # results
        data = []
        for x, y, z in zip(days, produced_water, yfit):
            obj = {"day": x, "produced_water": y, "fitted_produced_water": z}
            data.append(obj)

        # evaluation
        sstotal = (len(values_list) - 1) * np.var(produced_water)
        ssresid = np.sum(np.power(produced_water - yfit, 2))
        r2 = 1 - (ssresid / sstotal)
        # rmse = np.std(produced_water)
        result = {"data": data, "Q0": round(Q0, 3), "D": round(D, 3), "b": round(b, 3), "r2": round(r2, 4)}
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
            month_range = 12 * (year_range - 1) + (12 - start_month + 1) + end_month
        end_day = calendar.monthrange(end_year, end_month)[1]
        day_range = (datetime.date(end_year, end_month, end_day) - datetime.date(start_year, start_month, 1)).days + 1
        days = 0
        n = 0
        days_arr = np.zeros([day_range, month_range], dtype=int)
        for year in range(start_year, start_year + year_range + 1):
            m = 1
            if year == start_year:
                m = start_month
            for month in range(m, 13):
                if datetime.date(year, month, 1) <= datetime.date(end_year, end_month, 1):
                    end_day = calendar.monthrange(end_year, end_month)[1]
                    days = (datetime.date(end_year, end_month, end_day) - datetime.date(year, month, 1)).days + 1
                    for i in range(days):
                        if n < month_range:
                            days_arr[day_range - i - 1][n] = days - i
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
                    q = Q0 / (1 + D * t) ** (1 / b)
                produced_water_arr[i][j] = round(q * wells_num_per_month, 3)

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
        self.unit = 158.987
        self.constituents = ["TDS", "Sodium", "Chloride", "Calcium", "Iron"]
        self.locations = ['Core', 'Mustang', 'Greeley Crescent', 'East Pony', 'West Pony', 'Wells Ranch', 'Commins']
        self.coefficients = {
            "Core": {"TDS": (2982.1, 4312.1),
                     "Sodium": (927.91, 1804.4),
                     "Chloride": (1971.8, 1177.2),
                     "Calcium": (61.173, -22.745),
                     "Iron": (0, 53.46)
                     },
            "Mustang": {"TDS": (2282.5, 10691),
                        "Sodium": (1601.8, -262.57),
                        "Chloride": (2293, 10729),
                        "Calcium": (52.016, 0.5952),
                        "Iron": (0, 29.75)
                        },
            "Greeley Crescent": {"TDS": (2322.1, 6992.7),
                                 "Sodium": (787.65, 2556.2),
                                 "Chloride": (1512.6, 3583.6),
                                 "Calcium": (68.964, -20.551),
                                 "Iron": (0, 66.40)
                                 },
            "East Pony": {"TDS": (4636.6, 1614.5),
                          "Sodium": (2062.2, -928.59),
                          "Chloride": (3000, -361.24),
                          "Calcium": (30.791, -2.6108),
                          "Iron": (0, 32.55)
                          },
            "West Pony": {"TDS": (6129.5, 1551.8),
                          "Sodium": (2344.5, 105.16),
                          "Chloride": (4007.2, -961.57),
                          "Calcium": (56.77, -9.5692),
                          "Iron": (0, 76.68)
                          },
            "Wells Ranch": {"TDS": (4028.5, 4924.5),
                            "Sodium": (1292.2, 2649),
                            "Chloride": (2084.4, 3499.4),
                            "Calcium": (51.705, 63.865),
                            "Iron": (0, 106.11)
                            },
            "Commins": {"TDS": (3244, 16778),
                        "Sodium": (1161.8, 6270.1),
                        "Chloride": (2033.8, 9192),
                        "Calcium": (22.732, 340.34),
                        "Iron": (0, 71.45)
                        }
        }
        self.parameters = {
            "Core": {"Fracturing Flowback": {"Q0": 1043.04, "D": 0.721, "b": 0.0},
                     "Transition": {"Q0": 90, "D": 0.0529, "b": 1.3},
                     "Produced Water": {"Q0": 19.4084, "D": 0.00715, "b": 1.7}
                     },
            "Mustang": {"Fracturing Flowback": {"Q0": 1157.61, "D": 0.725, "b": 0.0},
                        "Transition": {"Q0": 98.49, "D": 0.0693, "b": 1.533742331},
                        "Produced Water": {"Q0": 22.99, "D": 0.00119, "b": 1.46627566}
                        },
            "Greeley Crescent": {"Fracturing Flowback": {"Q0": 1406.48, "D": 0.863, "b": 0.0},
                                 "Transition": {"Q0": 74.65, "D": 0.011, "b": 0.480076812},
                                 "Produced Water": {"Q0": 12.93, "D": 0.0039, "b": 1.6}
                                 },
            "East Pony": {"Fracturing Flowback": {"Q0": 1590, "D": 0.2492, "b": 0.947867299},
                          "Transition": {"Q0": 165.92, "D": 0.057, "b": 1.346982759},
                          "Produced Water": {"Q0": 33.62, "D": 0.00837, "b": 1.200480192}
                          },
            "West Pony": {"Fracturing Flowback": {"Q0": 0.0, "D": 0.0, "b": 0.0},
                          "Transition": {"Q0": 0.0, "D": 0.0, "b": 0.0},
                          "Produced Water": {"Q0": 0.0, "D": 0.0, "b": 0.0}
                          },
            "Wells Ranch": {"Fracturing Flowback": {"Q0": 1516, "D": 0.0614, "b": 0.478011472},
                            "Transition": {"Q0": 176.33, "D": 0.0347, "b": 1.006},
                            "Produced Water": {"Q0": 29.39, "D": 0.0034, "b": 0.899280576}
                            },
            "Commins": {"Fracturing Flowback": {"Q0": 0.0, "D": 0.0, "b": 0.0},
                        "Transition": {"Q0": 0.0, "D": 0.0, "b": 0.0},
                        "Produced Water": {"Q0": 0.0, "D": 0.0, "b": 0.0}
                        }
        }

    def __calc_flowback_volume(self, parameter, location_name):

        def arp_model(x, Q0, D, b):
            if b > 0.0:
                return Q0 / ((1 + D * x) ** (1 / b))
            elif b == 0.0:
                k = D
                return Q0 * (x ** k)
            else:
                return 0.0

        objs = self.model.objects.filter(location=location_name).order_by("date")
        wells_increase = {}
        pre_wells_number = 0
        for obj in objs:
            cur_date = obj.date
            cur_wells_number = obj.wells_number
            if cur_wells_number > pre_wells_number:
                wells_increase[cur_date] = cur_wells_number - pre_wells_number
                pre_wells_number = cur_wells_number
        wells_matrix = np.zeros([len(wells_increase), len(objs)], dtype=int)
        days_matrix = np.zeros([len(wells_increase), len(objs)], dtype=int)
        for j in range(len(wells_increase)):
            jdate = sorted(wells_increase)[j]
            wells_increase_number = wells_increase[jdate]
            for i in range(len(objs)):
                idate = objs[i].date
                if idate >= jdate:
                    wells_matrix[j][i] = wells_increase_number
                    days_matrix[j][i] = (idate - jdate).days + 1
        volume_matrix = np.zeros([len(wells_increase), len(objs)], dtype=float)
        for j in range(len(wells_increase)):
            for i in range(len(objs)):
                day = days_matrix[j][i]
                wells_number = wells_matrix[j][i]
                if 0 < day <= 30:
                    Q0 = parameter["Fracturing Flowback"]["Q0"]
                    D = parameter["Fracturing Flowback"]["D"]
                    b = parameter["Fracturing Flowback"]["b"]
                    volume_matrix[j][i] = arp_model(day, Q0, D, b) * wells_number
                elif 30 < day <= 150:
                    Q0 = parameter["Transition"]["Q0"]
                    D = parameter["Transition"]["D"]
                    b = parameter["Transition"]["b"]
                    volume_matrix[j][i] = arp_model(day - 30, Q0, D, b) * wells_number
                elif day > 150:
                    Q0 = parameter["Produced Water"]["Q0"]
                    D = parameter["Produced Water"]["D"]
                    b = parameter["Produced Water"]["b"]
                    volume_matrix[j][i] = arp_model(day - 150, Q0, D, b) * wells_number
                else:
                    volume_matrix[j][i] = 0.0
        volume_matrix = volume_matrix * self.unit
        return volume_matrix, days_matrix

    def __calc_water_quality(self, parameter, coefficient, location_name):

        def water_quality_equation(x, alpha, beta):
            return alpha * math.log(x) + beta

        # produced water volume
        volume_matrix, days_matrix = self.__calc_flowback_volume(parameter, location_name)
        cols, rows = volume_matrix.shape
        volume_array = np.zeros(rows, dtype=float)
        volume_matrix2 = volume_matrix.transpose()
        for i in range(rows):
            volume_array[i] = np.sum(volume_matrix2[i])
        quality_dict = {}
        for constituent in self.constituents:
            # constituent quantity
            alpha = coefficient[constituent][0]
            beta = coefficient[constituent][1]
            quantity_matrix = np.zeros([cols, rows], dtype=float)
            for j in range(cols):
                for i in range(rows):
                    day = days_matrix[j][i]
                    if day > 0:
                        volume = volume_matrix[j][i]
                        quantity_matrix[j][i] = water_quality_equation(day, alpha, beta) * volume
                    else:
                        quantity_matrix[j][i] = 0.0
            quantity_array = np.zeros(rows, dtype=float)
            quantity_matrix = quantity_matrix.transpose()
            for i in range(rows):
                quantity_array[i] = np.sum(quantity_matrix[i])
            # constituent quality
            quality_array = np.divide(quantity_array, volume_array)
            quality_dict[constituent] = quality_array.tolist()
        return quality_dict, volume_array

    def set_database(self, parameter, coefficient, location_name):
        quality_dict, volume_array = self.__calc_water_quality(parameter, coefficient)
        objs = self.model.objects.filter(location=location_name).order_by("date")
        for i in range(len(objs)):
            obj = objs[i]
            for constituent in self.constituents:
                if constituent == "TDS":
                    obj.tds = abs(quality_dict[constituent][i])
                if constituent == "Chloride":
                    obj.chloride = abs(quality_dict[constituent][i])
                if constituent == "Sodium":
                    obj.sodium = abs(quality_dict[constituent][i])
                if constituent == "Calcium":
                    obj.calcium = abs(quality_dict[constituent][i])
                if constituent == "Iron":
                    obj.iron = abs(quality_dict[constituent][i])
            obj.volume = volume_array[i]
            obj.save()

    def get_water_quality_settings(self):
        result = {
            "locations": self.locations,
            "parameters": self.parameters,
            "coefficients": self.coefficients
        }
        return result

    def get_water_quality_result(self, parameter, coefficient, location_name):
        wells_number = self.model.objects.filter(location=location_name).values_list("wells_number")
        quality_dict, volume_array = self.__calc_water_quality(parameter, coefficient, location_name)
        objs = self.model.objects.filter(location=location_name).order_by("date")
        result = []
        for i in range(len(objs)):
            value = {"date": str(objs[i].date),
                     "Wells_number": wells_number[i][0],
                     "TDS": abs(quality_dict["TDS"][i]),
                     "Chloride": abs(quality_dict["Chloride"][i]),
                     "Sodium": abs(quality_dict["Sodium"][i]),
                     "Calcium": abs(quality_dict["Calcium"][i]),
                     "Iron": abs(quality_dict["Iron"][i]),
                     "Volume": np.sum(volume_array[:i + 1])
                     }
            result.append(value)
        return result


class WaterTreatmentAnalyzer():
    """
    Used for providing the water treatment results computed based on Water Treatment Model
    """

    def __init__(self, model):
        self.model = model
        self.qfrac = 3571.428571
        self.unit = 158.987
        self.locations = ['Core', 'Mustang', 'Greeley Crescent', 'East Pony', 'West Pony', 'Wells Ranch', 'Commins']
        self.coefficients = {
            "Core": {"TDS": (2982.1, 4312.1),
                     "Sodium": (927.91, 1804.4),
                     "Chloride": (1971.8, 1177.2),
                     "Calcium": (61.173, -22.745),
                     "Iron": (0, 53.46)
                     },
            "Mustang": {"TDS": (2282.5, 10691),
                        "Sodium": (1601.8, -262.57),
                        "Chloride": (2293, 10729),
                        "Calcium": (52.016, 0.5952),
                        "Iron": (0, 29.75)
                        },
            "Greeley Crescent": {"TDS": (2322.1, 6992.7),
                                 "Sodium": (787.65, 2556.2),
                                 "Chloride": (1512.6, 3583.6),
                                 "Calcium": (68.964, -20.551),
                                 "Iron": (0, 66.40)
                                 },
            "East Pony": {"TDS": (4636.6, 1614.5),
                          "Sodium": (2062.2, -928.59),
                          "Chloride": (3000, -361.24),
                          "Calcium": (30.791, -2.6108),
                          "Iron": (0, 32.55)
                          },
            "West Pony": {"TDS": (6129.5, 1551.8),
                          "Sodium": (2344.5, 105.16),
                          "Chloride": (4007.2, -961.57),
                          "Calcium": (56.77, -9.5692),
                          "Iron": (0, 76.68)
                          },
            "Wells Ranch": {"TDS": (4028.5, 4924.5),
                            "Sodium": (1292.2, 2649),
                            "Chloride": (2084.4, 3499.4),
                            "Calcium": (51.705, 63.865),
                            "Iron": (0, 106.11)
                            },
            "Commins": {"TDS": (3244, 16778),
                        "Sodium": (1161.8, 6270.1),
                        "Chloride": (2033.8, 9192),
                        "Calcium": (22.732, 340.34),
                        "Iron": (0, 71.45)
                        }
        }
        self.methods = {"TDS": {"Coagulation/Filtration": 0, "Softening/Clarification": 0, "Reverse Osmosis": 0.955},
                        "Sodium": {"Coagulation/Filtration": 0, "Softening/Clarification": 0,
                                   "Reverse Osmosis": 0.9694},
                        "Chloride": {"Coagulation/Filtration": 0, "Softening/Clarification": 0,
                                     "Reverse Osmosis": 0.9685},
                        "Calcium": {"Coagulation/Filtration": 0, "Softening/Clarification": 0.97,
                                    "Reverse Osmosis": 0.9982},
                        "Iron": {"Coagulation/Filtration": 0.8, "Softening/Clarification": 0.986,
                                 "Reverse Osmosis": 0.9744},
                        }
        self.constants = {"TDS": {"Critical Fracturing Fluids Quality": 9000, "Fresh Water Quality": 430},
                          "Sodium": {"Critical Fracturing Fluids Quality": 9000, "Fresh Water Quality": 3.56},
                          "Chloride": {"Critical Fracturing Fluids Quality": 9000, "Fresh Water Quality": 19.2},
                          "Calcium": {"Critical Fracturing Fluids Quality": 600, "Fresh Water Quality": 14.4},
                          "Iron": {"Critical Fracturing Fluids Quality": 75, "Fresh Water Quality": 0.1},
                          }
        self.parameters = {
            "Core": {"Fracturing Flowback": {"Q0": 1043.04, "D": 0.721, "b": 0.0},
                     "Transition": {"Q0": 90, "D": 0.0529, "b": 1.3},
                     "Produced Water": {"Q0": 19.4084, "D": 0.00715, "b": 1.7}
                     },
            "Mustang": {"Fracturing Flowback": {"Q0": 1157.61, "D": 0.725, "b": 0.0},
                        "Transition": {"Q0": 98.49, "D": 0.0693, "b": 1.533742331},
                        "Produced Water": {"Q0": 22.99, "D": 0.00119, "b": 1.46627566}
                        },
            "Greeley Crescent": {"Fracturing Flowback": {"Q0": 1406.48, "D": 0.863, "b": 0.0},
                                 "Transition": {"Q0": 74.65, "D": 0.011, "b": 0.480076812},
                                 "Produced Water": {"Q0": 12.93, "D": 0.0039, "b": 1.6}
                                 },
            "East Pony": {"Fracturing Flowback": {"Q0": 1590, "D": 0.2492, "b": 0.947867299},
                          "Transition": {"Q0": 165.92, "D": 0.057, "b": 1.346982759},
                          "Produced Water": {"Q0": 33.62, "D": 0.00837, "b": 1.200480192}
                          },
            "West Pony": {"Fracturing Flowback": {"Q0": 0.0, "D": 0.0, "b": 0.0},
                          "Transition": {"Q0": 0.0, "D": 0.0, "b": 0.0},
                          "Produced Water": {"Q0": 0.0, "D": 0.0, "b": 0.0}
                          },
            "Wells Ranch": {"Fracturing Flowback": {"Q0": 1516, "D": 0.0614, "b": 0.478011472},
                            "Transition": {"Q0": 176.33, "D": 0.0347, "b": 1.006},
                            "Produced Water": {"Q0": 29.39, "D": 0.0034, "b": 0.899280576}
                            },
            "Commins": {"Fracturing Flowback": {"Q0": 0.0, "D": 0.0, "b": 0.0},
                        "Transition": {"Q0": 0.0, "D": 0.0, "b": 0.0},
                        "Produced Water": {"Q0": 0.0, "D": 0.0, "b": 0.0}
                        }
        }

    def get_water_treatment_general_settings(self):
        result = {
            "locations": self.locations,
            "methods": self.methods,
            "parameters": self.constants,
        }
        return result

    def get_water_treatment_location_settings(self):
        result = {
            "coefficients": self.coefficients,
            "parameters": self.parameters,
        }
        return result

    def __calc_flowback_volume(self, end_day, parameter, percent):

        def arp_model(x, Q0, D, b):
            if b > 0.0:
                return Q0 / ((1 + D * x) ** (1 / b))
            elif b == 0.0:
                k = D
                return Q0 * (x ** k)
            else:
                return 0.0

        flowback_volume = np.zeros(end_day, dtype=float)
        for i in range(end_day):
            day = i + 1
            if 0 < day <= 30:
                Q0 = parameter["Fracturing Flowback"]["Q0"]
                D = parameter["Fracturing Flowback"]["D"]
                b = parameter["Fracturing Flowback"]["b"]
                flowback_volume[i] = arp_model(day, Q0, D, b)
            elif 30 < day <= 150:
                Q0 = parameter["Transition"]["Q0"]
                D = parameter["Transition"]["D"]
                b = parameter["Transition"]["b"]
                flowback_volume[i] = arp_model(day - 30, Q0, D, b)
            elif day > 150:
                Q0 = parameter["Produced Water"]["Q0"]
                D = parameter["Produced Water"]["D"]
                b = parameter["Produced Water"]["b"]
                flowback_volume[i] = arp_model(day - 150, Q0, D, b)
            else:
                flowback_volume[i] = 0.0
            flowback_volume = flowback_volume * percent
        return flowback_volume

    def __calc_water_quality(self, end_day, coefficient):

        def water_quality_equation(x, alpha, beta):
            return alpha * math.log(x) + beta

        alpha = coefficient[0]
        beta = coefficient[1]
        water_quality = np.zeros(end_day, dtype=float)
        for i in range(end_day):
            day = i + 1
            water_quality[i] = water_quality_equation(day, alpha, beta)
        return water_quality

    def __calc_water_treatment(self, end_day, coefficient, method, constant, parameter, stages, percent):
        # water quality fitting
        water_quality = self.__calc_water_quality(end_day, coefficient)
        # constant values
        wqcritical = constant["Critical Fracturing Fluids Quality"]
        wqfresh = constant["Fresh Water Quality"]
        flowback_volume = self.__calc_flowback_volume(end_day, parameter, percent)
        # calculate treatment
        result_matrix = np.zeros([10, end_day], dtype=float)
        for i in range(end_day):
            # calculate Vrec(mg/L)
            vrec = 0.0
            water_quantity = 0.0
            for k in range(i + 1):
                vrec = vrec + flowback_volume[k]
                water_quantity = water_quantity + water_quality[k] * flowback_volume[k] * self.unit
            # calculate Vfrac (mg/L)
            vfrac = self.qfrac * stages * self.unit
            result_matrix[0][i] = self.qfrac * stages
            # calculate Vfresh (mg/L)
            vfresh = vfrac - vrec
            # claculate WQtreat (mg/L)
            wqtreat = water_quantity / vrec;
            for idx, val in enumerate(["Coagulation/Filtration", "Softening/Clarification", "Reverse Osmosis"]):
                wqtreat = wqtreat * (1 - method[val])
                wqfrac = (vfresh * wqfresh + vrec * wqtreat) / vfrac
                if wqfrac <= wqcritical:
                    result_matrix[3 * idx + 1][i] = wqfrac
                else:
                    result_matrix[3 * idx + 1][i] = float("nan")
                vfresh_quality = (vfrac * wqcritical - vrec * wqtreat) / wqfresh
                if vfresh <= vfresh_quality and vfresh > 0:
                    result_matrix[3 * idx + 2][i] = vfresh / self.unit
                    result_matrix[3 * idx + 3][i] = vfresh / vrec
                else:
                    result_matrix[3 * idx + 2][i] = float("nan")
                    result_matrix[3 * idx + 3][i] = float("nan")
        return result_matrix

    def set_result_to_database(self, end_day, coefficients, methods, constants, parameters, stages, location_name,
                               constituent_name, percent):
        coefficient = coefficients[location_name][constituent_name]
        method = methods[constituent_name]
        constant = constants[constituent_name]
        parameter = parameters[location_name]
        result_matrix = self.__calc_water_treatment(end_day, coefficient, method, constant, parameter, stages, percent)
        result_matrix = result_matrix.transpose()
        water_quality = self.__calc_water_quality(end_day, coefficient)
        objs = self.model.objects.filter(location=location_name, constituent=constituent_name,
                                         days__lte=end_day).order_by("days")
        for i in range(len(objs)):
            obj = objs[i]
            result = result_matrix[i]
            obj.quality = water_quality[i]
            obj.vfrac = result[0]
            obj.wqfrac_iter_1 = result[1]
            obj.vfresh_iter_1 = result[2]
            obj.ratio_iter_1 = result[3]
            obj.wqfrac_iter_2 = result[4]
            obj.vfresh_iter_2 = result[5]
            obj.ratio_iter_2 = result[6]
            obj.wqfrac_iter_3 = result[7]
            obj.vfresh_iter_3 = result[8]
            obj.ratio_iter_3 = result[9]
            obj.save()

    def get_treatment_iteration_result(self, end_day, coefficients, methods, constants, parameters, stages,
                                       location_name, constituent_name, percent):
        coefficient = coefficients[location_name][constituent_name]
        method = methods[constituent_name]
        constant = constants[constituent_name]
        parameter = parameters[location_name]
        result_matrix = self.__calc_water_treatment(end_day, coefficient, method, constant, parameter, stages, percent)
        water_quality = self.__calc_water_quality(end_day, coefficient)
        result = []
        f = lambda x: "null" if math.isnan(x) else x
        for i in range(end_day):
            obj = {"day": i + 1,
                   "quality": water_quality[i],
                   "vfrac": f(result_matrix[0][i]),
                   "wqfrac_iter_1": f(result_matrix[1][i]),
                   "vfresh_iter_1": f(result_matrix[2][i]),
                   "ratio_iter_1": f(result_matrix[3][i]),
                   "wqfrac_iter_2": f(result_matrix[4][i]),
                   "vfresh_iter_2": f(result_matrix[5][i]),
                   "ratio_iter_2": f(result_matrix[6][i]),
                   "wqfrac_iter_3": f(result_matrix[7][i]),
                   "vfresh_iter_3": f(result_matrix[8][i]),
                   "ratio_iter_3": f(result_matrix[9][i])
                   }
            result.append(obj)
        return result
