import pygame
from utils.constants import WHITE, DARK, LIGHT
from screens.TableDisplay import Display_board
from utils.set_table import Table
from screens.screen import Screen

class PlayScreen(Screen):
    def __init__(self, game):
        super().__init__(game)