import json
import Geo
import os
import urllib3

url = "https://www.drogas.lv/lv/mahazyny/all"


def scrap_drogas(url):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    raw_json = response.data.decode('utf-8')

    with open("Drogas.json", "w+", encoding='utf8') as f:
        f.write(json.loads(json.dumps(raw_json, ensure_ascii=False, indent=5)))


scrap_drogas(url)


def make_geojson(data):
    most_final = {"type": "FeatureCollection", "features": []}
    print("Drogas extracting......")
    # iterate over dictionary
    for each in data["features"]:
        lat = float(each["geometry"]["coordinates"][1])
        lon = float(each["geometry"]["coordinates"][0])
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
        props['NOSAUKUMS'] = each['properties']["storeName"]
        props['SUBCATEGORY'] = 'Drogas'
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


with open('Drogas.json', 'r', encoding='utf8') as f:
    data = json.loads(f.read())
    geo_out = make_geojson(data)

    with open(os.path.join(Geo.SAVE_PATH, "Drogas_out.json"), "w+", encoding='utf8') as fayl:
        fayl.write(json.dumps(geo_out, ensure_ascii=False, indent=6))
        print("Drogas extracted successfully!")
