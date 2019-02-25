import math
import random
import time

import pygame


class Box:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.background_color = (0, 0, 0, 0)


class Scene(Box):

    def __init__(self, width, height):
        super().__init__(width, height)


class Locale:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def tup(self):
        return (self.x, self.y)


class Color:

    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    @property
    def tup(self):
        return (self.red, self.green, self.blue)


class Phenomena:

    def __init__(self, local_args, color_args):
        self.locale = Locale(*local_args)
        self.color = Color(*color_args)
        self.thickness = 1
        self.time = 1
        self.wavelength = 200

    # def phase(radius):
    #     phase = ((radius % self.wavelength - self.time) / (self.wavelength / 2)) * math.pi
    #     return phase

    def field(self):
        if self.time < 1:
            return 0
        phase = ((self.time % self.wavelength) / (self.wavelength / 2)) * math.pi
        phase_intensity = abs(math.sin(phase))
        # print(phase_intensity)
        return phase_intensity
        # return phase_intensity / ((self.time ** 2)

    def intensity(self, iteration=None):
        # radius = iteration or 0
        # if radius < 1:
        #     return 0
        # phase = ((radius % self.wavelength - self.time) / (self.wavelength / 2)) * math.pi
        # phase_intensity = abs(math.sin(phase))
        # decay_factor = phase_intensity / (math.pi * radius ** 2)
        # decay_factor = decay_factor * 10000 * 20
        # if decay_factor > 1:
        #     return 1
        # elif decay_factor < 0.01:
        #     return 0
        return self.field()
        # return phase_intensity

    def draw_cone(self, surface):
        if self.time < 10:
            return
        else:
            alpha = self.intensity() * 7
            color = self.color.tup + (alpha, )
            # print(color)
            pygame.draw.circle(surface, color, self.locale.tup, self.size(), self.thickness)
            # for i in range(int(self.wavelength / 14)):
            #     delay = i * 7
            #     iteration = self.time - delay
            #     self.draw_iteration(display, iteration)

    # def draw_iteration(self, display, iteration):
    #     if iteration < 10:
    #         return
    #     intensity = self.intensity(iteration)
    #     color = (int(self.color.red * intensity),
    #              int(self.color.green * intensity),
    #              int(self.color.blue * intensity),)
    #     pygame.draw.circle(display, color, self.locale.tup, self.size(iteration),
    #                        self.thickness)
    #
    def increment(self):
        self.time += 1

    def size(self, iteration=None):
        size = iteration or self.time
        return size

    def intro_cone(self, display):
        if self.time < 10:
            if self.time < 4:
                width = self.time
            else:
                width = 3
                pygame.draw.circle(display, (255, 0, 0), self.locale.tup, self.time,
                                   width)


class Universe:
    def __init__(self):
        self.time = 1
        self.p = {}

    def draw(self, surface):
        for p_id, phenomena in self.p.items():
            phenomena.draw_cone(surface)

    def increment(self, surface):
        self.time += 1
        for p_id, phenomena in self.p.items():
            phenomena.increment()

        radius = self.time
        wavelength = 200

        # if self.time == 10:
        #     new_p = Phenomena((800, 400,), (0, 255, 0))
        #     self.p[id(new_p)] = new_p
        if self.time < 100:
            distance = random.randint(0, radius)
            position = random.randint(0, wavelength)
            phase = ((radius % wavelength - position) / (wavelength / 2)) * math.pi
            x = int(math.cos(phase) * distance) + 800
            y = int(math.sin(phase) * distance) + 400
            # x = int(math.cos(phase) * radius/2) + 800
            # y = int(math.sin(phase) * radius/2) + 400
            new_p = Phenomena((x, y,), (0, 255, 0))
            self.p[id(new_p)] = new_p
        # if self.time % 1 == 0:
        #     distance = random.randint(0, radius)
        #     position = random.randint(0, wavelength)
        #     phase = ((radius % wavelength - position) / (wavelength / 2)) * math.pi
        #     # x = int(math.cos(phase) * radius/2) + 800
        #     # y = int(math.sin(phase) * radius/2) + 400
        #     x = int(math.cos(phase) * distance) + 800
        #     y = int(math.sin(phase) * distance) + 400
        #     new_p = Phenomena((x, y,), (0, 0, 200))
        #     self.p[id(new_p)] = new_p
        # if self.time % 1 == 0:
        #     distance = random.randint(0, radius)
        #     position = random.randint(0, wavelength)
        #     phase = ((radius % wavelength - position) / (wavelength / 2)) * math.pi
        #     # x = int(math.cos(phase) * radius/ 2) + 800
        #     # y = int(math.sin(phase) * radius / 2) + 400
        #     x = int(math.cos(phase) * distance) + 800
        #     y = int(math.sin(phase) * distance) + 400
        #     new_p = Phenomena((x, y,), (190, 0, 0))
        #     self.p[id(new_p)] = new_p
        self.next_phenomena(surface)

    def next_phenomena(self, surface):
        bitmap = []
        # for x in range(1600):
        #     bitmap.append([])
        #     for y in range(800):
        #         bitmap[x].append(surface.get_at((x, y)))
        center_color = surface.get_at((825, 425))
        if self.time == 50:
            import ipdb; ipdb.set_trace()

        remove = []
        for p_id, phenomena in self.p.items():
            if phenomena.time > phenomena.wavelength:
                remove.append(p_id)

        for p_id in remove:
            self.p.pop(p_id)
        # Caclulate combined field intensity (weight)
        # weight_field = "?"
        # locale = random.somewhere_in_field(weight_field)
        # local
        # new_phenomena = Phenomena(locale)


class App:
    def __init__(self):
        self.universe = Universe()
        self.window = Box(1600, 800)
        self.display = pygame.display.set_mode((self.window.width, self.window.height))
        self.create_display()
        self.run()

    def create_display(self):
        self.surface = pygame.Surface((self.window.width, self.window.height), pygame.SRCALPHA)
        # self.display.flip()

    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.next_frame()

    def next_frame(self):
        # self.display.fill(self.window.background_color)
        # self.create_display()
        self.create_display()
        # modifier = self.universe.time / 1000
        # alpha = 100 - 50 * modifier
        # print(alpha)
        pygame.draw.rect(self.surface, (0, 0, 0, 10), pygame.Rect(0, 0, 1600, 800))
        self.universe.draw(self.surface)
        self.display.blit(self.surface, (0, 0))
        self.universe.increment(self.surface)
        pygame.display.flip()
        pygame.image.save(self.display, f"3/{self.universe.time}.jpeg")


app = App()
pygame.display.flip()


# wave = 10
# for i in range(wave * 2):
#     phase = ((i % wave) / (wave / 2)) * math.pi
#     intensity = abs(math.sin(phase))
#     print(intensity)
