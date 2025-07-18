import pygame as pg

from .. import prepare
from .. import tools
from ..components.animation import Task, Animation
from ..components.ball import Ball
from ..components.course_hole import CourseHole


class Spectating(tools._State):
    """
    During this state the ball moves according to its velocity and is checked
    for collision with the hole's mask and the cup. The state exits when the
    ball goes in the cup or when its velocity drops below a minimum velocity. 
    """
    def __init__(self):
        super(Spectating, self).__init__()
        
    def startup(self, persistent):
        self.persist = persistent
        self.player = self.persist["player"]
        self.ball = self.persist["ball"]
        self.putter = self.persist["putter"]
        self.hole = self.persist["hole"]
        self.music_handler = self.persist["music handler"]
        self.animations = pg.sprite.Group()
        self.holed_out = False
        
    def get_event(self, event):
        self.music_handler.get_event(event)
        if event.type == pg.QUIT:
            self.quit = True
            self.player.save()
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True

    def update(self, dt):
        self.animations.update(dt)
        self.music_handler.update()
        self.ball.update(dt, self.hole)
        self.putter.update(dt, pg.mouse.get_pos(), self.ball)
        self.hole.update(dt, self.ball)
        if self.ball.holed and not self.holed_out:
            self.holed_out = True
            prepare.SFX["cup-drop"].play()
            self.ball.velocity = [0, 0]
            self.ball.stopped_timer = 0
            task = Task(self.hole_out, 2000)
            cx, cy = self.hole.cup.rect.center
            ani = Animation(centerx=cx, centery=cy, duration=500,
                                    transition="out_bounce", round_values=True)
            ani.start(self.ball.rect)
            self.animations.add(task, ani)
            
        stopped = False
        if self.ball.on_ramp:
            cutoff = .025
        else:
            cutoff = .005
        if abs(self.ball.velocity[0]) < cutoff and abs(self.ball.velocity[1]) < cutoff:
            self.ball.stopped_timer += dt
        else:
            self.ball.stopped_timer = 0
        if self.ball.stopped_timer >= 1500:
                stopped = True
        if stopped and not self.holed_out:
            self.back_to_putting()
            
    def hole_out(self):
        self.done = True
        self.player.sink_one()
        self.next = "SCORECARD"
            
    def back_to_putting(self):
        self.ball.velocity = [0, 0]
        self.ball.stopped_timer = 0
        self.done = True
        self.next = "PUTTING"


    def draw(self, surface):
        surface.fill(pg.Color("blue"))
        self.hole.draw(surface)
        self.ball.draw(surface)
        self.putter.draw(surface)
        if self.hole.windmill:
            self.hole.windmill.draw(surface)