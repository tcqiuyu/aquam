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
        dt = xlrd.xldate_as_tuple(sheet.cell(row, 0).value, wb.datemode)
        date = str(datetime.datetime(dt[0], dt[1], dt[2]).date())
        stages = sheet.cell(row, 1).value 
        TDS = sheet.cell(row, 2).value
        iron = sheet.cell(row, 3).value
        calcium = sheet.cell(row, 4).value
        chloride = sheet.cell(row, 5).value
        sodium = sheet.cell(row, 6).value
        sql = 'INSERT INTO src_watertreatment (date, stages, TDS, iron, calcium, chloride, sodium) \
               VALUES (%s, %s, %s, %s, %s, %s, %s);'
        try:
            vals = [date, stages, TDS, iron, calcium, chloride, sodium]
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
    excel_file = '/home/gu/workspace/warehouse/water_treatment.xls'
    import_data(excel_file)