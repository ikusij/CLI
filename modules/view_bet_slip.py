from datetime import datetime

import modules.utility as utility

def load_bet_slip(filename: str = "bet-slip.json") -> dict:
    
    """Fetches the JSON data stored in the bet-slip file"""
    
    bet_slip = utility.load_json(filename)
    return bet_slip

def sort_by_date(dates: list) -> list:
    
    """Sorts date keys from bet slip in ascending order"""
    
    sorted_dates = sorted(dates, key = lambda date: datetime(*[int(num) for num in date.split("-")]).timestamp())
    return sorted_dates

def format_bet_display(bet: dict) -> str:
    
    """Formats the bet into a string"""

    bet_name, bet_amount, bet_payout = bet.values()
    return f"{bet_name}\n    Cost: {bet_amount} | Payout: {bet_payout}\n"

def track_total_cost_and_payout(total_cost: float, total_payout: float, cost: float, payout: float) -> tuple:
    
    """Tracks the total cost and payout of all bets in the bet slip"""

    total_cost += float(cost.split("$")[-1])
    total_payout += float(payout.split("$")[-1])
    
    return total_cost, total_payout

def display_bets(bet_slip: dict, date: str, total_cost: float, total_payout: float) -> tuple:

    """Displays the bets stored for the passed date"""

    print(date, end = "\n\n")
    
    for event, bets in bet_slip[date].items():
        print(event, end = "\n\n")
        for bet in bets:
            print(f"    - {format_bet_display(bet)}")
            total_cost, total_payout = track_total_cost_and_payout(total_cost, total_payout, cost = bet["amount"], payout = bet["payout"])
    
    return total_cost, total_payout

def view_bet_slip() -> str:
    
    """Displays the data in the bet slip"""

    bet_slip = load_bet_slip()
    dates = sort_by_date(dates = bet_slip.keys())
    total_cost, total_payout = 0, 0

    print("\n")

    for date in dates:
        total_cost, total_payout = display_bets(bet_slip, date, total_cost, total_payout)
    
    print(f"Total Cost: ${total_cost:.2f} | Total Payout: ${total_payout:.2f}\n")