import pygame as pg

from .. import tools, prepare
from ..components.labels import Label
from ..components.course_hole import HOLE_INFO, CourseHole
from ..components.ball import Ball
from ..components.scorecard import Scorecard

            
class ViewScorecard(tools._State):
    def __init__(self):
        super(ViewScorecard, self).__init__()
        
    def startup(self, persistent):
        self.persist = persistent
        self.player = self.persist["player"]
        self.music_handler = self.persist["music handler"]
        self.card = Scorecard(self.player)
        
    def get_event(self, event):
        self.music_handler.get_event(event)
        if event.type == pg.QUIT:
            self.quit = True
            self.player.save()
        elif event.type == pg.MOUSEBUTTONUP:
            self.player.hole_num += 1
            if self.player.hole_num > max(HOLE_INFO.keys()):
                self.player.scores = {}
                self.player.hole_num = 1
            hole = CourseHole(self.player.hole_num)
            self.persist["hole"] = hole
            self.persist["ball"] = Ball(hole.ball_pos)
            self.done = True
            self.next = "HOLESTART"

    def update(self, dt):
        self.music_handler.update()

    def draw(self, surface):
        surface.blit(self.card.image, self.card.rect)