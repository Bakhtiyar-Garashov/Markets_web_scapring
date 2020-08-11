import json
import requests
import re
import time
from bs4 import BeautifulSoup
import Geo

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


def make_geojson(data):
    most_final = {"type": "FeatureCollection", "features": []}
    print("Narvessen extracting....")

    for entry, value in data.items():
        for acar, qiymet in value.items():
            parsed_coords = qiymet['coordinates'].split(',')
            if len(parsed_coords) == 2:
                lat = float(parsed_coords[0].strip()[:17])
                lon = float(parsed_coords[1].strip()[:17])
                coordinates = [lon, lat]
                dms_lat = Geo.fraction_to_min_sec(coordinates[1]) + " N"
                dms_lon = Geo.fraction_to_min_sec(coordinates[0]) + " E"
                X = coordinates[0]
                Y = coordinates[1]
                X1 = dms_lon
                Y1 = dms_lat
                props = dict()
                additional_props = Geo.get_info(lat, lon)
                props.update(qiymet)
                props.update(additional_props)
                final = dict()
                props['NOSAUKUMS'] = Geo.final_name(qiymet['name'], entry)
                props['SUBCATEGORY'] = 'Narvesen'
                props['GRUPA'] = 'Pārtikas/mājsaimniecības preču tīklu veikali'
                props['X'] = X
                props['Y'] = Y
                props['X1'] = X1
                props['Y1'] = Y1
                final['type'] = "Feature"
                final['geometry'] = {"type": "Point", "coordinates": coordinates}
                final['properties'] = props
                final = Geo.apdz_vietas_filter(final)
                most_final['features'].append(final)

    # most_final = {"type": "FeatureCollection", "features": [final]}
    return most_final


with open('Narvessen.json', 'r', encoding='utf8') as f:
    data = json.loads(f.read())
    geo_out = make_geojson(data)

    with open("Narvessen_out.json", "w+", encoding='utf8') as fayl:
        fayl.write(json.dumps(geo_out, ensure_ascii=False, indent=5))
        print("Narvessen extracted successfully!")
