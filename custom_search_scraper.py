import requests
import re
import json
import pandas as pd  # pandasをインポート
from secret_key import api_key, cse_id  # APIキーとCSE IDのインポート

def search_with_custom_search_api(query, api_key, cse_id, start_index, sort_order):
    try:
        search_url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': api_key,
            'cx': cse_id,
            'q': query,
            'start': start_index,
        }

        # sort_orderがdateの場合にsortパラメータを追加
        if sort_order == "date":
            params['sort'] = "date"

        response = requests.get(search_url, params=params)
        response.raise_for_status()
        return response.json().get('items', [])
    except requests.RequestException as e:
        print(f"Error during API request: {e}")
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
            company_info.append([phone_number, title])
    return company_info

def save_to_csv(filename, data):
    # pandas DataFrameを使用してCSVファイルとして保存
    df = pd.DataFrame(data, columns=['電話番号','顧客名',])
    df.to_csv(filename, index=False, encoding='utf-8')  # エンコーディングを指定


def main():
    # Load parameters from the JSON file
    with open('params.json') as f:
        params = json.load(f)

    query = params.get("key_word")
    search_start_page = params.get("search_start_page")
    search_end_page = params.get("search_end_page")
    output_csv = params.get("output_csv")
    sort_order = params.get("sort_order", "Relevance")  # デフォルトはRelevance

    if not query or not output_csv:
        print("Error: Missing required parameters")
        return

    all_company_info = []
    for page in range(search_start_page, search_end_page + 1):
        start_index = (page - 1) * 10 + 1
        results = search_with_custom_search_api(
            query, api_key, cse_id, start_index, sort_order)
        if not results:
            print(f"No results found for page {page}")
            continue

        company_info = extract_company_info_from_results(results)
        all_company_info.extend(company_info)

    if not all_company_info:
        print("No company information found")
        return

    save_to_csv(output_csv, all_company_info)


if __name__ == "__main__":
    main()