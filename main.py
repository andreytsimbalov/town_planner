from app import settings
from app.data_proc import save_data, load_data
from work_steps.buildings_parser import parse_building_gdf
import geopandas as gpd

from work_steps.cain_df_by_gdf import get_cain_df_by_gdf
from work_steps.cain_gdf_by_dict import get_cain_gdf_by_dict
from work_steps.cian_df_joiner import concat_cian_df_files
from work_steps.cian_parser import parce_cian_df_files
from work_steps.garbage_parser import parse_garbage_gdf
from work_steps.nature_parser import parse_nature_gdf
from work_steps.metro_parser import parce_metro
from work_steps.update_cian_by_buildings import update_cian_by_buildings
from work_steps.generate_cian_obj_dict import generate_cian_gdf_obj_dict
from work_steps.water_parser import parse_water_gdf


def get_buildings(city_name='Russia, Saint Petersburg'):
    gdf_buildings = parse_building_gdf(city_name)  # Парсинг зданий
    gdf_buildings.to_file(settings.files.building_gdf, encoding='utf-8')
    save_data(gdf_buildings, settings.files.building_gdf_pickle)
    gdf = load_data(settings.files.building_gdf_pickle)
    return gdf


def get_cian(city_name_ru='Санкт-Петербург'):
    parce_cian_df_files(city_name_ru)  # Парсинг данный с Циана по лимитам стоимостей квартир
    room = 'all'
    cian_df = concat_cian_df_files(room)  # Объединение файлов данных с Циана
    data_result_filename = f'result_cian_parsing_sale_room_{room}_sankt-peterburg_02_Nov_2023.csv'
    cian_df.to_csv(f'{settings.files.cian_parsing_df}/{data_result_filename}')
    return cian_df


def update_cain_by_buildings_geodata():
    cian_buildings_gdf = update_cian_by_buildings()
    cian_buildings_gdf.to_file(settings.files.cian_gdf, encoding='utf-8')
    save_data(cian_buildings_gdf, settings.files.cian_gdf_pickle)
    gdf_buildings = load_data(settings.files.cian_gdf_pickle)
    return gdf_buildings


def get_metro(city_name_ru="Санкт-Петербург"):
    gdf_metro = parce_metro(city_name_ru)
    save_data(gdf_metro, settings.files.metro_gdf_pickle)
    return gdf_metro


def get_water(city_name='Russia, Saint Petersburg'):
    gdf_water = parse_water_gdf(city_name)
    save_data(gdf_water, settings.files.water_gdf_pickle)
    gdf = load_data(settings.files.water_gdf_pickle)
    return gdf


def get_garbage(city_name='Russia, Saint Petersburg'):
    gdf_garbage = parse_garbage_gdf(city_name)
    save_data(gdf_garbage, settings.files.garbage_gdf_pickle)
    gdf = load_data(settings.files.garbage_gdf_pickle)
    return gdf


def get_nature(city_name='Russia, Saint Petersburg'):
    gdf_nature = parse_nature_gdf(city_name)
    save_data(gdf_nature, settings.files.nature_gdf_pickle)
    gdf = load_data(settings.files.nature_gdf_pickle)
    return gdf


def create_grid():
    return None


def update_cian_by_objects():
    cian_dict = generate_cian_gdf_obj_dict()
    save_data(cian_dict, settings.files.cian_by_objs_pickle)
    cian_dict = load_data(settings.files.cian_by_objs_pickle)
    return cian_dict


def generate_cain_gdf_by_dict():
    gdf = get_cain_gdf_by_dict()
    save_data(gdf, settings.files.cian_gdf_by_dict_pickle)
    gdf = load_data(settings.files.cian_gdf_by_dict_pickle)
    return gdf


def generate_cain_df_by_gdf():
    df = get_cain_df_by_gdf()
    save_data(df, settings.files.cian_df_by_gdf_pickle)
    df = load_data(settings.files.cian_df_by_gdf_pickle)
    return df


def main():
    city_name_en = 'Russia, Saint Petersburg'
    city_name_ru = 'Санкт-Петербург'
    steps = [
        # (get_buildings, [], {'city_name': city_name_en}),
        # (get_cian, [], {'city_name_ru': city_name_ru}),
        # (update_cain_by_buildings_geodata, [], {}),
        # (get_metro, [], {'city_name_ru': city_name_ru}),
        # (get_water, [], {'city_name': city_name_en}),
        # (get_garbage, [], {'city_name': city_name_en}),
        # (get_nature, [], {'city_name': city_name_en}),
        # (create_grid, [], {}),
        # (update_cian_by_objects, [], {}),
        (generate_cain_gdf_by_dict, [], {}),
        # (generate_cain_df_by_gdf, [], {}),
    ]
    for step_func, args, kwargs in steps:
        print()
        print(f"RUN step: '{step_func.__name__}'")
        result = step_func(*args, **kwargs)
        a = 2
        print()


if __name__ == '__main__':
    main()
