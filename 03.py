import csv
import json
import requests
from datetime import datetime, timedelta
from decouple import config
from pprint import pprint

result2 = []

with open('movies.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        code = row.get('peopleNm')
        result2.append(code)


result3 = {}
for code3 in result2:
    token = config('MOIVE_KOBIS_TOKEN')
    peoplename_url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?key={token}&peopleNm={code3}&itemPerPage=100'
    api_peoplename_data = requests.get(peoplename_url).json()
    peoplename_info = api_peoplename_data.get('peopleListResult').get('peopleList')[0]

   
    for peoplename in peoplename_info:
        # print(type(peoplename))
        # print(type(peoplename_info))
        director = peoplename_info.get('peopleNm')
        judge = peoplename_info.get('repRoleNm')
        # print(type(judge))
        # print(type(director))
        
        if judge == '감독':
            result3[director] = {
                'peopleCd': peoplename_info.get('peopleCd'),
                'peopleNm': peoplename_info.get('peopleNm'),
                'peopleNmEn': peoplename_info.get('peopleNmEn'),
                'filmoNames': peoplename_info.get('filmoNames')
                }

with open('director.csv', 'w', encoding='utf-8',newline='') as f:   
    fieldnames = ('peopleCd', 'peopleNm', 'peopleNmEn', 'filmoNames')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for value in result3.values():
        #print(value)
        writer.writerow(value)