import json
import DB
from pyproj import Transformer
import requests
import math
from datetime import datetime, time


# transform to Latvian coord system
def convert_to_lks(coords):
    transformer = Transformer.from_crs(4326, 25884)
    converted = transformer.transform(coords[1], coords[0])
    return round(converted[1]), round(converted[0])


def fraction_to_min_sec(coord):
    coord = abs(coord)
    deg = math.floor(coord)
    coord = (coord - deg) * 60
    min = math.floor(coord)
    sec = round((coord - min) * 60, 3)
    return f"{deg}°{min}'{sec}\""


# geocoding from KIJS server
def geo_code(x, y):
    url = f"https://maps.kartes.lv/kijs/v3/JSED/api?method=reverse_geocoding&x={x}&y={y}";
    response = requests.get(url)
    if response:
        result = json.loads(response.text)
        return result
    return False


# important props from original data
def get_needed_data(original):
    if original:
        apdzvieta = original['apdz_vieta'] if original['apdz_vieta'] != "" and original[
            'apdz_vieta'] is not None else ""
        iela = original['iela'] if original['iela'] != "" and original['iela'] is not None else ""
        pasta_indekss = original['index'] if original['index'] != "" and original['index'] is not None else ""

        if original['korpuss'] and original['korpuss'] != "":
            maja = original['maja'] + " k-" + original['korpuss']
        else:
            maja = original['maja'] if original['maja'] != "" and original['maja'] is not None else ""

        terit_vien = original['terit_vien'] if original['terit_vien'] != "" and original[
            'terit_vien'] is not None else ""
        admin_vien = original['admin_vien'] if original['admin_vien'] != "" and original[
            'admin_vien'] is not None else ""
        data_dict = {"APDZ_VIETA": apdzvieta,
                     "IELA": iela,
                     "indekss": pasta_indekss,
                     "MAJA": maja,
                     "ADMIN_VIEN": admin_vien,
                     "TERIT_VIEN": terit_vien}
    else:
        data_dict = {"APDZ_VIETA": "",
                     "IELA": "",
                     "indekss": "",
                     "MAJA": "",
                     "ADMIN_VIEN": "",
                     "TERIT_VIEN": ""}

    return data_dict


def final_name(init, tip):
    if tip == 'veikals' or tip == 'degvielas-uzpildes-stacija-dus':
        return init + " (veikals)"
    elif tip == 'kiosks':
        return init + " (kiosks)"


def prettify_tag_name(entry):
    result = dict()
    for key, value in entry.items():
        new_key = key.replace(':', '_')
        result[new_key] = value
    return result


def apdz_vietas_filter(data):
    result = dict()
    validApdzVietas = ['Rīga', 'Valmiera', 'Cēsis', 'Kuldīga', 'Jelgava', 'Daugavpils', 'Ventspils', 'Liepāja',
                       'Sigulda', 'Tukums', 'Bauska', 'Ādaži']

    apdzVieta = data['properties']["APDZ_VIETA"]

    if apdzVieta in validApdzVietas:
        result = data

    return result if result else None


# db process
def get_info(lat, lon):
    connection = DB.connect_db()
    curs = connection.cursor()
    curs.execute("SELECT returned from osm_poi where lat=%s and lon=%s", (lat, lon))
    data = curs.fetchall()
    if data:
        # record exists in db
        curs.execute("SELECT original from osm_poi where lat=%s and lon=%s", (lat, lon))
        original_data = curs.fetchall()
        original_data = json.loads(original_data[0][0])

        return get_needed_data(original_data)
    else:
        # record doesnt exist- add it into db
        lks = convert_to_lks([lon, lat])
        address_data = geo_code(lks[0], lks[1])
        parsed_data = get_needed_data(address_data)
        insert_curs = connection.cursor()
        insert_query = """INSERT INTO osm_poi
                       (lat, lon, x, y, returned, original, date_exe) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        insert_curs.execute(insert_query, (lat, lon, lks[0], lks[1], json.dumps(parsed_data), json.dumps(address_data),
                                           datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        connection.commit()
        print("New poi added successfully")
        return parsed_data
