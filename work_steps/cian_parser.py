import cianparser
import pandas as pd
import numpy as np
import geopandas as gpd

from app import settings


def parce_cian_df_files(city_name_ru='Санкт-Петербург'):
    # ("rent_long", "rent_short", "sale")
    rooms = ("studio", 1, 2, 3, 4, 5, 6)
    rooms = ('all', )
    price_const = 1000000
    step = 0.2
    for room in rooms:
        print(f"room: {room}")
        for i in np.arange(75.2, 250, step):
            min_price = int(i * price_const)
            max_price = int((i + step) * price_const)
            print(f'i: {i}, {round(min_price / price_const, 2)}-{round(max_price / price_const, 2)}')
            data = cianparser.parse(
                deal_type="sale",
                accommodation_type="flat",
                location=city_name_ru,
                rooms=room,
                start_page=1,
                end_page=54,
                is_latin=False,
                additional_settings={
                    "min_price": min_price + 1,
                    "max_price": max_price,
                }
            )
            if data:
                df = pd.DataFrame(data)
                data_filename = settings.files.cian_df_filename(
                    room, round(min_price / price_const, 1), round(max_price / price_const, 1)
                )
                df.to_csv(data_filename)
    # data = pd.read_csv(data_filename)


if __name__ == '__main__':
    parce_cian_df_files()
