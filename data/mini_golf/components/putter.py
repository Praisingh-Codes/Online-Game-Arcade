from math import degrees, sqrt

import pygame as pg

from .. import prepare
from .angles import get_distance, get_angle, project
from .animation import Animation, Task


class Putter(pg.sprite.Sprite):
    """Sprite to represent the player's club."""
    def __init__(self, pos, *groups):
        super(Putter, self).__init__(*groups)
        self.pos = pos
        self.base_image = prepare.GFX["putter"]
        self.rect = self.base_image.get_rect(center=pos)        
        self.image = self.base_image
        self.mask = pg.mask.from_surface(self.base_image)
        self.putted = False
        self.acceleration = .0015
        self.animations = pg.sprite.Group()
        self.putt_sound =  prepare.SFX["putt"]
        
    def set_swing(self, ball):
        """Calculate the angle and velocity that will be applied to the ball."""
        self.swing_start = self.rect.center
        self.swing_angle = get_angle(self.rect.center, ball.rect.center)
        dist = get_distance(self.rect.center, ball.rect.center)
        self.swing_power = min(.7, dist * .005)
        duration = dist * 5
        ani = Animation(centerx=ball.rect.centerx, centery=ball.rect.centery,
                                 duration=duration, transition="in_quad")
        ani.start(self.rect)
        task = Task(self.hit_ball, duration, args=(ball,))
        task2 = Task(self.play_putt_sound, duration - 150)
        self.animations.add(ani, task, task2)
        self.putted = True
        
    def hit_ball(self, ball):
        """
        Alter the ball's velocity based on the angle and distance to the ball
        at the beginning of the putt.
        """
        angle = self.swing_angle
        ball.velocity = list(project((0, 0), angle, self.swing_power))
        
    def play_putt_sound(self):
        volume = self.swing_power * (1 / .6)
        self.putt_sound.set_volume(volume)
        self.putt_sound.play()
        
    def face_ball(self, ball):
        """"Orient the putter's image to match the angle to the ball."""
        self.angle_to_ball = get_angle(self.rect.center, ball.rect.center)
        angle = degrees(self.angle_to_ball) + 90
        self.image  = pg.transform.rotate(self.base_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pg.mask.from_surface(self.image)
        
    def update(self, dt, mouse_pos, ball):
        self.animations.update(dt)        
        if not self.putted:
            self.pos = mouse_pos
            self.rect.center = self.pos
            self.face_ball(ball)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        line_end = project(self.rect.center, self.angle_to_ball, 500)
        pg.draw.line(surface, pg.Color("white"), self.rect.center, line_end)        
        