import pygame
import random
import sys
import json
from settings import *
from sprites import Background, Snake, Food, Counter
from collision import Collision


class Game:
    def __init__(self) -> None:
        # Initiate pygame
        pygame.init()

        # Set up window
        pygame.display.set_caption(WINDOW_TITLE)
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        # Fonts
        self.GAME_FONT = pygame.font.SysFont(GAME_FONT_PATH, GAME_FONT_SIZE)

        # Init objects
        self.background = Background(BACKGROUND_COLOR_1, BACKGROUND_COLOR_2, BORDER_COLOR)

        self.snake = Snake(random.randint(0, GRID_WIDTH - 4),
                           random.randint(0, GRID_HEIGHT - 1),
                           SNAKE_HEAD_COLOR, SNAKE_BODY_COLOR)

        self.apple = Food(APPLE_COLOR)

        self.score = Counter("Score", self.GAME_FONT, TEXT_COLOR, PADDING, 2)
        self.highscore = Counter("Highscore", self.GAME_FONT, TEXT_COLOR, PADDING, 2, "topright")

        self.CLOCK = pygame.time.Clock()  # Setup clock

        # Load saved values
        self.save_data = {}
        self.load()

    def run(self) -> None:
        # Main loop
        while True:
            # Event handler
            for event in pygame.event.get():
                # If the X in the upper right corner is clicked the game stops
                if event.type == pygame.QUIT:
                    self.save()
                    pygame.quit()
                    sys.exit()
                self.handle_keyboard_inputs(event)  # Handle keyboard inputs

            self.snake.move()  # Move snake

            self.handle_collisions()  # Handle collisions

            self.draw()  # Draw frame

            # Update display
            pygame.display.update()
            self.CLOCK.tick(FPS)

    def draw(self) -> None:
        # Draw background, objects and score
        self.background.draw(self.window)
        self.apple.draw(self.window)
        self.snake.draw(self.window)
        self.score.draw(self.window)
        self.highscore.draw(self.window)

    def handle_keyboard_inputs(self, event) -> None:
        # Change snakes direction when receiving key inputs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                self.snake.temp_direction = 1
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                self.snake.temp_direction = 2
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                self.snake.temp_direction = 3
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                self.snake.temp_direction = 4

    def handle_collisions(self) -> None:
        # If a game over condition is True the game resets
        if Collision.headWall(self.snake) or Collision.headTail(self.snake):
            self.score.value = 0  # Set score to 0
            # Spawn snake in random location on grid
            self.snake.spawn(random.randint(0, GRID_WIDTH - 4),
                             random.randint(0, GRID_HEIGHT - 1))
            self.apple.spawn()  # Spawn the apple at a new location

        # Checks for food being eaten
        if Collision.headFood(self.snake, self.apple):
            self.snake.add_tail_element()  # Add a element to the snakes tail
            self.score.value += 1  # Increase the score by one
            # Spawn the apple at a new location
            while Collision.headFood(self.snake, self.apple) or Collision.tailFood(self.snake, self.apple):
                self.apple.spawn()
            if self.highscore.value < self.score.value:
                self.highscore.value = self.score.value

    def save(self) -> None:
        self.save_data["highscore"] = self.highscore.value
        with open(SAVE_FILE_PATH, "w") as file:
            json.dump(self.save_data, file)

    def load(self) -> None:
        with open(SAVE_FILE_PATH, "r") as file:
            data = json.load(file)
        try:
            self.save_data = data
            self.highscore.value = self.save_data["highscore"]
        except:
            self.save_data = {}


if __name__ == "__main__":
    game = Game()
    game.run()
