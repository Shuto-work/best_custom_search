from yaml.loader import SafeLoader
import yaml
import streamlit_authenticator as stauth
import json
import sys
import subprocess
import streamlit as st
import os

# 環境に応じて設定を読み込む関数

def load_config():
    if os.path.exists('config.yaml'):
        # ローカル環境
        with open('config.yaml') as file:
            return yaml.load(file, Loader=SafeLoader)
    else:
        # デプロイ環境 (Streamlit Secrets を使用)
        return {
            'credentials': {
                'usernames': {
                    username: {
                        'name': name,
                        'password': password
                    } for username, name, password in zip(
                        st.secrets["authentication"]["usernames"],
                        st.secrets["authentication"]["name"],
                        st.secrets["authentication"]["passwords"]
                    )
                }
            },
            'cookie': {
                'expiry_days': st.secrets["authentication"]["cookie_expiry_days"],
                'key': st.secrets["authentication"]["cookie_key"],
                'name': st.secrets["authentication"]["cookie_name"]
            },
            'pre-authorized': {
                'emails': st.secrets["authentication"]["pre_authorized_emails"]
            }
        }

# 設定を読み込む
config = load_config()

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

authenticator.login()

if st.session_state["authentication_status"]:
    authenticator.logout()
    st.write(f'ログインに成功しました。ようこそ**{st.session_state["name"]}**さん！')

    st.title('Custom Search API')
    st.caption('検索キーワードを入力すると、検索結果から電話番号と社名のリストを取得できます')

    with st.expander("留意点"):
        st.markdown("""
              1. **検索回数の上限について**:
              - 無料枠の場合、1日100クエリが上限。1クエリ = 1ページ分の検索結果。1ページ = 10位までの表示。
              - （例 1）「大阪　090 土木」で検索、取得ページ数が1ページ分 = 1クエリ
              - （例 2）「大阪　090 土木」で検索、取得ページ数が10ページ分 = 10クエリ
              - 上限は、日本時間の17時にリセット。※詳細はユーザーマニュアルにて
              2. **検索ページ数について**:
              - APIの仕様上、10ページまでが上限。
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

    with st.form(key="key_word_form"):
        key_word = st.text_input("検索キーワード")
        search_start_page = st.number_input(
            "データ取得開始ページ", step=1, value=1, min_value=1, max_value=10)
        search_end_page = st.number_input(
            "データ取得終了ページ", step=1, value=1, min_value=1, max_value=10)
        sort_order = st.selectbox(
            "検索結果の表示順序（Relevance = 関連順, date = 日付順）", ["Relevance", "date"])
        output_csv = st.text_input("出力するCSVファイル名", "CSEスクレイピングリスト.csv")
        action_btn = st.form_submit_button("実行")

        if action_btn:
            st.subheader('以下の条件で実行しています...')
            st.text(f'検索キーワード：「{key_word}」')
            st.text(f'取得開始ページ：「{search_start_page}」')
            st.text(f'取得終了ページ：「{search_end_page}」')
            st.text(f'検索結果の表示順序：「{sort_order}」')
            st.text(f'出力CSVファイル名：「{output_csv}」')

            params = {
                "key_word": key_word,
                "search_start_page": search_start_page,
                "search_end_page": search_end_page,
                "sort_order": sort_order,
                "output_csv": output_csv
            }
            with open('params.json', 'w') as f:
                json.dump(params, f)

            # Pythonのフルパスを取得
            python_path = sys.executable

            # subprocess.runを使ってスクリプトを実行。Python実行環境を明示的に指定。
            result = subprocess.run([python_path, 'custom_search_scraper.py'],
                                    capture_output=True,
                                    text=True
                                    )

            # CSVデータの準備
            if result.returncode == 0:
                csv_data = result.stdout
                st.session_state.csv_data = csv_data
                st.session_state.csv_file_name = output_csv
                st.success('実行完了')
            else:
                st.error('エラーが発生しました: ' + result.stderr)

    # ダウンロードボタンをフォーム外に配置
    if 'csv_data' in st.session_state:
        st.download_button(
            label="CSVファイルをダウンロード",
            data=st.session_state.csv_data,
            file_name=st.session_state.csv_file_name,
            mime="text/csv"
        )

elif st.session_state["authentication_status"] is False:
    st.error('ユーザー名/パスワードが登録されていません。このアプリは限定ユーザーのみ利用できます。')
elif st.session_state["authentication_status"] is None:
    st.warning('ユーザー名とパスワードを入力してください')
