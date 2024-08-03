import requests
from bs4 import BeautifulSoup
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def search_with_custom_search_api(query, api_key, cse_id):
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': api_key,
        'cx': cse_id,
        'q': query
    }
    response = requests.get(search_url, params=params)
    response.raise_for_status()
    return response.json().get('items', [])

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

def save_to_google_sheets(data, spreadsheet_name, worksheet_name):
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('path_to_your_credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open(spreadsheet_name).worksheet(worksheet_name)

    for row_index, (company, phone) in enumerate(data, start=2):
        sheet.update_cell(row_index, 2, company)
        sheet.update_cell(row_index, 3, phone)

def main():
    api_key = 'AIzaSyAw1MqIItrA5PYxnhxYr7JkX4IEz5BasgA'
    cse_id = '117168291298141ab'
    query = "大阪 土木 090"
    results = search_with_custom_search_api(query, api_key, cse_id)
    company_info = extract_company_info_from_results(results)
    save_to_google_sheets(company_info, "検索結果スクレイピング", "シート1")

if __name__ == "__main__":
    main()
