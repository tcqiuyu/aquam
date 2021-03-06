# !/usr/bin/env/python 
# -*- coding:utf-8 -*-

import psycopg2
import xlrd
import datetime


def import_data(excel_file, location_name):
    try:
        conn = psycopg2.connect(database='aquamdb', user='aquam', password='admin', host='127.0.0.1', port='5432')
    except:
        print 'unable to connect to the database.';
    cur = conn.cursor()
    
    wb = xlrd.open_workbook(excel_file)
    sheet = wb.sheet_by_index(0)
    nrows = sheet.nrows
    for row in range(1, nrows):
        location = location_name
        dt = xlrd.xldate_as_tuple(sheet.cell(row, 0).value, wb.datemode)
        date = str(datetime.datetime(dt[0], dt[1], dt[2]).date())
        wells_number = sheet.cell(row, 1).value
        sql = 'INSERT INTO solutions_waterquality (location, date, wells_number) \
               VALUES (%s, %s, %s);'
        try:
            vals = [location, date, wells_number]
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
    excel_file = '/home/gu/Workspace/aquam/data/water_quality.xls'
    location_names = ['Core', 'Mustang', 'Greeley Crescent', 'East Pony', 'West Pony', 'Wells Ranch', 'Commins']
    for location_name in location_names:
        import_data(excel_file, location_name)
