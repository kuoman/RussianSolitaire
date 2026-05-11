import argparse
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from solitaire.deck import Deck
from solitaire.tableau import Tableau
from solitaire.display import Display

def main():
    parser = argparse.ArgumentParser(description="Yukon Russian Solitaire")
    parser.add_argument("--debug", action="store_true", help="Reveal face-down cards")
    args = parser.parse_args()

    deck = Deck()
    deck.shuffle()
    tableau = Tableau(deck)
    print(Display(tableau, debug=args.debug).render())

if __name__ == "__main__":
    main()
