#  :bamboo:pjt_01 : 파이썬을 활용한 데이터 수집1

## 1. 프로젝트 요약

주어진 명세서를 해결하라!

```
최근 50주간 데이터 중에 주간 박스오피스 TOP10데이터를 수집합니다. 해당 데이터는 향후 화평점서비스에 서 기본으로 제공되는 화 목록으로 사용될 예정입니다. 
```

:panda_face: 필요 사항 

		- python
  - 라이브러리
    		- requests
  - API
    		- 영화진흥위원회 오픈 API
    		- http://www.kobis.or.kr/kobisopenapi/homepg/main/main.do

:panda_face: 명세서의 필수사항

	- 최근 50주간 데이터가 필요
	- 주간 박스오피스 TOP10데이터를 수집

:panda_face: 명세서의 요구사항

	- 주간(월~일)까지 기간의 데이터를 조회합니다.
	- 조회 기간은 총 50주이며, 기준일(마지막 일자)은 2019년 7월 13일입니다.
	- 다양성 화/상업 화를 모두 포함하여야 합니다.
	- 한국/외국 화를 모두 포함하여야 합니다.
	- 모든 상지역을 포함하여야 합니다.

## 2. 01.py에 대한 설명

:panda_face: 명세서의 결과

	- 수집된 데이터에서 `영화 대표코드`, `영화명`, `해당일 누적관객수`를 기록합니다.
	- `해당일 누적관객수`는 중복시 최신 정보를 반하여야 합니다.
	- `boxoffice.csv` 에 저장합니다.

:panda_face: 01.py  요약

  - 수행과정 
     	- API의 url를 불러와서 데이터를 저장해야함 : requests를 적절히 활용하자
     	- 필요한 데이터를 불러와서 dict 형태로 저장. : .get()과 반복문 그리고 조건문을 사용하자.
     	- dict의 자료를 .csv에 저장함. : with open() 함수를 활용하자.
- 주의사항 
  - dictionary와 리스트와의 관계를 고려해햐함.
  - jason 형태의 자료에 dictionary로 되어있는지, 리스트로 되어있는지 구별해야함.



---

```python
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
```

---

```python
import csv
import json
import requests
from datetime import datetime, timedelta
from decouple import config
from pprint import pprint
```

	- `import csv `: csv파일 생성에 필요
	- `import jason `: url에 해당되는 자료가 jason의 dict 형태로 저장함.
	- `import requests `:  python언어가 다른 언어와 소통할 수 있게 함.
	- `import datetime `:  현재시간 계산시 필요.
	- `import config`: token값을 숨기기위해 필요

---

```python
for i in range(50):

    token = config('MOIVE_KOBIS_TOKEN')
    targetDt = datetime(2019,7,13) - timedelta(weeks=i)
    targetDt = targetDt.strftime('%Y%m%d')
```

	- for구문은 50주간의 시간 데이터를 불러오기 위함
	- targetDt는 자료에 필요한 20190713의 형태로 변환하기 위하.

---

```python
 api_url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json?weekGb=0&key={token}&targetDt={targetDt}'

    api_data = requests.get(api_url).json()
    movies = api_data.get('boxOfficeResult').get('weeklyBoxOfficeList')

```

	- 영화진흥위원회 오픈 API에서 필요한 자료 가져오기

---

```python
for movie in movies:
        code = movie.get('movieCd')
        if code not in result:
            result[code] = {
                'movieCd': movie.get('movieCd'),
                'movieNm': movie.get('movieNm'),
                'audiAcc': movie.get('audiAcc')
            }
```

	- for 구문은 불러온 데이터를 result라는 새로운 dict에 데이터를 저장한다.

---

```python
    with open('boxoffice.csv', 'w', encoding='utf-8',newline='') as f:   
        fieldnames = ('movieCd', 'movieNm', 'audiAcc')
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for value in result.values():
            #print(value)
            writer.writerow(value)
```

	- boxoffice.csv에 데이터를 저장하기 위해 필요.



## 3. 02.py에 대한 설명

:panda_face: 명세서의 결과

- 위의 수집된 데이터에서 `영화 대표코드`를 불러와 영화별로 `영화 대표코드`, `영화명(국문)`, `영화명(영문)`, `영화명(원문)`, `관람등급`, `개봉연도`, `상영시간`,`장르`,`감독명`을 기록합니다.
- `movie.csv` 에 저장합니다.

:panda_face: 02.py  요약

- 수행과정 
  - `boxoffice.csv`의 파일에 저장된 `영화대표코드`를 가져오자. :with open() 함수 활용하자.
  - 새로운 `url` 에서 필요한 정보를 가져오자. 
  - `영화대표코드`에 일치하는 dict 형태로 저장. : .get()과 반복문 그리고 조건문을 사용하자.
  - dict의 자료를 .csv에 저장함. : with open() 함수를 활용하자.
- 주의사항 
  - `url` 자료에서 dictionary에 비어있는 자료로 인한 오류가 발생한다.
    - `list has out of range` 오류발생 : if 문 활용.
  - 자료가 방대해질수록 프로그램 작동 시간이 길어진다. (1분정도소요)
    - 코드를 확인할 때에 필요한 부분만 보일 수 있도록 코딩하여, 실행과 취소를 반복하자.

---

```python
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
    

    #pprint(result2)


with open('movies.csv', 'w', encoding='utf-8',newline='') as f:   
    fieldnames = ('movieCd', 'movieNm', 'movieNmEn', 'movieNmOg', 'watchGradeNm', 'openDt', 'showTm', 'genreNm', 'directors')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for value in result2.values():
        #print(value)
        writer.writerow(value)
```

