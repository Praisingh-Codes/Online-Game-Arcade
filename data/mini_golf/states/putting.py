import pygame as pg

from .. import tools
from ..components.ball import Ball
from ..components.putter import Putter
from ..components.course_hole import CourseHole


class Putting(tools._State):
    """
    This state allows the player to position the putter with the mouse. Clicking
    the mouse starts the next state, Swinging.
    """
    def __init__(self):
        super(Putting, self).__init__()
        
    def startup(self, persistent):
        self.persist = persistent
        self.ball = self.persist["ball"]
        self.putter = self.persist["putter"]
        self.hole = self.persist["hole"]
        self.player = self.persist["player"]
        self.music_handler = self.persist["music handler"]
        self.putter.putted = False
        pg.mouse.set_visible(False)
        
    def quit_game(self):
        self.quit = True
        self.player.save()
        
    def get_event(self, event):
        self.music_handler.get_event(event)
        if event.type == pg.QUIT:
            self.quit_game()
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit_game()
        elif event.type == pg.MOUSEBUTTONUP:
            self.putter.set_swing(self.ball)
            self.putter.putted = True
            self.player.strokes += 1
            self.done  = True
            pg.mouse.set_visible(True)
            self.next = "SWINGING"

    def update(self, dt):
        self.music_handler.update()
        mouse_pos = pg.mouse.get_pos()
        self.putter.update(dt, mouse_pos, self.ball)
        self.hole.update(dt, self.ball)

    def draw(self, surface):
        surface.fill(pg.Color("yellow"))
        self.hole.draw(surface)
        self.ball.draw(surface)
        if self.hole.windmill:
            self.hole.windmill.draw(surface)
        self.putter.draw(surface)