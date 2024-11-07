""" Final project -> intro_to_python 2 """

import pygame
import random
import json
import os

from typing import List
from baseairplane import Airplane, Missile
from interface import UserInterface
from coin import NormalCoin, Coin, InvincibleCoin, DeleteAllMissileCoin

"""
TODO List
    - *Adjust speed and turn_rate for both missiles and airplane
    - reset
    - Optimize

    - Some objects to boost or increase score
                    immortal for seconds

    Important
        - add at least one decorator
            - Special Coin that can immortal and increase score

        - Look other design pattern
"""


class Game:
    """ TODO: Document Here """

    # Color
    WHITE = (255, 255, 255)
    BLUE = (0, 255, 255)
    RED = (250, 128, 114)
    BLACK = (0, 0, 0)
    YELLOW = (255, 222, 33)

    # Constant value
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    DISPLAY_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

    # Missile generation constant
    MISSILE_SPAWN_TIME = 4  # Seconds between spawns
    MAX_MISSILES = 3
    SPAWN_POSITION = [
        (0, 0),
        (SCREEN_WIDTH, 0),
        (0, SCREEN_HEIGHT),
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    ]

    # Constant for Airplane
    AIRPLANE_SIZE = 8
    AIRPLANE_SPEED = 10
    AIRPLANE_ROTATION_ANGLE = 7.0
    AIRPLANE_EFFECT_TIME = 3

    # Constant for Missile
    MISSILE_SIZE = 5
    MISSILE_SPEED = 7
    MISSILE_ACCELERATION = 0.5
    MISSILE_MAX_SPEED = 10

    # Constant for Coin
    COIN_SPAWN_TIME = 4
    COIN_SCORE = 5
    COIN_RADIUS = 15

    def __init__(self) -> None:
        # Game setup
        self.screen = pygame.display.set_mode(self.DISPLAY_SIZE)
        self.clock = pygame.time.Clock()

        # Main object
        self.missiles = []
        self.player = None
        self.coin = []

        # State
        self.last_spawn_misslie = 0
        self.last_spawn_coin = 0
        self.last_num = 0
        self.high_score = 0
        self.score = 0
        self.state = "menu"
        self.running = True
        self.player_effect = ""

        # Simple Text UI
        self.ui = UserInterface(self.screen)

    # Set data
    def set_player(self, player: Airplane) -> None:
        self.player = player

    def set_missiles(self, missiles: List[Missile]) -> None:
        self.missiles = missiles

    def set_coin(self, coin: List[Coin]) -> None:
        self.coin = coin

    def run_main(self) -> None:

        self.load_high_score()

        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            dt = self.clock.tick(60) / 1000.0  # 60 FPS

            self.screen.fill(self.WHITE)
            key = pygame.key.get_pressed()

            # TODO: Menu, State, Died
            if self.state == "menu":

                self.ui.draw_text("Airplane", "title", self.BLACK,
                                  (self.SCREEN_WIDTH/2 - 100, self.SCREEN_HEIGHT/5))

                self.ui.draw_text("Press P to start", "menu", self.BLACK,
                                  (self.SCREEN_WIDTH/2 - 125, self.SCREEN_HEIGHT/2 + 100))

                if key[pygame.K_p]:
                    self.state = "playing"

                    # set new time
                    self.last_spawn_missile = pygame.time.get_ticks() / 1000
                    self.last_spwan_coin = pygame.time.get_ticks() / 1000

            elif self.state == "playing":
                if key[pygame.K_d]:
                    self.player.rotation_points(self.AIRPLANE_ROTATION_ANGLE)
                elif key[pygame.K_a]:
                    self.player.rotation_points(-self.AIRPLANE_ROTATION_ANGLE)

                self.ui.draw_text(f"score: {self.score}", "hud", self.BLACK,
                                  (0, 0))

                self.spwan_missiles()
                self.spawn_coin()
                self.update_positions(dt)
                self.check_colision()
                self.increase_score_misslie()
                self.draw()

            elif self.state == "died":
                self.ui.draw_text("You died!", "title", self.RED,
                                  (self.SCREEN_WIDTH/2 - 125, 100))

                self.ui.draw_text(f"Your score is: {self.score - 1}", "hud", self.BLACK,
                                  (self.SCREEN_WIDTH/2 - 100, self.SCREEN_HEIGHT/2))

                self.ui.draw_text(f"Your high score is: {self.high_score}", "hud", self.BLACK,
                                  (self.SCREEN_WIDTH/2 - 125, self.SCREEN_HEIGHT/2 + 50))

                self.ui.draw_text(f"Press R to restart", "hud", self.BLACK,
                                  (self.SCREEN_WIDTH/2 - 100, self.SCREEN_HEIGHT/2 + 100))

                self.high_score = max(self.high_score, self.score)

                if key[pygame.K_r]:
                    self.reset()

            if not self.player.get_alive():
                self.state = "died"

            # Update display
            pygame.display.update()

        self.save_high_score()
        pygame.quit()

    def reset(self) -> None:
        """ TODO: Document and reset """
        self.state = "menu"
        self.player._is_alive = True
        self.score = 0

        self.set_missiles([])
        self.set_coin([])
        self.set_player(Airplane(
                        size=self.AIRPLANE_SIZE,
                        center=(self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2),
                        speed=self.AIRPLANE_SPEED))

        # set new time
        self.last_num = 0
        self.last_spawn_missile = pygame.time.get_ticks() / 1000
        self.last_spwan_coin = pygame.time.get_ticks() / 1000

    def update_positions(self, dt: float) -> None:

        # Handling error
        if not self.player:
            return

        self.player.move_forward()

        for m in self.missiles:
            try:
                m.rotation_to_target(self.player)
                m.update(dt)
            except Exception as e:
                print(f"Error updating missile: {e}")

    def draw(self) -> None:

        if not self.player:
            return

        # Draw player
        try:
            if not self.player._is_alive:
                return

            if self.player_effect == "invincible":
                pygame.draw.polygon(self.screen,
                                    self.YELLOW,
                                    self.player.get_points())

            else:
                pygame.draw.polygon(self.screen,
                                    self.BLUE,
                                    self.player.get_points())
        except Exception as e:
            print(f"Error drwing player: {e}")

        # Draw missiles
        for m in self.missiles:
            try:
                if not m._is_alive:
                    continue

                pygame.draw.polygon(self.screen, self.RED,  m.get_points())
            except Exception as e:
                print(f"Error drawing missile: {e}")

        # Draw Coin
        for c in self.coin:
            try:
                if c._is_collected:
                    continue

                pygame.draw.circle(self.screen,
                                   c.get_color(),
                                   c.get_center(),
                                   c.get_radius())

            except Exception as e:
                print(f"Error drawing coin: {e}")

        pygame.display.update()

    def check_colision(self) -> None:
        if not self.player:
            return

        for m in self.missiles:
            if self.player_effect == "invincible":
                self.reset_effect_time()
                continue

            elif self.player.is_colliding(m):
                self.player._is_alive = False
                m._is_alive = False

        for i in range(len(self.missiles)):
            for j in range(i+1, len(self.missiles)):
                if self.missiles[i].is_colliding(self.missiles[j]):
                    self.missiles[i]._is_alive = False
                    self.missiles[j]._is_alive = False

        for c in self.coin:
            if c.is_colliding(self.player):
                c._is_collected = True
                self.score += c.get_score()

                try:
                    effect = c.get_effect()

                    if effect == "invincible":
                        self.player_effect = effect
                        self.effect_time_start = pygame.time.get_ticks() / 1000

                    elif effect == "BOOM":
                        self.set_missiles([])

                except Exception as e:
                    print("this Object has no effect")

        self.missiles = [m for m in self.missiles if m.get_alive()]
        self.coin = [c for c in self.coin if not c.get_collected()]

    def spwan_missiles(self) -> None:
        """ Generate new missiles at random """
        current_time = pygame.time.get_ticks() / 1000  # Convert ms to s

        if current_time - self.last_spawn_missile >= self.MISSILE_SPAWN_TIME:

            num_new_missiles = random.randint(2, self.MAX_MISSILES)

            spawn_postions = random.sample(
                self.SPAWN_POSITION, num_new_missiles)

            for pos in spawn_postions:
                new_missile = Missile(
                    size=self.MISSILE_SIZE,
                    center=pos,
                    speed=self.MISSILE_SPEED,
                    acceleration=self.MISSILE_ACCELERATION,
                    max_speed=self.MISSILE_MAX_SPEED
                )
                self.missiles.append(new_missile)

            self.last_num = num_new_missiles
            self.last_spawn_missile = current_time

    def increase_score_misslie(self) -> None:
        current_num = len(self.missiles)

        if current_num < self.last_num:
            self.score += self.last_num - len(self.missiles)
            self.last_num = current_num

    def spawn_coin(self) -> None:
        current_time = pygame.time.get_ticks() / 1000  # Convert ms to s

        all_type = [NormalCoin, InvincibleCoin, DeleteAllMissileCoin]
        weight = [0.6, 0.3, 0.1]

        # TODO: score and radius and random type of Coin
        if current_time - self.last_spawn_coin >= self.COIN_SPAWN_TIME:

            spawn_area = (
                (10, 10),
                (self.SCREEN_WIDTH - 10, self.SCREEN_HEIGHT - 10)
            )

            rand_obj = random.choice(all_type)
            rand_x = random.randint(spawn_area[0][0], spawn_area[1][0])
            rand_y = random.randint(spawn_area[0][1], spawn_area[1][1])

            self.coin.append(rand_obj(
                center=(rand_x, rand_y),
                score=self.COIN_SCORE,
                radius=self.COIN_RADIUS
            ))
            self.last_spawn_coin = current_time

    def save_high_score(self) -> None:
        with open(r"./score.json", "w", encoding="utf-8") as file:
            data = {
                "high_score": self.high_score
            }

            json.dump(data, file)

    def load_high_score(self) -> None:

        file_path = "./score.json"
        data = {}

        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.high_score = data["high_score"]

    def reset_effect_time(self) -> None:
        current_time = pygame.time.get_ticks() / 1000

        if current_time - self.effect_time_start >= self.AIRPLANE_EFFECT_TIME:
            self.player_effect = ""
            self.effect_time_start = current_time


# main function
if __name__ == "__main__":

    pygame.init()
    pygame.display.set_caption("Airplane")
    game = Game()

    # Create player in center of screen
    airplane = Airplane(size=game.AIRPLANE_SIZE,
                        center=(game.SCREEN_WIDTH/2, game.SCREEN_HEIGHT/2),
                        speed=game.AIRPLANE_SPEED)

    # Create Test Missile
    m1 = Missile(size=game.MISSILE_SIZE,
                 center=(100, 100),
                 speed=game.MISSILE_SPEED,
                 acceleration=game.MISSILE_ACCELERATION,
                 max_speed=game.MISSILE_MAX_SPEED)

    game.set_player(airplane)

    # for testing
    game.set_missiles([m1])
    game.run_main()
