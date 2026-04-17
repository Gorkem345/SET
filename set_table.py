from image_dictionary import cards
from image_dictionary import Card
import random

class Table:
    def __init__(self):
        self.deck = cards
        self.cards_on_table = []
        self.selected = []
        self.selection_mode = False

    def handle_start_game(self):
        self.pull12cards()

    def handle_click(self, index):
        if self.selection_mode:
            if index not in self.selected:
                self.selected.append(index)
                if len(self.selected) == 3:
                    self.handle_selection()
                else:
                    self.selected.append(index)

    def handle_selection(self): #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        ###### STOP THE TIMER
        if is_set(self.selected[0], self.selected[1], self.selected[2]):
            self.pull3cards(self.selected)
            ###### INCREASE THE PLAYER'S SCORE ######
        else:
            ###### DECREASE THE PLAYER'S SCORE ######
            pass
        self.selection_mode = False
        self.selected = []

    def pull3cards(self, selected):
        for _ in range(3):
            pass
    def pull12cards(self):
        for _ in range(12):
            pass

    # This function returns the indices that form a set from the table.
    def find_sets(self):
        set_indices = []

        index_c1 = 0
        for card1 in self.cards_on_table:
            index_c2 = 0
            for card2 in self.cards_on_table:
                if index_c1 < index_c2:  # To not get duplicate sets.
                    index_c3 = 0
                    for card3 in self.cards_on_table:
                        if index_c2 < index_c3:  # To not get duplicate sets.
                            if is_set(card1, card2, card3):  # Returns True if they form a set.
                                set_indices.append([index_c1, index_c2, index_c3])
                        index_c3 += 1
                index_c2 += 1
            index_c1 += 1

        return set_indices

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


#Debug
myTable = Table()
myTable.cards_on_table = [Card("erc1"), Card("erc2"), Card("erc3"), Card("src1"), Card("frc1"), Card("frc2")]

print(myTable.find_sets())
print(is_set(myTable.cards_on_table[0], myTable.cards_on_table[3], myTable.cards_on_table[4]))



