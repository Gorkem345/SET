from utils.card_deck import cards #the 81-card dictionary
import random
import copy
import pygame

class Table:
    '''
    DESCRIPTION:
    Table class handles the games logic, keeps the deck and the cards on the table information. Clicking on the cards,
    making selections, validating and finding sets are handled using this class.
    PARAMETERS:
    None
    LIMITATIONS:
    Does not have full test coverage. (Note: There are no known bugs)
    STRUCTURES:
    The deck is a deepcopy and stored in this class. An array of cards represents the cards on the table. If
    the type is None, it means there is no card being displayed in that index. hint and selected arrays hold the
    indices of their related cards. Has some flags; selection_mode, waiting_for_replace, correct_set and game_end.
    Lastly, replace_time is used to synchronize the GUI and the logic of the game.
    OUTPUT:
    None
    '''

    def __init__(self):
        '''
        Sets the default values.
        '''
        self.deck = {} #The remaining undealt cards
        self.num_cards_in_deck = 81
        self.cards_on_table = [None for _ in range(12)] # None or a card object
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
        '''
        Description:
        Called at the start of the game or when the game resets. Assigns the default values and pulls 12 cards out
        of the deck and puts them on the table to start the game.
        Parameters:
        None
        Limitations:
        -
        Structures:
        Uses deepcopy for assigning the deck. This way the original card deck will not be affected by the changes,
        so when the game resets it is possible to reset the deck.
        Outputs:
        None
        '''
        self.deck = copy.deepcopy(cards) #a copy of 81 card dictionary
                                         #so everytime remove card will not destroy the original one
        self.num_cards_in_deck = 81
        self.selected = []
        self.selection_mode = False
        self.game_end = False
        self.pull12cards()

    def handle_click(self, index): #left click add a card to the selection
        '''
        Description:
        Called when a card is clicked using the left click. Adds the card's index to the selected array. If the selected
        card count reaches 3, it means a selection has been made and calls the handle_selection method.
        Parameters:
        index: It is the index of the selected card. It can be between 1-12.
        Limitations:
        -
        Structures:
        First 'if' checks if the table is in selection mode. (Selection mode is when a player had pressed their button,
        and selecting the cards.) Seconds 'if' checks if there is actually a card displayed on the current index to
        prevent game from crashing, and makes sure that the clicked card is not already selected.
        Outputs:
        Returns None if the selection is not complete yet; only 1 or 2 cards are selected, not 3. Otherwise, using the
        handle_selection method, returns True if the 3 selected cards form a set or returns False if cards do not form
        a set.
        '''
        if self.selection_mode:
            if self.cards_on_table[index] != None and index not in self.selected:
                self.selected.append(index)
                if len(self.selected) == 3:
                    return self.handle_selection()
        return None #No complete selection made yet

    def handle_right_click(self, index): #right click: remove a card from the selection
        '''
        Description:
        Called when a card is clicked using the right click. Removes the card's index from the selected array if the
        card was selected.
        Parameters:
        index: The index of the right-clicked card. It can be between 1-12.
        Limitations:
        -
        Structures:
        Similar to handle_click method, it checks if the table is in selection mode, if the clicked card is displayed on
        the table. If its index is in the selected array, it gets removed.
        Outputs:
        Returns True if the removal happens, returns False otherwise.
        '''
        if self.selection_mode:
            if self.cards_on_table[index] != None and index in self.selected:
                self.selected.remove(index)
                #print(f"Removed {index}. New list: {self.selected}")  # Debug
                return True
        return False

    def handle_selection(self):
        '''
        Description:
        This method is called when a selection happens (3 cards are selected by the player). It checks if the cards
        selected form a set. Synchronizes the GUI and the game logic by using a timer.
        Parameters:
        None, uses the self.selected array.
        Limitations:
        -
        Structures:
        Uses is_set method to figure out if the cards form a set. Uses a timer to keep the selected cards displayed to
        give feedback to the user.
        Outputs:
        Returns True if a set is formed, False otherwise.
        '''
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
        '''
        Description:
        When a set is correctly selected, this method replaces the cards with new cards from the deck using the
        pull3cards method.
        Parameters:
        None
        Limitations:
        Not exactly a limitation, but this method could have been merged with pull3cards method since they are always
        used together.
        Structures:
        Sees the flag handled in handle_selection and if it is True and there are cards left in the deck, it calls
        pull3cards method. Moreover, if a set is correctly identified but there are no cards left in the deck to replace
        them, it sets the cards value to None. This way cards are no longer displayed on the table.
        '''
        if not self.game_end and self.correct_set:
            if self.num_cards_in_deck > 0:
                self.pull3cards()
            else:
                self.cards_on_table[self.selected[0]] = None
                self.cards_on_table[self.selected[1]] = None
                self.cards_on_table[self.selected[2]] = None
                if self.find_sets() == []:
                    self.game_end = True
        self.correct_set = False
        self.selected = []

    def pull3cards(self):
        '''
        Description:
        Pulls 3 random cards from the deck, deletes them from the deck and replaces the card's index from the selected.
        Parameters:
        None
        Limitations:
        Could be merged with replace_selection method.
        Structures:
        First checks if there are cards left in the deck, if so sets the game_end flag as True. Otherwise, picks a
        random card from the deck, places it on the table and deletes it from the deck. If there are no possible sets
        left, it calls pull12cards again and again until either there are no more cards left in the deck or a set is
        available.
        '''
        if self.num_cards_in_deck < 3 and self.find_sets() == []:
            ###### HANDLE END OF GAME #######
            self.game_end = True
        else:
            for iter_num in range(3):
                if not self.game_end:
                    key, value = random.choice(list(self.deck.items()))
                    self.cards_on_table[self.selected[iter_num]] = value
                    del self.deck[key]
                    self.num_cards_in_deck -= 1
        if self.find_sets() == []:
            ###### HANDLE NO MORE MATCHES ######
            print("No available matches, redistributing!")
            self.pull12cards() #after replacing the 3 cards, check whether the table has any valid SETs
    def pull12cards(self):
        '''
        Description:
        Pulls 12 random cards from the deck, deletes them from the deck and replaces the cards on the table. This method
        is called when the game first starts or there are no more available matches left. It calls itself recursively
        until there is a possible set.
        Parameters:
        None
        Limitations:
        When there are no possible sets left and this method is called, the only thing done is printing a message
        through the console (Which is actually done in handle_selection method.) A nice way to broadcast this to the
        players would be nice.
        Structures:
        First checks if there are at least 12 cards in the deck, if so sets the game_end flag as True. Otherwise, picks a
        random card from the deck, places it on the table and deletes it from the deck. If there are no possible sets
        left, calls itself again until either the cards in the deck goes lower than 12 or a set is available.
        Outputs:
        None
        '''
        if self.num_cards_in_deck < 12:
            ###### HANDLE END OF GAME #######
            self.game_end = True
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
                #print("No available matches, redistributing!")
                self.pull12cards()

    # This function returns the indices that form a set from the table.
    def find_sets(self):
        '''
        Description:
        Finds all available sets' indices and returns them in an 2-dimensional array. Returns no duplicates and checks
        each combination exactly once. (O(n3) complexity)
        Parameters:
        None, uses self.cards_on_table.
        Limitations:
        -
        Outputs:
        Returns a 2-dimensional array holding the indices of every possible set.
        '''
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
        '''
        Assigns values for the start of a selection. This is triggered when a player presses their button.
        '''
        self.selection_mode = True
        self.selected = []

    # Selects two cards of a set to display as hint
    def give_hint(self):
        '''
        Returns an available random set's 2 random cards' indices.
        '''
        sets = self.find_sets()
        if sets != []:
            set = random.choice(sets)
            hint = random.sample(set, 2)
        else:
            hint = False
        return hint
    # For the computer to find a set
    def give_set(self):
        '''
        Returns an available random set's indices.
        '''
        sets = self.find_sets()
        if sets != []:
            set = random.choice(sets)
        else:
            set = False
        return set

    def __repr__(self):
        '''
        Prints all the cards on the table in an order.
        '''
        message = str("")
        for index in range(len(self.cards_on_table)):
            message += "Card " + str(index) + ": " +self.cards_on_table[index].__repr__()
        return message

    def update(self):
        '''
        Delays replacing the cards on the table after a correct selection is made. This method is called continuously
        in the game loop.
        '''
        if not self.game_end and self.waiting_for_replace and pygame.time.get_ticks() >= self.replace_time:
            self.waiting_for_replace = False
            self.replace_selection()

# Looks at the first 2 cards and finds the required card to form a set. Compares the third card to the required card,
# if they are the same, returns True; otherwise, returns False.
def is_set(card1, card2, card3):
    '''
    Description:
    Checks if 3 cards form a set or not.
    Parameters:
    card1, card2, card3 -> Card objects
    Limitations:
    -
    Structures:
    In the game set, any combination of two cards has only one unique third card to make a set. This method looks at the
    first 2 cards and finds the required card. Later compares the required card with the third card.
    Output:
    If the required card and the third card matches, it returns True. Otherwise, it returns False.
    '''
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
#Debugging part, commented out for later use.
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