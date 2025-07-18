from math import degrees
import pygame as pg

from ..components.angles import get_angle, get_distance, project


class Ball(pg.sprite.Sprite):
    """A golf ball."""
    def __init__(self, pos, *groups):
        super(Ball, self).__init__(*groups)
        self.radius = 4
        self.image = pg.Surface((self.radius * 2, self.radius * 2))
        self.image.set_colorkey(pg.Color("black"))
        self.rect = self.image.get_rect()
        pg.draw.circle(self.image, pg.Color("dodgerblue"),
                       self.rect.center, self.radius)
        self.mask = pg.mask.from_surface(self.image)
        self.rect.center = pos
        #movement per ms on each axis
        self.velocity = [0, 0]
        #integer amounts of how far the ball should move (magnitude only)
        self.banked = [0, 0]
        self.height = 0
        self.holed = False
        self.stopped_timer = 0
                
    def update(self, dt, hole):
        #check if ball is in cup
        self.check_cup(hole.cup)
        if self.holed:
            return            
        self.on_ramp = False
        self.check_ramps(dt, hole.ramps)
        self.check_hills(dt, hole.hills)
        self.update_position(dt, hole)
        #add some friction to slow the ball down
        self.velocity[0] -= self.velocity[0] * (.00065 * dt)
        self.velocity[1] -= self.velocity[1] * (.00065 * dt)
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
    def check_ramps(self, dt, ramps):
        for ramp in ramps:
            if ramp.rect.collidepoint(self.rect.center):
                self.velocity[0] += ramp.velocity_mod[0] * dt
                self.velocity[1] += ramp.velocity_mod[1] * dt
                self.on_ramp = True
    
    def check_hills(self, dt, hills):
        for hill in hills:
            dist = get_distance(hill.rect.center, self.rect.center)
            if hill.flat_radius <= dist <= hill.radius:
                hill.roll_ball(self, dt)
                self.on_ramp = True
                
    def check_cup(self, cup):
        """"Check if ball is over cup and not moving too fast."""
        if get_distance(self.rect.center, cup.rect.center) <= cup.radius:
            speed = sum((abs(self.velocity[0]), abs(self.velocity[1])))
            if  speed <= .2:
                self.holed = True
                
    def check_windmill(self, hole):
        if hole.windmill:
            mill = hole.windmill
            if self.rect.colliderect(mill.blades.blocker.rect):
                self.velocity[0] *= mill.velocity_flip[0]
                self.velocity[1] *= mill.velocity_flip[1]
                
    def update_position(self, dt, hole):
        ramp_mod = .8 if self.on_ramp else 1
        self.banked[0] += abs(self.velocity[0] * dt) * ramp_mod
        self.banked[1] += abs(self.velocity[1] * dt) * ramp_mod
        #direction of travel on x and y axes. Possible values are -1, 0, and 1.
        dx = self.velocity[0] / abs(self.velocity[0]) if self.velocity[0] else 0
        dy = self.velocity[1] / abs(self.velocity[1]) if self.velocity[1] else 0
        #number of pixels to move this frame on each axis
        mx = int(self.banked[0])
        my = int(self.banked[1])
        #adjust the amount of banked movement on each axis
        self.banked[0] -= mx
        self.banked[1] -= my
        #move one pixel at a time, alternating between x and y axes
        #if a collision occurs, the ball's direction on that axis is flipped
        while mx or my:
            if mx:               
                self.rect.move_ip(dx, 0)
                mx = max(0, mx - 1)
                self.check_windmill(hole)
                if pg.sprite.collide_mask(self, hole):
                    self.velocity[0] *= -1
                    dx *= -1
                    self.rect.move_ip(dx, 0)
            if my:               
                self.rect.move_ip(0, dy)
                my = max(0, my - 1)
                self.check_windmill(hole)
                if pg.sprite.collide_mask(self, hole):
                    self.velocity[1] *= -1
                    dy *= -1
                    self.rect.move_ip(0, dy)
