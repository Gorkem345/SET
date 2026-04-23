'''
Description:
Create a dictionary to store the indexing info of each cards
so that the game can call and show each cards by slicing and
retrieve the certain part of the cover.png
without creating 81 cards images individually,
which reduce the computational memory and increase the loading speed

class Card is the blueprint of creating one card from the cover.png, storing the attribute of each card
dictionary card store all 81 Card objects, using the card ID as the key
and assign the coordinates of each card in the image to each card
'''

'''
******Rules for Cards Indexing******

FILLING
empty -> e
semi-filled -> s
filled -> f

COLOR:
red -> r
purple -> p
green -> g

SHAPE:
circle -> c
diamond -> d
squash -> s

COUNT:
1 -> 1
2 -> 2
3 -> 3

Example id: empty red circle 1 -> erc1
'''


class Card:
    '''
    Description:
    Represents a single SET game card, parsing and storing its visual attributes (filling, color, shape, count) based
    on a 4-character ID. It also holds the spatial pixel coordinates to locate the specific card image on the main
    sprite sheet (cover.png).
    Parameters:
    id (str): A 4-character string defining the card's properties based on the indexing rules.
    Limitations:
    The 'id' parameter must strictly adhere to the predefined 4-character format and character set.
    The class lacks built-in validation to ensure the parsed ID is a valid id or that the coordinates fall within the
    actual bounds of the source image.
    Structures:
    Public string attributes for traits: 'filling', 'color', 'shape', and 'count'.
    Private list attribute _coordinates (managed via @property getter/setter methods) to store the spatial data
    as [x_start, y_start, width, height].
    Outputs:
    An instantiated `Card` object containing its parsed attributes and a default '_coordinates' list of [0, 0, 0, 0]
    until updated using the set method.
    '''
    def __init__(self, id):
        '''
        Builds the card from id(str)
        '''
        self._coordinates = [0,0,0,0] #Temporary coordinate value.
        self.filling = id[0]
        self.color = id[1]
        self.shape = id[2]
        self.count = id[3]

    @property #with this, when do card.coordinates, it actually does card.coordinates()
              #a method behave like a normal variable
    def coordinates(self):
        '''
        Getter for coordinates
        '''
        return self._coordinates #e.g. card.coordinates = [13, 11, 178, 115]

    @coordinates.setter
    def coordinates(self, value):
        '''
        Setter for coordinates
        Parameters:
        value (list): list of coordinates -> [x_start, y_start, width, length]
        '''
        self._coordinates = value

    #Set the coordinates of the card
    def set(self, x, y, width, height):
        '''
        Calls the setter for coordinates
        Parameters:
        value (list): list of coordinates -> [x_start, y_start, width, length]
        '''
        self.coordinates = [x,y,width,height]

    #rebuild the card ID from its attributes into a string
    def get_id(self):
        '''
        Rebuilds the id string from attributes of the card.
        '''
        return str(self.filling) + str(self.color) + str(self.shape) + str(self.count)

    #define the outprint pattern when print a card, for debugging
    def __repr__(self):
        '''
        Used to print the card object
        '''
        return str("Coordinates: ") + str(self.coordinates) + str(" / ID: ") + str(self.filling) + str(self.color) + str(self.shape) + str(self.count) + "\n"

#Create a card dictionary for store and to be called and used in the game
cards = {}

#9×9 grid of all 81 card ID, same as cover.png layout
ids = [
    ["epc2", "fgs2", "srd2", "frs1", "spd1", "egc1", "sgd3", "erc3", "fps3"],
    ["ers3", "fpd3", "sgc3", "fgd2", "src2", "eps2", "spc1", "egs1", "frd1"],
    ["egd1", "frc1", "sps1", "fpc3", "sgs3", "erd3", "srs2", "epd2", "fgc2"],
    ["sgd1", "erc1", "fps1", "epc3", "fgs3", "srd3", "frs2", "spd2", "egc2"],
    ["spc2", "egs2", "frd2", "ers1", "fpd1", "sgc1", "fgd3", "src3", "eps3"],
    ["srs3", "epd3", "fgc3", "egd2", "frc2", "sps2", "fpc1", "sgs1", "erd1"],
    ["frs3", "spd3", "egc3", "sgd2", "erc2", "fps2", "epc1", "fgs1", "srd1"],
    ["fgd1", "src1", "eps1", "spc3", "egs3", "frd3", "ers2", "fpd2", "sgc2"],
    ["fpc2", "sgs2", "erd2", "srs1", "epd1", "fgc1", "egd3", "frc3", "sps3"]
]

#Every card image on the sheet has the same size
card_width = 178
card_height = 115

#This is coordinates of the top-left corner of the first card in the cover.png.
x_cor = 13
y_cor = 11

#loop over one by one, start from the first column of the first row
#follow the pattern seen on the image
for row in range(9):
    for col in range(9):
        cards[ids[row][col]] = Card(ids[row][col]) #now in cards dictionary, {epc2: Card('epc2)}
        cards[ids[row][col]].set(x_cor, y_cor, card_width, card_height) #call the set() function
                                                                        #give the card object a coordinate
        x_cor = x_cor + card_width #move to next column
        if col % 3 == 2 and col != 0: #when col = 2, 5, 8, every 3rd column
            x_cor += 47 #jump over the gap between sets
        else:
            x_cor += 16 ##jump over the gap between cards

    x_cor = 13 #after finishing one row, reset the initial coordinate
    y_cor += 115 #move to next row
    if row % 3 == 2 and row != 0: #when col = 2, 5, 8, every 3rd row
        y_cor += 63 #jump over the gap between sets vertically
    else:
        y_cor += 27 #jump over the gap between cards vertically


#Debug dictionary
#print(cards)