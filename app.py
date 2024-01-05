from flask import Flask, render_template, request, send_from_directory
import pandas as pd
import random
import sqlite3

app = Flask(__name__)

# 예시 데이터프레임 생성
conn = sqlite3.connect('lottoRatio.db')
cursor = conn.cursor()

query = cursor.execute("SELECT * FROM lotto_ratio")

cols = [column[0] for column in query.description]

df = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)

conn.close()

@app.route('/sitemap.xml')
@app.route('/robots.txt')
@app.route('/ads.txt')
def robot_to_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def result():

    del_number = []
    for i in range(1, 7):
        try:
            value = int(request.form[f'deleteNumber{i}'])
            if 1 <= value <= 45:
                del_number.append(value - 1)
            else:
                pass
        except (KeyError, ValueError):
            pass

    num_of_games = int(request.form['game_count']) * 5
    weight_option = request.form['weight_option']

    # 번호 삭제
    if len(del_number) >= 1:
        df_temp = df.drop(index=del_number)
    else:
        df_temp = df

    # 가중치 계산
    if weight_option == '1':
        weights = df['Ratio']
    elif weight_option == '2':
        weights = 1 / df['Ratio']
    elif weight_option == '3':
        df['Ratio'] = 1
        weights = df['Ratio']
    else:
        return "올바른 가중치 옵션을 선택하세요."

    # 로또 번호 추출 및 정렬
    results = []
    if weight_option == '1' or weight_option == '2':
        for game in range(1, num_of_games + 1):
            selected_numbers = random.sample(sorted(df_temp['Value'].tolist(), key=lambda x: random.choice(weights)),
                                             k=6)
            results.append({"game": game, "numbers": sorted(selected_numbers)})
    else:
        for game in range(1, num_of_games + 1):
            selected_numbers = sorted(random.sample(df_temp['Value'].tolist(), k=6))
            results.append({"game": game, "numbers": sorted(selected_numbers)})

    return render_template('result.html', results=results)


@app.route('/statics')
def statics():
    return render_template('statics.html', lotto_data=df.sort_values('Count', ascending=False))


if __name__ == '__main__':
    app.run()
