""" Interface in game """

import pygame
from typing import Tuple


class UserInterface:
    def __init__(self, screen: pygame.Surface) -> None:
        self.__screen = screen

        pygame.font.init()
        self.__title_font = pygame.font.Font(None, 74)
        self.__menu_font = pygame.font.Font(None, 48)
        self.__hud_font = pygame.font.Font(None, 36)

    def draw_text(self,
                  text: str,
                  style: str,
                  text_col: Tuple[int, int, int],
                  pos: Tuple[float | int, float | int]) -> None:

        if style == "menu":
            font = self.__menu_font
        elif style == "title":
            font = self.__title_font
        elif style == "hud":
            font = self.__hud_font

        img = font.render(text, True, text_col)
        self.__screen.blit(img, pos)
