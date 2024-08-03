# 社名◯ 番号×の場合。Custom search APIの使用
import requests
from bs4 import BeautifulSoup
import re
# from googlesearch import search

def get_company_names(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # 取得したHTMLの一部を出力して確認
        print(soup.prettify()[:1000])  # 最初の1000文字を出力

        # 企業名を含む要素を取得
        company_name_tags = soup.find_all('p', class_='_matterFrame__p01')
        company_names = [tag.get_text(strip=True) for tag in company_name_tags]

        # 抽出結果を確認
        print(company_names)

        return company_names

    except requests.RequestException as e:
        print(f"{url} の取得中にエラーが発生しました: {e}")
        return []

def find_company_phone(company_name, api_key, cse_id):
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': api_key,
        'cx': cse_id,
        'q': f"{company_name} 公式サイト"
    }
    response = requests.get(search_url, params=params)
    response.raise_for_status()
    results = response.json().get('items', [])
    if not results:
        return None

    # 最初の検索結果のURLを取得
    first_result_url = results[0].get('link')
    if not first_result_url:
        return None

    try:
        response = requests.get(first_result_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        phone_number_tag = soup.find(string=re.compile(r'\d{2,4}-\d{2,4}-\d{4}'))
        if phone_number_tag:
            phone_number = phone_number_tag.strip()
            return phone_number
    except requests.RequestException as e:
        print(f"{first_result_url} の取得中にエラーが発生しました: {e}")

    return None

# 使用例
job_list_url = 'https://www.baitoru.com/kansai/jlist/osaka/factory/btp4/shain/'  # 実際の求人情報リストページのURLに置き換えてください
api_key = 'AIzaSyAw1MqIItrA5PYxnhxYr7JkX4IEz5BasgA'  # 取得したAPIキーをここに記入
cse_id = '117168291298141ab'  # 取得したCSE IDをここに記入

# 求人一覧ページから企業名を取得
company_names = get_company_names(job_list_url)

# 各企業の公式ウェブサイトから電話番号を取得
results = []
for company_name in company_names:
    phone_number = find_company_phone(company_name, api_key, cse_id)
    if phone_number:
        results.append((company_name, phone_number))

# 結果を表示
for company, phone in results:
    print(f"Company: {company}, Phone: {phone}")

# 電話番号が見つからない場合、空のリストを返す
if not results:
    print([])