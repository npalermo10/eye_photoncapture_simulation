from pymunk.vec2d import Vec2d
import pygame as pg
import numpy as np

class Photon():
    def __init__(self, screen, loc, angle):
        self.screen = screen
        self.loc = Vec2d(loc)
        self.angle = angle
        self.v = 5
        self.crossing_s_p = False
        

    def move(self):
        vec = Vec2d().unit().rotated_degrees(self.angle) * self.v
        self.loc += vec
        
    def draw(self):
        pg.draw.circle(self.screen, (0, 125, 255), (int(self.loc[0]), int(self.loc[1])), 2)

class Detector():
    def __init__(self, boundaries):
        self.boundaries = np.array(boundaries)
        self.n_photons = 0
        self.label_loc_vec = Vec2d().unit().rotated_degrees(-(self.boundaries.mean() + 5) ) 
        
    def reset(self):
        self.n_photons = 0
