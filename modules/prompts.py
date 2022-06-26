import modules.fetch as fetch
import questionary
import os

def prompt_template(choices: list, message: str) -> str:

    """Template prompt."""

    return questionary.select(message, choices).ask()

def sport_prompt(message: str = "SELECT SPORT:") -> str:
    
    """Asks which sport to see bets."""
    
    choices = fetch.fetch_available_sports()
    return prompt_template(choices, message)

def league_prompt(sport: str, message: str = "SELECT {sport} LEAGUE:") -> str:
    
    """Asks which league for the passed sport to see bets."""
    
    message = message.format(sport = sport.upper())
    choices = fetch.fetch_available_leagues(sport)
    
    return prompt_template(choices, message)

def bet_date_prompt(sport: str, league: str, message: str = "SELECT BET DATE:") -> str:
    
    """Asks which date for the passed sport and corresponding league to see bets."""
    
    choices = [os.path.splitext(choice)[0] for choice in fetch.fetch_bets(sport, league)][::-1]
    
    return prompt_template(choices, message)

def event_prompt(choices: list, message: str = "SELECT EVENT") -> str:
    
    """Asks which event for the passed date."""
    
    return prompt_template(choices, message)

def event_bets_prompt(choices: list, message: str = "SELECT BET TO ADD TO BET SLIP:") -> str:
    
    """Asks which bets (can select 0+) to select for the passed event"""
    
    return questionary.checkbox(choices, message).ask()

def format_odds(bet: str) -> int:
    
    """Fetches the odd for the passed bet."""
    
    odds = bet[bet.find("(") + 1:bet.find(")")]
    return int(odds)

def bet_preview(bet: str, bet_amount: float) -> float:
    
    """Displays the outcome preview (cost and payout) for the passed bet and bet amount."""

    bet_amount = bet_amount * 100
    odds = format_odds(bet) / 100

    if odds > 0:
        to_win = bet_amount * odds / 100
        payout = bet_amount / 100 + to_win
    else:
        to_win = bet_amount / (-odds) / 100
        payout = bet_amount / 100 + to_win

    print(f"Bet Preview:\nTo Win: ${to_win:.2f}\nPayout: ${payout:.2f}")
    
    return payout

def bet_prompt(bet: str, message: str = "BET AMOUNT FOR {bet}:") -> tuple:
    
    """Asks how much to bet and keeps asking if decide to change bet amount"""

    message = message.format(bet = bet)
    
    bet_amount = float(questionary.text(message).ask())
    payout = bet_preview(bet, bet_amount)
    
    while not questionary.confirm(f"AMOUNT TO BET ${bet_amount:.2f}").ask():
        bet_amount = float(questionary.text(message).ask())
        payout = bet_preview(bet, bet_amount)
    
    return bet_amount, payout