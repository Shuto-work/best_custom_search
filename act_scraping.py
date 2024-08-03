# 2nd 抽出結果をスプシにまとめる。抽出できなかったデータへの対応なし。
import requests
from bs4 import BeautifulSoup
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def scrape_job_site_list(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        detail_links = [a['href'] for a in soup.find_all('a', class_='btn btn-black btn-next btn-small')]
        return detail_links
    except requests.RequestException as e:
        print(f"{url} の取得中にエラーが発生しました: {e}")
        return []

def scrape_job_detail(base_url, link):
    try:
        detail_url = base_url + link
        response = requests.get(detail_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        company_name_tag = soup.find('p', class_='text-white')
        phone_number_tag = soup.find('span', class_='contacttxt')
        company_name = company_name_tag.get_text(strip=True) if company_name_tag else None
        phone_number = None
        if phone_number_tag:
            raw_text = phone_number_tag.get_text(strip=True)
            phone_match = re.search(r'\d{2,4}-\d{2,4}-\d{4}', raw_text)
            phone_number = phone_match.group(0) if phone_match else None
        return company_name, phone_number
    except requests.RequestException as e:
        print(f"{base_url + link} の取得中にエラーが発生しました: {e}")
        return None, None

def write_to_google_sheet(results):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('./eternal-ruler-429403-f1-4149103d6f77.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1IWVx1k1GsVjXdzaYok5ZERLyvDsvP1pAEvxHHEFiJXc/edit?gid=1701544838').worksheet("Python")
    for i, (company, phone) in enumerate(results, start=2):
        sheet.update_cell(i, 2, company)
        sheet.update_cell(i, 3, phone)

# 使用例
job_list_url = 'https://www.gaten.info/list.php?Pref_ids%5B%5D=1&Job_ids%5B%5D=1&Job_ids%5B%5D=2&keyword='  # 実際の求人情報リストページのURLに置き換えてください
base_url = 'https://www.gaten.info'  # ベースURL
detail_links = scrape_job_site_list(job_list_url)
results = []
for link in detail_links:
    company_name, phone_number = scrape_job_detail(base_url, link)
    if company_name and phone_number:
        results.append((company_name, phone_number))
write_to_google_sheet(results)


# 1st ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
# import requests
# from bs4 import BeautifulSoup
# import re

# def scrape_job_site_list(url):
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.content, 'html.parser')

#         # 「詳細を見る」リンクのURLを取得
#         detail_links = [a['href'] for a in soup.find_all('a', class_='btn btn-black btn-next btn-small')]

#         return detail_links

#     except requests.RequestException as e:
#         print(f"{url} の取得中にエラーが発生しました: {e}")
#         return []

# def scrape_job_detail(base_url, link):
#     try:
#         detail_url = base_url + link
#         response = requests.get(detail_url)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.content, 'html.parser')

#         # 企業名と電話番号の抽出（HTML構造に応じて適宜修正してください）
#         company_name_tag = soup.find('p', class_='text-white')
#         phone_number_tag = soup.find('span', class_='contacttxt')

#         company_name = company_name_tag.get_text(strip=True) if company_name_tag else None

#         # 電話番号の抽出とフィルタリング
#         phone_number = None
#         if phone_number_tag:
#             raw_text = phone_number_tag.get_text(strip=True)
#             phone_match = re.search(r'\d{2,4}-\d{2,4}-\d{4}', raw_text)
#             phone_number = phone_match.group(0) if phone_match else None

#         return company_name, phone_number

#     except requests.RequestException as e:
#         print(f"{base_url + link} の取得中にエラーが発生しました: {e}")
#         return None, None

# # 使用例
# job_list_url = 'https://www.gaten.info/list.php?Pref_ids%5B%5D=1&Job_ids%5B%5D=1&Job_ids%5B%5D=2&keyword='  # 実際の求人情報リストページのURLに置き換えてください
# base_url = 'https://www.gaten.info'  # ベースURL

# # リストページから詳細リンクを取得
# detail_links = scrape_job_site_list(job_list_url)

# # 各詳細ページで企業名と電話番号を取得
# results = []
# for link in detail_links:
#     company_name, phone_number = scrape_job_detail(base_url, link)
#     if company_name and phone_number:
#         results.append((company_name, phone_number))

# # 結果を表示
# for company, phone in results:
#     print(f"Company: {company}, Phone: {phone}")

# # 電話番号が見つからない場合、空のリストを返す
# if not results:
#     print([])