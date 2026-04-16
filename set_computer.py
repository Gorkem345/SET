#This file contains the Computer class which is used to quickly find sets on a table or check whether 3 cards
#form a set.

import image_dictionary

class Computer:
    def __init__(self):
        pass

    # This function returns the indices that form a set from the table.
    def find_sets(self, table):
        set_indices = []

        index_c1 = 0
        for card1 in table:
            index_c2 = 0
            for card2 in table:
                if index_c1 < index_c2: #To not get duplicate sets.
                    index_c3 = 0
                    for card3 in table:
                        if index_c2 < index_c3: # To not get duplicate sets.
                            if self.is_set(card1, card2, card3): # Returns True if they form a set.
                                set_indices.append([index_c1, index_c2, index_c3])
                        index_c3 += 1
                index_c2 += 1
            index_c1 += 1

        return set_indices

    #Looks at the first 2 cards and finds the required card to form a set. Compares the third card to the required card,
    #if they are the same, returns True; otherwise, returns False.
    def is_set(self, card1, card2, card3):
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


#Test Debug
#computer = Computer()
#table = [image_dictionary.Card("erc1"), image_dictionary.Card("erc2"), image_dictionary.Card("erc3"), image_dictionary.Card("src1"), image_dictionary.Card("frc1")]
#print(computer.find_sets(table))

#print(computer.is_set(table[0], table[3], table[4]))