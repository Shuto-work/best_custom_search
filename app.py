import requests
import json
import sys
import subprocess
import streamlit as st
import os

st.title('Custom Search API')
st.caption('検索キーワードを入力すると、検索結果から電話番号と社名のリストを取得できます')

with st.expander("留意点"):
    st.markdown("""
    1. **検索回数について**:
    - 1日100回までの上限（検索ページ数によらず）。
    - 日本時間の16時 or 17時にリセット。
    2. **検索ページ数について**:
    - 最初の10ページまでの上限。APIの仕様上、11ページ目以降は検索結果が表示されません。そのため、検索ワードを適宜変えてヒット件数の母数を増やす等の工夫が必要です。
    3. **検索結果の表示順について**: 
    - Relevance（関連順）とdate（日付順）から選択可能。  
    - 同じ検索ワードで異なるデータを取得できますが、重複結果もあるため取得量が2倍になるわけではありません。
    """)

with st.expander("用語辞典"):
    st.markdown("""
    **CSE**:  
    Custom Search Engineの略。Google検索結果のスクレイピングは規約違反になるため、Googleが提供しているAPIサービスのCSEを利用する必要があります。

    **API**:  
    アプリ同士の連携のこと。今回はCSEとPythonで構成したこちらの画面を連携させています。
    """)

# OSに応じてデスクトップのパスを取得する関数
def get_desktop_path():
    return os.path.join(os.path.expanduser("~"), "Desktop")

with st.form(key="key_word_form"):
    key_word = st.text_input("検索キーワード")
    search_start_page = st.number_input(
        "検索結果の何ページ目からデータ取得しますか？※最低1ページ目", step=1, value=1, min_value=1, max_value=10)
    search_end_page = st.number_input(
        "検索結果の何ページ目までデータ取得しますか？※最大10ページ目", step=1, value=1, min_value=1, max_value=10)
    sort_order = st.selectbox(
        "検索順序を選択してください", ["Relevance", "date"])
    output_csv = st.text_input("出力するCSVファイル名", "CSEスクレイピングリスト.csv")

    # デスクトップのパスを生成
    desktop_path = get_desktop_path()
    output_csv_path = os.path.join(desktop_path, output_csv)
    st.text(f'出力CSVファイルパス: {output_csv_path}')

    action_btn = st.form_submit_button("実行")

    if action_btn:
        st.subheader('以下の条件で実行しています...')
        st.text(f'検索キーワード：「{key_word}」')
        st.text(f'取得開始ページ：「{search_start_page}」')
        st.text(f'取得終了ページ：「{search_end_page}」')
        st.text(f'検索結果の表示順序：「{sort_order}」')
        st.text(f'出力CSVファイル名：「{output_csv}」')
        st.text(f'CSV出力先のパス:「{output_csv_path}」')

        params = {
            "key_word": key_word,
            "search_start_page": search_start_page,
            "search_end_page": search_end_page,
            "sort_order": sort_order,
            "output_csv_path": output_csv_path
        }
        with open('params.json', 'w') as f:
            json.dump(params, f)

        # Pythonのフルパスを取得
        python_path = sys.executable

        # subprocess.runを使ってスクリプトを実行します
        result = subprocess.run([python_path, 'custom_search_scraper.py'],
                                capture_output=True,
                                text=True
                                )

        # Display execution result
        if result.returncode == 0:
            st.success('実行完了')
        else:
            st.error('エラーが発生しました: ' + result.stderr)
