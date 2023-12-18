import random

import cianparser
import pandas as pd
import geopandas as gpd
import numpy as np
import re
from dadata import Dadata
from shapely import Point as ShPoint
from geojson import Point as GeoPoint, Polygon as GeoPolygon

from app import settings
from app.visualizer import show


# смотреть на Буфер станций Метро
# искать по номеру дома, брать улицу, смотреть на пересечение Буферов улиц
#
#
#

def street_name_converter(street_name):
    street_name = street_name.strip()
    street_name = street_name.replace('Васильевского острова линия', 'линия В.О.')
    street_name = street_name.replace('проспект Малый Васильевского острова', 'Малый проспект В.О.')
    street_name = street_name.replace('проспект Большой Васильевского острова', 'Большой проспект В.О.')
    street_name = street_name.replace('набережная Реки Карповки', 'набережная реки Карповки')
    return street_name


def local_street_name_converter(street_name):
    local_street_name = street_name.lower()
    replace_map = [
        'проспект',
        'переулок',
        'набережная',
        'остров',
        'бульвар',
        'аллея',
        'шоссе',
        'дорога',
    ]
    for replacer in replace_map:
        local_street_name = local_street_name.replace(replacer, '')
    local_street_name = local_street_name.strip()
    return local_street_name


def house_number_name_converter(house_number_name):
    house_number_name = house_number_name.replace('К', ' к')
    house_number_name = house_number_name.replace('к', ' к')
    if len(house_number_name.split(' к')) == 2:
        korp = ''
        for i, k in enumerate(house_number_name.split(' к')[1]):
            new_korp = korp + k
            if not new_korp.isdigit():
                liter = ''
                house_number_name = f"{house_number_name.split(' к')[0]} к{korp} лит{house_number_name.split(' к')[1][i:]}"
                break
            korp = new_korp
    house_number_name = house_number_name.replace('  ', ' ')
    return house_number_name


def update_cian_by_buildings():
    # cian_data_filename = 'data/cian_parsing_result_sale_1_2_sankt-peterburg_02_Nov_2023_10_52_33_305909.csv'
    # cian_data_filename = 'data/cian_parsing_result_sale_room_1_i_0_sankt-peterburg_02_Nov_2023.csv'
    # cian_data_filename = f'data/result_cian_parsing_sale_room_all_sankt-peterburg_02_Nov_2023.csv'
    cian_data_filename = settings.files.cian_df_filename()
    df_cian = pd.read_csv(cian_data_filename)
    df_cian.street.fillna('', inplace=True)
    df_cian.house_number.fillna('', inplace=True)
    # show(cian_pickle)

    buildings_gdf_filename = settings.files.building_gdf
    gdf_buildings = gpd.GeoDataFrame.from_file(buildings_gdf_filename)
    gdf_buildings.rename({'housenumbe': 'house_number'}, axis=1, inplace=True)
    gdf_buildings.house_number.fillna('', inplace=True)
    gdf_buildings = gdf_buildings[gdf_buildings.house_number != '']

    token = "1501aa7ebe304e5df50910907248b8693481238d"
    secret = "00455ae0e2a898064abf69e065893761e19af964"
    dadata = Dadata(token, secret)

    error_street_name_set = set()
    error_street_counter = 0
    error_house_counter = 0
    error_empty_street = 0
    error_empty_house = 0
    error_empty_both = 0

    cian_buildings_list = []
    for i in range(len(df_cian)):
        cain_item = df_cian.iloc[i]
        street_name_source = cain_item.street
        house_number_name_source = cain_item.house_number

        local_dadata = {}

        if not (street_name_source and house_number_name_source):
            if not street_name_source and not house_number_name_source:
                error_empty_both += 1
            elif not street_name_source:
                error_empty_street += 1
            elif not house_number_name_source:
                error_empty_house += 1

            a = 2
            continue

        # if street_name != np.nan and street_name != float('nan') and house_number_name != np.nan and house_number_name != float('nan'):
        street_name = street_name_converter(street_name_source)
        house_number_name = house_number_name_converter(house_number_name_source)

        # Чистое название улицы
        building_items = gdf_buildings[gdf_buildings.street == street_name]
        # [i for i in gdf_buildings.street if (i is not None) and ('___ASD___' in i)]
        if len(building_items) == 0:
            # Формат "улица ЙЦУ"
            building_items = gdf_buildings[gdf_buildings.street == f'улица {street_name}']
        if len(building_items) == 0:
            # Формат "ЙЦУ улица"
            building_items = gdf_buildings[gdf_buildings.street == f'{street_name} улица']
        if len(building_items) == 0:
            # Поиск подстроки в строке с lower()
            local_street_name = local_street_name_converter(street_name)
            streets = [(i, street) for i, street in enumerate(gdf_buildings.street) if (street is not None) and (local_street_name in street.lower())]
            index_list = [i[0] for i in streets]
            building_items = gdf_buildings.iloc[index_list]
        # if len(building_items) == 0:
        #     # Запрос на получение адреса
        #     result = dadata.clean("address", f"Санкт-Петербург, {street_name_source}, {house_number_name_source}")
        #     local_dadata['street'] = result['street_with_type']
        #     local_dadata['house_number'] = result['house']
        #     local_dadata['center_x'] = result['geo_lon']
        #     local_dadata['center_y'] = result['geo_lat']
        #     house_point = ShPoint((result['geo_lon'], result['geo_lat']))
        #     house_polygon = house_point.buffer(0.0003)
        #     local_dadata['geometry'] = house_polygon

            a = 2
        if len(building_items) == 0:
            # Заполнение Множества неверных улиц
            if street_name not in error_street_name_set:
                print(f"{i} Error street name: {len(error_street_name_set)} '{street_name}'")
                error_street_name_set.add(street_name)
            error_street_counter += 1
            a = 2
            continue

        building_items_house_number = building_items[building_items.house_number == house_number_name]
        if len(building_items_house_number) > 1:
            #
            a = 2
            # continue
        if len(building_items_house_number) == 0:
            #
            house_numbers = [(i, house_number) for i, house_number in enumerate(building_items.house_number) if (house_number is not None) and (house_number_name.lower() == house_number.lower())]
            index_list = [i[0] for i in house_numbers]
            building_items_house_number = building_items.iloc[index_list]
        if len(building_items_house_number) == 0:
            #
            fullmatch = re.fullmatch(r'\d+[а-яА-Я]', house_number_name)
            if fullmatch:
                for i, s in enumerate(house_number_name):
                    if not s.isdigit():
                        local_house_number_name = f'{house_number_name[:i]} лит{house_number_name[i:]}'
                        building_items_house_number = building_items[building_items.house_number == local_house_number_name]
                        break
        if len(building_items_house_number) == 0:
            #
            house_number_list = list(building_items.house_number)
            asd = house_number_name
            a = 2
            error_house_counter += 1
            continue

        building_item = building_items_house_number.iloc[0]
        cian_buildings_list.append({
            "type": "Feature",
            "properties": {
                "n": i,
                "obj_id": building_item['obj_id'],
                "obj_type": building_item['obj_type'],
                "lvls": building_item['lvls'],
                "tags": building_item['tags'],
                "center_x": building_item['center_x'],
                "center_y": building_item['center_y'],
                "street": building_item['street'],
                "house_num": building_item['house_number'],

                "author": cain_item['author'],
                "author_t": cain_item['author_type'],
                "link": cain_item['link'],
                "city": cain_item['city'],
                "deal_type": cain_item['deal_type'],
                "accom_type": cain_item['accommodation_type'],
                "floor": cain_item['floor'],
                "floors_c": cain_item['floors_count'],
                "rooms_c": cain_item['rooms_count'],
                'tot_meters': cain_item['total_meters'],
                'pr_m2': cain_item['price_per_m2'],
                'pr_month': cain_item['price_per_month'],
                'commis': cain_item['commissions'],
                'price': cain_item['price'],
                'district': cain_item['district'],
                'undergr': cain_item['underground'],
                'resident': cain_item['residential_complex'],
            },
            "geometry":  building_item['geometry'],
        })

    print(f"Errors: street - {error_street_counter}, house - {error_house_counter}")
    print(f"Errors empty: street - {error_empty_street}, house - {error_empty_house}, both - {error_empty_both}")
    error_sum = error_street_counter + error_house_counter + error_empty_street + error_empty_house + error_empty_both
    print(f"Error sum: {error_sum} + {len(cian_buildings_list)} = {len(df_cian)}")
    print(len(cian_buildings_list) / len(df_cian))

    cian_buildings_gdf = gpd.GeoDataFrame.from_features(cian_buildings_list)
    return cian_buildings_gdf


if __name__ == '__main__':
    cian_buildings_gdf = update_cian_by_buildings()
    cian_result_gdf_filename = settings.files.cian_gdf
    cian_buildings_gdf.to_file(cian_result_gdf_filename, encoding='utf-8')
    gdf_buildings = gpd.GeoDataFrame.from_file(cian_result_gdf_filename)
