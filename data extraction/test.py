from bs4 import BeautifulSoup
import requests

url = "http://elvi.lv/veikali/engure-elvi-veikals/"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
info_div = soup.find('div', attrs={'class': 'info'})
test = dict()

props = info_div.select('p')
for i in props:
    print(i.text)

print(test)
