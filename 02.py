import csv
import json
import requests
from datetime import datetime, timedelta
from decouple import config
from pprint import pprint

result = []

with open('boxoffice.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        code = row.get('movieCd')
        result.append(code)

result2 = {}
for code2 in result:
    token = config('MOIVE_KOBIS_TOKEN')
    info_url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key={token}&movieCd={code2}'
    api_info_data = requests.get(info_url).json()
    movie_info = api_info_data.get('movieInfoResult').get('movieInfo')
    


    result2[code2] = {
        'movieCd': movie_info.get('movieCd'),
        'movieNm': movie_info.get('movieNm'),
        'movieNmEn': movie_info.get('movieNmEn'),
        'movieNmOg': movie_info.get('movieNmOg'),
        'openDt': movie_info.get('openDt'),
        'showTm': movie_info.get('showTm'),
        'watchGradeNm': movie_info.get('audits')[0].get('watchGradeNm') if movie_info.get('audits') else None,
        'genreNm': movie_info.get('genres')[0].get('genreNm') if movie_info.get('genres') else None,
        'directors': movie_info.get('directors')[0].get('peopleNm') if movie_info.get('directors') else None
        }
    

    pprint(result2)


with open('movies.csv', 'w', encoding='utf-8',newline='') as f:   
    fieldnames = ('movieCd', 'movieNm', 'movieNmEn', 'movieNmOg', 'watchGradeNm', 'openDt', 'showTm', 'genreNm', 'directors')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for value in result2.values():
        #print(value)
        writer.writerow(value)

  
        