import json

from .course_hole import HOLE_INFO


class Player(object):
    """Class to represent the player."""
    def __init__(self, stats_dict):
        d = stats_dict
        self.hole_num = d["hole num"]
        self.scores = d["scores"]
        self.best_round = d["best round"]
        self.best_scores = d["best scores"]
        self.strokes = 0
        self.par = self.get_par()
        
    def sink_one(self):
        """Called when the ball goes in the cup."""
        self.scores[self.hole_num] = self.strokes
        try:
            if self.strokes < self.best_scores[self.hole_num]:
                self.best_scores[self.hole_num] = self.strokes
        except KeyError:
            self.best_scores[self.hole_num] = self.strokes
        self.strokes = 0
        if self.hole_num == max(HOLE_INFO.keys()):
            self.finish_course()
        
    def finish_course(self):
        """Called when the player finishes the last hole of the course."""
        if not self.best_round:
            self.best_round = {k:v for k, v in self.scores.iteritems()}
        else:
            total = sum(self.scores.values())
            best = sum(self.best_round.values())
            if total < best:
                self.best_round = {k:v for k, v in self.scores.iteritems()}        
        self.save()

    def get_par(self):
        """Calculate whether the player is over or under par."""
        par = 0
        score = 0
        for x in range(1, self.hole_num):
            par += HOLE_INFO[x]["par"]
            score += self.scores[x]
        return score - par

    def save(self):
        """Save the player's stats to JSON."""
        stats = {    
                "hole num": self.hole_num,
                "scores": self.scores,
                "best round": self.best_round, 
                "best scores": self.best_scores}
        with open("player-stats.json", "w") as f:
            json.dump(stats, f)
        
            