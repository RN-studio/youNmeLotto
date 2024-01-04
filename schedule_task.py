import pandas as pd
from urllib.request import urlopen
import json
import schedule
import time
from datetime import datetime
import sqlite3


def weekly_function():
    conn = sqlite3.connect('lotto.db')
    cursor = conn.cursor()

    query = "SELECT * FROM lottery_results ORDER BY ROWID DESC LIMIT 1"
    df = pd.read_sql_query(query, conn)

    if df['drwNoDate'] < datetime.today():
        url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo="

        URL = url + str(df['drwNo'])

        result_url = urlopen(URL)
        result = result_url.read()

        result_json = json.loads(result)
        result_df = pd.DataFrame([result_json])

        result_df.to_sql('lottery_results', conn, if_exists='append', index=False)
        conn.close()


schedule.every().sunday.at("00:00").do(weekly_function())

while True:
    schedule.run_pending()
    time.sleep(1)
