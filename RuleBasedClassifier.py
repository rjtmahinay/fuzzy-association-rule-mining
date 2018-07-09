"""
Created by Harry Pardo
Copyright (c) 2018 Reynaldo John Tristan Mahinay Jr., Franz Stewart Dizon, Stephen Kyle Farinas and Harry Pardo
"""

import pyodbc
import time

import pandas as pd


def get_rules():
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                          "Server=(localdb)\MSSQLLocalDB;"
                          "Database=ThesisSampleDB;"
                          "Trusted_Connection=yes;")
    cursor = cnxn.cursor()
    start_time = time.time()
    query = "SELECT * FROM [dbo].[Apriori_Rules2] WHERE (CONSEQUENT = 'DENGUE NEXT_HIGH' or CONSEQUENT = 'DENGUE NEXT_LOW')  ORDER BY  CONSEQUENT,CONFIDENCE  DESC, LIFT DESC,NUM_ANTECEDENT ASC"
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    temp = cursor.fetchall()
    for i in range(0, len(temp)):
        temp[i] = tuple(temp[i])
    apriori_rules = pd.DataFrame(temp, columns=columns)
    print("Apriori get rules: --- %s seconds ---" % (time.time() - start_time))

    start_time = time.time()
    query = "SELECT * FROM [dbo].[FP_Rules] WHERE (CONSEQUENT = 'DENGUE NEXT_HIGH' or CONSEQUENT = 'DENGUE NEXT_LOW')  ORDER BY  CONSEQUENT,CONFIDENCE DESC,NUM_ANTECEDENT ASC"
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    temp = cursor.fetchall()
    for i in range(0, len(temp)):
        temp[i] = tuple(temp[i])
    fp_rules = pd.DataFrame(temp, columns=columns)
    print("FP get rules: --- %s seconds ---" % (time.time() - start_time))

    return apriori_rules, fp_rules


# Rule-base Classifier
def find_match(test_data, rules):
    answers = []
    listdata = test_data[test_data.columns[:-1]].values.tolist()
    temp = 0
    ans = False
    for data in listdata:
        for ant, con, n in zip(rules['Antecedent'], rules['Consequent'], rules['Num_Antecedent']):
            if (n > 1):
                antecedents = ant.split(',')
            else:
                antecedents = ant

            ans = set(antecedents) < set(list(data))

            if (ans == True):

                answers.append(con)
                if (con == 'DENGUE NEXT_HIGH'):
                    temp += 1
                break
        if (ans == False):
            answers.append('DENGUE NEXT_LOW')
    print(temp)
    return answers

def check_accuracy(test_data_dengue, rule_based_answers):
    total = len(test_data_dengue)  # might need checking

    tp = 0
    fp = 0
    tn = 0
    fn = 0
    testRows = 0
    for x, y in zip(test_data_dengue, rule_based_answers):
        # print(str(x) + " " + str(y))
        # print("TestRows = " + str(testRows))
        if (str(x) == 'DENGUE NEXT_HIGH' and str(y) == 'DENGUE NEXT_HIGH'):
            tp += 1
            # print("True Positive: " + str(tp))
        elif (str(x) == 'DENGUE NEXT_LOW' and str(y) == 'DENGUE NEXT_HIGH'):
            fp += 1
            # print("False Positive: " + str(fp))
        elif (str(x) == 'DENGUE NEXT_LOW' and str(y) == 'DENGUE NEXT_LOW'):
            tn += 1
            # print("True Negative: " + str(tn))
        elif (str(x) == 'DENGUE NEXT_HIGH' and str(y) == 'DENGUE NEXT_LOW'):
            fn += 1

        testRows += 1

    if (tp == 0):
        PPV = 0
    else:
        PPV = float(tp / (tp + fp))
    print("PPV:" + str(PPV * 100))
    print("NPV:" + str(float(tn / (tn + fn) * 100)))
    print("Sensitivity:" + str(float(tp / (tp + fn) * 100)))
    print("Specificity:" + str(float(tn / (tn + fp) * 100)))
    if (PPV == 0):
        print("F: 0")
    else:
        print("F1:" + str(float((2 * tp) / (2 * tp + fp + fn) * 100)))
    print(str(float((tp + tn) / (total) * 100)))
    print("TP:" + str(tp) + " FP: " + str(fp) + " TN: " + str(tn) + " FN: " + str(fn))


def classfiy(test_data):
    apriori_rules, fp_rules = get_rules()

    start_time = time.time()
    prediction_apriori = find_match(test_data, apriori_rules)
    print("Apriori classify: --- %s seconds ---" % (time.time() - start_time))

    start_time = time.time()
    prediction_fp = find_match(test_data, fp_rules)
    print("FP classify: --- %s seconds ---" % (time.time() - start_time))

    print('---------------------------------------------------')
    print('Apriori')
    check_accuracy(test_data['dengue_next'], prediction_apriori)

    print('---------------------------------------------------')
    print('Fp Growth')
    check_accuracy(test_data['dengue_next'], prediction_fp)