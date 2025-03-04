from random import shuffle

# Create a class for the card. 
class Card:
    def __init__(self, name, suit, value):
        self.name = name
        self.suit = suit
        self.value = value

# Function to print a card.
def print_card(card):
    print('[' + card.name + card.suit + ']', end=' ')

# Function to check if the hand is a flush.
# Input - hand: a list of cards
# Output - boolean based on if the hand is a flush or not
def check_flush(hand):
    for i in range(len(hand)-1):
        if hand[i].suit != hand[i+1].suit:
            return False # If the loop finds two cards next to eachother which don't match suit, it isn't a flush
    return True

# Function to check for pairs, three of a kind, four of a kind and full houses
# Input - hand: a list of cards
# Output - an integer which corresponds to a different hand type. 0 = high card, 1 = pair, 2 = 2 pair, 3 = three of a kind, 4 = full house, 5 = four of a kind
def check_duplicates(hand):
    duplicate_array = [0, 0, 0, 0, 0] # Each position in this array corresponds to a card in the hand

    # Below nested loops will compare each card to all other cards in the hand, count the number of duplicates, and store the number of duplicates in the array
    for count, card in enumerate(hand):
        for i in range(5):
            if count != i: # if statement prevents comparing the card to itself
                if card.value == hand[i].value:
                    duplicate_array[count] += 1

    # The array will sum to specific values depending on what the hand is
    if sum(duplicate_array) == 0: # High card: Example array [0,0,0,0,0] no cards have any duplicates
        return 0
    elif sum(duplicate_array) == 2: # Pair: Example array [1,1,0,0,0] two cards (the pair) will have one duplicate each
        return 1
    elif sum(duplicate_array) == 4: # Two Pair: Example array [1,1,1,1,0] four cards (two per pair) will have one duplicate each
        return 2
    elif sum(duplicate_array) == 6: # Three of a kind: Example array [2,2,2,0,0] three cards (the three of a kind) will have two duplicates each
        return 3
    elif sum(duplicate_array) == 8: # Full house: Example array [2,2,2,1,1] three cards (the three of a kind) will have two duplicates each, and two cards (the pair) will have one duplicate each
        return 4
    elif sum(duplicate_array) == 12: # Four of a kind: Example array [3,3,3,3,0] four cards (the four of a kind) will have three duplicates each
        return 5
    else: # The array shouldn't be able to sum to anything else, but if it does it will return -1 for debugging
        return -1

# Function to check for a straight
# Input - hand: a list of cards
# Output - two booleans, one for if the hand is a straight, one for if the hand is an ace high straight
def check_straight(hand):
    # Find the lowest card in the hand, used for an equation later
    lowest_card = min(hand, key=lambda card : card.value)

    # Initialise variables
    is_straight = False
    is_acehigh = False
    ace_high_check = 0
    straight_check = 0

    for card in hand:
        ace_high_check = ace_high_check + card.value # For an ace high straight, the sum of all card values will be 47
        straight_check = straight_check + (card.value - lowest_card.value) # For a straight, this equation will equal 10
    if ace_high_check == 47:
        is_acehigh = True # This is only needed to be able to check for a royal flush
        is_straight = True
    elif straight_check == 10:
        is_straight = True
    return [is_straight, is_acehigh]

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

# Array of duplicate hand types. Location in the array corresponds to the integers output by check_duplicates()
duplicate_hands = ['high card', 'pair', 'two Pair', 'three of a kind', 'full house', 'four of a kind']

# Loop through the suits and names to generate a deck of cards
deck=[]
for suit in suits:
    for name in names:
        card = Card(name, suit, card_values[name])
        deck.append(card)

# Foak & Full House test array
# deck = [Card(2, 'H', 2), Card(2, 'H', 2), Card(2, 'H', 2), Card(2, 'H', 2), Card(3, 'D', 3), Card(3, 'D', 3), Card(3, 'D', 3), Card(3, 'D', 3)]

# Straight check arrays
# deck = [Card('A', 'H', 9), Card('2', 'H', 10), Card('3', 'H', 11), Card('4', 'H', 12), Card('5', 'D', 13)]
# deck = [Card('A', 'H', 1), Card('J', 'H', 11), Card('10', 'H', 10), Card('Q', 'H', 12), Card('K', 'H', 13),]

while True:
    # Shuffle the deck
    shuffle(deck)

    # Deal a hand and print it
    hand=[]
    for i in range(5):
        hand.append(deck[i])
    for card in hand:
        print_card(card)
    print('\n')

    # Check for the strongest hand and print the results
    duplicate_type = check_duplicates(hand)
    is_flush = check_flush(hand)
    is_straight = check_straight(hand)
    text_start = 'Your best hand is a'

    if duplicate_type == -1:
        print('Your code is cooked!')
    elif is_flush and is_straight[0] and is_straight[1]:
        print(text_start, 'royal flush! Holy shitballs!')
    elif check_duplicates(hand) > 3:
        print(text_start, duplicate_hands[duplicate_type])
    elif is_flush:
        print(text_start, 'flush.')
    elif is_straight[0]:
        print(text_start, 'straight.')
    else:
        print(text_start, duplicate_hands[duplicate_type])
    
    replay_answer = input('Would you like to play again? (y/n):')
    if replay_answer.lower() == 'y':
        print('\n')
        continue
    else:
        break

