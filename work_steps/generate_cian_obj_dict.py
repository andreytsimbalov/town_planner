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


class PointData:
    def __init__(
        self, cian_item, gdf, radius, min_length=None, min_length_obj=None, objs_sum_square=None, max_obj_square=None, max_obj_square_obj=None,
        mean_lvl=None
    ):
        self.cian_item = cian_item
        self.gdf = gdf
        self.radius = radius
        self.min_length = min_length
        self.min_length_obj = min_length_obj
        self.area_square = (radius ** 2) * math.pi
        self.objs_sum_square = objs_sum_square
        self.max_obj_square = max_obj_square
        self.max_obj_square_obj = max_obj_square_obj
        self.count = len(gdf)
        self.mean_lvl = mean_lvl


def get_point_data(cian_item, gdf_buildings, gdf_metro, gdf_nature, gdf_garbage, gdf_water, pathfinder):

    center_point = cian_item.geometry.centroid
    config = [
        dict(name='buildings', gdf=gdf_buildings, rad=METER.BUILD_LVL_VIEW, square=False, lvl=True, length=False),
        dict(name='metro', gdf=gdf_metro, rad=METER.WALK, square=False, lvl=False, length=True),
        dict(name='nature', gdf=gdf_nature, rad=METER.WALK, square=True, lvl=False, length=True),
        dict(name='garbage', gdf=gdf_garbage, rad=METER.BAD_AIR, square=True, lvl=False, length=True),
        dict(name='water', gdf=gdf_water, rad=METER.WALK, square=True, lvl=False, length=True),
    ]

    data_dict = {}

    for conf in config:
        gdf_nearest = utils.get_gdf_by_center_buffer(conf['gdf'], center_point, conf['rad'], circle=True)
        center_buffer = center_point.buffer(conf['rad'])

        min_length = 999999
        min_length_obj = None
        objs_sum_square = 0
        max_obj_square = 0
        max_obj_square_obj = None
        mean_lvl = []

        if gdf_nearest is not None:
            for i in range(len(gdf_nearest)):
                gdf_item = gdf_nearest.iloc[i]

                if conf['length']:
                    geom_point_coord_list = utils.get_geo_coord_list(gdf_item.geometry)
                    for geom_point_coord in geom_point_coord_list:
                        coords_0 = [x[0] for x in center_point.coords.xy]
                        coords_1 = geom_point_coord
                        length = pathfinder.find_length_btw_two_points(coords_0, coords_1)
                        """
                        point_0 = Point(coords_0)
                        point_1 = Point(coords_1)
                        point_0 = utils.geom_epsg2wgs(point_0)
                        point_1 = utils.geom_epsg2wgs(point_1)
                        coords_pth_0 = [x[0] for x in point_0.coords.xy]
                        coords_pth_1 = [x[0] for x in point_1.coords.xy]
                        length_2, _ = pathfinder.find_route_length(coords_pth_0, coords_pth_1)
                        """
                        if length < min_length:
                            min_length = length
                            min_length_obj = gdf_item
                if conf['square']:
                    objs_sum_square += intersection(center_buffer, gdf_item.geometry).area
                    if gdf_item.geometry.area > max_obj_square:
                        max_obj_square = gdf_item.geometry.area
                        max_obj_square_obj = gdf_item
                if conf['lvl']:
                    try:
                        lvl = gdf_item.lvls
                        if 0 <= lvl <= 30:
                            mean_lvl.append(lvl)
                    except:
                        pass

        min_length = min_length if min_length != 999999 else None
        min_length_obj = min_length_obj
        objs_sum_square = objs_sum_square
        max_obj_square = max_obj_square
        max_obj_square_obj = max_obj_square_obj
        mean_lvl = np.mean(mean_lvl) if mean_lvl else None

        data_dict[conf['name']] = PointData(
            cian_item, gdf_nearest, conf['rad'], min_length, min_length_obj, objs_sum_square, max_obj_square, max_obj_square_obj, mean_lvl
        )
    return data_dict


def generate_cian_gdf_obj_dict(save_in_place=False):
    start_time = time.time()

    # pathfinder = Pathfinder()
    # save_data(pathfinder, settings.files.pathfinder_pickle)
    pathfinder = load_data(settings.files.pathfinder_pickle)

    gdf_cian = utils.gdf_to_epsg(load_data(settings.files.cian_gdf_pickle))

    gdf_buildings = utils.gdf_to_epsg(load_data(settings.files.building_gdf_pickle))
    gdf_metro = utils.gdf_to_epsg(load_data(settings.files.metro_gdf_pickle))
    gdf_nature = utils.gdf_to_epsg(load_data(settings.files.nature_gdf_pickle))
    gdf_garbage = utils.gdf_to_epsg(load_data(settings.files.garbage_gdf_pickle))
    gdf_water = utils.gdf_to_epsg(load_data(settings.files.water_gdf_pickle))
    # show(gdf_metro)

    # gdf_cian: gpd.GeoDataFrame = gpd.GeoDataFrame.from_file(settings.Files.cian_gdf)
    # gdf_cian = utils.gdf_to_epsg(gdf_cian)
    # show(gdf_cian, Point((30.276424072543968, 59.94587683528832)))

    # gdf_buildings: gpd.GeoDataFrame = gpd.GeoDataFrame.from_file(settings.Files.building_gdf)
    # gdf_buildings.rename({'housenumbe': 'house_number'}, axis=1, inplace=True)
    # gdf_buildings.house_number.fillna('', inplace=True)
    # gdf_buildings = load_data(settings.files.building_gdf_pickle)
    # gdf_buildings = utils.gdf_to_epsg(gdf_buildings)

    # save_data

    # buildings_polygon_tree: STRtree = STRtree(gdf_buildings.geometry)

    cian_dict = {}

    iter_time = time.time()
    for i in range(len(gdf_cian)):
        print(
            f'Update obj: {i} '
            f'[{time.time() - iter_time}] '
            f'[{time.time() - start_time}] '
            f'[{round((time.time() - start_time) / 60, 2)}] '
            f'[{round((time.time() - start_time) / 60 / 60, 2)}] '
        )
        iter_time = time.time()

        cian_item = gdf_cian.iloc[i]
        cian_data = get_point_data(cian_item, gdf_buildings, gdf_metro, gdf_nature, gdf_garbage, gdf_water, pathfinder)
        # show(gdf_nearest_buildings, center_point, METER.WALK)
        cian_dict[i] = cian_data
        # if save_in_place and i % 1000 == 0:
        #     save_data(cian_dict, settings.files.cian_by_objs_dict_pickle)

    return cian_dict


if __name__ == '__main__':
    cian_by_obj_dict = generate_cian_gdf_obj_dict(True)
    # save_data(cian_by_obj_dict, settings.files.cian_by_objs_dict_pickle)
    # cian_by_obj_dict = load_data(settings.files.cian_by_objs_dict_pickle)
