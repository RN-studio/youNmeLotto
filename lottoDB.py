import pandas as pd
from urllib.request import urlopen
import json


# 빈 데이터프레임 생성
columns = ['drwNo', 'drwtNo1', 'drwtNo2', 'drwtNo3', 'drwtNo4', 'drwtNo5', 'drwtNo6', 'bnusNo', 'drwNoDate', 'totSellamnt', 'firstPrzwnerCo', 'firstWinamnt']
df = pd.DataFrame(columns=columns)

url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo="

for i in range(1, 1100):
    URL = url + str(i)
    result_url = urlopen(URL)
    result = result_url.read()

    result_json = json.loads(result)
    result_df = pd.DataFrame([result_json])
    result_df = result_df[columns]
    df = pd.concat([df, result_df])

print(df.head())

csv_filename = 'lottoDB.csv'
df.to_csv(csv_filename, index=False)





