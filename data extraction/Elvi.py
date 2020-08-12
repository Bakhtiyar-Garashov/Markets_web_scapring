import json
import requests
import re
import os
import Geo
from bs4 import BeautifulSoup

url = "http://elvi.lv/elvi-veikali/"


def scrap_elvi(url):
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
    output = json.loads(output)
    for i in output:
        additional_data = get_html_data(i['data'][0]['link'])
        i['data'][0]['address'] = additional_data['Adrese']
        i['data'][0]['email'] = additional_data['E-pasts']
        i['data'][0]['phone'] = additional_data['Tālruņa numurs']
        i['data'][0]['working_hours'] = additional_data['Darba laiks']

    with open("Elvi.json", 'w', encoding='utf8') as f:
        f.write(json.dumps(output, ensure_ascii=False, indent=4))


def get_html_data(chain_url):
    response = requests.get(chain_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    info_div = soup.find('div', attrs={'class': 'info'})
    test = dict()
    props = info_div.select('p')
    test[props[0].text] = props[1].text
    test[props[2].text] = props[3].text
    test[props[4].text] = props[5].text
    test[props[6].text] = props[7].text

    return test


scrap_elvi(url)


def make_geojson(data):
    most_final = {"type": "FeatureCollection", "features": []}
    print("Elvi extracting......")
    # iterate over dictionary
    for each in data:
        lat = float(each['data'][0]['lat'])
        lon = float(each['data'][0]['lng'])
        if lat != lon:
            coordinates = [lon, lat]
            dms_lat = Geo.fraction_to_min_sec(coordinates[1]) + " N"
            dms_lon = Geo.fraction_to_min_sec(coordinates[0]) + " E"
            X = coordinates[0]
            Y = coordinates[1]
            X1 = dms_lon
            Y1 = dms_lat
            props = dict()
            additional_props = Geo.get_info(lat, lon)
            props.update(each)
            props.update(additional_props)
            final = dict()
            props['NOSAUKUMS'] = "Elvi"
            props['SUBCATEGORY'] = 'Elvi'
            props['GRUPA'] = 'Pārtikas/mājsaimniecības preču tīklu veikali'
            props['X'] = X
            props['Y'] = Y
            props['X1'] = X1
            props['Y1'] = Y1
            final['type'] = "Feature"
            final['geometry'] = {"type": "Point", "coordinates": coordinates}
            final['properties'] = props
            most_final['features'].append(final)

    return most_final


with open('Elvi.json', 'r', encoding='utf8') as f:
    data = json.loads(f.read())
    geo_out = make_geojson(data)

    # save result as json/geojson in dir
    with open(os.path.join(Geo.SAVE_PATH, "Elvi_out.json"), "w+", encoding='utf8') as fayl:
        fayl.write(json.dumps(geo_out, ensure_ascii=False, indent=6))
        print("Elvi extracted successfully!")
