from typing import List, Dict, Union
import osmnx as ox
from turfpy import measurement
from geojson import LineString as GeoLineString, Feature
from geojson_length import calculate_distance, Unit
import time

from app import settings


class PthPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def coord(self):
        return self.x, self.y


class Pathfinder:
    _crs = 'urn:ogc:def:crs:OGC:1.3:CRS84'

    def __init__(self):
        self.G = ox.load_graphml(settings.files.drive_graph)

    @staticmethod
    def _point2node(point: Union[int, list, PthPoint]) -> int:
        """Возвращает хеш точки PthPoint"""
        if isinstance(point, int):
            return point
        elif isinstance(point, list):
            return PthPoint(long=point[0], lat=point[1]).id
        return point.id

    def _node2point(self, node: Union[int, list, PthPoint]) -> PthPoint:
        """Возвращает точку PthPoint по хешу"""
        if isinstance(node, int):
            node = self.G.nodes()[node]
            return PthPoint(long=node['x'], lat=node['y'])
        elif isinstance(node, list):
            return PthPoint(long=node[0], lat=node[1])
        elif isinstance(node, PthPoint):
            return node
        raise

    def _nearest_node(self, point: PthPoint) -> int or None:
        """Находит хеш ближайшей точки графа"""
        nearest_node = ox.distance.nearest_nodes(self.G, point.x, point.y)
        return nearest_node

    def _edge_length(
        self, point_0: Union[int, list, PthPoint], point_1: Union[int, list, PthPoint]
    ) -> float:
        """Расстояние между двумя точками графа (без учета весов)"""
        point_0 = self._node2point(point_0)
        point_1 = self._node2point(point_1)
        line_string = GeoLineString([point_0.coord, point_1.coord])
        length = calculate_distance(line_string, Unit.meters)
        return measurement.length(line_string)

    def find_route_length(self, coord_0, coord_1):
        start_time = time.time()

        point_0 = PthPoint(coord_0[0], coord_0[1])
        point_1 = PthPoint(coord_1[0], coord_1[1])

        start_node = self._nearest_node(point_0)
        finish_node = self._nearest_node(point_1)
        shortest_route_by_distance = ox.shortest_path(
            self.G, start_node, finish_node
        )

        points_list = []
        for i in shortest_route_by_distance:
            node = self.G.nodes[i]
            points_list.append(PthPoint(node['x'], node['y']))

        if len(points_list) == 1:
            points_list = []
            # points_list = [point_0, point_1]
        points_list.insert(0, point_0)
        points_list.append(point_1)

        geo_line_string = GeoLineString([point.coord for point in points_list])
        # length = measurement.length(geo_line_string, units='m')

        goe_line_string_2 = Feature(geometry=geo_line_string)
        length_2 = calculate_distance(goe_line_string_2, Unit.meters)
        # length_3 = sum(ox.utils_graph.get_route_edge_attributes(self.G, shortest_route_by_distance, 'length'))
        # print(length, length_2, length_3)

        end_time = time.time() - start_time
        print(f"Pathfinder time: {end_time}")

        return length_2, geo_line_string

    @staticmethod
    def find_length_btw_two_points(coord_0, coord_1):
        if coord_0[0] > 180 or coord_0[1] > 180 or coord_1[0] > 180 or coord_1[1] > 180:
            return ((coord_1[0] - coord_0[0]) ** 2 + (coord_1[1] - coord_0[1]) ** 2) ** 0.5
        geo_line_string = GeoLineString([coord_0, coord_1])
        goe_line_string_feature = Feature(geometry=geo_line_string)
        length_2 = calculate_distance(goe_line_string_feature, Unit.meters)
        return length_2

    @staticmethod
    def _speed_coef(unit: str):
        speed_coef = {
            'km': 1.852,
            'm': 1852,
            'mi': 1.15078,
            'ft': 6076.12,
            'in': 72913.4,
            'deg': 1.852,
            'cen': 185200,
            'rad': 1.852,
            'yd': 2025.37,
        }
        if unit not in speed_coef:
            return 1
        return speed_coef[unit]

# pathfinder = Pathfinder()


if __name__ == '__main__':
    _min_point = (30.05, 59.79)
    _max_point = (30.60, 60.10)

    pathfinder = Pathfinder()
    length, _ = pathfinder.find_route_length(_min_point, _max_point)
    print(length)
