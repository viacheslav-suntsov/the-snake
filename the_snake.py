from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Координаты центра экрана
CENTER_OF_SCREEN = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

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
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR):
        """Инициализирует объект. Задаются начальная позиция и цвет."""
        self.position = CENTER_OF_SCREEN
        self.body_color = body_color

    def draw(self):
        """Метод предусматривает возможность
        отрисовки объектов в дочерних классах.
        Метод сообщает, что его необходимо реализовать в дочернем классе.
        """
        raise NotImplementedError('Подклассы должны реализовать метод draw()')

    def draw_cell(self, object_coordinates):
        """Метод отрисовывает одну ячейку объекта.
        Метод принимает координаты клетки в виде кортежа (x, y).
        """
        rect = pg.Rect(object_coordinates, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс для объекта - яблоко. Наследует от GameObject."""

    def __init__(self, body_color=APPLE_COLOR,
                 occupied_positions=(CENTER_OF_SCREEN,)
                 ):
        """Инициализирует объект Apple. Задаёт начальную позицию и цвет.
        Метод учитывает занятые позиции,
        переданные через occupied_positions.
        Вызывает метод randomize_position() для выбора свободной клетки.
        """
        super().__init__(body_color)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """Метод определяет позицию яблока случайным образом
        внутри игрового поля и исключает занятые позиции.
        """
        while True:
            random_x_index = randint(0, ((SCREEN_WIDTH // GRID_SIZE) - 1))
            random_y_index = randint(0, ((SCREEN_HEIGHT // GRID_SIZE) - 1))
            random_coordinate_x = random_x_index * GRID_SIZE
            random_coordinate_y = random_y_index * GRID_SIZE
            self.position = (random_coordinate_x, random_coordinate_y)
            if self.position not in occupied_positions:
                break

    def draw(self):
        """Метод реализует отрисовку яблока на игровом поле."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс для объекта - змейка. Наследует от GameObject."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализирует объект Snake с длиной змейки, списком сегментов,
        текущим направлением движения, цветом змейки.
        Метод инициализирует атрибут для
        хранения следующего направления движения.
        """
        super().__init__(body_color)
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
        x_coordinate, y_coordinate = self.get_head_position()
        direction_x, direction_y = self.direction
        new_x_coordinate = (x_coordinate + direction_x * GRID_SIZE)
        new_y_coordinate = (y_coordinate + direction_y * GRID_SIZE)

        new_head_position = (new_x_coordinate % SCREEN_WIDTH,
                             new_y_coordinate % SCREEN_HEIGHT)

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
        """Метод отвечает за восстановление начальной длины и позиции змейки
        с выбором случайного направления.
        """
        self.length = 1
        self.positions = [self.position]
        self.direction = choice(LIST_OF_DIRECTIONS)

    def draw(self):
        """Метод отвечает за отрисовку всех сегментов змейки."""
        for position in self.positions[:-1]:
            self.draw_cell(position)

        # Отрисовка головы змейки
        self.draw_cell(self.get_head_position())

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Отвечает за изменение направления движения змейки,
    обрабатывая действия пользователя, в том числе закрытие окна.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Управляет обновлением всей игры:
    получает действия пользователя,
    изменяет состояние объектов и обновляет экран.
    """
    pg.init()

    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
