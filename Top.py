import streamlit as st


# --- CSS setting --- 
with open("style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# --- Authentication ---
password = st.text_input("パスワード", type="password")
if password == st.secrets["password"]:
    # カラムの配置
    # 1行目の3つのカラム
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            '''
            <a href="/Search">
                <div class="container">
                    <p>① 以下のサイトから検索</p>
                    <p>・レインズ</p>
                    <p>・エイブル</p>
                    <p>・東急</p>
                    <p>・宅都</p>
                </div>
            </a>
            ''',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            '''
            <a href="/REINS_detail">
                <div class="container">
                    <p>② レインズから詳細な情報を含めて検索</p>
                    <p>・Adとか含め検索</p>
                </div>
            </a>
            ''',
            unsafe_allow_html=True
        )
else:
    st.write("合言葉は？")