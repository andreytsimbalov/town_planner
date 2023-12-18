import json

from shapely import Point, STRtree, Polygon, intersection, MultiPolygon
from shapely.geometry import shape

from app.constants import PROJ
from app.data_proc import save_data, load_data
from app.geoutils import get_city_area_id
from app.osm_data import create_objects_gdf
import geopandas as gpd
import pandas as pd
from app import settings
from app.utils import get_geom_box
from app.visualizer import show


def parse_water_gdf(city_name='Russia, Saint Petersburg'):
    area_id = get_city_area_id(city_name)
    tags = ['natural']
    keys = ['water']
    gdf_water = create_objects_gdf(area_id, tags, keys, geom_type=None)
    # save_data(gdf_water, settings.Files.water_gdf_pickle)
    # gdf_water = load_data(settings.Files.water_gdf_pickle)
    water_geom = gdf_water.geometry
    water_limit_polygon = get_geom_box(water_geom)

    earth_sea_multipolygon = shape(json.load(open(settings.files.earth_sea_polygon_map_path))['geometries'][0])
    sea_polygon = intersection(earth_sea_multipolygon, water_limit_polygon)
    gdf_sea = gpd.GeoDataFrame(crs=PROJ.WGS_EPSG_STR, geometry=[sea_polygon])
    gdf_sea['n'] = [len(gdf_water)]
    gdf_sea['obj_id'] = [-1]
    gdf_sea['name'] = ['Море']
    gdf_sea['tag'] = ['natural']
    gdf_sea['key'] = ['water']
    gdf_water = pd.concat([gdf_water, gdf_sea])

    # show(gdf_water)
    # show(gdf_water, center_point=Point((3362500, 8383000)), center_buffer=10000)
    return gdf_water


if __name__ == '__main__':
    gdf = parse_water_gdf()
    show(gdf)
    save_data(gdf, settings.files.water_gdf_pickle)
    gdf = load_data(settings.files.water_gdf_pickle)
