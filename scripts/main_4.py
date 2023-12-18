import geopandas as gpd

geojson_filename = '../data/building_hotel/building_hotel.shp'

# nominatim = Nominatim()
# overpass = Overpass()
# city = 'Russia, Saint Petersburg'
# areaId = nominatim.query(city).areaId()
# tags = ['building']
# keys = ['hotel']
# gdf_hotel = create_objects_gdf(areaId, tags, keys)
# gdf_hotel.to_file(geojson_filename, encoding='utf-8')


gpd_hotel_2 = gpd.GeoDataFrame.from_file(geojson_filename)
gpd_hotel_3 = gpd_hotel_2.to_crs(epsg=32636)

# edge = ShapelyLineString([point_0.coord, point_1.coord])
# for polygon in self.earth_polygon_tree.query_geoms(edge):
#     if polygon.intersects(edge):
#         return False

a = 2
