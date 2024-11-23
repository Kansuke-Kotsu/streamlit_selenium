import requests
import json
import streamlit as st
import streamlit_authenticator as sa

# Using Streamlit for a better user interface 
st.title("Search property")

# --- Authentication ---
password = st.text_input("パスワード", type="password")
 

def invoke_lambda(api_gateway_url, payload, site_name):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url=api_gateway_url, json=payload, headers=headers)
    print(f"Raw response: {response.text}")
    response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
    result = response.json()
    name_1 = result["name1"]
    name_2 = result["name2"]
    name_3 = result["name3"]
    print(f"Lambda function response: {name_1}, {name_2}, {name_3}")
    st.write(f"--------- {site_name} ---------  ") 
    st.write(f"{name_1}") 
    st.write(f"{name_2}") 
    st.write(f"{name_3}") 
    st.write(f"") 

 
if password == st.secrets["password"]:
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
        result = invoke_lambda(
            api_gateway_url = "https://11l79ngo06.execute-api.ap-northeast-1.amazonaws.com/dev/docker-selenium-tokyu", 
            payload=payload,
            site_name="東急"
            )
        
        result = invoke_lambda(
            api_gateway_url = "https://11l79ngo06.execute-api.ap-northeast-1.amazonaws.com/dev/docker-selenium-able", 
            payload=payload,
            site_name="エイブル"
            )
        
        result = invoke_lambda(
            api_gateway_url = "https://11l79ngo06.execute-api.ap-northeast-1.amazonaws.com/dev/docker-selenium-takuto", 
            payload=payload,
            site_name="宅都"
            )

else:
    st.error("パスワードを入力してください。")
# --- End Authentication ---

