from settings import *
from sprites import Snake, Food


class Collision:
    @staticmethod
    def headWall(snake: Snake) -> bool:
        """Returns if snake head is colliding with wall."""
        return snake.grid_x < 0 or snake.grid_x > GRID_WIDTH - 1 or snake.grid_y < 0 or snake.grid_y > GRID_HEIGHT - 1

    @staticmethod
    def headFood(snake: Snake, food: Food) -> bool:
        """Returns if snake head is colliding with food item."""
        return snake.grid_x == food.grid_x and snake.grid_y == food.grid_y

    @staticmethod
    def headTail(snake: Snake) -> bool:
        """Returns if the snake head is colliding with own tail."""
        for tail_element in snake.tail:
            if tail_element.grid_x == snake.grid_x and tail_element.grid_y == snake.grid_y:
                return True
        return False

    @staticmethod
    def tailFood(snake: Snake, food: Food) -> bool:
        """Returns if tail or snake head is colliding with food item."""
        for tail_element in snake.tail:
            if tail_element.grid_x == food.grid_x and tail_element.grid_y == food.grid_y:
                return True
        return False
