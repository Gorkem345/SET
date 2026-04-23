class Screen:
    '''
    Description: A base class for all screen classes.
    Parameters: Game object.
    Limitations: No real functionality.
    Structures: Every screen has the same game object.
    Outputs: A base screen class that is related to the game object.
    '''
    def __init__(self, game):
        self.game = game

    def handle_event(self):
        pass

    def draw(self):
        pass