import csv
import json
import requests
from datetime import datetime, timedelta
from decouple import config
from pprint import pprint

result = {}

for i in range(50):

    token = config('MOIVE_KOBIS_TOKEN')
    targetDt = datetime(2019,7,13) - timedelta(weeks=i)
    targetDt = targetDt.strftime('%Y%m%d')

    api_url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json?weekGb=0&key={token}&targetDt={targetDt}'

    api_data = requests.get(api_url).json()
    movies = api_data.get('boxOfficeResult').get('weeklyBoxOfficeList')

    for movie in movies:
        code = movie.get('movieCd')
        if code not in result:
            result[code] = {
                'movieCd': movie.get('movieCd'),
                'movieNm': movie.get('movieNm'),
                'audiAcc': movie.get('audiAcc')
            }
    with open('boxoffice.csv', 'w', encoding='utf-8',newline='') as f:   
        fieldnames = ('movieCd', 'movieNm', 'audiAcc')
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for value in result.values():
            #print(value)
            writer.writerow(value)