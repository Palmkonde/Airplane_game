"""Final project -> intro_to_python 2 

"""

import random
import json
import os
from typing import List

import pygame
from baseairplane import Airplane, Missile
from interface import UserInterface
from coin import Coin, CoinFactory


class Game:
    """The Game is the main loop of game. it contains a lot of logical of this game behind of it

    Attributes:
        WHITE, BLUE, RED, BLACK, YELLOW (tuple): Color constants for drawing.
        SCREEN_WIDTH (int): Width of the game screen.
        SCREEN_HEIGHT (int): Height of the game screen.
        DISPLAY_SIZE (tuple): Screen dimensions as a tuple of width and height.
        MISSILE_SPAWN_TIME (int): Time interval (in seconds) between missile spawns.
        MAX_MISSILES (int): Maximum number of missiles allowed on screen.
        SPAWN_POSITION (list of tuples): Predefined missile spawn positions around the screen.
        AIRPLANE_SIZE (int): Size of the player's airplane.
        AIRPLANE_SPEED (int): Speed of the airplane.
        AIRPLANE_ROTATION_ANGLE (int): Angle (in degrees) the airplane rotates per input.
        AIRPLANE_EFFECT_TIME (int): Duration for which temporary effects last on the airplane.
        MISSILE_SIZE (int): Size of each missile.
        MISSILE_SPEED (int): Starting speed of missiles.
        MISSILE_ACCELERATION (float): Rate at which missile speed increases.
        MISSILE_MAX_SPEED (float): Maximum speed a missile can achieve.
        MISSLIE_MAX_TURN_RATE (int): Maximum rate (in degrees) at which a missile can turn.
        COIN_SPAWN_TIME (int): Time interval (in seconds) between coin spawns.
        COIN_SCORE (int): Score increment for collecting a coin.
        COIN_RADIUS (int): Radius of each coin.

    Methods:
        set_player(player): Sets the player (Airplane) object.
        set_missiles(missiles): Sets the list of missiles in the game.
        set_coin(coin): Sets the list of coins in the game.
        run_main(): Runs the main game loop, updating the screen and handling inputs.
        reset(): Resets the game state after the player dies, preparing for a new session.
        update_positions(dt): Updates the positions of player and missiles based on elapsed time.
        draw(): Draws the player, missiles, and coins onto the screen.
        check_collision(): Checks for collisions between the player, missiles, and coins.
        spwan_missiles(): Spawns new missiles at random positions if the spawn interval has passed.
        increase_score_misslie(): Increases the score based on missile count changes.
        spawn_coin(): Spawns a coin of a random type at a random position if the spawn interval has passed.
        save_high_score(): Saves the current high score to a JSON file.
        load_high_score(): Loads the high score from a JSON file.
        reset_effect_time(): Resets temporary player effects if the effect duration has ended.
    """

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
    MAX_MISSILES = 4
    SPAWN_POSITION = [
        (0, 0),
        (SCREEN_WIDTH, 0),
        (0, SCREEN_HEIGHT),
        (SCREEN_WIDTH, SCREEN_HEIGHT),
        (SCREEN_WIDTH/2, 0),
        (SCREEN_WIDTH/2, SCREEN_HEIGHT),
        (0, SCREEN_HEIGHT/2),
        (SCREEN_WIDTH, SCREEN_HEIGHT/2)
    ]

    # Constant for Airplane
    AIRPLANE_SIZE = 8
    AIRPLANE_SPEED = 6
    AIRPLANE_ROTATION_ANGLE = 7  # degrees
    AIRPLANE_EFFECT_TIME = 3

    # Constant for Missile
    MISSILE_SIZE = 5
    MISSILE_SPEED = 5
    MISSILE_ACCELERATION = 0.2
    MISSILE_MAX_SPEED = 6.5
    MISSLIE_MAX_TURN_RATE = 3.5  # degrees

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

        # Factory
        self.coin_factory = CoinFactory()

        # State
        self.last_spawn_missile = 0
        self.last_spawn_coin = 0
        self.last_num = 0
        self.high_score = 0
        self.score = 0
        self.state = "menu"
        self.running = True
        self.player_effect = ""
        self.effect_time_start = 0

        # Simple Text UI
        self.ui = UserInterface(self.screen)

    # Set data
    def set_player(self, player: Airplane) -> None:
        """set player of this game

        Args:
            player (Airplane): The airplane object representing the player
        """
        assert isinstance(player, Airplane), \
            f"player should be Airplane, but got {type(player)}"

        self.player = player

    def set_missiles(self, missiles: List[Missile]) -> None:
        """
        Sets the list of missiles in the game.

        Args:
            missiles (List[Missile]): A list of Missile objects in the game.
        """
        assert isinstance(missiles, list) and \
            all(isinstance(m, Missile) for m in missiles), \
            f"missiles should be List[Missile], but got {type(missiles)}"
        self.missiles = missiles

    def set_coin(self, coins: List[Coin]) -> None:
        """Sets the list of coins in the game.

        Args:
            coin (List[Coin]): A list of Coin objects in the game.
        """
        assert isinstance(coins, list) and \
            all(isinstance(c, Coin) for c in coins), \
            f"Coin should be List[Coin], but got {type(coins)}"
        self.coin = coins

    def run_main(self) -> None:
        """Run main game loop"""

        # Load Latest high_score
        self.load_high_score()

        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # get different in frame
            dt = self.clock.tick(60) / 1000.0  # 60 FPS

            self.screen.fill(self.WHITE)

            # get key from player
            key = pygame.key.get_pressed()

            # if player died always change state to died
            if not self.player.get_alive():
                self.state = "died"

            # State menu
            if self.state == "menu":

                # draw text
                self.ui.draw_text("Airplane", "title", self.BLACK,
                                  (self.SCREEN_WIDTH/2 - 100, self.SCREEN_HEIGHT/5))

                self.ui.draw_text("Press P to start", "menu", self.BLACK,
                                  (self.SCREEN_WIDTH/2 - 125, self.SCREEN_HEIGHT/2 + 100))

                # When player press P and change to new state
                if key[pygame.K_p]:
                    self.state = "playing"

                    # set time
                    self.last_spawn_missile = pygame.time.get_ticks() / 1000
                    self.last_spawn_coin = pygame.time.get_ticks() / 1000

            # playing state
            elif self.state == "playing":

                # chceck input whether a or d
                if key[pygame.K_d]:
                    self.player.rotation_points(self.AIRPLANE_ROTATION_ANGLE)
                elif key[pygame.K_a]:
                    self.player.rotation_points(-self.AIRPLANE_ROTATION_ANGLE)

                self.ui.draw_text(f"score: {self.score}", "hud", self.BLACK,
                                  (0, 0))

                # update all of object in game
                self.spwan_missiles()
                self.spawn_coin()
                self.update_positions(dt)
                self.check_colision()
                self.increase_score_misslie()
                self.draw()

            # State Died
            elif self.state == "died":

                # Draw texts
                self.ui.draw_text("You died!", "title", self.RED,
                                  (self.SCREEN_WIDTH/2 - 125, 100))

                self.ui.draw_text(f"Your score is: {self.score - 1}", "hud", self.BLACK,
                                  (self.SCREEN_WIDTH/2 - 100, self.SCREEN_HEIGHT/2))

                self.ui.draw_text(f"Your high score is: {self.high_score}", "hud", self.BLACK,
                                  (self.SCREEN_WIDTH/2 - 125, self.SCREEN_HEIGHT/2 + 50))

                self.ui.draw_text("Press R to restart", "hud", self.BLACK,
                                  (self.SCREEN_WIDTH/2 - 100, self.SCREEN_HEIGHT/2 + 100))

                self.high_score = max(self.high_score, self.score - 1)

                # Check player preesed R
                if key[pygame.K_r]:
                    self.reset()

            # Update display
            pygame.display.update()

        # Save_score before quit
        self.save_high_score()
        pygame.quit()

    def reset(self) -> None:
        """Resets the game state after the player dies."""
        self.state = "menu"
        self.player.set_is_alive(True)
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
        self.last_spawn_coin = pygame.time.get_ticks() / 1000

    def update_positions(self, dt: float) -> None:
        """Updates the positions of the player and missiles based on 
        the elapsed time since the last frame.

        Args:
            dt (float): The delta time (in seconds) since the last frame update.
        """
        assert isinstance(dt, float), f"dt should be float, but got {type(dt)}"

        # cannot find object player
        if not self.player:
            return

        # Player need no argument
        self.player.move_forward()

        # Update every missiles need dt for acceleration
        for m in self.missiles:
            try:
                m.rotation_to_target(self.player)
                m.update(dt)
            except Exception as e:
                print(f"Error updating missile: {e}")

    def draw(self) -> None:
        """Draws the player, missiles, and coins onto the screen"""
        if not self.player:
            return

        # Draw player
        try:
            if not self.player.get_alive():
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
                if not m.get_alive():
                    continue

                pygame.draw.polygon(self.screen, self.RED,  m.get_points())
            except Exception as e:
                print(f"Error drawing missile: {e}")

        # Draw Coin
        for c in self.coin:
            try:
                if c.get_collected():
                    continue

                pygame.draw.circle(self.screen,
                                   c.get_color(),
                                   c.get_center(),
                                   c.get_radius())

            except Exception as e:
                print(f"Error drawing coin: {e}")

        pygame.display.update()

    def check_colision(self) -> None:
        """Checks for collisions between the player, missiles, and coins."""
        if not self.player:
            return

        # Checking for missiles collding to player
        for m in self.missiles:

            # Player is invincing. So, missiles can go through player
            if self.player_effect == "invincible":
                self.reset_effect_time()
                continue

            elif self.player.is_colliding(m):
                self.player.set_is_alive(False)
                m.set_is_alive(False)

        # Checking for missile collding to themself
        for i in range(len(self.missiles)):
            for j in range(i+1, len(self.missiles)):
                if self.missiles[i].is_colliding(self.missiles[j]):
                    self.missiles[i].set_is_alive(False)
                    self.missiles[j].set_is_alive(False)

        # Checking that coin collding to player
        # We can't check player.is_collding(coin)
        # Because Coin is circle and bound box is different from Airplane
        for c in self.coin:
            if c.is_colliding(self.player):
                c.set_is_collected(True)
                self.score += c.get_score()

                # Check that coin is not a normal coin
                if hasattr(c, "get_effect"):
                    effect = c.get_effect()

                    if effect == "invincible":
                        self.player_effect = effect
                        self.effect_time_start = pygame.time.get_ticks() / 1000

                    elif effect == "BOOM":
                        self.set_missiles([])

        # Update current missiles and coin
        self.missiles = [m for m in self.missiles if m.get_alive()]
        self.coin = [c for c in self.coin if not c.get_collected()]

    def spwan_missiles(self) -> None:
        """Spawns new missiles at random positions"""
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
                    max_speed=self.MISSILE_MAX_SPEED,
                    max_turn_rate=self.MISSLIE_MAX_TURN_RATE
                )
                self.missiles.append(new_missile)

            # Update number of new_missies and last_spawn time
            self.last_num = num_new_missiles
            self.last_spawn_missile = current_time

    def increase_score_misslie(self) -> None:
        """Increases the score based on changes in the missile count"""
        current_num = len(self.missiles)

        # Because we have case that missiles run out of fuel
        # So we have to check that number of current missiles is different from last time
        if current_num < self.last_num:
            self.score += self.last_num - len(self.missiles)
            self.last_num = current_num

    def spawn_coin(self) -> None:
        """Increases the score based on changes in the missile count"""
        current_time = pygame.time.get_ticks() / 1000  # Convert ms to s

        all_type = ["normal", "invincible", "delete_missile"]
        weight = [0.6, 0.3, 0.1]

        if current_time - self.last_spawn_coin >= self.COIN_SPAWN_TIME:
            
            spawn_area = (
                (50, 50),
                (self.SCREEN_WIDTH - 50, self.SCREEN_HEIGHT - 50)
            )

            # random, (x,y)
            # random type get only one choices with rate
            # k means we want only one sample and choices return in List
            rand_type = random.choices(all_type, weights=weight, k=1)[0]
            rand_x = random.randint(spawn_area[0][0], spawn_area[1][0])
            rand_y = random.randint(spawn_area[0][1], spawn_area[1][1])

            # Use Factory pattern to create differnet type of coin
            new_coin = self.coin_factory.create_coin(coin_type=rand_type,
                                                     center=(rand_x, rand_y),
                                                     score=self.COIN_SCORE,
                                                     radius=self.COIN_RADIUS)

            # Update
            self.coin.append(new_coin)
            self.last_spawn_coin = current_time

    def save_high_score(self) -> None:
        """Saves the current high score to a JSON file."""
        with open(r"./score.json", "w", encoding="utf-8") as file:
            data = {
                "high_score": self.high_score
            }

            json.dump(data, file)

    def load_high_score(self) -> None:
        """Loads the high score from a JSON file"""

        file_path = "./score.json"
        data = {}

        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.high_score = data["high_score"]

    def reset_effect_time(self) -> None:
        """Resets any temporary effects on the player"""
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
                 max_speed=game.MISSILE_MAX_SPEED,
                 max_turn_rate=game.MISSLIE_MAX_TURN_RATE)

    game.set_player(airplane)

    # for testing
    game.set_missiles([m1])
    game.run_main()
