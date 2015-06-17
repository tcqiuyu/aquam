# !/usr/bin/env/python 
# -*- coding:utf-8 -*-

import psycopg2
import xlrd
import datetime


def import_data(excel_file):
    try:
        conn = psycopg2.connect(database='aquamdb', user='aquam', password='admin', host='127.0.0.1', port='5432')
    except:
        print 'unable to connect to the database.';
    cur = conn.cursor()
    
    wb = xlrd.open_workbook(excel_file)
    sheet = wb.sheet_by_index(0)
    nrows = sheet.nrows
    for row in range(1, nrows):
        location = sheet.cell(row, 0).value
        if location == "":
            location = None
        township = sheet.cell(row, 1).value
        if township == "":
            township = None
        range1 = sheet.cell(row, 2).value
        if range1 == "":
            range1 = None
        section = sheet.cell(row, 3).value
        if section == "":
            section = None
        idp = sheet.cell(row, 4).value
        if idp == "":
            idp = None
        area = sheet.cell(row, 5).value
        if area == "":
            area = None
        api = sheet.cell(row, 6).value
        if api == "":
            api = None
        latitude = sheet.cell(row, 7).value
        longtitude = sheet.cell(row, 8).value
        reservoir = sheet.cell(row, 9).value
        if reservoir == "":
            reservoir = None
        well_trajectory = sheet.cell(row, 10).value
        if well_trajectory == "":
            well_trajectory = None
        stages = sheet.cell(row, 11).value
        if stages == "":
            stages = None
        frac_fluid = sheet.cell(row, 12).value
        if frac_fluid == "":
            frac_fluid = None
        dt = xlrd.xldate_as_tuple(sheet.cell(row, 13).value, wb.datemode)
        frac_date = str(datetime.datetime(dt[0], dt[1], dt[2]).date())
        if frac_date == "":
            frac_date = None
        water_use = sheet.cell(row, 14).value
        
        sql = 'INSERT INTO src_noblewells (location, township, range, section, idp, area, api, latitude, longtitude, reservoir, well_trajectory, stages, frac_fluid, frac_date, water_use) \
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
        try:
            vals = [location, township, range1, section, idp, area, api, latitude, longtitude, reservoir, well_trajectory, stages, frac_fluid, frac_date, water_use]
            cur.execute(sql, vals)
            conn.commit()
            print row
        except Exception as ex:
            cur.close()
            conn.close()
            print ex.message
            break
    cur.close()
    conn.close()
    
if __name__ == '__main__':
    excel_file = '/Users/qiu/Github/aquam/data_input/noble_wells.xls'
    import_data(excel_file)
