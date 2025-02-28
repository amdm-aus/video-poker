from random import shuffle

# Create a class for the card. 
class Card:
    def __init__(self, name, suit):
        self.name = name
        self.suit = suit

# Function to print a card.
def print_card(card):
    print('[', card.name, card.suit, ']')

# Function to check if the hand is a flush.
# Input - hand: a list of cards
# Output - boolean based on if the hand is a flush or not
def check_flush(hand):
    for i in range(len(hand)-1):
        if hand[i].suit != hand[i+1].suit:
            return False
    return True


# Define the suits, card names, and a dictionary of the card values associated with those names.
suits = ['H', 'D', 'S', 'C']
names = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
card_values = {
    'A': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'J': 11,
    'Q': 12,
    'K': 13
}

# Loop through the suits and names to generate a deck of cards
deck=[]
for suit in suits:
    for name in names:
        card = Card(name, suit)
        deck.append(card)

# Shuffle the deck
shuffle(deck)

# Deal a hand and print it
hand=[]
for i in range(5):
    hand.append(deck[i])
for card in hand:
    print_card(card)

# Check if it's a flush and print the result
is_flush = check_flush(hand)
if is_flush:
    print("It's a flush!")
else:
    print("It's not a flush :(")