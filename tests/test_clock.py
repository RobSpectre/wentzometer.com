from unittest import TestCase

from .context import generate_chart
from .context import construct_tweet


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
                         "a first round pick.\n▓▓▓▓▓▓▓▓▓▓▓▓▓▓░ 91%")
