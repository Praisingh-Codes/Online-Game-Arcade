from math import pi, degrees

import pygame as pg

from .. import prepare
from .angles import get_angle, project


class Windmill(pg.sprite.Sprite):
    """A classic minigolf windmill."""    
    def __init__(self, midbottom, velocity_flip, *groups):
        super(Windmill, self).__init__(*groups)
        self.image = prepare.GFX["mill"]
        self.rect = self.image.get_rect(midbottom=midbottom)
        blade_center = self.rect.left + 49, self.rect.top + 32
        self.blades = WindmillBlades((blade_center))
        self.blocker = self.blades.blocker
        self.velocity_flip = velocity_flip

    def update(self, dt, ball):
        self.blades.update(dt, ball)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.blades.draw(surface)


class Blocker(pg.sprite.Sprite):
    """Used for checking if the blades collide with the ball."""
    def __init__(self, size, *groups):
        super(Blocker, self).__init__(*groups)
        self.image = pg.Surface(size)
        self.image.fill(pg.Color("purple"))
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)


class WindmillBlades(pg.sprite.Sprite):
    """A sprite to represent the spinning blades of the windmill."""
    def __init__(self, center, *groups):
        super(WindmillBlades, self).__init__(*groups)
        self.center = center
        self.base_image = prepare.GFX["blades"]
        self.rect = self.base_image.get_rect(center=center)
        self.blade_length = self.rect.height / 2
        self.blocker = Blocker((31, 4))
        self.angle = 0
        lead = (self.rect.centerx - (self.blocker.rect.width / 2.),
                   self.rect.bottom)
        lead_angle = get_angle(self.center, lead)
        self.lead_offset = (1.5 * pi) - lead_angle

    def update(self, dt, ball):
        self.angle = (self.angle - (.002 * dt)) % (2 * pi)
        self.image = pg.transform.rotate(self.base_image, degrees(self.angle))
        self.rect = self.image.get_rect(center=self.center)
        self.update_blocker()

    def update_blocker(self):
        angles = (pi * x for x in (0, .5, 1, 1.5))
        corners = (project(self.center, (self.angle - self.lead_offset)+ angle, self.blade_length)
                         for angle in angles)
        corner = max(corners, key=lambda x: x[1])
        self.blocker.rect.bottomleft = corner[0], self.center[1] + self.blade_length

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        #pg.draw.rect(surface, pg.Color("red"), self.blocker)
