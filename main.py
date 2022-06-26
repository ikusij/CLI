from plumbum import colors, cli 
from pyfiglet import Figlet
import questionary

from modules.view_bets import views_bets
from modules.view_bet_slip import view_bet_slip

def print_banner(text: str, color: str = "LIGHT_SEA_GREEN", font: str = "slant") -> None:

    """Prints passed text to the cli in a formated manner. Limited to the color and font of the passed text."""

    with colors[color]:
        print(Figlet(font = font).renderText(text))

class CaesarsPalaceCLI(cli.Application):
    
    VERSION = "1.0"

    def main(self):
        
        print_banner("Caesar's Palace Bookie")
        
        while True:
           
            choice = questionary.select("WHAT WOULD YOU LIKE TO DO:", choices = ["VIEW BETS", "VIEW BET SLIP", "EXIT"]).ask()

            if choice == "VIEW BETS":
                views_bets()
            elif choice == "VIEW BET SLIP":
                view_bet_slip()
            elif choice == "EXIT":
                print("GOODBYE")
                break
        
if __name__ == "__main__":
    CaesarsPalaceCLI()