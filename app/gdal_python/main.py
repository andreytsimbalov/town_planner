import osmnx as ox

from app.constants import Ext
from app.settings import files

place_name = "Edgewood Washington, DC, USA"


# area = ox.geocode_to_gdf(place_name)
# area.plot()

tags = {'building': True}
buildings = ox.geometries_from_place(place_name, tags)
# buildings.plot()
buildings = buildings.loc[:, buildings.columns.str.contains('addr:|geometry')]
buildings = buildings.loc[buildings.geometry.type == 'Polygon']
buildings.to_file('data/buildings')
# buildings.to_file(Files.filename('buildings', Ext.shp))

a = 2 + 2
