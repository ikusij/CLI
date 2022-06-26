from datetime import date, datetime

import modules.utility as utility
import modules.prompts as prompts
import modules.api_utility as api_utility

def load_bets(filename: str):
    
    """Fetches the JSON data from the api call"""

    bets = utility.load_json(filename)
    return bets

def format_json_to_choices(event: dict) -> list:
    
    """Formats event data into a string"""

    choices = []
    
    for bet, odds in event.items():
        for outcome, odd in odds.items():
            choices.append(f"{bet} {outcome} ({'+' if odd > 0 else ''}{odd})")
    
    return choices

def remove_expired_bets(filename: str) -> dict:
    
    """Removes bets inside the bet slip which date has passed current date"""

    bets = utility.load_json(filename)
    
    todays_date = date.today()
    todays_timestamp = datetime(todays_date.year, todays_date.month, todays_date.day).timestamp()

    for key in bets.copy().keys():
        
        bet_date_timestamp = datetime(*[int(num) for num in key.split("-")]).timestamp()

        if todays_timestamp > bet_date_timestamp:
            del bets[key]
    
    return bets

def post_bets(bet_slip: list, filename: str = "bet-slip.json") -> None:

    """Posts bets into the bet slip JSON file"""

    stored_bet_slip = remove_expired_bets(filename)

    for date, event, bet_name, bet_amount_dollars, payout in bet_slip:
        
        if date not in stored_bet_slip:
            stored_bet_slip[date] = { event: [{ "bet": bet_name, "amount": f"${bet_amount_dollars:.2f}", "payout": f"${payout:.2f}" }] }
        else:
            if event not in stored_bet_slip[date]:
               stored_bet_slip[date][event] = [{ "bet": bet_name, "amount": f"${bet_amount_dollars:.2f}", "payout": f"${payout:.2f}" }]
            else:
                stored_bet_slip[date][event] += [{ "bet": bet_name, "amount": f"${bet_amount_dollars:.2f}", "payout": f"${payout:.2f}" }]
    
    utility.post_json(filename, stored_bet_slip)

def views_bets() -> None:
    
    """Displays bets. If some bets are chosen they are posted to the bet slip"""

    sport = prompts.sport_prompt()
    league = prompts.league_prompt(sport)
    
    api_utility.await_api_call()
    
    date = prompts.bet_date_prompt(sport, league)
    
    date_filename = utility.construct_path(sport, league, date) + ".json"
    date_bets = load_bets(filename = date_filename)
    
    event = prompts.event_prompt(choices = date_bets.keys())
    event_bet_choices = format_json_to_choices(date_bets[event])
    event_bets = prompts.event_bets_prompt(choices = event_bet_choices)
    
    if len(event_bets) != 0: 
        bet_slip = [(date, event, bet_name, *prompts.bet_prompt(bet_name)) for bet_name in event_bets]
        post_bets(bet_slip)