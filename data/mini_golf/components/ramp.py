from math import pi

import pygame as pg

from .angles import get_angle, project


class Ramp(pg.sprite.Sprite):
    """
    An inclined section of a minigolf hole. The ramp's velocity
    determines the direction of the incline.
    """    
    def __init__(self, rect_style, velocity, *groups):
        super(Ramp, self).__init__(*groups)
        self.rect = pg.Rect(rect_style)
        self.image = pg.Surface(self.rect.size)
        self.image.fill(pg.Color("white"))
        self.mask = pg.mask.from_surface(self.image)
        modifier = .00011
        self.velocity_mod = velocity[0] * modifier, velocity[1] * modifier
        
        
class Hill(pg.sprite.Sprite):
    """
    A circular raised section of a minigolf hole with a flat peak. 
    The velocity applied to the ball depends on the ball's position
    relative to the center of the hill.
    """
    def __init__(self, center, flat_radius, hill_radius):
        self.flat_radius = flat_radius
        self.radius = hill_radius
        surf = pg.Surface((hill_radius * 2, hill_radius * 2))
        pg.draw.circle(surf, pg.Color(0, 109, 9), (hill_radius, hill_radius), hill_radius)
        pg.draw.circle(surf, pg.Color("black"), (hill_radius, hill_radius), flat_radius)
        surf.set_colorkey(pg.Color("black"))
        self.mask = pg.mask.from_surface(surf)
        img = surf.copy()
        img.fill((0, 127, 10))
        img.blit(surf, (0, 0))
        self.image = img
        self.rect = self.image.get_rect(center=center)
        self.modifier = .00012
        
    def roll_ball(self, ball, dt):
        angle = get_angle(self.rect.center, ball.rect.center)
        velocity = project((0, 0), angle, 1)
        ball.velocity[0] += velocity[0] * self.modifier * dt
        ball.velocity[1] += velocity[1] * self.modifier * dt