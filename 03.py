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
    peoplename_url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?key={token}&peopleNm={result2}'
    api_peoplename_data = requests.get(peoplename_url).json()
    peoplename_info = api_peoplename_data.get('peopleListResult').get('peopleList')


    for peoplename in peoplename_info:
        dircetor = peoplename.get('peopleNm')
        if peoplename.get('repRoleNm') == 'peopleNm':
            result3[code3] = {
                'peopleCd': peoplename_info.get('peopleCd'),
                'peopleNm': peoplename_info.get('peopleNm'),
                'peopleNmEn': peoplename_info.get('peopleNmEn'),
                'filmoNames': peoplename_info.get('filmoNames')
                }