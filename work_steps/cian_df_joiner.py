import pandas as pd
import numpy as np

from app import settings


def concat_cian_df_files(room_name='all'):
    # rooms = ('all', )
    price_const = 1000000
    step = 0.2
    result_df = None
    print(f"room: {room_name}")
    for i in np.arange(1.0, 250, step):
        min_price = int(i * price_const)
        max_price = int((i + step) * price_const)

        data_filename = settings.files.cian_df_filename(
            room_name, round(min_price / price_const, 1), round(max_price / price_const, 1)
        )
        try:
            df = pd.read_csv(data_filename)
            if result_df is not None:
                print(len(df), len(result_df), df.iloc[0].price)
                result_df = pd.concat([result_df, df])
            else:
                result_df = df
        except:
            pass
    return result_df


if __name__ == '__main__':
    room = 'all'
    cian_df = concat_cian_df_files(room)
    data_result_filename = f'result_cian_parsing_sale_room_{room}_sankt-peterburg_02_Nov_2023.csv'
    cian_df.to_csv(f'{settings.files.cian_parsing_df}/{data_result_filename}')
