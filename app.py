#coding: UTF-8
#Pythonsのライブラリから日経平均やNYダウ、S&P500、NASDAQのデータを取得して処理にに要するデータ量も指定して予測するアプリ
#前日から４日分のデータから翌日の株価指数を予測する
#指定された量の直近のデータを使用
#全データの前半75%を訓練に使用、直近25%でテスト実施。

import streamlit as st
from predict import predict

st.set_page_config(
  page_title="predic_ScikitL app",
  page_icon="🚁",
)

st.title('株価指数予測アプリ(Scikit-Learn)')
st.markdown('## 概要及び注意事項')
st.write("当アプリでは、翌営業日の指定された株価指数の終値を指定された直近のデータ量に基づき前日終値よりも上昇するか、下落するかを過去データ(FRED)によりScikit-Learn（サキットラーン）を使用して予測します。ただし本結果により投資にいかなる損失が生じても、当アプリでは責任を取りません。あくまで参考程度にご利用ください。")
st.info('ティッカー例　日経平均_NIKKEI225 NYダウ_DJIA S&P500_SP500 NASDAQ_NASDAQCOM')

ticker = st.text_input('銘柄のティッカーを入力してください。', ' NIKKEI225')
amount_of_data_requested = st.text_input('処理に使用するデータ量を入力してください。（３００以上）', '300')
amount_of_data_requested = int(amount_of_data_requested)

if st.button('予測開始'):
    try:
        comment = st.empty()
        comment.write('予測を開始しました。')
        when, raise_or_fall, volume, Positive_Solution_Rate, program_processing_time_seconds = predict(ticker, amount_of_data_requested) 
        st.write(f'{when}')
        st.write(f'{raise_or_fall}するでしょう。')
        st.write(f'データ量：{volume}')
        st.write(f'正解率：{Positive_Solution_Rate}%')
        st.write(f'プログラム処理時間：{program_processing_time_seconds}秒')
        comment.write('完了しました！')
    except:
        st.error('エラーが生じました。入力内容を確認・修正ののち、再度実行してください。')
