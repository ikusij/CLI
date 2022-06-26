import os
import modules.utility as utility

def fetch_path_content(*args: tuple) -> list:
    path = utility.construct_path(*args)
    return [item.upper() for item in os.listdir(path)]

def fetch_available_sports() -> list:

    """Fetches the list of sports currently supported by the api"""

    return fetch_path_content()

def fetch_available_leagues(sport: str) -> list:

    """Fetches the list of league's of the passed sport currently supported by the api"""

    return fetch_path_content(sport)

def fetch_bets(sport: str, league: str):

    """Fetches the bets files, by date, for the passsed sport and league"""

    return fetch_path_content(sport, league)