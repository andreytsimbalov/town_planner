import osmnx as ox
import geopandas as gpd

from app import settings

# Get place boundary related to the place name as a geodataframe

place_name = 'Russia, Saint Petersburg'
area = ox.geocode_to_gdf(place_name)
# area.plot()

tags = {'building': True}

buildings = ox.geometries_from_place(place_name, tags)
asd = buildings.head()

column_list = list(asd.columns)
column_list_upper_limit = []
for column_source in column_list:
    column = column_source.replace('addr:', '')
    if len(column) > 10:
        column_list_upper_limit.append((column, column_source))

# buildings.plot()

geojson_filename = settings.files.building_gdf
buildings.to_file(f'{geojson_filename}_2', encoding='utf-8')
gdf = gpd.GeoDataFrame.from_file(f'{geojson_filename}_2')
