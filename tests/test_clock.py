from unittest import TestCase
from unittest.mock import patch

import responses

from .context import generate_chart
from .context import construct_tweet
from .context import check_snap_count


class ClockTestCase(TestCase):
    def test_generate_chart(self):
        result = generate_chart(100)

        self.assertEqual(result, "▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 100%")

        result = generate_chart(70)

        self.assertEqual(result, "▓▓▓▓▓▓▓▓▓▓░░░░░ 70%")

        result = generate_chart(22)
        self.assertEqual(result, "▓▓▓░░░░░░░░░░░░ 22%")

        result = generate_chart(21.7)
        self.assertEqual(result, "▓▓▓░░░░░░░░░░░░ 21.7%")

    def test_construct_tweet(self):
        result = construct_tweet(91)

        self.assertEqual(result,
                         "Wentz is solidy above the snaps needed for Philly to get "
                         "a first round pick.\n\n▓▓▓▓▓▓▓▓▓▓▓▓▓▓░ 91%")

    @responses.activate
    @patch('tweepy.API.update_status')
    def test_check_snap_count(self, mock_tweet):
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
                                      'season_snap_percent': 91.6,
                                      'total': 76.0,
                                      'weeks': [76, 77, 78],
                                      'fantasy_position_depth_order': 1,
                                      'id': 31456,
                                      'touchdowns': 0.0,
                                      'snap_percentage_by_week': [100],
                                      'team_depth_chart_route':
                                      '/nfl/depth-charts/indianapolis-colts',
                                      'position': 'QB'}]},
                      status=200)

        expected = "Wentz is solidy above the snaps needed for Philly to get" \
                   " a first round pick.\n\n▓▓▓▓▓▓▓▓▓▓▓▓▓▓░ 91.6%"

        mock_tweet.text.return_value = expected

        check_snap_count()

        mock_tweet.assert_called_once_with(expected)

    @responses.activate
    @patch('tweepy.API.update_status')
    def test_check_snap_count_increase_weeks_but_same_snap_perc(self, mock_tweet):
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
                                      'weeks': [76, 77, 78],
                                      'fantasy_position_depth_order': 1,
                                      'id': 31456,
                                      'touchdowns': 0.0,
                                      'snap_percentage_by_week': [100],
                                      'team_depth_chart_route':
                                      '/nfl/depth-charts/indianapolis-colts',
                                      'position': 'QB'}]},
                      status=200)

        check_snap_count()

        mock_tweet.assert_not_called()

    @responses.activate
    @patch('tweepy.API.update_status')
    def test_check_snap_count_weeks_not_increased(self, mock_tweet):
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
                                      'weeks': [76, 77],
                                      'fantasy_position_depth_order': 1,
                                      'id': 31456,
                                      'touchdowns': 0.0,
                                      'snap_percentage_by_week': [100],
                                      'team_depth_chart_route':
                                      '/nfl/depth-charts/indianapolis-colts',
                                      'position': 'QB'}]},
                      status=200)

        check_snap_count()

        mock_tweet.assert_not_called()
