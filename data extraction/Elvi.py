import json
import requests
import re
from bs4 import BeautifulSoup

url = "http://elvi.lv/elvi-veikali/"


def scrape_elvi(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    all_scripts = soup.find_all('script')
    all_scripts = list(all_scripts)

    chunk = re.findall('var cities =((.|\n)*?)\];', str(all_scripts[13]))

    test = str(chunk[0][0]).replace('\n', '')
    test = list(test)

    new = [value for value in test if value != ' ']

    raw_str = ''.join(new)
    data = raw_str[:15983] + ']'
    output = re.sub(r'\bvalue\b', '"value"', data)
    output = re.sub(r'\bdata\b', '"data"', output)
    output = re.sub(r'\bid\b', '"id"', output)
    output = re.sub(r'\blink\b', '"link"', output)
    output = re.sub(r'\blat\b', '"lat"', output)
    output = re.sub(r'\blng\b', '"lng"', output)

    with open("Elvi.json", 'w', encoding='utf8') as f:
        f.write(json.loads(json.dumps(output, ensure_ascii=False, indent=4)))

    with open('Elvi.json', 'r', encoding='utf8') as f:
        data = json.loads(f.read())
        for i in data:
            print(i)




scrape_elvi(url)
