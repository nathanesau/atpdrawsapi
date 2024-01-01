# hack since pytest doesn't like absolute imports
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__)))

import datetime
from bs4 import BeautifulSoup
from custom_types import Draw
import atp_v1_parser

FORMAT_ATP_V1 = "atp_v1"
FORMAT_UNKNOWN = "unknown"

def get_format(soup):
    if soup.find("div", class_="draw-round-1"):
        return FORMAT_ATP_V1
    else:
        return FORMAT_UNKNOWN

def parse_draw(content) -> Draw:
    """
    return the draw (parsed from html content)
    """
    soup = BeautifulSoup(content, "html.parser")
    
    format = get_format(soup)
    
    if format == FORMAT_ATP_V1:
        return atp_v1_parser.parse_soup(soup)
    else:
        raise Exception("unable to parse draw with unknown format")
