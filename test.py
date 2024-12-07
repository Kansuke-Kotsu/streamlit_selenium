import streamlit as st
import pandas as pd
import numpy as np
import requests

def invoke_lambda(api_gateway_url, payload, site_name, df):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url=api_gateway_url, json=payload, headers=headers)
    response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
    result = response.json()
    for i in range(3):
        # AWSから情報を取得
        name = result[f"name_{i+1}"]
        address = result[f"address_{i+1}"]
        rent = result[f"rent_{i+1}"]
        # table表示
        new_row = {"　サイト名　": site_name, "　　　物件名　　　": name, "　　　　　　　　　住所　　　　　　　　　": address, "　家賃　": rent}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        table_placeholder.dataframe(df)
    return df


    
input_1 = st.text_input("物件名・キーワードを入力してください。")
options = [
"北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
"茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
"新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県",
"静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県",
"奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県",
"徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県",
"熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"
]
input_2 = st.selectbox("都道府県名を選択してください。", options)
# Only proceed if user input is provided (for both Streamlit and standard input)
if st.button("検索"): # 検索ボタンを追加
    # リクエストペイロード (必要に応じて)
    payload = {
        "key1": input_1,
        "key2": input_2,
    }
    # Lambda関数呼び出し
    st.write(f"< 検索結果 >") #For Streamlit
    # ヘッダー行
    header = ["　サイト名　", "　　　物件名　　　", "　　　　　　　　　住所　　　　　　　　　", "　家賃　"]
    # Pandas DataFrame を作成
    df = pd.DataFrame(columns=header)
    # テーブルを表示する場所を確保
    table_placeholder = st.empty()
    table_placeholder.dataframe(df)

    df = invoke_lambda(
        api_gateway_url = "https://11l79ngo06.execute-api.ap-northeast-1.amazonaws.com/dev/docker-selenium-tokyu", 
        payload=payload,
        site_name="東急",
        df=df
        )
    
    df = invoke_lambda(
        api_gateway_url = "https://11l79ngo06.execute-api.ap-northeast-1.amazonaws.com/dev/docker-selenium-able", 
        payload=payload,
        site_name="エイブル",
        df=df
        )
    
    df = invoke_lambda(
        api_gateway_url = "https://11l79ngo06.execute-api.ap-northeast-1.amazonaws.com/dev/docker-selenium-takuto", 
        payload=payload,
        site_name="宅都",
        df=df
        )

