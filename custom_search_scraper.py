import requests
import logging
import json
import pandas as pd
import re
import streamlit as st

# `secrets.toml`からAPIキーを取得
api_key = st.secrets["api_key"]
cse_id = st.secrets["cse_id"]

st.write(f"API Key: {api_key}")
st.write(f"CSE ID: {cse_id}")

logging.basicConfig(
    filename='debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def search_with_custom_search_api(query, api_key, cse_id, start_index,sort_order):
    try:
        search_url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': api_key,
            'cx': cse_id,
            'q': query,
            'start': start_index,
        }
        
        if sort_order == "date":
            params['sort'] = "date"

        logging.debug(f"Request URL: {search_url}")
        logging.debug(f"Request Params: {params}")

        response = requests.get(search_url, params=params)
        response.raise_for_status()
        data = response.json()
        logging.debug(f"API response: {data}")
        return data.get('items', [])
    except requests.RequestException as e:
        logging.error(f"Error during API request: {e}")
        if 'response' in locals():
          logging.error(f"Response content: {response.text}")
        return []

def extract_phone_number_from_snippet(snippet):
    phone_match = re.search(r'\d{2,4}-\d{2,4}-\d{4}', snippet)
    if phone_match:
        return phone_match.group(0)
    return None

def extract_company_info_from_results(results):
    company_info = []
    for result in results:
        title = result.get('title')
        snippet = result.get('snippet')
        phone_number = extract_phone_number_from_snippet(snippet)
        if title and phone_number:
            company_info.append([phone_number, title,snippet])
    return company_info


def create_csv(data):
    df = pd.DataFrame(data, columns=['電話番号', '顧客名', '備考欄'])
    logging.debug(f"DataFrame head: {df.head()}")
    return df.to_csv(index=False, encoding='cp932')

def main():
    with open('params.json') as f:
        params = json.load(f)

    query = params.get("key_word")
    search_start_page = params.get("search_start_page")
    search_end_page = params.get("search_end_page")
    output_csv = params.get("output_csv")
    output_csv_path = params.get("output_csv")
    sort_order = params.get("sort_order", "Relevance")

    if not query or not output_csv_path:
        logging.error("Error: Missing required parameters")
        return

    all_company_info = []
    for page in range(search_start_page, search_end_page + 1):
        start_index = (page - 1) * 10 + 1
        results = search_with_custom_search_api(query, api_key, cse_id, start_index, sort_order)
        if not results:
            logging.info(f"No results found for page {page}")
            continue

        company_info = extract_company_info_from_results(results)
        all_company_info.extend(company_info)

    if not all_company_info:
        logging.info("No company information found")
        return

    csv_data = create_csv(all_company_info)
    print(csv_data)  # CSVデータを標準出力に出力
    
    # create_csv(all_company_info, output_csv_path)
    # logging.info(f"CSV file created at {output_csv_path}")

if __name__ == "__main__":
    main()