from app.pathfinder import Pathfinder

_min_point = (30.05, 59.79)
_max_point = (30.60, 60.10)

pathfinder = Pathfinder()
length = pathfinder.find_route_length(_min_point, _max_point)

a = 2
