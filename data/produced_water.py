# !/usr/bin/env/python 
# -*- coding:utf-8 -*-

import psycopg2
import xlrd


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
        day = sheet.cell(row, 0).value
        well_1 = sheet.cell(row, 1).value
        if well_1 == "":
            well_1 = 0
        well_2 = sheet.cell(row, 2).value
        if well_2 == "":
            well_2 = 0
        well_3 = sheet.cell(row, 3).value
        if well_3 == "":
            well_3 = 0
        well_4 = sheet.cell(row, 4).value
        if well_4 == "":
            well_4 = 0
        well_5 = sheet.cell(row, 5).value
        if well_5 == "":
            well_5 = 0
        well_6 = sheet.cell(row, 6).value
        if well_6 == "":
            well_6 = 0
        well_7 = sheet.cell(row, 7).value
        if well_7 == "":
            well_7 = 0
        sql = 'INSERT INTO solutions_producedwater(days, well_1, well_2, well_3, well_4, well_5, well_6, well_7) \
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'
        try:
            vals = [day, well_1, well_2, well_3, well_4, well_5, well_6, well_7]
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
    excel_file = '/home/gu/Workspace/aquam/data/produced_water.xls'
    import_data(excel_file)
