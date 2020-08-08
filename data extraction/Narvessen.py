import json
import requests
import re
import time
from bs4 import BeautifulSoup

url = "https://narvesen.lv/"


def scrap_narvessen(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    all_scripts = soup.find_all('script')
    all_scripts = list(all_scripts)
    raw_json = re.findall(r"\{.*}", repr(all_scripts[2]))

    with open("Narvessen.json", 'w+') as f:
        data = json.dumps(raw_json[0], ensure_ascii=False, indent=5)
        f.write(json.loads(data))


scrap_narvessen(url)
