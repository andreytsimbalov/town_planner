import pandas as pd

from app.data_proc import save_data, load_data
from app.geoutils import get_city_area_id
from app.osm_data import create_objects_gdf
import geopandas as gpd
from app import settings
from app.visualizer import show


def parse_nature_gdf(city_name='Russia, Saint Petersburg'):
    area_id = get_city_area_id(city_name)
    tag_key_list = [
        (['boundary'], ['national_park']),
        (['leisure'], ['park']),
        (['landuse'], ['cemetery']),
        (['landuse'], ['greenery']),
    ]
    gdf_nature = None
    for tags, keys in tag_key_list:
        gdf_nature_item = create_objects_gdf(area_id, tags, keys, geom_type=None)
        if gdf_nature_item is None:
            continue
        if gdf_nature is None:
            gdf_nature = gdf_nature_item
        else:
            gdf_nature = pd.concat([gdf_nature, gdf_nature_item])
    return gdf_nature


if __name__ == '__main__':
    gdf = parse_nature_gdf()
    show(gdf)
    save_data(gdf, settings.files.nature_gdf_pickle)
    gdf = load_data(settings.files.nature_gdf_pickle)
