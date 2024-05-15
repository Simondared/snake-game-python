import pygame
import random
from settings import *


class Background:
    def __init__(self, color1, color2, border_color) -> None:
        self.color1 = color1
        self.color2 = color2
        self.border_color = border_color

    def draw(self, surface: pygame.Surface) -> None:
        """Draws the background on passed surface"""
        surface.fill(self.border_color)  # Fill the surface with border color

        # Fill grid by alternating between color 1 and color 2
        i = 0
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                if i % 2 == 0:
                    pygame.draw.rect(surface, self.color2, ((col * GRID_SQUARE_SIZE + PADDING),
                                                            (row * GRID_SQUARE_SIZE + PADDING),
                                                            GRID_SQUARE_SIZE, GRID_SQUARE_SIZE))
                else:
                    pygame.draw.rect(surface, self.color1, ((col * GRID_SQUARE_SIZE + PADDING),
                                                            (row * GRID_SQUARE_SIZE + PADDING),
                                                            GRID_SQUARE_SIZE, GRID_SQUARE_SIZE))

                if col != GRID_WIDTH - 1 and GRID_WIDTH % 2 == 0:
                    i += 1
                elif col != GRID_WIDTH and GRID_WIDTH % 2 != 0:
                    i += 1


class Snake:
    def __init__(self, start_grid_x: int, start_grid_y: int, head_color, tail_color) -> None:
        self.head_color = head_color
        self.tail_color = tail_color
        self.spawn(start_grid_x, start_grid_y)  # Spawn snake upon initiation

    def spawn(self, grid_x: int, grid_y: int) -> None:
        """Spawns snake at passed grid coordinates and sets/ resets vars and tail length."""
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.direction: int = 0  # 0 --> idle | 1 --> up | 2 --> down | 3 --> left | 4 --> right
        self.temp_direction: int = 0
        # Adds 3 tail elements to tail list
        self.tail: list[TailElement] = [TailElement(
            self.grid_x + 1 + i, self.grid_y, self.tail_color) for i in range(3)]

    def move(self) -> None:
        """Moves the snake including its tail."""

        # Set temp direction to actual direction | done to prevent accidental death when multiple keys are pressed in quick succession
        if self.temp_direction == 1 and self.direction != 2:
            self.direction = self.temp_direction
        elif self.temp_direction == 2 and self.direction != 1:
            self.direction = self.temp_direction
        elif self.temp_direction == 3 and self.direction != 4:
            self.direction = self.temp_direction
        elif self.temp_direction == 4 and self.direction != 3 and self.direction != 0:
            self.direction = self.temp_direction

        if self.direction != 0:
            self.add_tail_element()
            self.tail.pop()

        # Change snake heads position according to current direction
        if self.direction == 1:
            self.grid_y -= 1
        elif self.direction == 2:
            self.grid_y += 1
        elif self.direction == 3:
            self.grid_x -= 1
        elif self.direction == 4:
            self.grid_x += 1

    def add_tail_element(self) -> None:
        """Adds new tail element to the snakes tail."""
        # Create new object of class TailElement and add to tail list
        tail_element = TailElement(self.grid_x, self.grid_y, self.tail_color)
        self.tail.insert(0, tail_element)

    def draw(self, surface: pygame.Surface) -> None:
        """Draws snake on passed surface."""
        # Draw snake head
        pygame.draw.rect(surface, self.head_color,
                         (self.grid_x * GRID_SQUARE_SIZE + PADDING, self.grid_y * GRID_SQUARE_SIZE + PADDING, GRID_SQUARE_SIZE, GRID_SQUARE_SIZE))

        # Draw all tail elements
        for tail_element in self.tail:
            tail_element.draw(surface)


class TailElement:
    def __init__(self, grid_x: int, grid_y: int, color) -> None:
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.color = color

    # Method to draw tail element on a passed surface
    def draw(self, surface: pygame.Surface) -> None:
        # print(f"x:{self.grid_x}, y:{self.grid_y}")
        pygame.draw.rect(surface, self.color,
                         (self.grid_x * GRID_SQUARE_SIZE + PADDING, self.grid_y * GRID_SQUARE_SIZE + PADDING, GRID_SQUARE_SIZE, GRID_SQUARE_SIZE))


class Food:
    def __init__(self, color) -> None:
        self.color = color
        self.spawn()  # Spawn food object upon initiation

    def spawn(self) -> None:
        """Spawns food item at random grid coordinates."""
        self.grid_x: int = random.randint(0, GRID_WIDTH - 1)
        self.grid_y: int = random.randint(0, GRID_HEIGHT - 1)

    def draw(self, surface: pygame.Surface) -> None:
        """Draws food items on passed surface."""
        pygame.draw.rect(surface, self.color,
                         (self.grid_x * GRID_SQUARE_SIZE + PADDING, self.grid_y * GRID_SQUARE_SIZE + PADDING, GRID_SQUARE_SIZE, GRID_SQUARE_SIZE))


class Counter:
    def __init__(self, name: str, font: pygame.font.Font, color, x: int = 0, y: int = 0, anchor="topleft", start_value: int = 0) -> None:
        self.name = name
        self.font = font
        self.color = color
        self.x = x
        self.y = y
        self.anchor = anchor
        self.value = start_value

    def draw(self, surface: pygame.Surface) -> None:
        """Draws the score on passed surface."""
        # Convert the score value to a text
        self.text: str = f'{self.name}: {self.value}'
        # Render an image of the text using a font
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        if self.anchor == "topleft":
            surface.blit(self.image, (self.x, self.y))  # Draw the image
        elif self.anchor == "topright":
            surface.blit(self.image, (WINDOW_WIDTH - self.rect.width - self.x, self.y))  # Draw the image
