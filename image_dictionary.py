#Create a dictionary and a class for cards, link the Card instances to the coordinates of the image
#to retrieve the intended part of the image
#Import cards from this file (image_dictionary) to have all 81 cards with their images. To use the images, upload the
#images/cover.png and use the coordinates attribute to get that single card's image.
#Ex:
#sheet = pygame.image.load("images/cover.png").convert()
#card_rect = pygame.Rect(dict[id].coordinates[0], dict[id].coordinates[1], card_width, card_height) #Coordinates
#first_card = sheet.subsurface(card_rect) #Subsurface the needed part of the image
#first_card = pygame.transform.scale(first_card, (card_width*2, card_height*2)) #Scale the image as needed

# A class to represent the cards of the SET game
'''
******Rules for Indexing******

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
    def __init__(self, id):
        self._coordinates = [0,0,0,0] #Temporary coordinate value.
        self.filling = id[0]
        self.color = id[1]
        self.shape = id[2]
        self.count = id[3]

    @property
    def coordinates(self):
        return self._coordinates

    @coordinates.setter
    def coordinates(self, value):
        self._coordinates = value

    #Set the coordinates of the card
    def set(self, x, y, width, height):
        self.coordinates = [x,y,width,height]

    def get_id(self):
        return str(self.filling) + str(self.color) + str(self.shape) + str(self.count)

    def __repr__(self):
        return str("Coordinates: ") + str(self.coordinates) + str(" / ID: ") + str(self.filling) + str(self.color) + str(self.shape) + str(self.count) + "\n"


# Create a dictionary to store the cards
cards = {}

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

# Found the pattern to get the coordinates of each card
card_width = 178
card_height = 115

x_cor = 13
y_cor = 11

for row in range(9):
    for col in range(9):
        cards[ids[row][col]] = Card(ids[row][col])
        cards[ids[row][col]].set(x_cor, y_cor, card_width, card_height)
        x_cor = x_cor + card_width
        if col % 3 == 2 and col != 0:
            x_cor += 47
        else:
            x_cor += 16

    x_cor = 13
    y_cor += 115
    if row % 3 == 2 and row != 0:
        y_cor += 63
    else:
        y_cor += 27


#Debug dictionary
print(cards)