import json
import requests
import re
import time
from bs4 import BeautifulSoup

url = "https://citro.lv/musu-veikali/"


def scrap_citro(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    all_scripts = soup.find_all('script')
    all_scripts = list(all_scripts)
    chunk = repr(all_scripts[15])
    pattern = r"\[(.|\n)*];"
    print(re.findall(pattern, chunk))


scrap_citro(url)
