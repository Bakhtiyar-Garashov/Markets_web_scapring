import json
import requests
import re
import os
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
        made_result = json.dumps(raw_json[0], ensure_ascii=False, indent=5)
        f.write(json.loads(made_result))


scrap_narvessen(url)


def make_geojson(data):
    most_final = {"type": "FeatureCollection", "features": []}

    print("Narvessen extracting......")
    # iterating over multiple 3 level nested dictionary
    for entry, value in data.items():
        for acar, qiymet in value.items():
            parsed_coords = qiymet['coordinates'].split(',')  # get lat lon from coord pair
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
                additional_props = Geo.get_info(lat, lon)  # get additional props from server with Geo.py
                props.update(qiymet)  # merge dicts
                props.update(additional_props)  # merge dicts
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
                # final = Geo.apdz_vietas_filter(final)
                most_final['features'].append(final)

    return most_final


with open('Narvessen.json', 'r', encoding='utf8') as f:
    json_input = json.loads(f.read())  # read json file and
    geo_out = make_geojson(json_input)  # invoke function to process

    # save result as json/geojson in dir
    with open(os.path.join(Geo.SAVE_PATH, "Narvessen_out.json"), "w+", encoding='utf8') as fayl:
        fayl.write(json.dumps(geo_out, ensure_ascii=False, indent=6))
        print("Narvessen extracted successfully!")
