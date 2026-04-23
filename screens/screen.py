class Screen:
    '''
    Description: A parent class for all screen classes.
    Parameters: Game object.
    '''
    def __init__(self, game):
        self.game = game

    def handle_event(self):
        pass

    def draw(self):
        pass