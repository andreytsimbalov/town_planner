import math
import random
import time

import pandas as pd
import geopandas as gpd
import numpy as np
import re
from shapely import STRtree, Point, MultiLineString, Polygon, intersection

from app import settings, utils
from app.constants import PROJ, METER
from app.data_proc import load_data, save_data
from app.pathfinder import Pathfinder
from app.visualizer import show
from work_steps.generate_cian_obj_dict import PointData


def get_cian_feature(cian_item, cian_dict_item):
    house_area = cian_item.geometry.area

    view_buildings_max_lvl = cian_dict_item['buildings'].mean_lvl
    if len(cian_dict_item['buildings'].gdf):
        view_buildings_max_lvl = max(cian_dict_item['buildings'].gdf['lvls'])

    walk_metro_min_length_obj_name = None
    if cian_dict_item['metro'].min_length_obj is not None:
        walk_metro_min_length_obj_name = cian_dict_item['metro'].min_length_obj['name']

    feature = {
        "type": "Feature",
        "properties": {
            'n': cian_item['n'],
            'obj_id': cian_item['obj_id'],
            'obj_type': cian_item['obj_type'],
            'lvls': cian_item['lvls'],
            # 'tags': cian_item['tags'],
            'center_x': cian_item['center_x'],
            'center_y': cian_item['center_y'],
            'street': cian_item['street'],
            'house_num': cian_item['house_num'],
            'author': cian_item['author'],
            'author_t': cian_item['author_t'],
            # 'link': cian_item['link'],
            # 'city': cian_item['city'],
            # 'deal_type': cian_item['deal_type'],
            'accom_type': cian_item['accom_type'],
            'floor': cian_item['floor'],
            'floors_count': cian_item['floors_c'],
            'rooms_count': cian_item['rooms_c'],
            'total_meters': cian_item['tot_meters'],
            'price_m2': cian_item['pr_m2'],
            # 'price_month': cian_item['pr_month'],
            'commis': cian_item['commis'],
            'price': cian_item['price'],
            'district': cian_item['district'],
            'metro': cian_item['undergr'],
            'resident': cian_item['resident'],

            'house_area': house_area,
            'view_buildings_area': cian_dict_item['buildings'].area_square,
            'view_buildings_count': cian_dict_item['buildings'].count,
            'view_buildings_mean_lvl': cian_dict_item['buildings'].mean_lvl,
            'view_buildings_max_lvl': view_buildings_max_lvl,

            'walk_metro_count': cian_dict_item['metro'].count,
            'walk_metro_min_length': cian_dict_item['metro'].min_length,
            'walk_metro_min_length_obj_name': walk_metro_min_length_obj_name,

            'walk_nature_count': cian_dict_item['nature'].count,
            'walk_nature_max_obj_square': cian_dict_item['nature'].max_obj_square,
            'walk_nature_objs_sum_square': cian_dict_item['nature'].objs_sum_square,
            'walk_nature_min_length': cian_dict_item['nature'].min_length,

            'bad_air_garbage_count': cian_dict_item['garbage'].count,
            'bad_air_garbage_max_obj_square': cian_dict_item['garbage'].max_obj_square,
            'bad_air_garbage_objs_sum_square': cian_dict_item['garbage'].objs_sum_square,
            'bad_air_garbage_min_length': cian_dict_item['garbage'].min_length,

            'walk_water_count': cian_dict_item['water'].count,
            'walk_water_max_obj_square': cian_dict_item['water'].max_obj_square,
            'walk_water_objs_sum_square': cian_dict_item['water'].objs_sum_square,
            'walk_water_min_length': cian_dict_item['water'].min_length,
        },
        "geometry": cian_item.geometry,
    }
    return feature


def get_cain_gdf_by_dict():
    # PointData
    cian_dict = load_data(settings.files.cian_by_objs_dict_pickle)
    gdf_cian = utils.gdf_to_epsg(load_data(settings.files.cian_gdf_pickle))

    feature_list = []
    for i in range(len(gdf_cian)):
        print(f"'get_cain_gdf_by_dict' step: {i}")
        cian_item = gdf_cian.iloc[i]
        cian_dict_item = cian_dict[i]
        feature = get_cian_feature(cian_item, cian_dict_item)
        feature_list.append(feature)

    gdf_cian_by_dict = gpd.GeoDataFrame.from_features(feature_list, crs=PROJ.EPSG)
    return gdf_cian_by_dict


if __name__ == '__main__':
    gdf = get_cain_gdf_by_dict()
    save_data(gdf, settings.files.cian_gdf_by_dict_pickle)
    gdf = load_data(settings.files.cian_gdf_by_dict_pickle)
