import pygame as pg

from .. import tools


class Swinging(tools._State):
    def __init__(self):
        super(Swinging, self).__init__()
        
    def startup(self, persistent):
        self.persist = persistent
        self.ball = self.persist["ball"]
        self.putter = self.persist["putter"]
        self.hole = self.persist["hole"]
        self.music_handler = self.persist["music handler"]
        
    def get_event(self, event):
        self.music_handler.get_event(event)
        if event.type == pg.QUIT:
            self.quit = True
            self.player.save()
        elif event.type == pg.KEYUP:
            self.quit = True

    def update(self, dt):
        self.music_handler.update()
        self.putter.update(dt, pg.mouse.get_pos(), self.ball)
        self.hole.update(dt, self.ball)
        if self.ball.velocity != [0, 0]:
            self.done = True
            self.next = "SPECTATING"
        
            
    def draw(self, surface):
        surface.fill(pg.Color("white"))
        self.hole.draw(surface)
        self.ball.draw(surface)
        self.putter.draw(surface)
        if self.hole.windmill:
            self.hole.windmill.draw(surface)