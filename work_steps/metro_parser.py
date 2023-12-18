from dadata import Dadata
import geopandas as gpd
from geojson import Point

from app import settings
from app.data_proc import save_data, load_data


def parce_metro(city_name_ru="Санкт-Петербург"):
    token = settings.config.dadata_token
    dadata = Dadata(token)

    counter_i = 0
    metro_feature_list = []
    for i in range(1, 6):
        metro_list = dadata.suggest("metro", city_name_ru, count=20, filters=[{"line_id": i}])
        for metro in metro_list:
            if metro['data']['is_closed']:
                continue
            point = Point((metro['data']['geo_lon'], metro['data']['geo_lat']))
            metro_feature = {
                "type": "Feature",
                "properties": {
                    "n": counter_i,
                    "name": metro['value'],
                    "line_name": metro['data']['line_name'],
                    "line_id": metro['data']['line_id'],
                    "center_x": metro['data']['geo_lon'],
                    "center_y": metro['data']['geo_lat'],
                    "tags": metro['data'],
                },
                "geometry": point,
            }
            metro_feature_list.append(metro_feature)
            counter_i += 1

    gdf_metro = gpd.GeoDataFrame.from_features(metro_feature_list)
    return gdf_metro


if __name__ == '__main__':
    gdf = parce_metro()
    save_data(gdf, settings.files.metro_gdf_pickle)
    gdf = load_data(settings.files.metro_gdf_pickle)
