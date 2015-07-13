# !/usr/bin/env/python 
# -*- coding:utf-8 -*-

import psycopg2
import xlrd
import datetime

def create_table():
    try:
        conn = psycopg2.connect(database='aquamdb', user='aquam', password='admin', host='127.0.0.1', port='5432')
    except Exception as ex:
        print 'unable to connect to the database.';
        print ex.message
    
    try:
        cur = conn.cursor()
        sql = 'CREATE TABLE sample_wu(id serial PRIMARY KEY, \
                                      api char(20), \
                                      frac_date date, \
                                      state varchar(50), \
                                      county varchar(50), \
                                      operator varchar(200), \
                                      well_name varchar(200), \
                                      latitude numeric, \
                                      longtitude numeric, \
                                      datum varchar(20), \
                                      wellbore_type varchar(30), \
                                      water_use numeric, \
                                      horizontal_length numeric);'
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as ex:
        print ex.message
        conn.close()

def import_data(excel_file, table_name):
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
        longtitude = float(sheet.cell(row, 8).value)
        datum = sheet.cell(row, 9).value
        well_trajectory = sheet.cell(row, 13).value
        water_use = float(sheet.cell(row, 12).value)
        horizontal_length = float(sheet.cell(row, 14).value)
        sql = 'INSERT INTO ' +table_name + ' (api, frac_date, state, county, well_name, latitude, longtitude, horizontal_length, water_use) \
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);'
        try:
            vals = [api, frac_date, state, county, well_name, latitude, longtitude, horizontal_length, water_use]
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
    table_name = 'solutions_wateruse'
    import_data(excel_file, table_name)
