import pandas as pd

from app.data_proc import save_data, load_data
from app.geoutils import get_city_area_id
from app.osm_data import create_objects_gdf
import geopandas as gpd
from app import settings
from app.visualizer import show


def parse_garbage_gdf(city_name='Russia, Saint Petersburg'):
    area_id = get_city_area_id(city_name)
    tag_key_list = [
        (['amenity'], ['waste_transfer_station', 'crematorium']),
        (['landuse'], ['landfill']),
        (['man_made'], ['spoil_heap', 'wastewater_plant', 'chimney']),
        (['building'], ['cowshed', 'sty', 'slurry_tank']),
    ]
    gdf_garbage = None
    for tags, keys in tag_key_list:
        gdf_garbage_item = create_objects_gdf(area_id, tags, keys, geom_type=None)
        if gdf_garbage_item is None:
            continue
        if gdf_garbage is None:
            gdf_garbage = gdf_garbage_item
        else:
            gdf_garbage = pd.concat([gdf_garbage, gdf_garbage_item])
    return gdf_garbage


if __name__ == '__main__':
    gdf = parse_garbage_gdf()
    show(gdf)
    save_data(gdf, settings.files.garbage_gdf_pickle)
    gdf = load_data(settings.files.garbage_gdf_pickle)
