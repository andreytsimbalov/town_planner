from OSMPythonTools.nominatim import Nominatim
# from OSMPythonTools.overpass import Overpass
from geojson import Polygon as GeoPolygon, Point as GeoPoint, LineString, MultiPolygon
from shapely import Point as ShPoint, Polygon as ShPolygon, STRtree

import geopandas as gpd

from app.constants import PROJ
from app.pathfinder import Pathfinder


def get_city_area_id(city_name='Russia, Saint Petersburg'):
    nominatim = Nominatim()
    # overpass = Overpass()
    area_id = nominatim.query(city_name).areaId()
    return area_id


def sh2geo_geom(geom):
    if isinstance(geom, ShPoint):
        res_geom = GeoPoint(geom.centroid)
    elif isinstance(geom, ShPolygon):
        polygon_coords = []
        for i in range(len(geom.boundary.xy[0])):
            polygon_coords.append((geom.boundary.xy[0][i], geom.boundary.xy[1][i],))
        res_geom = GeoPolygon(polygon_coords)
    else:
        raise
    return res_geom


def geo2sh_geom(geom):
    if isinstance(geom, GeoPoint):
        res_geom = ShPoint(geom.coordinates)
    elif isinstance(geom, GeoPolygon):
        res_geom = ShPolygon(geom.coordinates)
    else:
        raise
    return res_geom
