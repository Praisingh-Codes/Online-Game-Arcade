import pygame as pg

pg.init()
screen = pg.display.set_mode((800, 800))

small = pg.image.load("large.png")
w, h = small.get_size()
large = pg.Surface((w * 2, h))
colors = [small.get_at((x, 0)) for x in range(0, w, 32)]
for x, color in zip(range(0, w * 2, 64), colors):
    surf = pg.Surface((64, h))
    surf.fill(color)
    large.blit(surf, (x, 0))
pg.image.save(large, "yuge.png")