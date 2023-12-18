import json
from datetime import datetime


class Files:
    abs_path = "C:/Users/user/Desktop/Projects/PyCharmProjects/town_planner"
    data = f"{abs_path}/data"
    osm = f"{data}/osm"
    apartments_gdf = f"{data}/apartments"

    drive_graph = f"{data}/drive_graph"
    pathfinder_pickle = f"{data}/pathfinder_pickle"

    building_gdf = f"{data}/building"
    building_gdf_pickle = f"{data}/buildings_gdf_pickle"

    cian_parsing_df = f"{data}/cian_parsing_df"
    cian_gdf = f"{data}/cian"
    cian_df_pickle = f"{data}/cian_df_pickle"
    cian_gdf_pickle = f"{data}/cian_gdf_pickle"
    cian_by_objs_pickle = f"{data}/cian_by_objs_pickle"
    cian_by_objs_dict_pickle = f"{data}/cian_by_objs_dict_pickle"
    cian_gdf_by_dict_pickle = f"{data}/cian_gdf_by_dict_pickle"
    cian_df_by_gdf_pickle = f"{data}/cian_df_by_gdf_pickle"

    metro_gdf_pickle = f"{data}/metro_gdf_pickle"

    water_gdf_pickle = f"{data}/water_gdf_pickle"
    garbage_gdf_pickle = f"{data}/garbage_gdf_pickle"
    nature_gdf_pickle = f"{data}/nature_gdf_pickle"

    earth_sea_polygon_map_path = f"{data}/earth-seas-5m.geo.json"

    highway = f"{data}/highway"

    @classmethod
    def cian_df_filename(cls, room=None, short_min_price=None, short_max_price=None):
        if not all((room, short_min_price, short_max_price)):
            data_filename = "result_cian_parsing_sale_room_all_sankt-peterburg_02_Nov_2023.csv"
        else:
            data_filename = (
                f"cian_parsing_result_sale_room_{room}_"
                f"price_{short_min_price}-{short_max_price}_"
                f"sankt-peterburg_02_Nov_2023.csv"
            )
        return f"{cls.cian_parsing_df}/{data_filename}"


class Config:
    _config_filename = 'config.json'

    def __init__(self):
        self._config = json.load(open(f"{Files.abs_path}/{self._config_filename}"))
        self.dadata_token = self._config['dadata_token']


files = Files()
config = Config()
