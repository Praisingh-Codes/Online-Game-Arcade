import pygame as pg

from .. import tools

class BallPlacement(tools._State):
    def __init__(self):
        super(BallPlacement, self).__init__()
        self.next = "PUTTING"
        
    def startup(self, persistent):
        self.persist = persistent
        self.music_handler = self.persist["music handler"]

    def get_event(self, event):
        self.music_handler.get_event(event)
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.done = True
            
    def update(self, dt):
        pass

    def draw(self, surface):
        surface.fill(pg.Color("white"))
        



        



        
