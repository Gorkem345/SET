from utils.card_deck import Card #the 81-card dictionary
import random
import copy
import pygame
from utils.card_deck import cards


class Table:
    def __init__(self):
        self.deck = {} #The remaining undealt cards
        self.num_cards_in_deck = 81
        self.cards_on_table = [None for _ in range(12)]
        #Creates 12 slots on the table
        #[None, None, None, ..., None] at first
        self.hint = []
        self.selected = []
        self.selection_mode = False
        self.waiting_for_replace = False
        self.replace_time = 0
        self.correct_set = False #check if the selected cards are a real set
        self.game_end = False

    def handle_start_game(self):
        self.deck = copy.deepcopy(cards) #a copy of 81 card dictionary
                                         #so everytime remove card will not destory the original one
        self.num_cards_in_deck = 81
        self.selected = []
        self.selection_mode = False
        self.game_end = False
        self.pull12cards()

    def handle_click(self, index): #left click add a card to the selection
        if self.selection_mode:
            if self.cards_on_table[index] != None and index not in self.selected:
                self.selected.append(index)
                if len(self.selected) == 3:
                    return self.handle_selection()
        return None #No complete selection made yet

    def handle_right_click(self, index): #right click: remove a card from the selection
        if self.selection_mode:
            if self.cards_on_table[index] != None and index in self.selected:
                self.selected.remove(index)
                #print(f"Removed {index}. New list: {self.selected}")  # Debug
                return True
        return False

    def handle_selection(self): #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        set_formed = False
        ###### STOP THE TIMER
        if is_set(self.cards_on_table[self.selected[0]], self.cards_on_table[self.selected[1]], self.cards_on_table[self.selected[2]]):
            set_formed = True
            self.correct_set = True
        else:
            self.correct_set = False

        self.waiting_for_replace = True
        self.replace_time = pygame.time.get_ticks() + 1500
        self.selection_mode = False
        return set_formed

    def replace_selection(self):
        if self.correct_set:
            if self.num_cards_in_deck > 0:
                self.pull3cards()
            else:
                self.cards_on_table[self.selected[0]] = None
                self.cards_on_table[self.selected[1]] = None
                self.cards_on_table[self.selected[2]] = None
                if self.find_sets() == []:
                    self.game_end = True
            ###### INCREASE THE PLAYER'S SCORE ######
        else:
            ###### DECREASE THE PLAYER'S SCORE ######
            pass
        self.correct_set = False
        self.selected = []

    def pull3cards(self): #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if self.num_cards_in_deck < 3 and self.find_sets() == []:
            ###### HANDLE END OF GAME #######
            self.game_end = True # For debug
        else:
            for iter_num in range(3):
                key, value = random.choice(list(self.deck.items()))
                self.cards_on_table[self.selected[iter_num]] = value
                del self.deck[key]
                self.num_cards_in_deck -= 1
        if self.find_sets() == []:
            ###### HANDLE NO MORE MATCHES ######
            print("No available matches, redistributing!")
            self.pull12cards() #after replacing the 3 cards, check whether the table has any valid SETs
    def pull12cards(self):
        if self.num_cards_in_deck < 12:
            ###### HANDLE END OF GAME #######
            self.game_end = True # For debug
        else:
            for iter_num in range(12):
                key, value = random.choice(list(self.deck.items()))
                #after calling self.handle_start_game(), self.deck is the 81 cards deck
                #in this loop of 12 loops in total, randomly pick one
                #each loop have key = card id, value = one Card object
                self.cards_on_table[iter_num] = value #place this Card object to one position of the empty 12 slots
                del self.deck[key] #each card will be used only once
                self.num_cards_in_deck -= 1
            if len(self.find_sets()) == 0:
                ###### HANDLE NO MORE MATCHES ######
                print("No available matches, redistributing!")
                self.pull12cards()

    # This function returns the indices that form a set from the table.
    def find_sets(self):
        set_indices = []

        index_c1 = 0
        for card1 in self.cards_on_table: #loop through all cards on the table
                                          #pick first card
            if card1 != None:
                index_c2 = 0
                for card2 in self.cards_on_table: #for each card1, loop through all cards (cards2)
                    if card2 != None:
                        if index_c1 < index_c2:  # only use cards 2 if it comes after card, so only use card2 = B, C, D when card1 = A
                                                 # To not get duplicate sets, like (A, B), (B, A)
                            index_c3 = 0
                            for card3 in self.cards_on_table: #for each card2, loop through all card3
                                if card3 != None:
                                    if index_c2 < index_c3:  # To not get duplicate sets.
                                        if is_set(card1, card2, card3):  # Returns True if they form a set.
                                            set_indices.append([index_c1, index_c2, index_c3])
                                index_c3 += 1
                    index_c2 += 1
            index_c1 += 1

        return set_indices

    def handle_start_selection(self):
        self.selection_mode = True
        self.selected = []

    # Selects two cards of a set to display as hint
    def give_hint(self):
        sets = self.find_sets()
        if sets != []:
            set = random.choice(sets)
            hint = random.sample(set, 2)
        else:
            hint = False
        return hint
    # For the computer to find a set
    def give_set(self):
        sets = self.find_sets()
        if sets != []:
            set = random.choice(sets)
        else:
            set = False
        return set

    def update(self):
        if self.waiting_for_replace:
            if pygame.time.get_ticks() >= self.replace_time:
                self.replace_selection()
                self.waiting_for_replace = False

    def __repr__(self):
        message = str("")
        for index in range(len(self.cards_on_table)):
            message += "Card " + str(index) + ": " +self.cards_on_table[index].__repr__()
        return message

# Looks at the first 2 cards and finds the required card to form a set. Compares the third card to the required card,
# if they are the same, returns True; otherwise, returns False.
def is_set(card1, card2, card3):
    # Find filling
    if card1.filling == card2.filling:
        required_filling = card1.filling
    else:
        for filling in ["e", "s", "f"]:
            if filling != card1.filling and filling != card2.filling: #Find the filling that is NOT card1 and NOT card2
                required_filling = filling

    # Find color
    if card1.color == card2.color:
        required_color = card1.color
    else:
        for color in ["r", "p", "g"]:
            if color != card1.color and color != card2.color:
                required_color = color

    # Find shape
    if card1.shape == card2.shape:
        required_shape = card1.shape
    else:
        for shape in ["c", "d", "s"]:
            if shape != card1.shape and shape != card2.shape:
                required_shape = shape

    # Find count
    if card1.count == card2.count:
        required_count = card1.count
    else:
        for count in ["1", "2", "3"]:
            if count != card1.count and count != card2.count:
                required_count = count

    # Look if the card3 is the required card
    if card3.filling == required_filling and card3.color == required_color and card3.shape == required_shape and card3.count == required_count:
        return True
    else:
        return False





'''
#Debug
myTable = Table()
myTable.handle_start_game()

print(myTable)

sets = myTable.find_sets()
print(sets)
print()

#for set in sets:
    #print(is_set(myTable.cards_on_table[set[0]], myTable.cards_on_table[set[1]], myTable.cards_on_table[set[2]]))

while not myTable.game_end:
    myTable.handle_start_selection()
    myTable.handle_click(sets[0][0])
    myTable.handle_click(sets[0][1])
    myTable.handle_click(sets[0][2])
    print(myTable)
    sets = myTable.find_sets()
    print(sets)
'''