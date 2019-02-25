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


def mod_serpinski_triangles(chart_size, screen):
    # Create and store all the bits. They have to be stored instead of rendered so we can look at
    # them in future iterations.
    bit_rows = []
    for x in range(0, chart_size[0]):
        row = []
        for y in range(0, chart_size[1]):
            diff = 1
            if x > diff and y > diff:
                diff = max(x % y, y % x)

            # Look to the left.
            try:
                # If it exists but is undefined (0, 0), just assign 0.
                prev_x = bit_rows[x - diff][y].value or 0
            except IndexError:
                # This isn't on the grid! But unlike serpinski, we can't just ignore it because
                # there will be values (x = y) that will be comparing 2 None values, and thus be
                # undefined. Instead just set it to True (x value is truthy except at 0, which is
                # correct because it can be undefined at 0).
                prev_x = x or None

            # Look down.
            try:
                # If it exists but is undefined (0, 0), just assign 0.
                prev_y = row[y - diff].value or 0
            # This isn't on the grid! Let it be undefined.
            except IndexError:
                # This isn't on the grid! But unlike serpinski, we can't just ignore it because
                # there will be values (x = y) that will be comparing 2 None values, and thus be
                # undefined. Instead just set it to True (y value is truthy except at 0, which is
                # correct because it can be undefined at 0).
                prev_y = y or None

            # This is (0,0) which is undefined. None is rendered as black.
            if prev_x is None and prev_y is None:
                value = None
            else:
                # If the bits we looked at are the same, this is a 1, otherwise 0
                value = (prev_x == prev_y)

            bit = Bit(chart_size, x, y, value)
            row.append(bit)
        bit_rows.append(row)

    # Render the thing.
    for row in bit_rows:
        for bit in row:
            bit.draw(screen)


def serpinski_triangles(chart_size, screen):
    # Create and store all the bits. They have to be stored instead of rendered so we can look at
    # them in future iterations.
    bit_rows = []
    for x in range(0, chart_size[0]):
        row = []
        for y in range(0, chart_size[1]):
            diff = 1

            # Look to the left.
            try:
                # If it exists but is undefined (0, 0), just assign 0.
                prev_x = bit_rows[x - diff][y].value or 0
            except IndexError:
                # This isn't on the grid! Let it be undefined.
                prev_x = None

            # Look down.
            try:
                # If it exists but is undefined (0, 0), just assign 0.
                prev_y = row[y - diff].value or 0
            # This isn't on the grid! Let it be undefined.
            except IndexError:
                prev_y = None

            # This is (0,0) which is undefined. None is rendered as black.
            if prev_x is None and prev_y is None:
                value = None
            else:
                # If the bits we looked at are the same, this is a 1, otherwise 0
                value = (prev_x == prev_y)

            bit = Bit(chart_size, x, y, value)
            row.append(bit)
        bit_rows.append(row)

    # Render the thing.
    for row in bit_rows:
        for bit in row:
            bit.draw(screen)

if __name__ == "__main__":
    chart_size = (1000, 1000)
    size_modifier = 1
    display_size = [dimension * size_modifier for dimension in chart_size]
    screen = pygame.display.set_mode(display_size)

    # Halfway there
    # serpinski_triangles(chart_size, screen)
    mod_serpinski_triangles(chart_size, screen)
    pygame.display.flip()
    # pygame.image.save(screen, "wtf-bits.bmp")

    # This just doesn't close the thing until you click X
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
