from unittest import TestCase

import responses

from .context import app


class WentzoMeterTest(TestCase):
    def setUp(self):
        self.app = app.test_client()

    @responses.activate
    def test_snap_count(self):
        responses.add(responses.GET,
                      'https://api.lineups.com/nfl/'
                      'fetch/snaps/2021/QB?season_type=1',
                      json={'data': [{'full_name': 'Shrimply Pibbles'},
                                     {'full_name': 'Carson Wentz',
                                      'average': 76.0,
                                      'team': 'IND',
                                      'lineups_rating': 74,
                                      'profile_url':
                                      '/nfl/player-stats/carson-wentz',
                                      'season_snap_percent': 100.0,
                                      'total': 76.0,
                                      'weeks': [76],
                                      'fantasy_position_depth_order': 1,
                                      'id': 31456,
                                      'touchdowns': 0.0,
                                      'snap_percentage_by_week': [100],
                                      'team_depth_chart_route':
                                      '/nfl/depth-charts/indianapolis-colts',
                                      'position': 'QB'}]},
                      status=200)

        response = self.app.get('/snap_count')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(),
                         {'snap_percentage': 100.0})

    @responses.activate
    def test_snap_count_error(self):
        responses.add(responses.GET,
                      'https://api.lineups.com/nfl/'
                      'fetch/snaps/2021/QB?season_type=1',
                      status=500)

        response = self.app.get('/snap_count')

        self.assertEqual(response.status_code, 500)
