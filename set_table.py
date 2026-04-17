from image_dictionary import cards
from image_dictionary import Card
import random
import copy


class Table:
    def __init__(self):
        self.deck = {}
        self.num_cards_in_deck = 81
        self.cards_on_table = [None for _ in range(12)]
        self.selected = []
        self.selection_mode = False
        self.game_end = False

    def handle_start_game(self):
        self.deck = copy.deepcopy(cards)
        self.num_cards_in_deck = 81
        self.selected = []
        self.selection_mode = False
        self.game_end = False
        self.pull12cards()

    def handle_click(self, index):
        if self.selection_mode:
            if self.cards_on_table[index] != None and index not in self.selected:
                self.selected.append(index)
                if len(self.selected) == 3:
                    self.handle_selection()

    def handle_selection(self): #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        ###### STOP THE TIMER
        if is_set(self.cards_on_table[self.selected[0]], self.cards_on_table[self.selected[1]], self.cards_on_table[self.selected[2]]):
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
        self.selection_mode = False
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
            self.pull12cards()
    def pull12cards(self):
        if self.num_cards_in_deck < 12:
            ###### HANDLE END OF GAME #######
            self.game_end = True # For debug
        else:
            for iter_num in range(12):
                key, value = random.choice(list(self.deck.items()))
                self.cards_on_table[iter_num] = value
                del self.deck[key]
                self.num_cards_in_deck -= 1
            if len(self.find_sets()) == 0:
                ###### HANDLE NO MORE MATCHES ######
                print("No available matches, redistributing!")
                self.pull12cards()

    # This function returns the indices that form a set from the table.
    def find_sets(self):
        set_indices = []

        index_c1 = 0
        for card1 in self.cards_on_table:
            if card1 != None:
                index_c2 = 0
                for card2 in self.cards_on_table:
                    if card2 != None:
                        if index_c1 < index_c2:  # To not get duplicate sets.
                            index_c3 = 0
                            for card3 in self.cards_on_table:
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
            if filling != card1.filling and filling != card2.filling:
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