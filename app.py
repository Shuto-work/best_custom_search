import json
import subprocess
import streamlit as st

st.title('Custom Search API')
st.caption('検索キーワードを入力すると、検索結果から電話番号と社名のリストを取得できます')

with st.expander("留意点"):
    st.write("This is the content inside the expander.")

with st.form(key="key_word_form"):
    key_word = st.text_input("検索キーワード")
    search_start_page = st.number_input(
        "検索結果の何ページ目からデータ取得しますか？", step=1, value=1, min_value=1)
    search_end_page = st.number_input(
        "検索結果の何ページ目までデータ取得しますか？", step=1, value=1, min_value=1)
    sheet_area = st.number_input(
        "スプレッドシートの何行目からデータ書き込みますか？", step=1, value=1, min_value=1)
    action_btn = st.form_submit_button("実行")

    if action_btn:
        st.subheader('以下の条件で実行しています...')
        st.text(f'検索キーワード：「{key_word}」')
        st.text(f'取得開始ページ：「{search_start_page}」')
        st.text(f'取得終了ページ：「{search_end_page}」')
        st.text(f'データを書き込み始める行：{sheet_area}')

        # Save parameters to a JSON file
        params = {
            "key_word": key_word,
            "search_start_page": search_start_page,
            "search_end_page": search_end_page,
            "sheet_area": sheet_area
        }
        with open('params.json', 'w') as f:
            json.dump(params, f)

        # Call custom_search_scraper.py with subprocess
        result = subprocess.run(
            ['python', 'custom_search_scraper.py'], capture_output=True, text=True)

        # Display execution result
        if result.returncode == 0:
            st.success('実行完了')
        else:
            st.error('エラーが発生しました: ' + result.stderr)
