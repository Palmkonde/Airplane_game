""" modules that cotains All of interface in game """

from typing import Tuple

import pygame


class UserInterface:
    """Class that work to create UserInterface in game
    
    Attributes:
        screen (pygame.Surface): Surface of pygame
        title_font: font size 74 use for title
        menu_font: font size 48 use for menu
        hud_font: font size 36 use for othertext
    
    Medthods:
        draw_text(): draw a text
    """

    def __init__(self, screen: pygame.Surface) -> None:
        
        assert isinstance(screen, pygame.Surface), \
            f"screen should be pygame.Surface, but got {type(screen)}"

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
        """draw a text on screen
        
        Args:
            text (str): string that want to draw
            style (str): choose size of font according to attributes
            text_col (Tuple[int, int, int]): color of text in rgb
            pos (Tuple[float | int, float | int]): position of text
        
        Returns:
            None: nothing
        """
        assert isinstance(text, str), f"text should be str, but got {type(text)}"

        assert isinstance(style, str) and style in ["menu", "title", "hud"], \
            f"style should be str and Must be menu, titile or hud"

        assert isinstance(text_col, tuple) and \
                len(text_col) == 3 and \
                all(isinstance(c, int) for c in text_col), \
                    f"text_col should be Tuple[int, int, int], but got {type(text_col)}"

        font = None
        if style == "menu":
            font = self.__menu_font
        elif style == "title":
            font = self.__title_font
        elif style == "hud":
            font = self.__hud_font

        try:
            img = font.render(text, True, text_col)
            self.__screen.blit(img, pos)
        except Exception as e:
            print(f"Error to draw Text: {e}")
