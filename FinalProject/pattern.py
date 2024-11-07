"""
This module contains decorators and design patterns implementations
for the game components.
"""
from typing import Callable, Any, Dict
from functools import wraps
import time
from coin import Coin, NormalCoin, InvincibleCoin, DeleteAllMissileCoin


def log_coin_collection(func: Callable) -> Callable:
    """
    A decorator that logs when coins are collected and their effects.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result:
            try:
                coin = kwargs.get('coin', None)
                if coin and hasattr(coin, 'get_score'):
                    score = coin.get_score()
                    effect = getattr(coin, 'effect', 'normal')
                    print(f"Collected coin worth {score} points with effect: {effect}")
                    print(f"Collection time: {time.strftime('%H:%M:%S')}")
            except Exception as e:
                print(f"Error logging coin collection: {e}")
        return result
    return wrapper


# Singleton Pattern for Game State
class GameState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameState, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        self.score = 0
        self.high_score = 0
        self.player_effect = ""
        self.effect_start_time = 0

    def update_score(self, points: int) -> None:
        self.score += points
        self.high_score = max(self.high_score, self.score)


# Factory Pattern for Coin Creation
class CoinFactory:
    @staticmethod
    def create_coin(coin_type: str, center: tuple, score: int, radius: int) -> Coin:
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


# Observer Pattern for Game Events
class GameEventManager:
    _observers: Dict[str, list] = {
        'coin_collected': [],
        'missile_destroyed': [],
        'player_died': []
    }

    @classmethod
    def subscribe(cls, event_type: str, observer: Callable) -> None:
        if event_type in cls._observers:
            cls._observers[event_type].append(observer)

    @classmethod
    def notify(cls, event_type: str, data: Any = None) -> None:
        if event_type in cls._observers:
            for observer in cls._observers[event_type]:
                try:
                    observer(data)
                except Exception as e:
                    print(f"Error notifying observer: {e}")


# Strategy Pattern for Different Game Difficulties
class DifficultyStrategy:
    def adjust_game_parameters(self, game) -> None:
        pass


class EasyDifficulty(DifficultyStrategy):
    def adjust_game_parameters(self, game) -> None:
        game.MISSILE_SPAWN_TIME = 5
        game.MAX_MISSILES = 2
        game.MISSILE_SPEED = 5


class HardDifficulty(DifficultyStrategy):
    def adjust_game_parameters(self, game) -> None:
        game.MISSILE_SPAWN_TIME = 3
        game.MAX_MISSILES = 4
        game.MISSILE_SPEED = 9
