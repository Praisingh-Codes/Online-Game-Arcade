import pygame as pg

from ..import tools, prepare
from ..components.labels import Label
from ..components.animation import Animation


class HoleStart(tools._State):
    """Display the hole number and par for the current hole."""
    def __init__(self):
        super(HoleStart, self).__init__()

    def startup(self, persistent):
        self.persist = persistent
        self.hole = self.persist["hole"]
        self.player = self.persist["player"]
        self.make_labels()

    def make_labels(self):
        self.animations = pg.sprite.Group()
        style = {"font_path": prepare.FONTS["weblysleekuisb"],
                     "text_color": "antiquewhite"}
        self.labels = pg.sprite.Group()
        hole = Label("Hole {}".format(self.player.hole_num),
                           {"midtop": (prepare.SCREEN_RECT.centerx, -300)},
                           self.labels, font_size=96, **style)
        par = Label("Par {}".format(self.hole.par),
                         {"midtop": (prepare.SCREEN_RECT.centerx, -200)},
                         self.labels, font_size=64, **style)
        drop1 = Animation(centery=250, duration=2000,
                                     transition="out_bounce", round_values=True)
        drop2 = Animation(centery=350, duration=2000,
                                     transition="out_bounce", round_values=True)
        drop1.start(hole.rect)
        drop2.start(par.rect)
        self.animations.add(drop1, drop2)

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.done = True
            self.next = "BALLPLACEMENT"

    def update(self, dt):
        self.animations.update(dt)

    def draw(self, surface):
        surface.fill(pg.Color("black"))
        self.hole.draw(surface)
        self.labels.draw(surface)
