# hack since pytest doesn't like absolute imports
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__)))

import datetime
from typing import List
from custom_types import Player, Matchup, Round, Tournament, Draw

def _month_to_int(month):
    month_map = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12
    }
    return month_map[month]

def _get_tournament_type(badge):
    img_path = badge.find("img").get_attribute_list("src")[0]
    if "categorystamps_250" in img_path:
        return "250"
    else:
        return "Unknown"
    
def _parse_tournament(soup) -> Tournament:
    name = soup.find("h3", class_="title").find("a").text
    location, date = [e.text for e in soup.find("div", class_="date-location").find_all("span")]
    year = date.split(',')[1].strip() # ex. 2024
    start_date = date.split(',')[0].split('-')[0].strip() # ex. 31 Dec
    end_date = date.split(',')[0].split('-')[1].strip() # ex. 7 Jan
    end_day, end_month = end_date.split(' ')
    try:
        start_day, start_month = start_date.split(' ') # for case when months are different
    except:
        start_day, start_month = start_date, end_month
    start_year = year if start_month == end_month else str(int(year) - 1)
    end_year = year
    badge = soup.find("div", class_="badge")
    
    return Tournament(name=name,
                      location=location,
                      category=_get_tournament_type(badge),
                      start_date=datetime.date(year=int(start_year), month=_month_to_int(start_month), day=int(start_day)),
                      end_date=datetime.date(year=int(end_year), month=_month_to_int(end_month), day=int(end_day)))

def _parse_players(soup) -> List[Player]:
    # parse players using first round
    round1 = soup.find("div", class_="draw-round-1")
    entrants = round1.find_all("div", class_="stats-item")
    players = []
    for i, entrant in enumerate(entrants):
        order = i + 1
        try:
            name = entrant.find("div", class_="name")
            id = name.find("a").get_attribute_list("href")[0].split("/")[-2]
            abbrev_name = name.find("a").text
            players.append(Player(id=id, name=abbrev_name, order=order))
        except: # qualifier, etc.
            pass
    return players

def _find_player(stats_item, players):
    try:
        id = stats_item.find("div", class_="name").find("a").get_attribute_list("href")[0].split("/")[-2]
        match = [player for player in players if player.id == id]
        return match[0] if match else None
    except:
        return None

def _parse_rounds(soup, players) -> List[Round]:
    rounds = []
    draws = soup.find_all("div", class_="draw")
    for i, draw in enumerate(draws):
        round_description = draw.find("div", class_="draw-header").text.strip()
        round_number = i + 1
        matchups = []
        draw_items = draw.find_all("div", class_="draw-item")
        for j, draw_item in enumerate(draw_items):
            matchup_number = j + 1
            stats_items = draw_item.find_all("div", class_="stats-item")
            player1 = _find_player(stats_items[0], players)
            player2 = _find_player(stats_items[1], players)
            if stats_items[0].find("div", class_="winner"):
                winner, loser = player1, player2
            elif stats_items[1].find("div", class_="winner"):
                winner, loser = player2, player1
            else:
                winner, loser = None, None
            matchups.append(Matchup(player1=player1, player2=player2, winner=winner, loser=loser, order=matchup_number))
        rounds.append(Round(number=round_number, description=round_description, matchups=matchups))
    return rounds

def parse_soup(soup):
    tournament = _parse_tournament(soup)
    players = _parse_players(soup)
    rounds = _parse_rounds(soup, players=players)
    draw = Draw(tournament=tournament, players=players, rounds=rounds)
    return draw
