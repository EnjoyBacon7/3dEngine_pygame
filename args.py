import argparse
import config

def init():
    parser = argparse.ArgumentParser(description='3D engine in python')

    parser.add_argument('-r', '--resolution', nargs=2, type=int, default=(config.RESOLUTION[0], config.RESOLUTION[1]), help='Set the resolution of the window')
    parser.add_argument('-o', '--overlay', action="store_true", default=config.SHOW_OVERLAY, help='Enable the stats overlay')
    parser.add_argument('-rm', '--render-mode', type=str, default=config.RENDER_MODE, help='Set the render mode (wireframe, solid, points)')
    parser.add_argument('-fps', '--fps', type=int, default=config.FPS, help='Set the target FPS')
    parser.add_argument('-l', '--log', action="store_true", default=False, help='Launch as a logging session (will generate a frame time graph)')

    args = parser.parse_args()

    return args
