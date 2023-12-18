from app.gdal_python.geotools import burn
from osgeo import ogr, gdal


# filename = 'map.png'
# gdal_raster = gdal.Open(filename, gdal.GA_ReadOnly)
# asd = get_geodata_from_raster(gdal_raster)

geojson_filename = '../../data/building_hotel/building_hotel.shp'
# org_hotel_vector = ogr.Open(geojson_filename)
org_hotel_vector = gdal.OpenEx(geojson_filename, gdal.OF_VECTOR)

# from osgeo import gdal
# # Define NoData value of new raster
# NoData_value = -9999
# # Filename of input OGR file
# vector_fn = 'Boroughs.shp'
# # Filename of the raster Tiff that will be created
# raster_fn = 'Boroughs.tif'
# # Open the data source and read in the extent
# source_ds = gdal.OpenEx(vector_fn)
# pixel_size = 0.00025  # about 25 metres(ish) use 0.001 if you want roughly 100m
# gdal.Rasterize(raster_fn, source_ds, format='GTIFF', outputType=gdal.GDT_Byte, creationOptions=["COMPRESS=DEFLATE"], noData=NoData_value, initValues=NoData_value, xRes=pixel_size, yRes=-pixel_size, allTouched=True, burnValues=1)


geojson_filename = '../../data/building_hotel/building_hotel.shp'
geojson_filename_2 = '../../map.tif'

ras_ds = gdal.OpenEx(geojson_filename_2)
vec_ds = ogr.Open(geojson_filename)
vec_ds_2 = gdal.OpenEx(geojson_filename)
lyr = vec_ds.GetLayer()

geot = ras_ds.GetGeoTransform()

drv_tiff = gdal.GetDriverByName("GTiff")
chn_ras_ds = drv_tiff.Create('map_2.tif', ras_ds.RasterXSize, ras_ds .RasterYSize, 1, gdal.GDT_Float32)
chn_ras_ds.SetGeoTransform(geot)

gdal.RasterizeLayer(chn_ras_ds, [1], lyr)
chn_ras_ds.GetRasterBand(1).SetNoDataValue(0.0)

chn_ras_ds.ReadAsArray().min(), chn_ras_ds.ReadAsArray().max()

chn_ras_ds = None

a = 2

org_hotel_raster = burn(
    org_hotel_vector,
    burn_value=1,
    x_res=4000,
    y_res=4000,
    spatial_ref_wkt="",
    # spatial_ref_wkt="EPSG:4326",
    geo_transform=[0, 1, 0, 0, 0, 1],
)
org_hotel_array = org_hotel_raster.ReadAsArray()

a = 2
