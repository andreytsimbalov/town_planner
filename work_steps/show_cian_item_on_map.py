import math
import random
import time

import pandas as pd
import geopandas as gpd
import numpy as np
import re
from shapely import STRtree, Point, MultiLineString, Polygon, intersection

from app import settings, utils, pathfinder
from app.constants import PROJ, METER
from app.data_proc import load_data, save_data
from app.pathfinder import Pathfinder
from app.visualizer import show, ShowColors, show_list_geometry_gdf, ShowGdfItem
from work_steps.generate_cian_obj_dict import PointData


#
# config = [
#     dict(name='buildings', gdf=gdf_buildings, rad=METER.BUILD_LVL_VIEW, square=False, lvl=True, length=False),
#     dict(name='metro', gdf=gdf_metro, rad=METER.WALK, square=False, lvl=False, length=True),
#     dict(name='nature', gdf=gdf_nature, rad=METER.WALK, square=True, lvl=False, length=True),
#     dict(name='garbage', gdf=gdf_garbage, rad=METER.BAD_AIR, square=True, lvl=False, length=True),
#     dict(name='water', gdf=gdf_water, rad=METER.WALK, square=True, lvl=False, length=True),
# ]

def show_buildings():
    gdf = load_data(settings.files.building_gdf_pickle)
    show(gdf)


def show_cian():
    gdf = load_data(settings.files.cian_gdf_pickle)
    show(gdf)


def show_nature():
    gdf = load_data(settings.files.nature_gdf_pickle)
    show(gdf, color=ShowColors.green)


def show_water():
    gdf = load_data(settings.files.water_gdf_pickle)
    show(gdf, color=ShowColors.blue)


def show_garbage():
    gdf = load_data(settings.files.garbage_gdf_pickle)
    show(gdf, color=ShowColors.red)


def show_cian_item(number=123):
    cian_dict = load_data(settings.files.cian_by_objs_dict_pickle)
    gdf = load_data(settings.files.cian_gdf_by_dict_pickle)
    pathfinder = load_data(settings.files.pathfinder_pickle)

    gdf_cian_item = gdf.iloc[number]
    cian_dict_item = cian_dict[number]
    cian_item = gpd.GeoDataFrame(crs=PROJ.EPSG_STR, geometry=[gdf_cian_item.geometry])

    center_point = cian_item.geometry.centroid
    config = [
        dict(name='buildings', use_ph=True, rad=METER.BUILD_LVL_VIEW),
        dict(name='metro', use_ph=True, rad=METER.WALK),
        dict(name='nature', use_ph=True, rad=METER.WALK),
        dict(name='garbage', use_ph=False, rad=METER.BAD_AIR),
        dict(name='water', use_ph=True, rad=METER.WALK),
    ]

    gdf_dict = {}

    for conf in config:
        # gdf_nearest = utils.get_gdf_by_center_buffer(cian_dict_item[conf['name']].gdf, center_point, conf['rad'], circle=True)
        gdf_nearest = cian_dict_item[conf['name']].gdf
        center_buffer = center_point.buffer(conf['rad'])

        if gdf_nearest is not None:
            remove_i_gdf = []
            for i in range(len(gdf_nearest)):
                gdf_item = gdf_nearest.iloc[i]
                # intersection(center_buffer, gdf_item.geometry)

                is_remove_i_gdf = True
                geom_point_coord_list = utils.get_geo_coord_list(gdf_item.geometry)
                for geom_point_coord in geom_point_coord_list:
                    try:
                        coords_0 = [x[0] for x in center_point.coords.xy]
                    except:
                        coords_0 = [center_point.centroid.x[0], center_point.centroid.y[0]]
                    coords_1 = geom_point_coord
                    length = pathfinder.find_length_btw_two_points(coords_0, coords_1)
                    # if conf['use_ph']:
                    #     point_0 = Point(coords_0)
                    #     point_1 = Point(coords_1)
                    #     point_0 = utils.geom_epsg2wgs(point_0)
                    #     point_1 = utils.geom_epsg2wgs(point_1)
                    #     coords_pth_0 = [x[0] for x in point_0.coords.xy]
                    #     coords_pth_1 = [x[0] for x in point_1.coords.xy]
                    #     length, _ = pathfinder.find_route_length(coords_pth_0, coords_pth_1)
                    # else:
                    #     length = pathfinder.find_length_btw_two_points(coords_0, coords_1)
                    if length <= conf['rad']:
                        is_remove_i_gdf = False
                        break
                if is_remove_i_gdf:
                    remove_i_gdf.append(i)
            for i in remove_i_gdf[::-1]:
                gdf_nearest.drop(index=gdf_nearest.iloc[i].name, inplace=True)
        gdf_dict[conf['name']] = gdf_nearest

    center_gdf = ShowGdfItem(gdf=cian_item, color=ShowColors.blue)
    list_geometry_gdf = [
        ShowGdfItem(gdf=gdf_dict['buildings'], buffer=METER.BUILD_LVL_VIEW, color=ShowColors.black),
        ShowGdfItem(gdf=gdf_dict['metro'], buffer=METER.WALK, color=ShowColors.red),
        ShowGdfItem(gdf=gdf_dict['nature'], buffer=METER.WALK, color=ShowColors.green),
        ShowGdfItem(gdf=gdf_dict['garbage'], buffer=METER.BAD_AIR, color=ShowColors.yellow),
        ShowGdfItem(gdf=gdf_dict['water'], buffer=METER.WALK, color=ShowColors.blue),
    ]

    show_list_geometry_gdf(center_gdf, list_geometry_gdf)
    return cian_item


if __name__ == '__main__':
    show_list = [
        # show_buildings,
        # show_cian,
        # show_nature,
        # show_water,
        # show_garbage,
    ]
    for show_func in show_list:
        show_func()
    gdf_item_one = show_cian_item()
