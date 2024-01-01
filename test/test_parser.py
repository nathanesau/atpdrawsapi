import os

from src import draw_parser
import datetime

def test_parse_draw_brisbane_2024():
    draw_filename = os.path.join(os.path.dirname(__file__), "resources/brisbane_draw.html")
    with open(draw_filename) as f:
        data = f.read()
    draw = draw_parser.parse_draw(data)

    # current this just contains a list of round1 matchups
    assert("Brisbane" in draw.tournament.name)
    assert(datetime.date(2023, 12, 31) == draw.tournament.start_date)
    assert(datetime.date(2024, 1, 7) == draw.tournament.end_date)
    assert(draw.tournament.category == "250")
    assert(draw.tournament.location == "Australia")
    assert(len(draw.rounds) == 5)
    assert(len(draw.players) >= 16) # R32 tournament has at least 16 players

def test_parse_draw_hong_kong_2024():
    draw_filename = os.path.join(os.path.dirname(__file__), "resources/hong_kong_draw.html")
    with open(draw_filename) as f:
        data = f.read()
    draw = draw_parser.parse_draw(data)
