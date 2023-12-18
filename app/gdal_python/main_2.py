from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import Overpass

from app.gdal_python.geotools import burn
from app.osm_data import create_objects_gdf
from app.gdal_python.raster import Raster
from osgeo import ogr, gdal
import numpy as np


nominatim = Nominatim()
overpass = Overpass()

raster = Raster(4000)

city = 'Russia, Saint Petersburg'
areaId = nominatim.query(city).areaId()

geojson_filename = '../../data/building_hotel/building_hotel.shp'

tags = ['building']
keys = ['hotel']
gdf_hotel = create_objects_gdf(areaId, tags, keys)
gdf_hotel.to_file(geojson_filename)



# for geometry in gdf_hotel.geometry:
#     coords = list(zip(geometry.exterior.coords.xy[0], geometry.exterior.coords.xy[1]))
#     raster.add_polygon(coords)
# raster.save()

# filename = 'map.png'
# gdal_raster = gdal.Open(filename, gdal.GA_ReadOnly)
# asd = get_geodata_from_raster(gdal_raster)


# org_hotel_vector = ogr.Open(geojson_filename)

a = 2

# _min_point = (30.05, 59.79)
# _max_point = (30.60, 60.10)


driver = ogr.GetDriverByName('ESRI Shapefile')
org_hotel_vector = driver.Open(geojson_filename)

# org_hotel_vector = gdal.OpenEx(geojson_filename, gdal.OF_VECTOR)
org_hotel_vector = gdal.OpenEx(geojson_filename)

org_hotel_raster = burn(
    org_hotel_vector,
    burn_value=1,
    x_res=4000,
    y_res=4000,
    spatial_ref_wkt="",
    # spatial_ref_wkt="EPSG:4326",
    # geo_transform=[30.05, 0.6, 0, 60.10, 0, 0.5],
    geo_transform=[30.18, 0.3, 0, 60.02, 0, 0.2],
)
org_hotel_array = org_hotel_raster.ReadAsArray()
min_org_hotel_array = org_hotel_array.min()
max_org_hotel_array = org_hotel_array.max()
unique_org_hotel_array = np.unique(org_hotel_array)

a = 2
