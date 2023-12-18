import time

from shapely import Point, Polygon, STRtree, MultiLineString, MultiPolygon, intersection

import geopandas as gpd

from app.constants import PROJ, METER
from app.pathfinder import Pathfinder


def time_wrapper(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Time '{func.__name__}': {end - start}")
        return result
    return wrapper


def geom_is_epsg_check(geom):
    try:
        coords = geom.centroid.coords[0]
    except:
        coords = [geom.centroid.x[0], geom.centroid.y[0]]
    if abs(coords[0]) > 180 and abs(coords[1]) > 180:
        return True
    return False


def gdf_to_epsg(gdf: gpd.GeoDataFrame):
    # if len(gdf) == 0:
    #     return gdf
    if gdf.crs is None:
        gdf.crs = PROJ.WGS_EPSG_STR
    geometry = gdf.geometry.iloc[0]
    if geom_is_epsg_check(geometry):
        gdf.crs = PROJ.EPSG_STR
    if gdf.crs == PROJ.WGS_EPSG_STR:
        gdf = gdf.to_crs(epsg=PROJ.EPSG)
    return gdf


def geom_epsg2wgs(geom):
    if not geom_is_epsg_check(geom):
        return geom
    gdf = gpd.GeoDataFrame(crs=PROJ.EPSG_STR, geometry=[geom])
    gdf = gdf.to_crs(epsg=PROJ.WGS_EPSG)
    geom = gdf.geometry[0]
    return geom


def geom_wgs2epsg(geom):
    if geom_is_epsg_check(geom):
        return geom
    gdf = gpd.GeoDataFrame(crs=PROJ.WGS_EPSG_STR, geometry=[geom])
    gdf = gdf.to_crs(epsg=PROJ.EPSG)
    geom = gdf.geometry[0]
    return geom


def get_gdf_by_center_buffer(gdf, center_point, buffer=METER.CENTER_BUFFER, circle=False, crop_circle_geom=False):
    gdf = gdf_to_epsg(gdf)
    center_point = geom_wgs2epsg(center_point)
    # pathfinder = Pathfinder()
    buildings_polygon_tree: STRtree = STRtree(gdf.geometry)

    center_polygon = center_point.buffer(buffer)

    gdf_center_buffer_list = []
    for i_, polygon_id in enumerate(buildings_polygon_tree.query(center_polygon)):
        gdf_building_item = gdf.iloc[polygon_id]
        if circle:
            if not center_polygon.intersects(gdf_building_item.geometry):
                gdf_building_item = None
            # # length, route = pathfinder.find_route_length(coords_0, coords_1)
            # length = Pathfinder.find_length_btw_two_points(gdf_building_item.geometry.centroid.coords[0], center_point.coords[0])
            # if length > buffer:
                gdf_building_item = None
            elif crop_circle_geom:
                if abs(intersection(center_polygon, gdf_building_item.geometry).area - gdf_building_item.geometry.area) > 1:
                    a = 2
                    gdf_building_item.geometry = intersection(center_polygon, gdf_building_item.geometry)
        if gdf_building_item is not None:
            gdf_center_buffer_list.append(gdf_building_item)
    result_gdf = gpd.GeoDataFrame(gdf_center_buffer_list)
    if len(result_gdf) == 0:
        return result_gdf
    result_gdf = gdf_to_epsg(result_gdf)
    return result_gdf


def get_geom_box(geom):
    if not isinstance(geom, list):
        geom = [geom]
    x_limits = []
    y_limits = []
    for p in list(geom):
        try:
            x_limits.append(min(p.boundary.xy[0]))
            x_limits.append(max(p.boundary.xy[0]))
            y_limits.append(min(p.boundary.xy[1]))
            y_limits.append(max(p.boundary.xy[1]))
        except:
            pass
    box_polygon = Polygon(
        [
            (min(x_limits), min(y_limits)),
            (min(x_limits), max(y_limits)),
            (max(x_limits), max(y_limits)),
            (max(x_limits), min(y_limits)),
        ]
    )
    return box_polygon


def get_geo_coord_list(geom):
    geom_point_coord_list = []
    if isinstance(geom, Point):
        coords = [x[0] for x in geom.coords.xy]
        geom_point_coord_list = [coords]
    else:
        poly_list = []
        if isinstance(geom, MultiPolygon):
            poly_list = list(geom.geoms)
        elif isinstance(geom, Polygon):
            poly_list = [geom]
        else:
            raise
        for poly in poly_list:
            for i_ in range(len(poly.exterior.xy[0])):
                geom_point_coord_list.append(
                    (
                        poly.exterior.xy[0][i_],
                        poly.exterior.xy[1][i_],
                    )
                )
    return geom_point_coord_list
