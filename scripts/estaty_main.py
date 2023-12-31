from estaty.analysis.action import Analyzer
from estaty.data_source.action import DataSource
from estaty.main import EstateModel
from estaty.preprocessing.action import Preprocessor

import warnings
warnings.filterwarnings('ignore')


def launch_proximity_analysis_for_bars_objects():
    point_for_analysis = {'lat': 59.944843895537566, 'lon': 30.294778398601856}
    # point_for_analysis = {'lat': 59.94587683528832, 'lon': 30.276424072543968}
    osm_source = DataSource('osm', params={'category': 'bar'})

    osm_reprojected = Preprocessor('reproject', params={'to': 'auto'}, from_actions=[osm_source])

    analysis = Analyzer(
        'distance', params={'network_type': 'walk', 'visualize': True, 'color': 'orange', 'edgecolor': 'black', 'title': 'Bars'},
        from_actions=[osm_reprojected]
    )

    model = EstateModel().for_property(point_for_analysis, radius=2000)
    founded_routes = model.compose(analysis)

    print(founded_routes.lines)
    print(f'Min length: {founded_routes.lines["Length"].min():.2f}, m')
    print(f'Mean length: {founded_routes.lines["Length"].mean():.2f}, m')
    print(f'Max length: {founded_routes.lines["Length"].max():.2f}, m')
    a = 2


if __name__ == '__main__':
    launch_proximity_analysis_for_bars_objects()
