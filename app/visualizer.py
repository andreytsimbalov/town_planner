from typing import List

import contextily as cx
import matplotlib.pyplot as plt
import geopandas as gpd
from geopandas import GeoDataFrame

from app import utils
from app.constants import PROJ
from app.utils import geom_wgs2epsg


class ShowColors:
    red = '#cc3300'
    blue = '#003399'
    yellow = '#ffff66'
    green = '#33cc33'
    green_dark = '#006600'
    black = '#000000'


class ShowGdfItem:
    def __init__(self, gdf, buffer=2000, color=ShowColors.red):
        self.gdf = gdf
        self.buffer = buffer
        self.color = color


def show_one_geometry_gdf(geometry_gdf, center_point=None, center_buffer=2000, color=ShowColors.red, ax=None):
    edge_color = 'black'
    point_color = 'blue'

    figure_size_x = 12
    figure_size_y = 9

    buffer_const = 10

    center_point_gdf = None
    if center_point is not None:
        center_point = utils.geom_wgs2epsg(center_point)
        geometry_gdf = utils.get_gdf_by_center_buffer(geometry_gdf, center_point,  center_buffer)
        center_point_gdf = GeoDataFrame(crs=PROJ.EPSG_STR, geometry=[center_point])

    geometry_gdf = geometry_gdf.to_crs(epsg=PROJ.EPSG)
    poly_buffer = geometry_gdf.geometry.buffer(buffer_const)
    poly_buffer_gdf = GeoDataFrame(crs=PROJ.EPSG_STR, geometry=poly_buffer)

    ax = poly_buffer_gdf.plot(color=color, edgecolor=edge_color, alpha=0.0, linewidth=2, figsize=(figure_size_x, figure_size_y))
    ax = geometry_gdf.plot(ax=ax, color=color, edgecolor=edge_color, alpha=0.5)
    if center_point_gdf is not None:
        ax = center_point_gdf.plot(ax=ax, color=point_color, edgecolor=edge_color, alpha=1.0)
    return ax


def show_list_geometry_gdf(center_gdf_item: ShowGdfItem, geometry_gdf_list: List[ShowGdfItem]):
    # ax = show_one_geometry_gdf(
    #     center_gdf_item.gdf,
    #     color=center_gdf_item.color
    # )
    # for geometry_gdf_item in geometry_gdf_list:
    #     if len(geometry_gdf_item.gdf) == 0:
    #         continue
    #     ax = show_one_geometry_gdf(
    #         geometry_gdf_item.gdf, center_point=center_gdf_item.gdf.geometry[0],
    #         color=geometry_gdf_item.color, ax=ax
    #     )

    edge_color = 'black'
    figure_size_x = 12
    figure_size_y = 9
    buffer_const = 10

    center_gdf = center_gdf_item.gdf
    center_point = center_gdf.geometry[0]

    poly_buffer = center_gdf.geometry.buffer(buffer_const)
    poly_buffer_gdf = GeoDataFrame(crs=PROJ.EPSG_STR, geometry=poly_buffer)

    ax = poly_buffer_gdf.plot(color=ShowColors.black, edgecolor=edge_color, alpha=0.0, linewidth=2, figsize=(figure_size_x, figure_size_y))
    ax = center_gdf.plot(ax=ax, color=center_gdf_item.color, edgecolor=edge_color, alpha=0.5)

    for geometry_gdf_item in geometry_gdf_list:
        geometry_gdf = geometry_gdf_item.gdf
        if len(geometry_gdf) == 0:
            continue

        center_point = utils.geom_wgs2epsg(center_point)
        geometry_gdf = utils.get_gdf_by_center_buffer(
            geometry_gdf, center_point, geometry_gdf_item.buffer, circle=True,
            crop_circle_geom=True
        )
        # center_point_gdf = GeoDataFrame(crs=PROJ.EPSG_STR, geometry=[center_point])

        center_point = geom_wgs2epsg(center_point)
        center_polygon = center_point.buffer(geometry_gdf_item.buffer)
        center_polygon_gdf = gpd.GeoDataFrame(crs=PROJ.EPSG_STR, geometry=[center_polygon])

        ax = geometry_gdf.plot(ax=ax, color=geometry_gdf_item.color, edgecolor=edge_color, alpha=0.5)
        ax = center_polygon_gdf.plot(ax=ax, color=geometry_gdf_item.color, edgecolor=edge_color, alpha=0.1)
    cx.add_basemap(ax, crs=center_gdf.crs.to_string(), source=cx.providers.CartoDB.Voyager)
    plt.show()


def show(geometry_gdf, center_point=None, center_buffer=2000, color=ShowColors.red, ax=None):
    ax = show_one_geometry_gdf(geometry_gdf, center_point, center_buffer, color)
    cx.add_basemap(ax, crs=geometry_gdf.crs.to_string(), source=cx.providers.CartoDB.Voyager)
    plt.show()


if __name__ == '__main__':
    from shapely.geometry import Point
    # WGS_EPSG = 32636
    WGS_EPSG = 4326  #
    # epsg = 3857

    point = Point((30.276424072543968, 59.94587683528832))
    # point = Point((30.294778398601856, 59.944843895537566))

    point_gdf = GeoDataFrame(crs=f"EPSG:{PROJ.WGS_EPSG}", geometry=[point])
    show(point_gdf)
