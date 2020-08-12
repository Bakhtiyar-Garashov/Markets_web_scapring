import json
import requests
import re
import os
import Geo
from bs4 import BeautifulSoup

url = "https://www.latts.lv/lv/veikali"


def scrap_lats(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    all_scripts = soup.find_all('script')
    all_scripts = list(all_scripts)
    final = []
    data = repr(all_scripts[12])
    pattern = r"\{.*}"
    result = re.findall(pattern, data)

    address_patter = r"<h3>(.*?)\."
    # r"<h3>(.*?)\/h3>"
    lat = r'\"latitude\":[-+]?(\d+\.\d+)'
    lon = r'\"longitude\":[-+]?(\d+\.\d+)'
    for i in result:
        dicts = dict()
        prop = re.findall(address_patter, i)
        address = prop[0].replace('"', "'")
        full_address = address.split('</a>')
        if full_address:
            for each in full_address:
                each_text = BeautifulSoup(each, 'html.parser')
                dicts['address'] = each_text.text[:len(each_text.text) - 15]

        dicts['feature'] = "Point"
        dicts['lat'] = re.findall(lat, i)[0] if re.findall(lat, i) else ""
        dicts['lon'] = re.findall(lon, i)[0] if re.findall(lon, i) else ""
        final.append(dicts)

    with open("Lats.json", "w", encoding='utf8') as f:
        f.write(json.dumps(final, ensure_ascii=False, indent=4))


scrap_lats(url)


def make_geojson(data):
    most_final = {"type": "FeatureCollection", "features": []}
    print("Lats extracting......")
    # iterate over dictionary
    for each in data:
        lat = float(each["lat"].strip()[:17])
        lon = float(each["lon"].strip()[:17])
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
        props['NOSAUKUMS'] = "Lats"
        props['SUBCATEGORY'] = "Lats"
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


with open('Lats.json', 'r', encoding='utf8') as f:
    data = json.loads(f.read())
    geo_out = make_geojson(data)

    with open(os.path.join(Geo.SAVE_PATH, "Lats_out.json"), "w+", encoding='utf8') as fayl:
        fayl.write(json.dumps(geo_out, ensure_ascii=False, indent=6))
        print("Lats extracted successfully!")
