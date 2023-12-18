from osgeo import gdal

from app.gdal_python.geotools import get_geodata_from_raster

filename = '../../data/buildings/buildings.shp'
filename = '../../data/buildings/buildings.dbf'
filename = '../../map.png'
raster = gdal.Open(filename, gdal.GA_ReadOnly)
asd = get_geodata_from_raster(raster)

a = 2
