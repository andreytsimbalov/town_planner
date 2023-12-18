from staticmap import StaticMap, Line, Polygon, CircleMarker


class Color:
    red = '#cc3300'
    blue = '#003399'
    yellow = '#ffff66'
    green = '#33cc33'
    green_dark = '#006600'
    black = '#000000'


class Raster:
    _min_point = (30.05, 59.79)
    _max_point = (30.60, 60.10)

    def __init__(self, image_side=400, ):
        self.m = StaticMap(image_side, image_side)

        self.m.add_marker(CircleMarker(self._min_point, Color.black, 1))
        self.m.add_marker(CircleMarker(self._max_point, Color.black, 1))

    def add_line(self, coords):
        line = Line(coords, Color.red, 3)
        self.m.add_line(line)

    def add_polygon(self, coords):
        # polygon = Polygon(coords, Color.green, Color.green_dark)
        polygon = Polygon(coords, Color.black, Color.black)
        self.m.add_polygon(polygon)

    def save(self):
        image = self.m.render()
        image.save('map.png')


if __name__ == '__main__':
    # Example draw Line
    coord_s = (
        (
            30.22,
            59.87
        ),
        (
            30.34,
            59.96,
        )
    )
    raster = Raster(400)
    raster.add_line(coord_s)
    raster.save()
