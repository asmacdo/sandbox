import pygame
from itertools import cycle
import math

RESOLUTION = (800, 800)
BITS = 16
MAX_SAMPLE = 2**(BITS - 1) - 1

LEFT_FREQUENCY = 0
RIGHT_FREQUENCY = 262


def left_sample(time):
    return 0
    return int(MAX_SAMPLE * sum([math.sin(math.pi * 880 * time) + 1,
                                 math.sin(math.pi * 1100 * time) + 1,
                                 math.sin(math.pi * 1320 * time) + 1]) / 3)


def right_sample(time):
    sin = math.sin(math.pi * 262 * time)
    value = 1.5 if sin > 0 else .5
    return int(MAX_SAMPLE * value)
    return int(MAX_SAMPLE * 1 * (math.sin(math.pi * RIGHT_FREQUENCY * time) + 1))


pygame.mixer.pre_init(44100, -BITS, 2)
pygame.init()
display = pygame.display.set_mode(RESOLUTION)

duration = 1.0

sample_rate = 44100
n_samples = int(duration*sample_rate*2)

buffer = bytes()
for s, f in zip(range(n_samples), cycle([left_sample, right_sample])):
    for b in abs(f(s/sample_rate)).to_bytes(2, byteorder="little"):
        buffer += b.to_bytes(1, byteorder="little")
# sound = pygame.mixer.Sound(buffer=buffer)
#
# sound.set_volume(0.1)
# sound.play()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
