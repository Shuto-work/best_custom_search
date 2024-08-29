import streamlit as st

st.title('カスタムサーチAPIです')

with st.expander("留意点"):
    st.write("This is the content inside the expander.")

with st.form(key="key_word_form"):
    key_word = st.text_input("1. 検索キーワード")
    search_start_page = st.number_input("2. 検索結果の何ページ目からデータ取得しますか？", step=1)
    search_end_page = st.number_input("3. 検索結果の何ページ目までデータ取得しますか？", step=1)
    sheet_area = st.number_input("4. スプレッドシートの何行目からデータ書き込みますか？", step=1)
    action_btn = st.form_submit_button("実行")
    
    if action_btn:
      st.text('以下の条件で実行しました。')
      st.text(f'検索キーワード：「{key_word}」')
      st.text(f'取得開始ページ：「{search_start_page}」')
      st.text(f'取得終了ページ：「{search_end_page}」')
      st.text(f'データを書き込み始める行：{sheet_area}')