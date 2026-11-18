from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

LIST_OF_DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, body_color=(0, 0, 0)):
        """Инициализирует объект с позицией объекта
        на игровом поле и цветом объекта.
        """
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self):
        """Метод предусматривает возможность
        отрисовки объектов в дочерних классах.
        Переопределяется в дочерних классах.
        """
        pass


class Apple(GameObject):
    """Класс для объекта - яблоко. Наследует от GameObject."""

    def __init__(self):
        """Инициализирует объект Apple с позицией объекта
        на игровом поле и цветом объекта.
        """
        super().__init__((255, 0, 0))
        self.randomize_position()

    def randomize_position(self):
        """Метод определяет позицию яблока
        случайным образом внутри игрового поля.
        """
        random_num_1 = randint(0, ((SCREEN_WIDTH // GRID_SIZE) - 1))
        random_num_2 = randint(0, ((SCREEN_HEIGHT // GRID_SIZE) - 1))

        random_num_1_coordinate = random_num_1 * GRID_SIZE
        random_num_2_coordinate = random_num_2 * GRID_SIZE
        coordinates = (random_num_1_coordinate, random_num_2_coordinate)

        self.position = coordinates

    def draw(self):
        """Метод реализует отрисовку яблока на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для объекта - змейка. Наследует от GameObject."""

    def __init__(self):
        """Инициализирует объект Snake с длиной змейки, списком сегментов,
        текущим направлением движения, следующим направлением,
        которое выбрано пользователем, цветом змейки.
        """
        super().__init__((0, 255, 0))
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Метод возвращает координаты головы змейки."""
        return self.positions[0]

    def move(self):
        """Метод отвечает за обновление координат всех сегментов змейки."""
        x_coordinate = (
            self.get_head_position()[0] + self.direction[0] * GRID_SIZE
        )

        y_coordinate = (
            self.get_head_position()[1] + self.direction[1] * GRID_SIZE
        )

        new_head_position = (x_coordinate % SCREEN_WIDTH,
                             y_coordinate % SCREEN_HEIGHT)

        self.positions.insert(0, new_head_position)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def update_direction(self):
        """Метод обновляет текущее направление движения змейки на
        основе значения следующего направления, выбранного пользователем.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """Метод возвращает змейку в начальное состояние."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice(LIST_OF_DIRECTIONS)

    def draw(self):
        """Метод отвечает за отрисовку всех сегментов змейки."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Отвечает за изменение направления движения змейки,
    обрабатывая действия пользователя, в том числе закрытие окна.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Управляет обновлением всей игры:
    получает действия пользователя,
    изменяет состояние объектов и обновляет экран.
    """
    pygame.init()

    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:

            snake.length += 1
            apple.randomize_position()

        for position in snake.positions[1:]:
            if position == snake.get_head_position():
                snake.reset()
                screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
