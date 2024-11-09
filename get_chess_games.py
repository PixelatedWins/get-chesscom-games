import requests
from datetime import datetime

def getgames(username, monthspast, useragent='unknown'):
    """
    Fetch games of a Chess.com user going back a specified number of months from the current month.

    Parameters:
    - username (str): The Chess.com username.
    - monthspast (int): The number of months to go back from the current month.
    - headers (dict, optional): Optional headers to include in the request.

    Returns:
    - list: A list of PGN strings for the fetched games.
    """
    games_list = []
    
 
    now = datetime.now()
    current_year, current_month = now.year, now.month

    # Chess.com's API requires a user-agent
    if useragent is None:
        headers = {
            "User-Agent": "unknown"
        }
    else:
        headers = {
            "User-Agent": str(useragent)
        }
        

    for i in range(monthspast):
        year = current_year - (current_month - i - 1) // 12
        month = (current_month - i - 1) % 12 + 1

        url = f"https://api.chess.com/pub/player/{username}/games/{year}/{month:02d}"

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an error for HTTP errors
            games_data = response.json()
            for game in games_data.get("games", []):
                games_list.append(game["pgn"])

        except requests.exceptions.RequestException as e:
            print(f"An error occurred for {year}-{month:02d}: {e}")
            break  
        
    return games_list
