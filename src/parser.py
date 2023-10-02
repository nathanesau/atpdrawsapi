import requests
from bs4 import BeautifulSoup
from collections import defaultdict

def _parse_player_data(data):
    """
    return player obj containing "name", "link" and "flag_link"
    """
    a_tag = data.find("a")
    img_tag = data.find("img", class_="scores-draw-entry-box-players-item-flag")
    name = a_tag["data-ga-label"]
    link = f'https://www.atptour.com/{a_tag["href"]}'
    flag_link = f'https://www.atptour.com/{img_tag["src"]}'
    return {"name": name, "link": link, "flag_link": flag_link}

def parse_draw(draw_content):
    """
    return round1 matchups for a draw containing pairs of player obj
    """
    soup = BeautifulSoup(draw_content, "html.parser")
    draw_table_content = soup.find(id="scoresDrawTableContent")
    draw_table = draw_table_content.find(id="scoresDrawTable")
    tbody = draw_table.find("tbody")

    round1_matchups = []

    for tbody_row in tbody.find_all("tr", recursive=False):
        tbody_row_entry = tbody_row.find("div", class_="scores-draw-entry-box")

        # parse round1 matchup
        matchup = []
        for tbody_row_entry_row in tbody_row_entry.find_all("tr"):
            position_data, seed_data, player_data = tbody_row_entry_row.find_all("td")
            position = position_data.text
            seed = seed_data.text.strip() if seed_data.text else "(U)"
            player = _parse_player_data(player_data)
            matchup.append({"position": position, "seed": seed, "player": player})
        
        round1_matchups.append(matchup)

        # TODO: parse matchups after round1

    return round1_matchups

def handler(event, _):
    """
    lambda function for parsing draw and storing the parsed information in dynamodb
    """
    page = requests.get(event["url"])
    round1_matchups = parse_draw(page.content)
    return {"round1_matchups": round1_matchups}
