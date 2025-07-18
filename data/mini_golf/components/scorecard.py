import pygame as pg

from .. import prepare
from .course_hole import HOLE_INFO
from .labels import Label


class Scorecard(object):
    def __init__(self, player):
        front_par_centers = [(155 + (40 * x), 121) for x in range(9)]
        back_par_centers = [(573 + (40 * x), 121) for x in range(9)]
        self.par_centers = front_par_centers + back_par_centers
        self.score_centers = [(x[0], 159) for x in self.par_centers]
        self.best_round_centers = [(x[0], 197) for x in self.par_centers]
        self.best_score_centers = [(x[0], 235) for x in self.par_centers]
        self.hole_centers = [(x[0], 83) for x in self.par_centers]
        self.out_par_center = 523, 121
        self.in_par_center = 941, 121
        self.total_par_center = 1000, 121
        self.current_out_center = 523, 159
        self.current_in_center = 941, 159
        self.current_total_center = 1000, 159
        self.best_score_out_center = 523, 235
        self.best_score_in_center = 941, 235
        self.best_score_total_center = 1000, 235
        self.best_round_out_center = 523, 197
        self.best_round_in_center = 941, 197
        self.best_round_total_center = 1000, 197
        
        self.image = prepare.GFX["scorecard"].copy()
        self.rect = self.image.get_rect()    
        self.labels = pg.sprite.Group()
        self.style = {"font_path": prepare.FONTS["weblysleekuisb"], "font_size": 24} 
        self.make_hole_labels(player)
        self.make_par_labels(player)
        self.make_score_labels(player)
        self.make_best_round_labels(player)
        self.make_best_score_labels(player)
        self.make_in_out_labels(player)
        self.labels.draw(self.image)
        self.rect.center = prepare.SCREEN_RECT.center
        
    def make_in_out_labels(self, player):
        front_par = sum((HOLE_INFO[x]["par"] for x in range(1, 10)))
        back_par = sum((HOLE_INFO[x]["par"] for x in range(10, 19)))
        total_par = front_par + back_par
        
        current_front_par = sum((HOLE_INFO[x]["par"] for x in range(1, min(10, player.hole_num + 1))))
        current_front_score = sum((player.scores[x] for x in range(1, min(10, player.hole_num + 1))))
        c_front_color = "gray20"
        if current_front_score > current_front_par:
            c_front_color = "darkred"
        elif current_front_score < current_front_par:
            c_front_color = "dodgerblue"
        
        if player.hole_num < 10:
            current_back_score = ""
            c_back_color = "gray20"
        else:    
            current_back_par = sum((HOLE_INFO[x]["par"] for x in range(10, player.hole_num + 1)))
            current_back_score = sum((player.scores[x] for x in range(10, player.hole_num + 1)))
            c_back_color = "gray20"
            if current_back_score > current_back_par:
                c_back_color = "darkred"
            elif current_back_score < current_back_par:
                c_back_color = "dodgerblue"
        
        current_total_par = sum((HOLE_INFO[x]["par"] for x in range(1, player.hole_num + 1)))
        current_total_score = sum(player.scores.values())
        c_total_color = "gray20"
        if current_total_score > current_total_par:
            c_total_color = "darkred"
        elif current_total_score < current_total_par:
            c_total_color = "dodgerblue"
                    
        Label("{}".format(front_par), {"center": self.out_par_center}, self.labels, text_color="goldenrod", **self.style)
        Label("{}".format(back_par), {"center": self.in_par_center}, self.labels, text_color="goldenrod", **self.style)
        Label("{}".format(total_par), {"center": self.total_par_center}, self.labels, text_color="goldenrod", **self.style)
        Label("{}".format(current_front_score), {"center": self.current_out_center}, self.labels, text_color=c_front_color, **self.style)
        Label("{}".format(current_back_score), {"center": self.current_in_center}, self.labels, text_color=c_back_color,  **self.style)
        Label("{}".format(current_total_score), {"center": self.current_total_center}, self.labels, text_color=c_total_color,  **self.style)
        
    def make_hole_labels(self, player):
        for h, hole_center in zip(range(1, len(self.hole_centers) + 1), self.hole_centers):
            Label("{}".format(h), {"center": hole_center}, self.labels, text_color="gray20", **self.style)    
        
    def make_par_labels(self, player):    
        pars = [HOLE_INFO[x]["par"] for x in sorted(HOLE_INFO.keys())]
        for par, spot in zip(pars, self.par_centers):
            Label("{}".format(par), {"center": spot}, self.labels, text_color="goldenrod", **self.style)
            
    def make_score_labels(self, player):    
        for i, x in enumerate(range(1, player.hole_num + 1)):
            score = player.scores[x]
            center = self.score_centers[i]
            if score > HOLE_INFO[x]["par"]:
                color = "darkred"
            elif score < HOLE_INFO[x]["par"]:
                color = "dodgerblue"
            else:
                color = "gray20"
            Label("{}".format(score), {"center": center}, self.labels, text_color=color, **self.style)
        
    def make_best_score_labels(self, player):
        high = len(player.best_scores) + 1
        front_range = list(range(1, min(10, high)))
        back_range = list(range(10,  min(19, high)))
        front_par = sum((HOLE_INFO[x]["par"] for x in front_range))
        front_score = sum((player.best_scores[x] for x in front_range))
        
        front_score_color = "gray20"
        if front_score > front_par:
            front_score_color = "darkred"
        elif front_score < front_par:
            front_score_color = "dodgerblue"
        
        back_score_color = "gray20"
        if len(player.best_scores) > 9:
            back_par = sum((HOLE_INFO[x]["par"] for x in back_range))  
            back_score = sum((player.best_scores[x] for x in back_range))
            if back_score > back_par:
                back_score_color = "darkred"
            elif back_score < back_par:
                back_score_color = "dodgerblue"
        else:
            back_score = ""
        
        total_score_color = "gray20"
        total_par = sum((HOLE_INFO[x]["par"] for x in range(1, high)))
        total_score = sum(player.best_scores.values())
        if total_score >  total_par:
            total_score_color = "darkred"
        elif total_score < total_par:
            total_score_color = "dodgerblue"        
        Label("{}".format(front_score), {"center": self.best_score_out_center}, self.labels, text_color=front_score_color, **self.style)
        Label("{}".format(back_score), {"center": self.best_score_in_center}, self.labels, text_color=back_score_color, **self.style)
        Label("{}".format(total_score), {"center": self.best_score_total_center}, self.labels, text_color=total_score_color, **self.style)
        for hole_num, best_score in sorted(player.best_scores.items()):
            score = player.best_scores[hole_num]
            if score > HOLE_INFO[hole_num]["par"]:
                color = "darkred"
            elif score < HOLE_INFO[hole_num]["par"]:
                color = "dodgerblue"
            else:
                color = "gray20"
            Label("{}".format(score), {"center": self.best_score_centers[hole_num-1]}, self.labels, text_color=color, **self.style)
        
    def make_best_round_labels(self, player):
        if not player.best_round:
            return
        high = len(player.best_round) + 1
        front_range = list(range(1, min(10, high)))
        back_range = list(range(10,  min(19, high)))
        front_par = sum((HOLE_INFO[x]["par"] for x in front_range))
        front_score = sum((player.best_round[x] for x in front_range))
        front_score_color = "gray20"
        if front_score > front_par:
            front_score_color = "darkred"
        elif front_score < front_par:
            front_score_color = "dodgerblue"
        
        back_score_color = "gray20"
        if len(player.best_round) > 9:
            back_par = sum((HOLE_INFO[x]["par"] for x in back_range))  
            back_score = sum((player.best_round[x] for x in back_range))
            if back_score > back_par:
                back_score_color = "darkred"
            elif back_score < back_par:
                back_score_color = "dodgerblue"
        else:
            back_score = ""
        
        total_score_color = "gray20"
        total_par = sum((HOLE_INFO[x]["par"] for x in range(1, high)))
        total_score = sum(player.best_round.values())
        if total_score >  total_par:
            total_score_color = "darkred"
        elif total_score < total_par:
            total_score_color = "dodgerblue"        
        Label("{}".format(front_score), {"center": self.best_round_out_center}, self.labels, text_color=front_score_color, **self.style)
        Label("{}".format(back_score), {"center": self.best_round_in_center}, self.labels, text_color=back_score_color, **self.style)
        Label("{}".format(total_score), {"center": self.best_round_total_center}, self.labels, text_color=total_score_color, **self.style)
        for hole_num, best_score in sorted(player.best_round.items()):
            score = player.best_round[hole_num]
            if score > HOLE_INFO[hole_num]["par"]:
                color = "darkred"
            elif score < HOLE_INFO[hole_num]["par"]:
                color = "dodgerblue"
            else:
                color = "gray20"
            Label("{}".format(score), {"center": self.best_round_centers[hole_num-1]}, self.labels, text_color=color, **self.style)
