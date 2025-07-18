from itertools import cycle

import pygame as pg

from .. import prepare


class MusicHandler(object):
    def __init__(self):
        names = ["firefly", "nosquirrelcommotion", "porsupuesto", "steppinintro", "twine"]
        self.songs = cycle([prepare.MUSIC[name] for name in names])
        pg.mixer.music.set_volume(.5)
        self.muted = False
        
    def get_event(self, event):
        if event.type == pg.KEYUP:
            if event.key == pg.K_m:
                self.muted = not self.muted
                if self.muted:
                    pg.mixer.music.stop()             
            elif event.key == pg.K_s:
                self.load_next()
                
    def load_next(self):
        song = next(self.songs)
        pg.mixer.music.load(song)
        pg.mixer.music.play()    
                
    def update(self):
        if not self.muted and not pg.mixer.music.get_busy():
            self.load_next()

