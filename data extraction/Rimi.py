import json
import requests
from bs4 import BeautifulSoup

url = "https://www.rimi.lv/veikali"


def scrap_rimi_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    all_scripts = soup.find_all('script')
    all_scripts = list(all_scripts)

    for text in str(all_scripts[8]).split(';'):
        if 'list' in text:
            text = text.split('=')
            raw_json_result = json.loads(text[1])
            with open('Rimi.json', 'w', encoding='utf8') as file_handler:
                json_data = json.dumps(raw_json_result, ensure_ascii=False, indent=4)
                json_data = json.loads(json_data)

                for i in json_data:
                    shop_items = soup.find('a', {'data-shop-id': i['id']})
                    if shop_items:
                        list_item = shop_items.parent.parent
                        i['full_address'] = str(list_item.select('.shop__address--desktop')[0].text).strip()
                        i['phone'] = str(list_item.select('.shop__info-value')[0].text).split(':')[1].strip()
                        i['email'] = str(list_item.select('.shop__info-value')[1].text).split(':')[1].strip()
                        days = list_item.select('.shop-hours__day')
                        times = list_item.select('.shop-hours__time')
                        opening_hours = dict()
                        for day, time in zip(days, times):
                            opening_hours[str(day.text).strip()] = str(time.text).strip()

                        i['opening_hours'] = opening_hours
                        i["google_map_url"] = list_item.find('a', {'class': 'gtm'}, href=True)['href']
                file_handler.write(json.dumps(json_data, ensure_ascii=False, indent=4))


# print("Data scraped")


# with open('Rimi.json','r',encoding='utf8') as f:
#     data = json.loads(f.read())
#     for i in data:
#         print(i)

scrap_rimi_data(url)
