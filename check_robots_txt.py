import requests

def check_robots_txt(url):
    robots_url = url.rstrip('/') + '/robots.txt'
    try:
        response = requests.get(robots_url)
        if response.status_code == 200:
            print(f"robots.txt for {url}:")
            print(response.text)
            if 'Disallow' in response.text:
                print("Disallowed paths found in robots.txt")
            else:
                print("No disallowed paths found in robots.txt")
        else:
            print(f"No robots.txt file found at {robots_url}")
    except requests.RequestException as e:
        print(f"Error fetching robots.txt: {e}")

# 使用例
check_robots_txt('https://www.hotpepper.jp/SA23/Y300/')
