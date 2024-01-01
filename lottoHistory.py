import pandas as pd

df_all = pd.read_csv("lottoDB.csv")

df_num = df_all.iloc[:, 1:8]

# 각 값의 등장 횟수를 저장할 빈 딕셔너리 생성
value_counts_dict = {}

# 데이터프레임을 돌면서 값의 등장 횟수 계산
for col in df_num.columns:
    for value, count in df_num[col].value_counts().items():
        if value in value_counts_dict:
            value_counts_dict[value] += count
        else:
            value_counts_dict[value] = count

value_counts_df = pd.DataFrame(list(value_counts_dict.items()), columns=['Value','Count'])
value_counts_df['Ratio'] = value_counts_df['Count'] / value_counts_df['Count'].sum()

csv_filename = 'lottoHistory.csv'
value_counts_df.to_csv(csv_filename, index=False)

