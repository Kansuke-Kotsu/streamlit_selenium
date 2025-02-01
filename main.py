import requests
import json
import pandas as pd
import streamlit as st

# タイトルと説明文の表示
st.set_page_config(page_title="物件検索", layout="wide")
st.title("物件検索アプリ")

# --- Authentication ---
password = st.text_input("パスワード", type="password")

if password == st.secrets["password"]:
    # --- 入力フォームの設置 ---
    with st.sidebar:
        st.header("検索条件")
        input_1 = st.text_input("物件名", placeholder="")
        options = [
            "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
            "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
            "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県",
            "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県",
            "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県",
            "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県",
            "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"
        ]
        input_2 = st.selectbox("都道府県名", options)
        input_3 = st.text_input("都市名", placeholder="例：江東区")
        search_button = st.button("検索")

    # --- 検索結果表示エリア ---
    st.markdown("## 検索結果")
    # ヘッダー行の設定
    header = ["サイト名", "物件名", "住所", "家賃"]
    df = pd.DataFrame(columns=header)
    # テーブル表示用プレースホルダー（検索途中は DataFrame 表示で更新）
    table_placeholder = st.empty()
    table_placeholder.dataframe(df, use_container_width=True)

    def invoke_lambda(api_gateway_url, payload, site_name, df):
        """
        指定の Lambda API を呼び出し、結果を DataFrame に追加する関数
        """
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url=api_gateway_url, json=payload, headers=headers)
            response.raise_for_status()  # HTTP エラーの場合は例外を発生させる
            result = response.json()
            # 例：レスポンスの件数分ループ
            for i in range(len(result)):
                name = result.get(f"name_{i+1}", "情報なし")
                address = result.get(f"address_{i+1}", "情報なし")
                rent = result.get(f"rent_{i+1}", "情報なし")
                # DataFrameへ新規行を追加
                new_row = {"サイト名": site_name, "物件名": name, "住所": address, "家賃": rent}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                table_placeholder.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"{site_name} の検索中にエラーが発生しました: {e}")
        return df

    if search_button:
        if not input_1 and not input_3:
            st.warning("少なくとも物件名・キーワードまたは都市名のいずれかを入力してください。")
        else:
            payload = {
                "key1": input_1,
                "key2": input_2,
                "key3": input_3,
            }
            # 各サイトの検索結果取得
            lambda_configs = [
                {"url": "https://11l79ngo06.execute-api.ap-northeast-1.amazonaws.com/dev/docker-selenium-reins", "site": "REINS"},
                {"url": "https://11l79ngo06.execute-api.ap-northeast-1.amazonaws.com/dev/docker-selenium-tokyu", "site": "東急"},
                {"url": "https://11l79ngo06.execute-api.ap-northeast-1.amazonaws.com/dev/docker-selenium-able", "site": "エイブル"},
                {"url": "https://11l79ngo06.execute-api.ap-northeast-1.amazonaws.com/dev/docker-selenium-takuto", "site": "宅都"}
            ]
            
            # 全体の進捗バーを表示
            progress_bar = st.progress(0)
            num_sites = len(lambda_configs)
            
            for idx, config in enumerate(lambda_configs):
                with st.spinner(f"{config['site']} の検索中..."):
                    df = invoke_lambda(
                        api_gateway_url=config["url"], 
                        payload=payload,
                        site_name=config["site"],
                        df=df
                    )
                progress_bar.progress((idx + 1) / num_sites)
            
            st.success("全ての検索が完了しました！")
            
            # 結果が存在する場合、個別にカード形式で表示
            if df.empty:
                st.info("検索結果がありませんでした。")
            else:
                st.markdown("### 詳細結果")
                for idx, row in df.iterrows():
                    with st.container():
                        st.markdown(f"**サイト名：** {row['サイト名']}")
                        st.markdown(f"**物件名：** {row['物件名']}")
                        st.markdown(f"**住所：** {row['住所']}")
                        st.markdown(f"**家賃：** {row['家賃']}")
                        st.markdown("---")
else:
    st.write("合言葉は？")
