""" Moudule that contains coin and factory that makes coin """

import math

from abc import ABC, abstractmethod
from typing import Tuple
from baseairplane import Airplane


class InterfaceCoin(ABC):
    """Interface of All Coin

    Every coin should implement get_color

    Medthods:
        get_color(): Abstract medthod that shoud return color of that object
    """
    @abstractmethod
    def get_color(self) -> Tuple[int, int, int]:
        """should get color of object"""


class Coin():
    """Main class that is a blueprint of many styles coin

    Attributes:
        center (Tuple[int | float, int | float]): The center position 
                                                  of the coin on the game map.
        score (int): The score value the coin provides when collected.
        radius (int | float): The radius of the coin, used for collision detection.
        _is_collected (bool): Whether the coin has been collected by the player.

    Methods:
        is_colliding(other): Checks if this coin is colliding with another object.
        set_collected(): set attributes is_collected
        get_center(): get the center coordinates of the coin.
        get_score(): get the score value of the coin.
        get_radius(): get the radius of the coin.
        get_collected(): Checks if the coin has been collected.
    """

    def __init__(self,
                 center: Tuple[int | float, int | float],
                 score: int,
                 radius: int | float) -> None:
        assert isinstance(center, tuple) \
                and len(center) == 2 \
                and all(isinstance(c, (int, float)) for c in center), \
                    f"center should be Tuple[int|float, int|float], but got {type(center)}"
        
        assert isinstance(score, int), \
            f"score should be int, but got {type(score)}"

        assert isinstance(radius, (int, float)), \
            f"radius should be int or float, but got {tpye(radius)}"

        self.__center = center
        self.__score = score
        self.__radius = radius
        self._is_collected = False

    def is_colliding(self, other: Airplane) -> bool:
        """Check that `this` object collding with another object or not

        Args:
            other (Airplane): object that we want to check with
        Returns:
            bool: `True` if it is collding `False` if it doesn't
        """
        assert isinstance(other, Airplane), \
            f"other should be Airplane, but got {type(other)}"

        # Calculate that distance of objects center is in radius
        distance = math.dist(self.get_center(), other.get_center())
        return distance < (self.get_radius())

    # Acess data
    def set_is_collected(self, state: bool) -> None:
        """set attributes is collected

        Args:
            state (bool): True or False

        Returns:
            None: nothing
        """
        self._is_collected = state

    def get_center(self) -> Tuple[int | float, int | float]:
        """get the center of object

        Returns:
            Tuple[int | float, int | float]: The center coordinates of the coin.
        """
        return self.__center

    def get_score(self) -> int:
        """get the score value of the coin.

        Returns:
            int: The score value the coin provides.
        """
        return self.__score

    def get_radius(self) -> int | float:
        """get the radius of the coin.

        Returns:
            int | float: The radius of the coin.
        """

        return self.__radius

    def get_collected(self) -> bool:
        """Checks if the coin has been collected.

        Returns:
            bool: `True` if the coin has been collected, `False` it doesn't.
        """
        return self._is_collected


class NormalCoin(Coin, InterfaceCoin):
    """Normal color that has only color

    Attributes:
        YELLOW  (Tuple[int, int, int]): Color Yellow

    Medthods:
        get_color(): return color of this object
    """
    YELLOW = (255, 222, 33)

    def get_color(self) -> Tuple[int, int, int]:
        """get color

        Returns:
            Tuple[int, int, int]: RGB color of this coin
        """
        return self.YELLOW


class InvincibleCoin(Coin, InterfaceCoin):
    """A coin type that has Blue color and effect called "invincible"

    Attributes:
        BLUE (Tuple[int, int, int]): RGB of blue

    Medthods:
        get_color(): return color of this object
        get_effect(): return effect of this Coin
    """
    BLUE = (8, 143, 143)

    def __init__(self, center, score, radius):
        super().__init__(center, score, radius)
        self.effect = "invincible"

    def get_color(self) -> Tuple[int, int, int]:
        """Get color of this objec

        Returns:
            Tuple[int, int, int]: RBG of this object 
        """
        return self.BLUE

    def get_effect(self) -> str:
        """get effect what is this object do

        Returns:
            str: "invincible"
        """
        return self.effect


class DeleteAllMissileCoin(Coin, InterfaceCoin):
    """A coin type that has a red color and effect BOOM

    Attributes:
        RED (Tuple[int, int, int]): color of this object

    Medthods:
        get_effect(): effect of this medthod
        get_color(): get_color of this medthod
    """
    RED = (250, 128, 114)

    def __init__(self, center, score, radius):
        super().__init__(center, score, radius)
        self.effect = "BOOM"

    def get_effect(self) -> str:
        """get effect what is this object do

        Returns:
            str: "BOOM"
        """
        return self.effect

    def get_color(self) -> Tuple[int, int, int]:
        """Get color of this objec

        Returns:
            Tuple[int, int, int]: RBG of this object 
        """
        return self.RED


class CoinFactory:
    """Using Factory Pattern design to create different type of Coin

    Medthods:
        create_coin(): Create object coin in different type
    """

    def create_coin(self,
                    coin_type: str,
                    center: Tuple[int, int],
                    score: int,
                    radius: int) -> Coin:
        """
        Factory method to create different types of coins.

        Args:
            coin_type (str): type of coin we want to create
            center (Tuple[int, int]): center of coin
            score (int): score of this coin
            radius (int): radius of coin 

        Returns:
            Coin: Object that create from this factory
        """
        assert isinstance(coin_type, str), \
            f"coin_type should be str, but got {type(coin_type)}"

        assert isinstance(center, tuple) \
                and len(center) == 2 \
                and all(isinstance(c, int) for c in center), \
                    f"center should be Tuple[int, int], but got {type(center)}"

        coin_types = {
            'normal': NormalCoin,
            'invincible': InvincibleCoin,
            'delete_missile': DeleteAllMissileCoin
        }

        if coin_type not in coin_types:
            raise ValueError(f"Invalid coin type: {coin_type}")

        return coin_types[coin_type](center, score, radius)
