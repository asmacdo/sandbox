from collections import Counter, defaultdict
import math
import random
import time

import numpy
import pygame


PLANK_CONSTANT = 5


class Space:
    def __init__(self):
        self.iteration = 0
        self._particles = []
        self.width = 1000
        self.height = 500
        self.background_color = (0, 100, 70)
        pygame.display.set_caption("Serialized Energy Density")
        self.screen = pygame.display.set_mode(self.dimensions)
        self.omega = 0.0
        self.waves = []
        self.accumulated_time = Counter()

    @property
    def dimensions(self):
        return (self.width, self.height)


    @property
    def particles(self):
        return sorted(self._particles, key=lambda p: p.f)


    def weighted_next(self):
        probabilities = []
        p_waves = {}
        for p in self.particles:
            energy, waves = p.possible_interactions()
            probabilities.append(energy)
            if energy:
                p_waves[p] = waves
                if not waves:
                    import ipdb; ipdb.set_trace()
        if sum(probabilities):
            normalized = [float(prob) / sum(probabilities) for prob in probabilities]
            next_p = numpy.random.choice(self.particles, p=normalized)
            next_w = numpy.random.choice(p_waves[next_p])
            return next_p, next_w
        else:
            for prob in probabilities:
                if prob:
                    import ipdb; ipdb.set_trace()
            return (False, False)


    def advance(self):
        self.iteration += 1
        print("Advancing to absolute frame {f}".format(f=self.iteration))
        particle, wave = self.weighted_next()
        if particle:
            self.accumulated_time[particle.f] += 1
            if not wave:
                import ipdb; ipdb.set_trace()
            distance = wave.particle.f - particle.f
            # prob = (particle.m + abs(particle.momentum)) ** 2 * 1000.0 / (distance ** 2)
            prob = 100000.0 / (distance ** 2)
            if random.random() < prob:
                right = distance > 0
                particle.accel(right)
                self.waves.remove(wave)
                # self.omega -= 1
                print("---- advancing particle: {p}".format(p=particle))
                print("-----          momentum: {m}".format(m=particle.momentum))
                print("-----              mass: {m}".format(m=particle.m))
        for particle in self.particles:
            print("momentum: {m}".format(m=particle.momentum))
            particle.move()
            particle.emit()
        for wave in self.waves:
            wave.advance()
        self.display_time_bar()
        pygame.display.flip()


    def add_particle(self, particle):
        self.omega += particle.m
        self._particles.append(particle)
        particle.space = self

    def display(self):
        self.screen.fill(self.background_color)
        for particle in self.particles:
            particle.display()
        for wave in self.waves:
            wave.display()
        self.display_time_bar()
        pygame.display.flip()

    def display_time_bar(self):
        for x, height in self.accumulated_time.items():
            pygame.draw.rect(
                self.screen,
                (255, 100, 0),
                (int(x), 10, 10, height * 5),
            )


class Wave:
    def __init__(self, particle, color=None):
        self.particle = particle
        self.center = int(particle.f)
        self.iteration = 0
        self.thickness = 1
        blue = (0, 0, 255)
        self.color = color or blue

    def interactable(self, f):
        if self.iteration == 0:
            return False
        if self.particle.f == f:
            return False
        radius = self.iteration * PLANK_CONSTANT
        positive = self.particle.f + radius
        negative = self.particle.f - radius

        if abs(f - positive) < 8 or abs(f - negative) < 8:
            return True
        else:
            return False
        #
        # if positive < 2 or negative
        #
        # return f == positive or f == negative


    @property
    def size(self):
        return self.iteration * PLANK_CONSTANT

    def advance(self):
        self.iteration += 1

    def display(self):
        pygame.draw.circle(
            self.particle.space.screen,
            self.color,
            (self.center, 250),
            self.size,
            self.thickness
        )


class Particle:
    def __init__(self, space, color=None, f=None, m=None):
        self.color = color or (255, 255, 255)
        self.f = f or 0
        self.m = m or 1
        self.space = space
        self.space.add_particle(self)
        self.momentum = 0
        self.delta = 0.0

    def accel(self, right):
        if right:
            self.momentum += 1
        else:
            self.momentum -= 1

    def move(self):
        max_diff = PLANK_CONSTANT - self.delta
        self.delta += max_diff * (float(self.momentum)  / (self.momentum + float(self.m)))
        if self.momentum > 0:

            # print("Moving, delta={delta}".format(delta=delta / PLANK_CONSTANT))
        else:
            self.delta += max_diff * (float(self.momentum)  / (self.momentum + float(self.m)))
            self.f += self.delta

    def possible_interactions(self):
        energy = 0
        waves = []
        for wave in self.space.waves:
            if wave.interactable(self.f):
                waves.append(wave)
                energy += 1
        if waves:
            return (energy + self.m, waves)
        else:
            return (0, [])


    def emit(self):
        wave = Wave(self)
        self.space.waves.append(wave)
        self.space.omega += 11

        return wave

    def __repr__(self):
        return "M:{mass}, f{frame}".format(mass=self.m, frame=self.f)

    def location(self):
        return (int(self.f), 250)

    def display(self):
        for one_mass in range(self.m):
            pygame.draw.circle(
                self.space.screen,
                self.color,
                self.location(),
                10,
                4
            )

def wave():
    s = Space()
    p1 = Particle(s, f=200, m=20)
    # p1 = Particle(s, f=250, m=5)
    # p1 = Particle(s, f=300, m=1)
    # p1 = Particle(s, f=400, m=5)
    # p1 = Particle(s, f=500, m=1)
    # p5 = Particle(s, f=710, m=1)
    # p5 = Particle(s, f=710, m=1)
    # p5 = Particle(s, f=720, m=1)
    # p5 = Particle(s, f=110, m=1)
    # p5 = Particle(s, f=730, m=1)
    # p5 = Particle(s, f=750, m=1)
    p5 = Particle(s, f=800, m=20)
    w1 = p1.emit()
    # w1 = p5.emit()

    for _ in range(100000):
        print(_)
        time.sleep(0.001)
        s.advance()
        s.display()

def space_sim():
    s = Space()

    p1 = Particle(s, f=500, m=3)
    p2 = Particle(s, f=800, m=1)
    s.display()
    print("test")
    for _ in range(9):
        print(s.advance())

def draw_rect():
    s = Space()
    pygame.display.flip()

def simulate():
    # space_sim()
    wave()
    # draw_rect()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
simulate()


