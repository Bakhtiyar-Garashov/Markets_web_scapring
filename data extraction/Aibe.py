import json
import requests
import os
import Geo

url = "http://www.aibe.lv/shops.json"


def scrap_aibe(url):
    response = requests.get(url)
    raw_json = response.json()

    with open("Aibe.json", "w+", encoding='utf8') as f:
        f.write(json.dumps(raw_json, ensure_ascii=False, indent=5))

    return json.loads(json.dumps(raw_json, ensure_ascii=False, indent=4))


scrap_aibe(url)


def make_geojson(data):
    most_final = {"type": "FeatureCollection", "features": []}
    print("Aibe extracting......")
    # iterate over dictionary
    for each in data:
        if data[each]["shopmapitem01_lat"]["value"] and data[each]["shopmapitem01_lng"]["value"].strip() != "":
            latitude = data[each]["shopmapitem01_lat"]["value"].replace(',', '.').strip()[:17]
            longtitude = data[each]["shopmapitem01_lng"]["value"].replace(',', '.').strip()[:17]
            if '.' in latitude and '.' in longtitude:
                lat = float(latitude)
                lon = float(longtitude)
                coordinates = [lon, lat]
                dms_lat = Geo.fraction_to_min_sec(coordinates[1]) + " N"
                dms_lon = Geo.fraction_to_min_sec(coordinates[0]) + " E"
                X = coordinates[0]
                Y = coordinates[1]
                X1 = dms_lon
                Y1 = dms_lat
                props = dict()
                additional_props = Geo.get_info(lat, lon)
                props.update(data[each])
                props.update(additional_props)
                final = dict()
                props['NOSAUKUMS'] = "Aibe"
                props['SUBCATEGORY'] = data[each]["shopmapitem01_type"]["value"]
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


with open('Aibe.json', 'r', encoding='utf8') as f:
    data = json.loads(f.read())
    geo_out = make_geojson(data)

    with open(os.path.join(Geo.SAVE_PATH, "Aibe_out.json"), "w+", encoding='utf8') as fayl:
        fayl.write(json.dumps(geo_out, ensure_ascii=False, indent=6))
        print("Aibe extracted successfully!")
