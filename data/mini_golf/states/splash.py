from itertools import cycle
import json

import pygame as pg

from ..tools import _State, strip_from_sheet
from .. import prepare
from ..components.animation import Animation, Task
from ..components.player import Player
from ..components.putter import Putter
from ..components.course_hole import CourseHole
from ..components.ball import Ball
from ..components.music_handler import MusicHandler
from ..components.labels import Label, Blinker


class GolfBall(pg.sprite.Sprite):
    def __init__(self, pos, *groups):
        super(GolfBall, self).__init__(*groups)
        self.stopped = False
        sheet = prepare.GFX["ball-sheet"]
        self.images = cycle(strip_from_sheet(sheet, (0, 0), (377, 456), 10))
        self.next_image()
        self.rect = self.image.get_rect(center=pos)
        
    def next_image(self):
        self.image = next(self.images)
    
    def stop(self):
        self.stopped = True
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        

class Splash(_State):
    """A poorly-named title screen that also loads the player's saved stats."""
    def __init__(self):
        super(Splash, self).__init__()
        self.next = "HOLESTART"
        img = prepare.GFX["bg1"]
        self.bg = pg.transform.smoothscale(img, prepare.SCREEN_SIZE)
        self.ball = GolfBall((1390, 950))
        self.animations = pg.sprite.Group()
        duration = 4000
        ani = Animation(centerx=900, centery=400,
                                 duration=duration, round_values=True)
        ani.start(self.ball.rect)
        task = Task(self.ball.next_image, 40, -1)
        task2 = Task(task.kill, duration)
        self.animations.add(ani, task, task2)
        self.load_player()
        self.labels = pg.sprite.Group()
        title = Label("Mini Golf", {"midtop": (1500, 50)}, self.labels,
                           font_path=prepare.FONTS["Souses"], font_size=96)
        mover = Animation(centerx=prepare.SCREEN_RECT.centerx,
                                      duration=3000, delay=2000, 
                                      transition="out_elastic", round_values=True)
        mover.start(title.rect)
        self.blinkers = pg.sprite.Group()
        task3 = Task(self.add_prompt, 4500)
        self.animations.add(mover, task3)
        
    def add_prompt(self):
        Blinker("Click anywhere to continue",
                   {"midtop": (prepare.SCREEN_RECT.centerx, 650)}, 600,
                   self.blinkers, font_path=prepare.FONTS["weblysleekuisb"],
                   font_size=36)
        
    def load_player(self):
        try:
            with open("player-stats.json", "r") as f:
                stats = json.load(f)
                stats["scores"] = {int(k): v for k, v in stats["scores"].items()}
                stats["best scores"] = {int(k): v for k, v in stats["best scores"].items()}
                stats["best round"] = {int(k): v for k, v in stats["best round"].items()}
        except IOError:
            stats = {
                    "hole num": 1,
                    "scores": {},
                    "best round": {}, 
                    "best scores": {}}
        return Player(stats)
        
    def leave_state(self):
        self.done = True
        player = self.load_player()
        hole = CourseHole(player.hole_num)
        self.persist = {
                "player": player,
                "putter": Putter(pg.mouse.get_pos()),
                "hole": hole,
                "ball": Ball(hole.ball_pos),
                "music handler": MusicHandler()}
        pg.mixer.music.fadeout(2000)

    def startup(self, persistent):
        self.persist = persistent

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
            self.player.save()
        elif event.type == pg.MOUSEBUTTONUP:
            self.leave_state()

    def update(self, dt):
        self.animations.update(dt)
        self.blinkers.update(dt)
        
    def draw(self, surface):
        surface.blit(self.bg, (0, 0))
        self.ball.draw(surface)
        self.labels.draw(surface)
        self.blinkers.draw(surface)