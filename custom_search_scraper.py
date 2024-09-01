import requests
import re
import json
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from secret_key import api_key, cse_id, spreadsheet_id  # ここでインポート


def search_with_custom_search_api(query, api_key, cse_id, start_index):
    try:
        search_url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': api_key,
            'cx': cse_id,
            'q': query,
            'start': start_index
        }
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
            company_info.append([title, phone_number])
    return company_info


def batch_update_google_sheets(spreadsheet_id, range_name, values):
    creds = Credentials.from_service_account_file(
        './eternal-ruler-429403-f1-4149103d6f77.json',
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    service = build('sheets', 'v4', credentials=creds)

    body = {
        'valueInputOption': 'RAW',
        'data': [
            {
                'range': range_name,
                'values': values
            }
        ]
    }
    request = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body
    )
    response = request.execute()
    print("Data saved successfully")


def main():
    # Load parameters from the JSON file
    with open('params.json') as f:
        params = json.load(f)

    query = params["key_word"]
    search_start_page = params["search_start_page"]
    search_end_page = params["search_end_page"]
    sheet_area = params["sheet_area"]

    all_company_info = []
    for page in range(search_start_page, search_end_page + 1):
        start_index = (page - 1) * 10 + 1
        results = search_with_custom_search_api(
            query, api_key, cse_id, start_index)
        if not results:
            print(f"No results found for page {page}")
            continue

        company_info = extract_company_info_from_results(results)
        all_company_info.extend(company_info)

    if not all_company_info:
        print("No company information found")
        return

    range_name = f'シート1!B{sheet_area}:C'  # 書き込む範囲を指定
    headers = [['Company Name', 'Phone Number']]
    data = headers + all_company_info  # ヘッダーとデータをまとめる

    batch_update_google_sheets(spreadsheet_id, range_name, data)


if __name__ == "__main__":
    main()
