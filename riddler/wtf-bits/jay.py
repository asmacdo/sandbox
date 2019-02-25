import math

import pygame


BLUE = (0, 0, 255)
RED = (255, 0, 0)


class Bit:
    def __init__(self, chart_size, x, y, value=None):
        self.chart_size = chart_size
        self.x = x
        self._y = y
        self.value = value

    # pygame starts at the top left, this allows us to easily invert.
    @property
    def y(self):
        return self.chart_size[1] - 1 - self._y

    def draw(self, screen):
        # Don't render undefined bits(0,0)
        if self.value is None:
            return
        if self.value:
            color = RED
        else:
            color = BLUE

        # This just lets us scale the thing up a bit so we don't have to stare at single pixels.
        screen_size = screen.get_size()
        stretch_x = screen_size[0] // self.chart_size[0]
        stretch_y = screen_size[1] // self.chart_size[1]
        x = self.x * stretch_x
        y = self.y * stretch_y
        big_pixel = pygame.Rect(
            (x, y , stretch_x, stretch_y)
        )
        pygame.draw.rect(
            screen,
            color,
            big_pixel
        )


def do_something(chart_size, screen):
    # Create and store all the bits. They have to be stored instead of rendered so we can look at
    # them in future iterations.
    bit_rows = []
    for x in range(0, chart_size[0]):
        row = []
        for y in range(0, chart_size[1]):
            value = (x + y) % 2
            bit = Bit(chart_size, x, y, value)
            row.append(bit)
        bit_rows.append(row)

    # Render the thing.
    for row in bit_rows:
        for bit in row:
            bit.draw(screen)

if __name__ == "__main__":
    chart_size = (100, 100)
    size_modifier = 5
    display_size = [dimension * size_modifier for dimension in chart_size]
    screen = pygame.display.set_mode(display_size)

    do_something(chart_size, screen)
    pygame.display.flip()
    # pygame.image.save(screen, "wtf-bits.bmp")

    # This just doesn't close the thing until you click X
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
