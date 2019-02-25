import pygame
import time
import math


# Some config width height settings
canvas_width = 1800
canvas_height = 480

# Just define some colors we can use
color = pygame.Color(255, 255, 0, 0)
background_color = pygame.Color(0, 0, 0, 0)


pygame.init()
# Set the window title
pygame.display.set_caption("Sine Wave")

# Make a screen to see
screen = pygame.display.set_mode((canvas_width, canvas_height))
screen.fill(background_color)

# Make a surface to draw on
surface = pygame.Surface((canvas_width, canvas_height))
surface.fill(background_color)


def draw_2sin(a, f, s):
    for x in range(0, canvas_width):
        y1 = calc_sin_y(a * 2, f, s, x)
        # surface.set_at((x, int(y1) + int(canvas_height/2)), color)

        y2 = calc_sin_y(a, -3 * f, s, x)
        # color2 = pygame.Color(255, 0, 255, 0)
        # surface.set_at((x, int(y2) + int(canvas_height/2)), color2)

        y3 = calc_cos_y(a, 2 * f, s, x)
        # color3 = pygame.Color(100, 100, 100, 0)
        # surface.set_at((x, int(y3) + int(canvas_height/2)), color3)

        y = y1 + y2 + y3
        # s = y

        x = int(x + abs(y) / 5)

        color3 = pygame.Color(0, 255, 255, 0)
        surface.set_at((x, int(y) + int(canvas_height/2)), color3)
        # time.sleep(.001)
        #
        # y1 = calc_sin_y(a * 2, f, s, x)
        surface.set_at((x, int(y1) + int(canvas_height/2)), color)
        #
        # y2 = calc_sin_y(a, -3 * f, s, x)
        color2 = pygame.Color(255, 0, 255, 0)
        surface.set_at((x, int(y2) + int(canvas_height/2)), color2)

        # y3 = calc_cos_y(a, 2 * f, s, x)
        color3 = pygame.Color(100, 100, 100, 0)
        surface.set_at((x, int(y3) + int(canvas_height/2)), color3)


def draw_sin(a, f, s):
    for x in range(0, canvas_width):
        y = calc_sin_y(a, f, s, x)
        surface.set_at((x, y), color)

def calc_sin_y(a, f, s, x):
    return  a * math.sin(f *((float(x)/canvas_width)*(2*math.pi) + (s * time.time())))

def draw_cos(a, f, s):
    for x in range(0, canvas_width):
        y = calc_cos_y(a, f, s, x)
        surface.set_at((x, y), color)

def calc_cos_y(a, f, s, x):
        return a * math.cos(f *((float(x)/canvas_width)*(2*math.pi) + (s * time.time())))

# Simple main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Redraw the background
    surface.fill(background_color)


    # Update sine wave
    frequency = 4
    amplitude = 50 # in px
    speed = 1

    draw_2sin(50, 4, 1)
    # draw_sin(-50, 4, 1)
    # draw_cos(50, 4, 1)
    # draw_cos(-50, 4, 1)

    # for x in range(0, canvas_width):
    #     y = int((canvas_height/2) + amplitude*math.sin(frequency*((float(x)/canvas_width)*(2*math.pi) + (speed*time.time()))))
    #     surface.set_at((x, y), color)
    #
    #     y = int((canvas_height/2) + amplitude*math.sin(frequency*-1*((float(x)/canvas_width)*(2*math.pi) + (speed*time.time()))))
    #     surface.set_at((x, y), color)
    #
    #     y = int((canvas_height/2) + amplitude*math.cos(frequency*2*((float(x)/canvas_width)*(2*math.pi) + (speed*time.time()))))
    #     surface.set_at((x, y), color)
    #
    #     y = int((canvas_height/2) - amplitude*math.cos(frequency*2*((float(x)/canvas_width)*(2*math.pi) + (speed*time.time()))))
    #     surface.set_at((x, y), color)

    # Put the surface we draw on, onto the screen
    screen.blit(surface, (0, 0))

    # Show it.
    pygame.display.flip()

