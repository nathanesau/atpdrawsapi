import os
from src import parser

def test_parse_draw():
    draw_filename = os.path.join(os.path.dirname(__file__), "resources/sample_draw.html")
    with open(draw_filename) as f:
        data = f.read()
    draw = parser.parse_draw(data)

    # current this just contains a list of round1 matchups
    assert(len(draw) == 16)