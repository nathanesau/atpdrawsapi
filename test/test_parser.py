import unittest
import os
from atpdraws import parser

class TestParser(unittest.TestCase):
    def test_parse_draw(self):
        draw_filename = os.path.join(os.path.dirname(__file__), "resources/sample_draw.html")
        with open(draw_filename) as f:
            data = f.read()
        draw = parser.parse_draw(data)

        # current this just contains a list of round1 matchups
        self.assertEqual(len(draw), 16)