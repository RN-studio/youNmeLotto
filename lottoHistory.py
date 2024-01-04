import pandas as pd
import sqlite3
import csv

# conn = sqlite3.connect('lotto.db')
# cursor = conn.cursor()
#
# query = "SELECT drwtNo1, drwtNo2, drwtNo3, drwtNo4, drwtNo5, drwtNo6, bnusNo FROM lottery_results"
# df_num = pd.read_sql_query(query, conn)
#
# # 각 값의 등장 횟수를 저장할 빈 딕셔너리 생성
# value_counts_dict = {}
#
# # 데이터프레임을 돌면서 값의 등장 횟수 계산
# for col in df_num.columns:
#     for value, count in df_num[col].value_counts().items():
#         if value in value_counts_dict:
#             value_counts_dict[value] += count
#         else:
#             value_counts_dict[value] = count
#
# value_counts_df = pd.DataFrame(list(value_counts_dict.items()), columns=['Value', 'Count'])
# value_counts_df['Ratio'] = value_counts_df['Count'] / value_counts_df['Count'].sum()
# value_counts_df = value_counts_df.sort_values('Value', ascending=True)
#
# csv_filename = 'lottoHistory.csv'
# value_counts_df.to_csv(csv_filename, index=False)

conn = sqlite3.connect('lottoRatio.sqlite3')
cursor = conn.cursor()

# CSV 파일에서 데이터를 가져옴
with open('lottoHistory.csv', 'r') as file:
    csv_reader = csv.reader(file)
    headers = next(csv_reader)  # 첫 번째 행은 헤더

    # 테이블 생성 쿼리
    create_table_query = f'''
        CREATE TABLE IF NOT EXISTS lotto_ratio (
            {', '.join([f'{header} TEXT' for header in headers])}
        );
    '''
    cursor.execute(create_table_query)

    # 데이터 삽입 쿼리
    insert_data_query = f'''
        INSERT INTO lotto_ratio ({', '.join(headers)})
        VALUES ({', '.join(['?' for _ in headers])});
    '''
    for row in csv_reader:
        cursor.execute(insert_data_query, row)

# 변경사항 저장
conn.commit()

# 연결 종료
conn.close()