"""
Copyright (c) 2018 Reynaldo John Tristan Mahinay Jr., Franz Stewart Dizon, Stephen Kyle Farinas and Harry Pardo
"""

import csv
import pyodbc
import time

import pandas as pd

import Apriori
import FPGrowth
import Fuzzification
import RuleBasedClassifier


def connect_db(method):
    # DB Connect
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                          "Server=(localdb)\MSSQLLocalDB;"
                          "Database=ThesisSampleDB;"
                          "Trusted_Connection=yes;")
    cursor = cnxn.cursor()
    if (method == 'train'):
        query = "SELECT * FROM [dbo].[PPSD_TrainingData2]"
    else:
        query = "SELECT * FROM [dbo].[PPSD_TestData2]"

    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    temp = cursor.fetchall()
    for i in range(0, len(temp)):
        temp[i] = tuple(temp[i])
    ppsd_data = pd.DataFrame(temp, columns=columns)

    return ppsd_data


'''
Database Columns:
City	WeekNo	Rainfall	Temperature	Humidity	NDVI_NE	NDVI_NW	NDVI_SE	NDVI_SW	SSTA	SOI	CityPopulation	Dengue
        City	WeekNo	Rainfall	Temperature	Humidity	NDVI_NE	NDVI_NW	NDVI_SE	NDVI_SW	SSTA	SOI	CityPopulation	Dengue

'''


def table_csv(data):
    # print(data)
    with open('fuzzified.csv', 'w+', newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

    file.close()


# IPR OF HARRY PARDO
def insert_fprulesCSV(rules, confi):
    antecedents = []
    consequents = []
    confidence = []
    for rule in rules:
        temp = []
        for x in rule:
            temp.append(x)

        antecedents.append(",".join(temp))
    for con in confi:
        temp = []
        for y in con[:-1]:
            for z in y:
                temp.append(z)
        consequents.append(",".join(temp))

        confidence.append(con[-1])
    with open('FPRules.csv', 'w+') as file:
        # for line in rules:
        # file.write("%s" % line)
        # file.write('\n')
        writer = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        writer.writerow(['Antecedent', 'Consequent', 'Confidence'])
        for x, y, z in zip(antecedents, consequents, confidence):
            writer.writerow(x, y, z)


def insert_fprules(rules, confi):
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                          "Server=(localdb)\MSSQLLocalDB;"
                          "Database=ThesisSampleDB;"
                          "Trusted_Connection=yes;")

    cursor = cnxn.cursor()
    truncate = "truncate table FP_Rules"
    cursor.execute(truncate)
    cnxn.commit()

    query = "insert into FP_Rules(Antecedent,Consequent,Confidence,Num_Antecedent) values (?,?,?,?)"

    antecedents = []
    consequents = []
    confidence = []
    for rule in rules:
        temp = []
        for x in rule:
            temp.append(x)

        antecedents.append(",".join(temp))
    for con in confi:
        temp = []
        for y in con[:-1]:
            for z in y:
                temp.append(z)
        consequents.append(",".join(temp))

        confidence.append(con[-1])

    for x, y, z in zip(antecedents, consequents, confidence):
        temp = x.split(',')
        count = len(temp)
        params = (x, y, z, count)
        # print(params)
        cursor.execute(query, params)

    cnxn.commit()


def insert_arules(antecedent, consequent, confidence, lift):
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                          "Server=(localdb)\MSSQLLocalDB;"
                          "Database=ThesisSampleDB;"
                          "Trusted_Connection=yes;")

    cursor = cnxn.cursor()
    truncate = "truncate table Apriori_Rules2"
    cursor.execute(truncate)
    cnxn.commit()

    query = "insert into Apriori_Rules2(Antecedent,Consequent,Confidence,Num_Antecedent,Lift) values (?,?,?,?,?)"

    for x, y, z, l in zip(antecedent, consequent, confidence, lift):
        count = len(x)
        sx = ','.join(x)
        sy = ','.join(y)

        params = (sx, sy, z, count, l)

        cursor.execute(query, params)
    cnxn.commit()


def insert_arulesCSV(antecedent, consequent, confidence):
    with open('Apriori_Rules.csv', 'w+') as file:
        writer = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        writer.writerow(['Antecedent', 'Consequent', 'Confidence'])
        for x, y, z in zip(antecedent, consequent, confidence):
            sx = ','.join(x)
            sy = ','.join(y)
            writer.writerow(sx, sy, z)


def insert_db(fuzzified_data, ppsd_data):
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                          "Server=(localdb)\MSSQLLocalDB;"
                          "Database=ThesisSampleDB;"
                          "Trusted_Connection=yes;")

    cursor = cnxn.cursor()
    truncate = "truncate table FFSD_TrainingData2"
    cursor.execute(truncate)
    cnxn.commit()

    query = "insert into FFSD_TrainingData2(region,month_no,popdensity,ssta,soi,typhoon_distance,typhoon_wind,rainfall,poverty,ndvi,evi,daily_temp,nightly_temp,polstab,dengue,dengue_next) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

    frame = ppsd_data['month_no']
    provinces = ppsd_data['region']
    week = []

    for x in frame:
        week.append("MONTH_" + str(x))

    fuzz = []
    temp = []

    for x in provinces:
        temp.append(x)
    fuzz.append(temp)

    fuzz.append(week)
    for x in fuzzified_data:
        temp = []

        for y in fuzzified_data[x]:
            temp.append(y)
        fuzz.append(temp)

    count = len(fuzz[0])

    table = []
    for i in range(0, count):
        row = []
        for x in fuzz:
            row.append(x[i])

        params = tuple(row)
        cursor.execute(query, params)
        table.append(row)
    cnxn.commit()
    table_csv(table)


def fixforcsv(fuzzified_data, ppsd_data):
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                          "Server=(localdb)\MSSQLLocalDB;"
                          "Database=ThesisSampleDB;"
                          "Trusted_Connection=yes;")

    cursor = cnxn.cursor()
    truncate = "truncate table FFSD_TestData2"
    cursor.execute(truncate)
    cnxn.commit()

    query = "insert into FFSD_TestData2(region,month_no,popdensity,ssta,soi,typhoon_distance,typhoon_wind,rainfall,poverty,ndvi,evi,daily_temp,nightly_temp,polstab,dengue,dengue_next) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

    dataframe = pd.DataFrame(
        columns=['region', 'month_no', 'popdensity', 'ssta', 'soi', 'typhoon_distance', 'typhoon_wind', 'rainfall',
                 'poverty', 'ndvi', 'evi', 'daily_temp', 'nightly_temp', 'polstab', 'dengue', 'dengue_next'])
    frame = ppsd_data['month_no']

    week = []
    for x in frame:
        week.append("MONTH_" + str(x))

    dataframe['month_no'] = week
    dataframe['region'] = ppsd_data['region']
    dataframe['popdensity'] = fuzzified_data[0]
    dataframe['ssta'] = fuzzified_data[1]
    dataframe['soi'] = fuzzified_data[2]
    dataframe['typhoon_distance'] = fuzzified_data[3]
    dataframe['typhoon_wind'] = fuzzified_data[4]
    dataframe['rainfall'] = fuzzified_data[5]
    dataframe['poverty'] = fuzzified_data[6]
    dataframe['ndvi'] = fuzzified_data[7]
    dataframe['evi'] = fuzzified_data[9]
    dataframe['daily_temp'] = fuzzified_data[9]
    dataframe['nightly_temp'] = fuzzified_data[10]
    dataframe['polstab'] = fuzzified_data[11]
    dataframe['dengue'] = fuzzified_data[12]
    dataframe['dengue_next'] = fuzzified_data[13]

    list1 = dataframe.values.tolist()
    for x in list1:
        params = tuple(x)
        cursor.execute(query, params)
    cnxn.commit()

    return dataframe


def conn():
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                          "Server=(localdb)\MSSQLLocalDB;"
                          "Database=ThesisSampleDB;"
                          "Trusted_Connection=yes;")
    cursor = cnxn.cursor()

    query = "SELECT * FROM [dbo].[FFSD_TestData2] WHERE region='XII'"

    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    temp = cursor.fetchall()
    for i in range(0, len(temp)):
        temp[i] = tuple(temp[i])
    ppsd_data = pd.DataFrame(temp, columns=columns)

    return ppsd_data


def main():
    # Connect to database
    ppsd_data = connect_db('train')

    fuzzified_data = Fuzzification.fuzzify(ppsd_data)
    # print(fuzzified_data)

    # Insert Fuzzified Data
    insert_db(fuzzified_data, ppsd_data)

    # Apriori Algorithm
    fuzzy_csv = pd.read_csv('fuzzified.csv')

    # FP Grwoth
    start_time = time.time()

    rules, confi = FPGrowth.mine('fuzzified.csv')
    print("FP: --- %s seconds ---" % (time.time() - start_time))

    insert_fprules(rules, confi)
    # insert_fprulesCSV(rules,confi)
    start_time = time.time()
    ant, con, conf, lift = Apriori.mine('fuzzified.csv')
    print("Apriori: --- %s seconds ---" % (time.time() - start_time))
    insert_arules(ant, con, conf, lift)
    # insert_arulesCSV(ant,con,conf)


def Nmain():
    fuzzified_data = conn()
    print(fuzzified_data)

    RuleBasedClassifier.classfiy(fuzzified_data)


Nmain()
