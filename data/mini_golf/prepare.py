"""
This module initializes the display and creates dictionaries of resources.
"""

import os
import pygame as pg

from . import tools


SCREEN_SIZE = (1280, 720)
ORIGINAL_CAPTION = "Mini Golf"

#Initialization

pg.mixer.pre_init(44100, -16, 1, 512)

pg.init()
os.environ['SDL_VIDEO_CENTERED'] = "TRUE"
pg.display.set_caption(ORIGINAL_CAPTION)
SCREEN = pg.display.set_mode(SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()


FONTS = tools.load_all_fonts(os.path.join("resources", "fonts__"), accept=(".ttf", ".otf"))
MUSIC = tools.load_all_music(os.path.join("resources", "music"))
SFX   = tools.load_all_sfx(os.path.join("resources", "sound"))
GFX   = tools.load_all_gfx(os.path.join("resources", "minigolf"))  # ✅ Corrected path

# Load background music safely
if "clay" in MUSIC:
    pg.mixer.music.load(MUSIC["clay"])
    pg.mixer.music.play(-1)
else:
    print("[Warning] Background music 'clay' not found in resources/music")

# Copy the front nine to the back nine safely
for x in range(1, 10):
    hole_src = f"hole{x}"
    green_src = f"green{x}"
    hole_dst = f"hole{x + 9}"
    green_dst = f"green{x + 9}"

    if hole_src in GFX:
        GFX[hole_dst] = GFX[hole_src]
    else:
        print(f"[Warning] Missing {hole_src}")

    if green_src in GFX:
        GFX[green_dst] = GFX[green_src]
    else:
        print(f"[Warning] Missing {green_src}")
