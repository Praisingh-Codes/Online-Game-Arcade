"""
The main function is defined here. It simply creates an instance of
tools.Control and adds the game states to its dictionary using
tools.setup_states.  There should be no need (theoretically) to edit
the tools.Control class.  All modifications should occur in this module
and in the prepare module.
"""


from data.mini_golf import prepare
from data.mini_golf import tools

from .states import splash, putting, swinging, spectating
from .states import view_scorecard, hole_start, ball_placement


def main():
    """Add states to control here."""
    run_it = tools.Control(prepare.ORIGINAL_CAPTION)
    state_dict = {
            "SPLASH": splash.Splash(),
            "PUTTING": putting.Putting(),
            "SWINGING": swinging.Swinging(),
            "SPECTATING": spectating.Spectating(),
            "SCORECARD": view_scorecard.ViewScorecard(),
            "HOLESTART": hole_start.HoleStart(),
            "BALLPLACEMENT": ball_placement.BallPlacement()
            }
    run_it.setup_states(state_dict, "SPLASH")
    run_it.main()