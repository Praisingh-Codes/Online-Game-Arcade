import pygame as pg

from .. import prepare
from .ramp import Ramp, Hill
from .windmill import Windmill


HOLE_INFO = {
        1: {"ramps": [((855, 279, 373, 27), (0, -1)),
                              ((855, 347, 373, 48), (0, 1))],
              "hills": [],
              "ball pos": (150, 200),
              "cup pos": (1047, 480),
              "par": 3},
        2: {"ramps": [((392, 97, 35, 237), (-1, 0)),
                               ((563, 97, 51, 237), (-1, 0)),
                               ((793, 97, 35, 237), (-1, 0)),
                               ((459, 97, 35, 237), (1, 0)),
                               ((670, 97, 51, 237), (1, 0)),
                               ((860, 97, 35, 237), (1, 0))],
             "hills": [],
             "ball pos": (250, 600),
             "cup pos": (1080, 568),
             "par": 3},
        3: {"ramps": [((343, 86, 322, 22), (-1, 0)),
                              ((343, 86, 17, 211), (0, 1))],
              "hills": [],
              "ball pos": (714, 641),
              "cup pos": (351, 330),
              "par": 3},
        4: {"ramps": [((358, 445, 277, 84), (1, 0))],
              "hills": [],
              "ball pos": (170, 155),
              "cup pos": (244, 484),
              "par": 4},           
        5: {"ramps": [((187, 253, 247, 94), (1, 0))],
              "hills": [],
              "ball pos": (117, 302),
              "cup pos": (1153, 301),
              "par": 4},
        6: {"ramps": [((197, 88, 670, 138), (1, 0)),
                              ((384, 327, 585, 78), (-1, 0)),
                              #((201, 405, 68, 113), (0, -1)),
                              ((269, 534, 435, 42), (-1, 0))],
              "hills": [],
              "ball pos": (140, 159),
              "cup pos": (809, 495),
              "par": 5},
        7: {"ramps": [((763, 253, 24, 32), (-1, 0)),
                               ((496, 429, 24, 32), (-1, 0))],
              "hills": [],
              "ball pos": (567, 164),
              "cup pos": (705, 554),
              "par": 3},
        8: {"ramps": [],
              "hills": [],
              "ball pos": (633, 322),
              "cup pos": (633, 582),
              "par": 4},
        9: {"ramps": [((621, 121, 167, 292), (1, 0)),
                              ((875, 311, 76, 352), (-1, 0))],
              "hills": [((72, 662), 100, 200)],
              "ball pos": (1106, 616),
              "cup pos": (424, 355),
              "par": 7}
        }

#copy the front nine for the back nine
for x in range(1, 10):
    HOLE_INFO[x + 9] = HOLE_INFO[x]
    

class Cup(pg.sprite.Sprite):
    def __init__(self, pos, *groups):
        super(Cup, self).__init__(*groups)
        
        self.image = prepare.GFX["cup"]
        self.radius = self.image.get_width() // 2
        self.rect = self.image.get_rect(center=pos)
        self.mask = pg.mask.from_surface(self.image)
        
        
class CourseHole(pg.sprite.Sprite):
    def __init__(self, hole_num):
        image = prepare.GFX["hole{}".format(hole_num)]
        self.rect = image.get_rect()
        self.mask = pg.mask.from_surface(image)
        self.image = prepare.GFX["green{}".format(hole_num)]
        self.image.blit(image, (0, 0))
        self.make_ramps(HOLE_INFO[hole_num]["ramps"])
        self.make_hills(HOLE_INFO[hole_num]["hills"])
        self.ball_pos = HOLE_INFO[hole_num]["ball pos"]
        self.cup = Cup(HOLE_INFO[hole_num]["cup pos"])
        self.par = HOLE_INFO[hole_num]["par"]
        if hole_num == 3:
            self.windmill = Windmill((716, 303), (1, -1))
        else:
            self.windmill = None
            
    def update(self, dt, ball):
        if self.windmill:
            self.windmill.update(dt, ball)
            
    def make_ramps(self, ramp_info):
        self.ramps = [Ramp(rect, velocity) for rect, velocity in ramp_info]
    
    def make_hills(self, hill_info):
        self.hills = [Hill(center, flat_radius, radius)
                         for center, flat_radius, radius in hill_info]
                         
    def draw(self, surface):        
        surface.blit(self.image, self.rect)
        surface.blit(self.cup.image, self.cup.rect)
        #for ramp in self.ramps:
        #    pg.draw.rect(surface, pg.Color("blue"), ramp.rect, 1)
        
