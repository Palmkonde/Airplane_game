""" Some document here """

import math

from typing import Tuple
from baseairplane import Airplane
from abc import ABC, abstractmethod


class InterfaceCoin(ABC):
    @abstractmethod
    def get_color(self) -> Tuple[int, int, int]:
        pass


class Coin():
    """ Some document here """

    def __init__(self,
                 center: Tuple[int | float, int | float],
                 score: int,
                 radius: int | float) -> None:
        self.__center = center
        self.__score = score
        self.__radius = radius
        self._is_collected = False

    def is_colliding(self, other: Airplane) -> bool:
        distance = math.dist(self.get_center(), other.get_center())
        return distance < (self.get_radius())

    # Acess data
    def get_center(self) -> Tuple[int | float, int | float]:
        return self.__center

    def get_score(self) -> int:
        return self.__score

    def get_radius(self) -> int | float:
        return self.__radius

    def get_collected(self) -> bool:
        return self._is_collected


class NormalCoin(Coin, InterfaceCoin):
    YELLOW = (255, 222, 33)

    def __init__(self, center, score, radius):
        super().__init__(center, score, radius)

    def get_color(self) -> Tuple[int, int, int]:
        return self.YELLOW


class InvincibleCoin(Coin, InterfaceCoin):
    BLUE = (8, 143, 143)

    def __init__(self, center, score, radius):
        super().__init__(center, score, radius)
        self.effect = "invincible"

    def get_color(self) -> Tuple[int, int, int]:
        return self.BLUE

    def get_effect(self) -> str:
        return self.effect


class DeleteAllMissileCoin(Coin, InterfaceCoin):
    RED = (250, 128, 114)

    def __init__(self, center, score, radius):
        super().__init__(center, score, radius)
        self.effect = "BOOM"

    def get_effect(self) -> str:
        return self.effect

    def get_color(self) -> Tuple[int, int, int]:
        return self.RED


class CoinFactory:
    def create_coin(self, coin_type: str, center: Tuple[int, int], score: int, radius: int) -> Coin:
        """
        Factory method to create different types of coins.
        """
        coin_types = {
            'normal': NormalCoin,
            'invincible': InvincibleCoin,
            'delete_missile': DeleteAllMissileCoin
        }

        if coin_type not in coin_types:
            raise ValueError(f"Invalid coin type: {coin_type}")

        return coin_types[coin_type](center, score, radius)


# c = Coin((0, 0), 0, 0)
# d = NormalCoin((0, 0), 0, 0)
