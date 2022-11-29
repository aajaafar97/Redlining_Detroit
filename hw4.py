# Problem 1.0
import requests
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from descartes import PolygonPatch
import matplotlib
import random as random
from matplotlib.path import Path
import numpy as np
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

redlineDataJSON = requests.get('https://dsl.richmond.edu/panorama/redlining/static/downloads/geojson/MIDetroit1939.geojson')
RedliningData = redlineDataJSON.json()
#print(RedliningData)
#print(RedliningData.keys())
#print(RedliningData['type'])
#print(RedliningData['features'])
#print(type(RedliningData['type']))
#print(type(RedliningData['features']))
#print(len(RedliningData['features']))
#print(len(RedliningData['features'][0]))
#print(type(RedliningData['features'][0]))
#print((RedliningData['features'][0]).keys())
#print((RedliningData['features'][0]['type']))
#print((RedliningData['features'][0]['geometry']))
#print((RedliningData['features'][0]['properties']))

class DetroitDistrict:
    def __init__(self, Coordinates, HolcGrade, HolcColor, name, Qualitative_Description, RandomLat, RandomLong, Median_Income, CensusTract):
        self.Coordinates = Coordinates
        self.HolcGrade = HolcGrade
        self.HolcColor = HolcColor
        self.name = name
        self.Qualitative_Description = Qualitative_Description
        self.RandomLat = RandomLat
        self.RandomLong = RandomLong
        self.Median_income = Median_Income
        self.CensusTract = CensusTract
        self.holc_id = CensusTract

Districts_features = []
for p in RedliningData['features']:
    Districts_features.append(p)

District_ids = []
for p in Districts_features:
    District_ids.append(p['properties']['holc_grade'])

Districts = []
for District in RedliningData['features']:
    Districts.append(
    DetroitDistrict(
        Coordinates = District['geometry'],
        HolcGrade = District['properties']['holc_grade'] ,
        HolcColor = None ,
        name = District['properties']['area_description_data']['9'] ,
        Qualitative_Description = District['properties']['area_description_data']['8'],
        RandomLat = None,
        RandomLong = None,
        Median_Income = None,
        CensusTract = None
    )
    )

for District in Districts:
    if District.HolcGrade == 'A':
        District.HolcColor = 'darkgreen'
    if District.HolcGrade == 'B':
        District.HolcColor = 'cornflowerblue'
    if District.HolcGrade == 'C':
        District.HolcColor = 'gold'
    if District.HolcGrade == 'D':
        District.HolcColor = 'maroon'




fig, ax = plt.subplots()
for District in Districts: 
 ax.add_patch(PolygonPatch(District.Coordinates, fc=District.HolcColor, ec='black', alpha=0.5, zorder=2 )) # add arguments here
 ax.autoscale()
 plt.rcParams["figure.figsize"] = (15,15)
plt.show()

random.seed(17)
xgrid = np.arange(-83.5,-82.8,.004)
ygrid = np.arange(42.1, 42.6, .004)
xmesh, ymesh = np.meshgrid(xgrid,ygrid)
points = np.vstack((xmesh.flatten(),ymesh.flatten())).T
for j in Districts:
    p = Path(j.Coordinates['coordinates'][0][0])
    grid = p.contains_points(points)
    print(j," : ", points[random.choice(np.where(grid)[0])])
    point = points[random.choice(np.where(grid)[0])]
    j.RandomLong = point[0]
    j.RandomLat = point[1]

BASE_URL = "https://geo.fcc.gov/api/census/block/find"
for District in Districts:
    District.CensusTract = ((requests.get(BASE_URL, params={"latitude":District.RandomLat, "longitude": District.RandomLong, "format": "json"})).json())['Block']['FIPS']

for District in Districts:
    District.CensusTract = District.CensusTract[5:11]

BASE_URL = 'https://api.census.gov/data/2015/acs/acs5?get=B19013_001E&for=tract:*&in=county:125,163,099,&in=state:26&key=f884a3136bc4a8514fdd396448c25d54d1d26c6d'
resp = requests.get(BASE_URL)
results_object = resp.json()

for District in Districts:
    for results in results_object:
        if District.CensusTract == results[3]:
            District.Median_income = results[0]
A_median_income_list = []
for District in Districts:
    if District.HolcGrade == 'A':
        if District.Median_income != None:
            A_median_income_list.append(District.Median_income)
A_median_income_list = [int(i) for i in A_median_income_list]
A_mean_income = np.mean(A_median_income_list)
A_median_income = np.median(A_median_income_list)

B_median_income_list = []
for District in Districts:
    if District.HolcGrade == 'B':
        if District.Median_income != None:
            B_median_income_list.append(District.Median_income)
B_median_income_list = [int(i) for i in B_median_income_list]
B_mean_income = np.mean(B_median_income_list)
B_median_income = np.median(B_median_income_list)

C_median_income_list = []
for District in Districts:
    if District.HolcGrade == 'C':
        if District.Median_income != None:
            C_median_income_list.append(District.Median_income)
C_median_income_list = [int(i) for i in C_median_income_list]
C_mean_income = np.mean(C_median_income_list)
C_median_income = np.median(C_median_income_list)

D_median_income_list = []
for District in Districts:
    if District.HolcGrade == 'D':
        if District.Median_income != None:
            D_median_income_list.append(District.Median_income)
D_median_income_list = [int(i) for i in D_median_income_list]
D_mean_income = np.mean(D_median_income_list)
D_median_income = np.median(D_median_income_list)

A_Qual_text = []
for District in Districts:
    if District.HolcGrade == 'A':
        A_Qual_text.append(District.Qualitative_Description)
A_Qual_text = ''.join(map(str, A_Qual_text))


B_Qual_text = []
for District in Districts:
    if District.HolcGrade == 'B':
        B_Qual_text.append(District.Qualitative_Description)
B_Qual_text = ''.join(map(str, B_Qual_text))

C_Qual_text = []
for District in Districts:
    if District.HolcGrade == 'C':
        C_Qual_text.append(District.Qualitative_Description)
C_Qual_text = ''.join(map(str, C_Qual_text))


D_Qual_text = []
for District in Districts:
    if District.HolcGrade == 'D':
        D_Qual_text.append(District.Qualitative_Description)
D_Qual_text = ''.join(map(str, D_Qual_text))



all_stopwords = set(stopwords.words('english'))
A_Qual_text = re.split(r'\s+', A_Qual_text)
A_Qual_text = [word for word in A_Qual_text if not word in all_stopwords]
B_Qual_text = re.split(r'\s+', B_Qual_text)
B_Qual_text = [word for word in B_Qual_text if not word in all_stopwords]
C_Qual_text = re.split(r'\s+', C_Qual_text)
C_Qual_text = [word for word in C_Qual_text if not word in all_stopwords]
D_Qual_text = re.split(r'\s+', D_Qual_text)
D_Qual_text = [word for word in D_Qual_text if not word in all_stopwords]

unique_D = []
for word in D_Qual_text:
    if word not in B_Qual_text and word not in C_Qual_text and word not in A_Qual_text:
            unique_D.append(word)
unique_A = []
for word in A_Qual_text:
    if word not in B_Qual_text and word not in C_Qual_text and word not in D_Qual_text:
            unique_A.append(word)
unique_B = []
for word in B_Qual_text:
    if word not in C_Qual_text and word not in A_Qual_text and word not in D_Qual_text:
            unique_B.append(word)
unique_C = []
for word in C_Qual_text:
    if word not in A_Qual_text and word not in B_Qual_text and word not in D_Qual_text:
            unique_C.append(word)

A_10_Most_Common = Counter(unique_A).most_common(10)
B_10_Most_Common = Counter(unique_B).most_common(10)
C_10_Most_Common = Counter(unique_C).most_common(10)
D_10_Most_Common = Counter(unique_D).most_common(10)
