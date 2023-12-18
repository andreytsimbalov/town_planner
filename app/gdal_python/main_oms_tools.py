from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
from collections import OrderedDict
from OSMPythonTools.data import Data, dictRangeYears

# overpass = Overpass()
# result = overpass.query('way["name"="Stephansdom"]; out body;')
# stephansdom = result.elements()[0]
# stephansdom.tag('name:en')
# stephansdom.tag('building')
# stephansdom.tag('denomination')


city = 'Russia, Saint Petersburg'

dimensions = OrderedDict([
  ('year', dictRangeYears(2013, 2017.5, 3)),
  ('city', OrderedDict({
    'heidelberg': 'Heidelberg, Germany',
    # 'manhattan': 'Manhattan, New York',
    # 'vienna': 'Vienna, Austria',
  })),
  ('typeOfRoad', OrderedDict({
    'primary': 'primary',
    # 'secondary': 'secondary',
    # 'tertiary': 'tertiary',
  })),
])

nominatim = Nominatim()
overpass = Overpass()

def fetch(year, city, typeOfRoad):
    areaId = nominatim.query(city).areaId()
    query = overpassQueryBuilder(area=areaId, elementType='way', selector='"highway"="' + typeOfRoad + '"', out='count')
    return overpass.query(query, date=year, timeout=60).countElements()

data = Data(fetch, dimensions)

nominatim = Nominatim()
areaId = nominatim.query(city).areaId()
overpass = Overpass()
query = overpassQueryBuilder(area=areaId, elementType='node', selector='"natural"="tree"', out='count')
query = overpassQueryBuilder(area=areaId, elementType='node')
result = overpass.query(query)
result.countElements()
# 137830
result1 = overpass.query(query, date='2013-01-01T00:00:00Z', timeout=60)
result1.countElements()
# 127689


a = 2 + 2
