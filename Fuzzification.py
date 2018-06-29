"""
Created by Kyle Farinas
Copyright (c) 2018 Reynaldo John Tristan Mahinay Jr., Franz Stewart Dizon, Stephen Kyle Farinas and Harry Pardo
"""

import pandas as pd
from sklearn.cluster import KMeans

fuzzy_str = {
    'popdensity': ["POPD_LOWLY DENSE", "POPD_LESS DENSE", "POPD_DENSE", "POPD_HIGHLY DENSE"],
    'ssta': ["SSTA_COLD", "SSTA_NORMAL", "SSTA_WARM", "SSTA_HOT"],
    'soi': ["SOI_EL NINO", "SOI_LOW", "SOI_HIGH", "SOI_LA NINA"],
    'typhoon_distance': ["TDIST_DIRECT HIT", "TDIST_NEAR", "TDIST_MIDDLING FAR", "TDIST_FAR"],
    'typhoon_wind': ["TWIND_WEAK", "TWIND_MODERATELY WEAK", "TWIND_MODERATELY STRONG", "TWIND_STRONG"],
    'rainfall': ["RAINFALL_SMALL", "RAINFALL_MEDIUM", "RAINFALL_LARGE", "RAINFALL_VERY LARGE"],
    'poverty': ["POV_POOR", "POV_MILDLY POOR", "POV_MILDLY NORMAL", "POV_NORMAL"],
    'ndvi': ["NDVI_LESS GREEN", "NDVI_GREEN", "NDVI_GREENER", "NDVI_GREENEST"],
    'evi': ["EVI_LESS DENSE", "EVI_DENSE", "EVI_DENSER", "EVI_DENSEST"],
    'daily_temp': ["TEMPS_COLD", "TEMPS_NORMAL", "TEMPS_WARM", "TEMPS_HOT"],
    'nightly_temp': ["TEMPN_COLD", "TEMPN_NORMAL", "TEMPN_WARM", "TEMPN_HOT"],
    'polstab': ["POLS_VERY UNSTABLE", "POLS_UNSTABLE", "POLS_STABLE", "POLS_VERY STABLE"],
    'dengue': ["DENGUE_LOW", "DENGUE_HIGH"],
    'dengue_next': ["DENGUE NEXT_LOW", "DENGUE NEXT_HIGH"]
}


def fuzzify(ppsd_data):
    col_headers = list(ppsd_data)
    col_headers = col_headers[2:]

    data_fuzzified = []

    for col in col_headers:
        # print(ppsd_data[col])
        data_normalized = normalize(ppsd_data[col])
        if (col == 'dengue' or col == 'dengue_next'):
            data_clustering = kmCluster_dengue(data_normalized, list(ppsd_data['month_no']))
            data_membership = membership_dengue(data_normalized, data_clustering)
        else:
            data_clustering = kmCluster(data_normalized, list(ppsd_data['month_no']))
            data_membership = membership(data_normalized, data_clustering)

        data_fuzzified.append(fuzzy(data_membership, col))

    data_fuzzified = pd.DataFrame(data_fuzzified)
    data_fuzzified = data_fuzzified.transpose()

    return data_fuzzified


def normalize(crispVal):
    converted = []
    for x in crispVal:
        x = float(x)
        converted.append(x)

    minimum = min(converted)
    maximum = max(converted)

    normalized = []

    for x in converted:
        x = 100 * ((x - minimum) / (maximum - minimum))
        normalized.append(x)

    return normalized


def membership(normVal, clusterVal):
    cA = clusterVal[0]
    cB = clusterVal[1]
    cC = clusterVal[2]
    cD = clusterVal[3]
    # print(clusterVal)

    mem_val = []

    # R-Function
    def A(x):
        if (x > cB):
            mem_A = 0
        elif (cA <= x <= cB):
            mem_A = (cB - x) / (cB - cA)
        elif (x < cA):
            mem_A = 1

        return mem_A

    # Triangle Function
    def B(x):

        if (x <= cA):
            mem_B = 0
        elif (cA < x <= cB):
            mem_B = (x - cA) / (cB - cA)
        elif (cB < x < cC):
            mem_B = (cC - x) / (cC - cB)
        elif (x >= cC):
            mem_B = 0

        return mem_B

    # Triangle Function
    def C(x):

        if (x <= cB):
            mem_C = 0
        elif (cB < x <= cC):
            mem_C = (x - cB) / (cC - cB)
        elif (cC < x < cD):
            mem_C = (cD - x) / (cD - cC)
        elif (x >= cD):
            mem_C = 0

        return mem_C

    # L-Function
    def D(x):

        if (x < cC):
            mem_D = 0
        elif (cC <= x <= cD):
            mem_D = (x - cC) / (cD - cC)
        elif (x > cD):
            mem_D = 1

        return mem_D

    for x in normVal:
        mem_val.append([A(x), B(x), C(x), D(x)])
    # mem_vals.append(mem_val)

    return mem_val


def fuzzy(memsVal, col_header):
    fuzzy_vals = fuzzy_str.get(col_header)

    final_fuzzy = []
    for mem in memsVal:
        y = mem.index(max(mem))
        final_fuzzy.append(fuzzy_vals[y])

    return final_fuzzy


def membership_dengue(normVal, clusterVal):
    cA = clusterVal[0]
    cB = clusterVal[1]
    mem_val = []

    def A(x):
        mem_A = 0
        if (x > cB):
            mem_A = 0
        elif (cA <= x <= cB):
            mem_A = (cB - x) / (cB - cA)
        elif (x > cA):
            mem_A = 1
        return mem_A

    def B(x):

        mem_B = 0
        if (x < cA):
            mem_B = 0
        elif (cA <= x <= cB):
            mem_B = (x - cA) / (cB - cA)
        elif (x > cB):
            mem_B = 1
        return mem_B

    for x in normVal:
        mem_val.append([A(x), B(x)])
    return mem_val


def kmCluster(toCluster, weekNo):
    kmc = []
    for x, y in zip(weekNo, toCluster):
        # smc = []
        smc = [x, y]
        kmc.append(smc)
    # print(kmc)

    mem_means = []

    kmeans = KMeans(n_clusters=4, init='k-means++', random_state=0)
    kmeans.fit(kmc)

    kk = kmeans.cluster_centers_
    # print(kk)
    for x, y in kk:
        mem_means.append(y)

    return sorted(mem_means)


def kmCluster_dengue(toCluster, weekNo):
    kmc = []
    for x, y in zip(weekNo, toCluster):
        # smc = []
        smc = [x, y]
        kmc.append(smc)
    mem_means = []
    kmeans = KMeans(n_clusters=2, init='k-means++', random_state=0)
    kmeans.fit(kmc)
    kk = kmeans.cluster_centers_
    # print(kk)
    for x, y in kk:
        mem_means.append(y)

    return sorted(mem_means)
