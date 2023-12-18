from app.geoutils import get_city_area_id
from app.osm_data import create_buildings_gdf
import geopandas as gpd
from app import settings


def parse_building_gdf(city_name='Russia, Saint Petersburg'):
    area_id = get_city_area_id(city_name)
    gdf_buildings = create_buildings_gdf(area_id)
    street_list = []
    house_number_list = []
    for tag in gdf_buildings.tags:
        street_list.append(tag.get('addr:street'))
        house_number_list.append(tag.get('addr:housenumber'))

    gdf_buildings['street'] = street_list
    gdf_buildings['house_num'] = house_number_list
    return gdf_buildings


if __name__ == '__main__':
    gdf_buildings = parse_building_gdf()
    geojson_filename = settings.files.building_gdf
    gdf_buildings.to_file(geojson_filename, encoding='utf-8')
    gdf = gpd.GeoDataFrame.from_file(settings.files.building_gdf)
