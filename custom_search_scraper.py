import requests
from bs4 import BeautifulSoup
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def search_with_custom_search_api(query, api_key, cse_id):
    try:
        search_url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': api_key,
            'cx': cse_id,
            'q': query
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
            company_info.append((title, phone_number))
    return company_info

def save_to_google_sheets(data, spreadsheet_id, worksheet_name):
    try:
        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('./eternal-ruler-429403-f1-4149103d6f77.json', scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(spreadsheet_id).worksheet(worksheet_name)

        # デバッグ用: シートの内容をクリア
        sheet.clear()
        
        # デバッグ用: シートのヘッダーを設定
        sheet.update_cell(1, 2, "Company Name")
        sheet.update_cell(1, 3, "Phone Number")

        # データを追加
        for row_index, (company, phone) in enumerate(data, start=2):
            sheet.update_cell(row_index, 2, company)
            sheet.update_cell(row_index, 3, phone)

        print("Data saved successfully")

    except Exception as e:
        print(f"Error during saving to Google Sheets: {e}")

def main():
    api_key = 'AIzaSyAw1MqIItrA5PYxnhxYr7JkX4IEz5BasgA'
    cse_id = '117168291298141ab'
    query = "大阪 建設 090"
    results = search_with_custom_search_api(query, api_key, cse_id)
    if not results:
        print("No results found")
        return

    company_info = extract_company_info_from_results(results)
    if not company_info:
        print("No company information found")
        return

    spreadsheet_id = '1iEt_TqDUam_rCqVXJbIgJTyKQICfh3yNE-TM0S-zTVg'
    worksheet_name = 'シート1'
    save_to_google_sheets(company_info, spreadsheet_id, worksheet_name)

if __name__ == "__main__":
    main()
