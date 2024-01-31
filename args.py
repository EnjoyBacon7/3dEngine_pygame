import argparse
import json


def init():
    """Initialises the command line arguments and returns them.

    Returns
    -------
    args : argparse.Namespace
        The command line arguments
    """

    with open("./default_vars.json") as f:
        defaults = json.load(f)

    parser = argparse.ArgumentParser(description='3D engine in python')

    parser.add_argument('-r', '--resolution', nargs=2, type=int, default=(defaults["resolution"][0], defaults["resolution"][1]), help='Set the resolution of the window')
    parser.add_argument('-o', '--overlay', action="store_true", default=defaults["show_overlay"], help='Enable the stats overlay')
    parser.add_argument('-rm', '--render-mode', type=str, default=defaults["render_mode"], help='Set the render mode (wireframe, solid, points)')
    parser.add_argument('-fps', '--fps', type=int, default=defaults["fps"], help='Set the target FPS')
    parser.add_argument('-p', '--profile-run', action="store_true", default=defaults["profile_run"], help='Enable profiling mode')

    args = parser.parse_args()

    return args
