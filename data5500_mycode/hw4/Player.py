'''
This is a function that stores a player, whether its a player or a dealer
I figured this would be better as it allows you to reuse the player, maybe even making the game multi-player
The class allows a player to add cards to their deck, calculating their score and the aces drawn
The class also prints the score
'''

# initialize by adding the number of cards drawn to the players deck
class Player():
    def __init__(self, deck : list, label : str):
        self.__score = 0
        self.__ace = 0
        self.__label = label
        self.__deck = []
        for card in deck:
            self.add_card(card)

# ----- Properties -----
    # Properties for label, score and the player's hand
    @property
    def label(self) -> str:
        return self.__label

    @property
    def score(self) -> int:
        return self.__score

    @property
    def upcard(self):
        # First card (for dealer show)
        return self.__deck[0] if self.__deck else None

# ----- Game play functions -----
    # Add a new card to the player's deck. 
    def add_card(self, card):
        self.__deck.append(card)
        self.track_score(card)
        return

    # Calculate the player's current score and track the number of aces
    # I separated this out in case we had a different game with a different scoring process
    def track_score(self, card):
        self.__score += card.val
        if card.face == "Ace":
            self.__ace += 1
        while self.__score > 21 and self.__ace > 0:
            self.__ace -= 1
            self.__score -= 10
        return

# ---- Hand State Helpers ----
# Good suggestion from ChatGPT to add these. Then the scoring is all handled by the Player class

    def is_blackjack(self):
        return len(self.__deck) == 2 and self.score == 21

    def is_busted(self):
        return self.score > 21

# ----- Printing -----
    # Print the current score along with the player's label
    # The label could be a name or something else. 
    def print_score(self):    
        print(f"{self.__label}'s Current Score: {self.__score}")
        return

    # Print's the current contents of the player's deck
    def print_hand(self):
        joined_str = ', '.join(f"{card.face} of {card.suit}" for card in self.__deck)
        print(f"Cards in {self.__label}'s hand: {joined_str}")
        self.print_score()
        return

    # Print the dealer's face-up cards
    # Blackjack has 1 card faceup and one facedown
    def print_dealer_hand(self, card):
        print(f"Dealer shows {card.face} of {card.suit}")
        return

