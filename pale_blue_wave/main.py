import math
import random
import time

import pygame


class Scene:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.background_color = (0, 0, 0, 0)


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

    def __init__(self, window, wavelength, local_args, color_args):
        self.window = window
        self.locale = Locale(*local_args)
        self._color = Color(*color_args)
        self.thickness = 1
        self.time = 1
        self.wavelength = wavelength

    @property
    def color(self):
        """
        Return the color, add the alpha value.

        alpha must be between (0, 255)
        """
        # TODO For interference paterns to exist, does alpha need to be negative?
        alpha = abs(int(self.intensity * 50))
        # alpha = abs(int(self.intensity * 50))
        # print(f"Alpha: {alpha}")
        return self._color.tup + (alpha,)

    @property
    def phase_intensity(self):
        """Return value between 0 and 1"""
        phase = (self.time % self.wavelength) / (self.wavelength / 2) * math.pi
        return math.cos(phase)

    @property
    def intensity(self):
        """Return a value between 0 and 1"""
        decay = (self.wavelength) / (self.wavelength + (self.time * 2 * math.pi))
        intensity = self.phase_intensity * decay
        # print(f"Intensity: {intensity}")
        # return decay
        return intensity

    def draw_cone(self):
        if self.time < 1:
            return
        else:
            surface = pygame.Surface((self.window.width, self.window.height), pygame.SRCALPHA)
            pygame.draw.circle(surface, self.color, self.locale.tup, self.time, self.thickness)
            return surface


class Universe:
    def __init__(self, window):
        self.time = 0
        self.p = {}
        self.window = window
        self.display = pygame.display.set_mode((window.width, window.height))

    def draw(self):
        # self.display.fill((0, 0, 0, 1))
        surface = pygame.Surface((self.window.width, self.window.height), pygame.SRCALPHA)
        if self.time % 10 == 0:
            surface.fill((0, 0, 0, 1))
            self.display.blit(surface, (0, 0))
        p_keys = list(self.p.keys())
        random.shuffle(p_keys)
        if p_keys:
            for p_id in p_keys:
                surface = self.p[p_id].draw_cone()
                self.display.blit(surface, (0, 0))

    def increment(self):
        print(f"Time: {self.time}")
        for p_id, phenomena in self.p.items():
            phenomena.time += 1
        self.next_phenomena()
        self.time += 1

    def interact(self, color_name, wavelength):
        colors = {
            'red': 0,
            'green': 1,
            'blue': 2
        }
        color = [0, 0, 0]
        color_index = colors[color_name]
        color[color_index] = 255
        color = tuple(color)
        x = random.randint(1, self.window.width - 1)
        y = random.randint(1, self.window.height - 1)
        location_color = self.display.get_at((x, y))
        interaction_liklihood = location_color[color_index] / 255
        num_phenom = len(self.p.keys())
        if interaction_liklihood > 0:
            if random.random() > interaction_liklihood:
                new_p = Phenomena(self.window, wavelength, (x, y,), color)
                self.p[id(new_p)] = new_p
                # if num_phenom > 100 or num_phenom > math.pi * self.time ** 2:
                if num_phenom < self.time // 2:
                    # TODO this should be a random choice of phenomena
                    # that are interacting with this pixel, weighted by the strength of
                    # that interaction
                    remove = random.choice(list(self.p.keys()))
                    self.p.pop(remove)
                return True
            else:
                return False

    def next_phenomena(self):
        # offset = self.time % wavelength
        # if self.time % 2 == 0:
        if self.time == 0:
            return
        if self.time == 1:
            wavelength = 50
            self.create_initial_phenomena(wavelength)
            return

        if self.time < 5:
            return

        interaction = 0
        wavelength = 100 - (200 - 200 / self.time ** 2)
        # wavelength = int(1000 / (self.time ** 2 )))
        print(f"WL: {wavelength}")
        # wavelength = 100
        while interaction < self.time / 2:
            color = random.choice(['red', 'green', 'blue'])
            interacted = self.interact(color, wavelength)
            if interacted:
                interaction += 1

    def create_initial_phenomena(self, wavelength):
        for i in range(5):
            sign = random.choice([-1, 1])
            offset = sign * i // 3
            sign = random.choice([-1, 1])
            offset2 = sign * i // 3
            new_p = Phenomena(self.window, wavelength, (800+offset, 400+offset2,), (0, 255, 0))
            self.p[id(new_p)] = new_p
            sign = random.choice([-1, 1])
            offset = sign * i // 3
            sign = random.choice([-1, 1])
            offset2 = sign * i // 3
            new_p = Phenomena(self.window, wavelength, (800+offset, 400+offset2,), (255, 0, 0))
            self.p[id(new_p)] = new_p
            sign = random.choice([-1, 1])
            offset = sign * i // 3
            sign = random.choice([-1, 1])
            offset2 = sign * i // 3
            new_p = Phenomena(self.window, wavelength, (800+offset, 400+offset2,), (0, 0, 255))
            self.p[id(new_p)] = new_p

    # def remove_old_phenomena(self):
    #     remove = []
    #     for p_id, phenomena in self.p.items():
    #         if phenomena.time > phenomena.wavelength / 2:
    #             remove.append(p_id)
    #     for p_id in remove:
    #         self.p.pop(p_id)

    def next_frame(self):
        self.draw()
        pygame.display.flip()
        pygame.image.save(self.display, f"5/{self.time}.jpeg")
        # pygame.image.save(self.display, f"3/{self.time}.jpeg")


class App:
    def __init__(self):
        window = Scene(1600, 800)
        self.universe = Universe(window)
        # self.display.fill((0, 0, 0, 255))
        # self.surface = pygame.Surface((self.window.width, self.window.height), pygame.SRCALPHA)
        self.run()

    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.next_frame()

    def next_frame(self):
        self.universe.increment()
        self.universe.next_frame()
        # self.surface.fill((0, 0, 0, 255))
        # self.universe.draw(self.display, self.surface)
        # self.universe.increment(self.surface)
        # pygame.display.flip()


app = App()
pygame.display.flip()


# wave = 10
# for i in range(wave * 2):
#     phase = ((i % wave) / (wave / 2)) * math.pi
#     intensity = abs(math.sin(phase))
#     print(intensity)
