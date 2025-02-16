import requests
import pandas as pd
import streamlit as st

# --- Authentication ---
password = st.text_input("パスワード", type="password")
if password == st.secrets["password"]:

    # --- 入力フォームの設置 ---
    with st.sidebar:
        st.header("検索条件")
        property_name = st.text_input("物件名", placeholder="例：ハイツ")
        prefecture_options = [
            "東京都", "神奈川県","大阪府",
            "------------",
            "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
            "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
            "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県",
            "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県",
            "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県",
            "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県",
            "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"
        ]
        prefecture = st.selectbox("都道府県名", prefecture_options)
        city = st.text_input("都市名", placeholder="例：江東区")
        search_button = st.button("検索")

    # --- 検索結果表示エリア ---
    st.markdown("## 検索結果")
    # 表示するカラム（APIレスポンスの全項目）
    columns = ["サイト名", "物件名", "住所", "部屋番号", "間取り", "家賃", "敷金", "礼金", "管理費", "報酬(Ad料)"]
    results_df = pd.DataFrame(columns=columns)
    table_placeholder = st.empty()  # 結果を随時更新する表示領域
    table_placeholder.dataframe(results_df, use_container_width=True)

    def invoke_lambda(api_gateway_url, payload, site_name, df):
        """
        指定の Lambda API を呼び出し、レスポンスから物件情報（全要素）を DataFrame に追加する関数
        """
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url=api_gateway_url, json=payload, headers=headers)
            response.raise_for_status()  # HTTPエラーの場合は例外を発生させる
            result = response.json()

            # 連番になった物件情報を順次取得
            i = 1
            while f"name_{i}" in result:
                new_row = {
                    "サイト名": site_name,
                    "物件名": result.get(f"name_{i}", "情報なし"),
                    "住所": result.get(f"address_{i}", "情報なし"),
                    "部屋番号": result.get(f"room_n_{i}", "情報なし"),
                    "間取り": result.get(f"Madori_{i}", "情報なし"),
                    "家賃": result.get(f"Rent_{i}", "情報なし"),
                    "敷金": result.get(f"Shikikin_{i}", "情報なし"),
                    "礼金": result.get(f"Reikin_{i}", "情報なし"),
                    "管理費": result.get(f"Kanrihi_{i}", "情報なし"),
                    "手数料": result.get(f"Fee_{i}", "情報なし"),
                }
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                table_placeholder.dataframe(df, use_container_width=True)
                i += 1

        except Exception as e:
            st.error(f"{site_name} の検索中にエラーが発生しました: {e}")

        return df

    if search_button:
        if not property_name and not city:
            st.warning("少なくとも物件名または都市名のいずれかを入力してください。")
        else:
            payload = {
                "key1": property_name,
                "key2": prefecture,
                "key3": city,
            }
            # 検索対象のサイト設定
            lambda_configs = [
                {
                    "url": "https://11l79ngo06.execute-api.ap-northeast-1.amazonaws.com/dev/docker-selenium-reins-detail",
                    "site": "REINS"
                },
                # 他のサイトがあればここに追加可能
            ]

            # 進捗バーの表示
            progress_bar = st.progress(0)
            num_sites = len(lambda_configs)

            for idx, config in enumerate(lambda_configs):
                with st.spinner(f"{config['site']} の検索中..."):
                    results_df = invoke_lambda(
                        api_gateway_url=config["url"],
                        payload=payload,
                        site_name=config["site"],
                        df=results_df
                    )
                progress_bar.progress((idx + 1) / num_sites)

            st.success("全ての検索が完了しました！")
else:
    st.write("合言葉は？")