#coding: UTF-8
#Pythonsのライブラリから指定銘柄ティッカーの指定日分のデータを取得してScikit-Learnを使用して予測する関数(2018.02.09からデータあり)
#前日から４日分のデータから翌日の株価を予測する
#銘柄のティッカー(ticker)と直近何日間のデータ(amount_of_data_requested)を使用するかを変数としてとる。
#全データの前半75%を訓練に使用、直近25%でテスト実施。
#戻り値は、「{いつ}の翌日の営業日の{ティッカー}の予測(prediction_of_when)」と「{上昇（下落）(raise_or_fall)}」、「実際のデータ量(actual_data_volume)」、「正解率（％）(Positive_Solution_Rate)」、
#「プログラム処理時間（秒）(program_processing_time_seconds)」の５つである。
#ティッカーの例：日経平均："NIKKEI225",NYダウ："DJIA",S&P500:"SP500",NASDAQ:"NASDAQCOM"

def predict(ticker, amount_of_data_requested):
    import time
    t1 = time.time()

    from sklearn import svm
    from pandas_datareader import data as web
    import numpy as np
    import pandas as pd
    from pandas import Series, DataFrame
    import csv
    import datetime

    n225 = web.DataReader(ticker, "fred", start=datetime.date(1900, 1, 1))
    n225 = n225.dropna()
    lastday = n225[-1:]
    lastday = lastday.index.tolist()
    lastday = map(str, lastday)
    lastday = ''.join(lastday)
    lastday = lastday.rstrip("00:00:00")
    n225.to_csv("prices.csv")

    #データフレーム型からリスト型に変換して、価格のみを取り出す
    n225 = n225.values.tolist()
    #2Dを１Dに変換する
    n225arr = np.array(n225)
    n225arr = n225arr.ravel()
    n225 = n225arr.tolist()

    #データ数を直近の何日分にするか設定する
    stock_data_close = n225[-int(amount_of_data_requested):]

    #予測する月日を示す
    prediction_of_when = f'{str(lastday)}の翌営業日の{ticker}の予測'
    #print(str(lastday) + "の翌営業日の予測")
    # データの確認
    # print (stock_data)
    count_s = len(stock_data_close)
    actual_data_volume = count_s
    #print ('データ量:' + str(count_s) + '日分')

    # 株価の上昇率を算出、おおよそ-1.0-1.0の範囲に収まるように調整
    modified_data = []
    for i in range(1, count_s):
        modified_data.append(float(stock_data_close[i] - stock_data_close[i-1])/float(stock_data_close[i-1]) * 20)
    # print (modified_data)
    count_m = len(modified_data)
    # print (count_m)

    # 前日までの4連続の上昇率のデータ
    successive_data = []
    # 正解値 価格上昇: 1 価格下落: 0
    answers = []
    for i in range(4, count_m):
        successive_data.append([modified_data[i-4], modified_data[i-3], modified_data[i-2], modified_data[i-1]])
        if modified_data[i] > 0:
            answers.append(1)
        else:
            answers.append(0)
    # print (successive_data)
    # print (answers)

    # データ数
    n = len(successive_data)
    # print (n)
    m = len(answers)
    # print (m)

    # 線形サポートベクターマシーン
    clf = svm.LinearSVC()
    # サポートベクターマシーンによる訓練 （データの75%を訓練に使用）
    clf.fit(successive_data[:int(n*750/1000)], answers[:int(n*750/1000)])

    # テスト用データ
    # 正解
    expected = answers[int(-n*250/1000):]
    # 予測
    predicted = clf.predict(successive_data[int(-n*250/1000):])

    # 末尾の10個を比較
    #print ('正解:' + str(expected[-10:]))
    #print ('予測:' + str(list(predicted[-10:])))

    # 正解率の計算
    correct = 0.0
    wrong = 0.0
    for i in range(int(n*250/1000)):
        if expected[i] == predicted[i]:
            correct += 1
        else:
            wrong += 1
            
    #print('正解数： ' + str(int(correct)))
    #print('不正解数： ' + str(int(wrong)))

    Positive_Solution_Rate = round(correct / (correct+wrong) * 100,  2)
    #print ("正解率: " + str(round(correct / (correct+wrong) * 100,  2)) + "%")

    successive_data.append([modified_data[count_m-4], modified_data[count_m-3], modified_data[count_m-2], modified_data[count_m-1]])
    predicted = clf.predict(successive_data[-1:])
    #print ('翌営業日の予測:' + str(list(predicted)) + ' 1:上昇,　0:下落')
    if str(list(predicted)) == str([1]):
        raise_or_fall = '上昇'
        #print('翌営業日の日経平均株価は「上昇」するでしょう。')
    else:
        raise_or_fall = '下落'
        #print('翌営業日の日経平均株価は「下落」するでしょう。')
        
    t2 = time.time()
    elapsed_time = t2- t1
    elapsed_time = round(elapsed_time, 2)
    program_processing_time_seconds = elapsed_time
    #print('プログラム処理時間： ' + str(elapsed_time) + '秒')

    return prediction_of_when, raise_or_fall, actual_data_volume, Positive_Solution_Rate, program_processing_time_seconds
