from random import shuffle
import pygame

# Pygame setup
pygame.init()
pygame.display.set_caption("Hodd Toward's Video Poker!")
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
poker_table = (34, 52, 38)
deal_button_img = pygame.image.load('images/deal_button.png')
deal_button_greyed_img = pygame.image.load('images/deal_button_greyed.png')
hand_dealt = False
clubs_img = pygame.image.load('images/clubs.png')
spades_img = pygame.image.load('images/spades.png')
hearts_img = pygame.image.load('images/hearts.png')
diamonds_img = pygame.image.load('images/diamonds.png')

# Create a class for the button.
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False
        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Draw button on screen
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

# Create deal button instance
deal_button_width = deal_button_img.get_width()
deal_button_height = deal_button_img.get_height()
deal_button_x = (SCREEN_WIDTH-deal_button_width)/2
deal_button_y = (4*SCREEN_HEIGHT/5) - (deal_button_height/2)
deal_button = Button(deal_button_x, deal_button_y, deal_button_img)

text_font = pygame.font.Font('fonts/Pixeled.ttf', 24)

def draw_text(text, font, text_col, x, y, flipped):
    txt_img = font.render(text, True, text_col)
    txt_img_flipped = pygame.transform.flip(txt_img, True, True)
    if flipped:
        screen.blit(txt_img_flipped, (x, y))
    else:
        screen.blit(txt_img, (x, y))

# Create a class for the card. 
class Card:
    def __init__(self, name, suit, value, x, y):
        self.name = name
        self.suit = suit
        self.value = value
        self.x = x
        self.y = y
        self.rect = (x, y, 160, 240)
    
    def set_x(self, new_x):
        self.x = new_x
        self.rect = (self.x, self.y, 160, 240)

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        if self.suit == 'D':
            text_colour = (255,0,0)
            suit_img = diamonds_img
        elif self.suit == 'H':
            text_colour = (255,0,0)
            suit_img = hearts_img
        elif self.suit == 'S':
            text_colour = (0,0,0)
            suit_img = spades_img
        else:
            text_colour = (0,0,0)
            suit_img = clubs_img
        draw_text(self.name, text_font, text_colour, self.x + 10, self.y, False)
        draw_text(self.name, text_font, text_colour, self.x + 120, self.y + 170, True)
        screen.blit(suit_img, (self.x + ((160-50)/2), self.y + ((240-50)/2)))

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
    # Sort the hand lowest to highest
    sorted_hand = sorted(hand, key=lambda card : card.value)

    # Initialise variables
    is_straight = False
    is_acehigh = False
    acehigh_check = [1,10,11,12,13]

    for i, card in enumerate(sorted_hand):
        if card.value == acehigh_check[i]:
            is_acehigh = True
            is_straight = True
        else:
            is_acehigh = False
            is_straight = False
            break
    
    if not is_acehigh:
        for i in range(4):
            if sorted_hand[i].value == sorted_hand[i+1].value - 1:
                is_straight = True
            else:
                is_straight = False
                break

    return [is_straight, is_acehigh]

# Function to deal a hand
def deal_hand(suits, names, card_values):
    # Generate a deck based on inputs
    deck=[]
    for suit in suits:
        for name in names:
            card = Card(name, suit, card_values[name], 0, 120)
            deck.append(card)
    
    # Shuffle the deck
    shuffle(deck)

    # Deal a hand and print it
    hand=[]
    for i in range(5):
        hand.append(deck[i])
    for i, card in enumerate(hand):
        card.set_x(80+(240*i))

    return hand

    # Check for the strongest hand and print the results
def check_hand(hand):
    duplicate_type = check_duplicates(hand)
    is_flush = check_flush(hand)
    is_straight = check_straight(hand)
    text_start = 'Your best hand is a'

    if duplicate_type == -1:
        return -1
    elif is_flush and is_straight[0] and is_straight[1]:
        return 6
    elif is_flush and is_straight[0]:
        return 7
    elif duplicate_type > 3:
        return duplicate_type
    elif is_flush:
        return 8
    elif is_straight[0]:
        return 9
    else:
        return duplicate_type



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
duplicate_hands = ['high card', 'pair', 'two pair', 'three of a kind', 'full house', 'four of a kind']
all_hands = ['high card', 'pair', 'two pair', 'three of a kind', 'full house', 'four of a kind', 'royal flush', 'straight flush', 'flush', 'straight']

# Foak & Full House test array
# deck = [Card(2, 'H', 2), Card(2, 'H', 2), Card(2, 'H', 2), Card(2, 'H', 2), Card(3, 'D', 3), Card(3, 'D', 3), Card(3, 'D', 3), Card(3, 'D', 3)]

# Straight check arrays
# deck = [Card('A', 'H', 9), Card('2', 'H', 10), Card('3', 'H', 11), Card('4', 'H', 12), Card('5', 'H', 13)]
# deck = [Card('A', 'H', 1), Card('J', 'H', 11), Card('10', 'H', 10), Card('Q', 'H', 12), Card('K', 'H', 13),]
# deck = [Card('A', 'S', 1), Card('3', 'D', 3), Card('3', 'H', 3), Card('A', 'D', 1), Card('7', 'S', 7)]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(poker_table)
    if deal_button.draw():
        hand = deal_hand(suits, names, card_values)
        hand_dealt = True

    if hand_dealt:
        for card in hand:
            card.draw()
        best_hand = check_hand(hand)
        result_text = 'Your hand is a ' + all_hands[best_hand]
        draw_text(result_text.upper(), text_font, (255, 255, 255), 80, 400, False)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
