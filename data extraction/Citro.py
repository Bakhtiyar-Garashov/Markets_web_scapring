import json
import requests
import re
import os
import Geo
from bs4 import BeautifulSoup

url = "https://citro.lv/musu-veikali/"


def scrap_citro(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    all_scripts = soup.find_all('script')
    all_scripts = list(all_scripts)
    chunk = all_scripts[15]
    test = r"\[(.|\n)*];"
    found = re.search(test, str(chunk))
    result = found.group(0)
    useless = [
        '"Veikals un kafejnīca Apsīte"',
        '"Bodnieki"',
        '"Ēdoles dzirnavas"',
        '"Pārslas"',
        '"Saktas"',
        '"Ģipkas veikals"',
        '"Veikals Nr.22"',
        '"Zvirgzdu pansija"',
        '"Spāres veikals"',
        '"Gundegas"',
        '"Rozes"']

    output = re.sub(r'\bcoords\b', '"coords"', result)
    output = re.sub(r'\bshopLogo\b', '"shopLogo"', output)
    output = re.sub(r'\blat\b', '"lat"', output)
    output = re.sub(r'\blng\b', '"lng"', output)
    output = re.sub(r'\bcontent\b:', '"content":', output)
    output = output.replace("'", '"')
    output = re.sub(r'\bstyle="margin:0 0 5px 0;font-size:16px;"', "style='margin:0 0 5px 0;font-size:16px;'", output)
    for each in useless:
        output = output.replace(each, "'" + each + "'")
    output = output.replace("'\"", "'")
    output = output.replace("\"'", "'")
    output = output.strip()
    output = output[:len(output) - 126] + "]"
    final = []
    data = json.loads(output)

    for i in data:
        temp_dict = dict()
        souplar = BeautifulSoup(i['content'], 'html.parser')
        address = souplar.find('strong').text
        working_hours = souplar.find_all('p')[1].text
        temp_dict["coords"] = i['coords']
        temp_dict["logo"] = i['shopLogo']
        temp_dict["info"] = i['content']
        temp_dict["address"] = address
        temp_dict["working_hours"] = working_hours
        final.append(temp_dict)

    with open("Citro.json", "w+", encoding='utf-8') as f:
        f.write(json.dumps(final, ensure_ascii=False, indent=5))


scrap_citro(url)


# get store type based on image name (logo-xs | logo-xs-mini)
def get_citro_type(entry):
    image_url = entry["logo"]
    url_parts_list = image_url.split('/')
    citro_class = url_parts_list[len(url_parts_list) - 1]
    if citro_class == "logo-xs-mini.svg":
        return "Citro mini"
    else:
        return "Citro"


def make_geojson(data):
    most_final = {"type": "FeatureCollection", "features": []}
    print("Citro extracting......")
    # iterate over dictionary
    for each in data:
        lat = float(each["coords"]["lat"])
        lon = float(each["coords"]["lng"])
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
            props['NOSAUKUMS'] = get_citro_type(each)
            props['SUBCATEGORY'] = "Citro"
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


with open('Citro.json', 'r', encoding='utf8') as f:
    data = json.loads(f.read())
    geo_out = make_geojson(data)

    with open(os.path.join(Geo.SAVE_PATH, "Citro_out.json"), "w+", encoding='utf8') as fayl:
        fayl.write(json.dumps(geo_out, ensure_ascii=False, indent=6))
        print("Citro extracted successfully!")
