import math
import random
import time

import pandas as pd
import geopandas as gpd
import numpy as np
import re
from shapely import STRtree, Point, MultiLineString, Polygon, intersection

from app import settings, utils
from app.constants import PROJ, METER
from app.data_proc import load_data, save_data
from app.pathfinder import Pathfinder
from app.visualizer import show


def get_cain_df_by_gdf():
    gdf_cian = utils.gdf_to_epsg(load_data(settings.files.cian_gdf_by_dict_pickle))
    df_cian = pd.DataFrame(gdf_cian)
    df_cian = df_cian.drop('geometry', axis=1)
    return df_cian


if __name__ == '__main__':
    df = get_cain_df_by_gdf()
    save_data(df, settings.files.cian_df_by_gdf_pickle)
    df = load_data(settings.files.cian_df_by_gdf_pickle)
