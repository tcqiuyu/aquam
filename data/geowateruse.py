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
        api = str(int(sheet.cell(row, 1).value))
        dt = xlrd.xldate_as_tuple(sheet.cell(row, 2).value, wb.datemode)
        frac_date = str(datetime.datetime(dt[0], dt[1], dt[2]).date())
        state = sheet.cell(row, 3).value
        county = sheet.cell(row, 4).value
        operator = sheet.cell(row, 5).value
        well_name = sheet.cell(row, 6).value
        latitude = float(sheet.cell(row, 7).value)
        longitude = float(sheet.cell(row, 8).value)
        datum = sheet.cell(row, 9).value
        well_trajectory = sheet.cell(row, 13).value
        water_use = float(sheet.cell(row, 12).value)
        horizontal_length = float(sheet.cell(row, 14).value)
        sql = "INSERT INTO geoanalytics_geowateruse(geometry, api, well_name, frac_date, state, county, latitude, longitude, horizontal_length, water_use) \
               VALUES (ST_GeomFromText(%s, 4326), %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        try:
            point = "POINT(%s %s)" % (longitude, latitude)
            vals = [point, api, well_name, frac_date, state, county, latitude, longitude, horizontal_length, water_use]
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
    excel_file = '/home/gu/Workspace/aquam/data/water_use.xls'
    import_data(excel_file)
