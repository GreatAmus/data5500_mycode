'''
Chatgpt history: https://chatgpt.com/share/68ae3a2e-f3f0-8010-8b55-8beda23e5023

HW4 - Create a blackjack game
Program Requirments:
1.  Rules of the game:
The user will always win if…
-User score does not exceed 21, and is higher than the dealer’s score.
-User score does not exceed 21, and the dealer “busts” (gets a score higher than 21).
The user will always lose if…
-User “busts” (gets a score higher than 21)
-User score does not exceed 21, but the dealer’s score is equal or higher and also does not exceed 21.

Your program will create a DeckOfCards object using your DeckOfCards class.  This object will contain a list of 52 Card objects. The DeckOfCards Class already contains a shuffle_deck() function to shuffle a new deck, and a get_card() function returns the next card in the deck (card at index 0 in the list).  
Your program must print the deck of cards before, and after, they are shuffled (I want to see they are being shuffled properly). 
Your program must also be able to correctly score the card based on the suit.  i.e...

2.  Playing the game
To begin the game, your program should have a welcome message, create the deck of cards, shuffle the deck, deal two cards to the user, two cards to the dealer (don't display the dealer's cards yet, just keep track of them).  Print the current user's score to the screen, and ask the user if they would like a ‘hit’.  Continue asking the user if they would like a hit until they stop, or their score exceeds 21.  If the user’s score exceeds 21 print a losing message to the screen. 
If the user has not exceeded 21, and stopped hitting, then display the two dealer's cards.  Have the Dealer keep hitting while the dealer's score is under 17.  Then calculate the dealer’s score, determine if the user won or lost, print the results, and ask the user if they would like to play again.
If the user chooses to play again, keep using the same deck.  Do not create a new deck.  You can simply shuffle the deck again.  You do not need to exclude the cards that have been dealt to the user.  You can simply shuffle the whole deck of 52 cards again.  You can see how this works in the sample output below.  Print the deck before and after it is shuffled, so I can verify your shuffle_deck() and deal_card() functions are working properly.

3.  Handling an Ace
An Ace has the value of 1 or 11 in BlackJack.  The user is in charge of when they hit, and they can keep track themselves what the value of an Ace should be.  Meaning your program simply has to keep track of how many aces the user, or the dealer, has.  If an Ace is present in the hand, and the score busts then reduce the score by ten automatically, so it is no longer busted.  Your program should also be able to do this multiple times to account for a hand with multiple Aces.

Other Requirements
- Have a separate file for DeckOfCards.py and play_game.py
- Card class definition can be in DeckOfCards.py 
- play_game.py should import DeckofCards from DeckOfCards import *

- All the logic for playing the game should be in play_game.py - note the teacher said I can use a separate class
- For each of the possible ways to win or lose, mentioned above, print a message to the user stating why they won or lost.  i.e. if the dealer busted print “Dealer busted, you win!” (or similar).
- As mentioned, when you shuffle the deck, print the deck before and after the shuffle. 
'''

from DeckOfCards import *
from Player import *

'''
 Used to print the original card order, shuffle the cards, and then reprint the deck.
 Returns the shuffled deck
 Parameters: Deck = A deck of cards based on the DeckofCards class
'''
def setup(deck):
    print("\nDeck before shuffling:")
    deck.print_deck()
    deck.shuffle_deck()
    print("\nDeck after shuffling:")
    deck.print_deck()
    return deck

'''
 Helper function to ask users whether to hit
 Loops until a valid response it given
'''
def ask_user_hit():
    while True:
        answer = input(f"\nWould you like to hit? Choose yes or no. ").lower()
        if answer in {"yes", "y", "1", "h", "hit"}:
            return True
        elif answer in {"no", "n", "0", "s", "stay", "stand"}:
            return False
        print('Invalid choice. Please choose "yes" or "no".')    
    return False

'''
 Helper function to ask user to play again
 Loops until a valid response it given
'''
def ask_user_play_again():
    while True:
        answer = input(f"\nWould you like to play again? Choose yes or no. ").lower()
        if answer in {"yes", "y", "1"}:
            return True
        elif answer in {"no", "n", "0", "q"}:
            return False
        print('Invalid choice. Please choose "yes" or "no".')    
    return False

'''
 Controls the game flow during the player's turn. 
 Asks the user whether they would like to hit. 
 If the user hits, add a card to their deck and print their deck
 Parameters:   Deck = A deck of cards based on the DeckofCards class
               Player = A player as an object of the Player class
               Dealer = A dealer as an object of the Player class
'''
def player_turn(deck, player, dealer):
    # Make sure the user knows what the dealer has shown face-up
    dealer.print_dealer_hand(dealer.upcard)

    # Loop untilt he user hits 21 or decides to stay
    while ask_user_hit():
        player.add_card(deck.get_card())
        player.print_hand()

        # Exit if the user hits 21 or busts
        if player.score > 20:
            break

'''
 The dealer goes after the player(s)
 The dealer always hits on 16 and stays on 17 unless the dealer has already beaten the player.
 When the dealer hits, add a card and print the dealer's hand
 Parameters:   Deck = A deck of cards based on the DeckofCards class
               Player = A player as an object of the Player class
               Dealer = A dealer as an object of the Player class
'''
def dealer_turn(deck, player, dealer):
    while dealer.score < 17:
        print(f"Dealer hits on {dealer.score}...")
        dealer.add_card(deck.get_card())
        dealer.print_hand()

'''
 Helper function to check whether a player was dealt a blackjack. 
 A blackjack automatically wins so we don't need to play the rest of the game
 Parameters:   Player = A player as an object of the Player class
               Dealer = A dealer as an object of the Player class
'''
def black_jack(player, dealer):

    # Both the dealer and player have blackjack
    if player.is_blackjack() and dealer.is_blackjack():
        print("Both you and the dealer have Blackjack! It should be a push, but this house is cheap. Ties go to the house, meaning you lose.")
        return True

    # The player has a blackjack
    elif player.is_blackjack():
        print("Blackjack! You win!")
        return True

    # The dealer has a blackjack
    elif dealer.is_blackjack():
        print("The dealer has Blackjack! You lose.")
        return True

    # Return false if the game needs to continue to determine the winner
    return False 

'''
 Determines whether the dealer won or the dealer busted
 This checks all end of game conditions except where the player won.
 This is a boolean that determines whether the game needs to continue
 Parameters:   Player = A player as an object of the Player class
               Dealer = A dealer as an object of the Player class
'''
def resolve_outcome(player, dealer):
        
    # Player lost - Busted
    if player.score > 21:
        print(f"You busted at {player.score}. You lose.")
        return True

    # Dealer lost - Busted
    elif dealer.score > 21:
        print(f"Dealer busted at {dealer.score}. You win!")
        return True
    
    # Player lost - Beat Player's score
    elif dealer.score > player.score:
        print(f"Dealer has you beat with {dealer.score} vs.{player.score}. You lose.")
        return True

    # Player lost - tied Player's score
    elif dealer.score == player.score: 
        print(f"Dealer and you tied at {dealer.score}. Ties go to the house. You lose.")
        return True

    # The player hasn't lost or won - continue the game
    return False

'''
 This function plays a round of blackjack. 
 Game starts with two new players, dealing them 2 cards. 
 Player cards are shown while the dealer shows 1 card faceup
 Parameters:   Deck = A deck of cards based on the DeckofCards class
'''
def round_of_blackjack(deck):

    # Create player and dealer - deal each 2 cards
    player = Player([deck.get_card(), deck.get_card()], "Player")
    dealer = Player([deck.get_card(), deck.get_card()], "Dealer")

    # Print the player's hand
    player.print_hand()

    # If someone gets a blackjack, the game is over
    if black_jack(player, dealer):
        dealer.print_hand()

    # No blackjack then print the dealer's faceup card
    # Have the player to decide whether to hit or stay
    # Once the player stays, have the dealer hit until they hit 17
    else:
        player_turn(deck, player, dealer)
        if not resolve_outcome(player, dealer):
            dealer.print_hand()
            dealer_turn(deck, player, dealer)
            if not resolve_outcome(player, dealer):
                print(f"You beat the dealer with a score of {player.score} vs. {dealer.score}. You won!")

# Main code
# Create a deck of cards and welcomes the user
deck = setup(DeckOfCards())
print("Welcome to Blackjack!")

# Allow the user to play continuous games of blackjack. 
# Don't create a new set of cards, just shuffle the existing one
while True:
    round_of_blackjack(deck)
    if ask_user_play_again():
        deck = setup(deck)
    else:
        break
