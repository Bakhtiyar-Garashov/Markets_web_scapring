import json
import time

from bs4 import BeautifulSoup
import requests

url = 'https://www.toppartika.lv/d/'


def scrap_top(url):
    data = "action=getShops&reg=0&nov=0&s="
    response = requests.post(url, data=data, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep - alive",
        "Host": "www.toppartika.lv",
        "Origin": "https:// www.toppartika.lv",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "referer": "https://www.toppartika.lv/veikali/",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest",

    })

    raw_json = json.loads(response.text.split('<br />')[2])

    for each_entry in raw_json['shops']:
        props = get_one_shop(each_entry['id'])
        each_entry['props'] = props

    with open('Top.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(raw_json, ensure_ascii=False, indent=4))

        return


def get_one_shop(id):
    # time.sleep(2)
    data = f"action=getShop&id={id}"
    response = requests.post(url, data=data, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep - alive",
        "Host": "www.toppartika.lv",
        "Origin": "https:// www.toppartika.lv",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "referer": "https://www.toppartika.lv/veikali/",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest",

    })

    raw = response.text
    soup = BeautifulSoup(raw, 'html.parser')
    props = {}
    category = soup.find('h3').text
    image_url = soup.find('a', attrs={'class': 'fancy'}, href=True)['href']

    address = soup.find_all('p')[1].text
    if '@' in soup.find_all('a', href=True)[1].text:
        email = soup.find_all('a', href=True)[1].text
        phone = soup.find_all('a', href=True)[2].text
        google_maps_url = soup.find_all('a', href=True)[3]['href']

    else:
        email = ""
        phone = soup.find_all('a', href=True)[1].text
        google_maps_url = soup.find_all('a', href=True)[2]['href']

    props['category'] = category
    props['image_url'] = image_url
    props['address'] = address
    props['phone'] = phone
    props['email'] = email
    props['google_maps_url'] = google_maps_url

    return props

scrap_top(url)
